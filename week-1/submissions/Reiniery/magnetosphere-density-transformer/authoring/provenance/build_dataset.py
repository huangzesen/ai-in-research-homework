"""Build compact THEMIS + OMNI SYM-H benchmark arrays.

This authoring-only script reads the locally supplied THEMIS density files and
downloads NASA SPDF's annual 5-minute OMNI files. It extracts SYM-H, aligns the
preceding 60 five-minute samples, and writes compressed public (2009--2013)
and hidden (2014) arrays.
"""

from __future__ import annotations

import argparse
import datetime as dt
import io
import urllib.request
from pathlib import Path

import numpy as np


OMNI_URL = (
    "https://spdf.gsfc.nasa.gov/pub/data/omni/high_res_omni/"
    "omni_5min{year}.asc"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--themis-dir", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def read_symh(years: range) -> dict[int, float]:
    values: dict[int, float] = {}
    for year in years:
        print(f"Downloading OMNI 5-minute data for {year}", flush=True)
        with urllib.request.urlopen(OMNI_URL.format(year=year), timeout=120) as response:
            stream = io.TextIOWrapper(response, encoding="ascii")
            for line in stream:
                fields = line.split()
                if len(fields) < 42:
                    continue
                y, doy, hour, minute = map(int, fields[:4])
                symh = float(fields[41])
                if symh >= 99999:
                    continue
                stamp = dt.datetime(y, 1, 1, tzinfo=dt.timezone.utc)
                stamp += dt.timedelta(days=doy - 1, hours=hour, minutes=minute)
                values[int(stamp.timestamp())] = symh
    return values


def read_themis(folder: Path) -> list[tuple[int, float, float, float, int]]:
    rows: list[tuple[int, float, float, float, int]] = []
    for path in sorted(folder.glob("den-scpot-*.dat")):
        for line in path.read_text().splitlines():
            fields = line.split()
            if len(fields) != 13:
                continue
            timestamp = int(fields[0])
            year = int(fields[1])
            density = float(fields[7])
            l_shell = float(fields[9])
            mlt = float(fields[10])
            if not (2009 <= year <= 2014):
                continue
            if not (np.isfinite(density) and density > 0):
                continue
            if not (np.isfinite(l_shell) and 0 < l_shell <= 10):
                continue
            if not (np.isfinite(mlt) and 0 <= mlt < 24):
                continue
            rows.append((timestamp, density, l_shell, mlt, year))
    return rows


def make_arrays(
    themis_rows: list[tuple[int, float, float, float, int]],
    symh: dict[int, float],
) -> dict[str, np.ndarray]:
    features: list[list[float]] = []
    targets: list[float] = []
    timestamps: list[int] = []
    years: list[int] = []
    for timestamp, density, l_shell, mlt, year in themis_rows:
        aligned = timestamp - (timestamp % 300)
        history_keys = [aligned - 300 * k for k in range(60, 0, -1)]
        if any(key not in symh for key in history_keys):
            continue
        history = [symh[key] for key in history_keys]
        theta = 2.0 * np.pi * mlt / 24.0
        features.append(history + [l_shell, np.cos(theta), np.sin(theta)])
        targets.append(density)
        timestamps.append(timestamp)
        years.append(year)
    return {
        "X": np.asarray(features, dtype=np.float32),
        "density": np.asarray(targets, dtype=np.float32),
        "timestamp": np.asarray(timestamps, dtype=np.int64),
        "year": np.asarray(years, dtype=np.int16),
    }


def save_subset(path: Path, data: dict[str, np.ndarray], mask: np.ndarray) -> None:
    np.savez_compressed(path, **{key: value[mask] for key, value in data.items()})


def main() -> None:
    args = parse_args()
    args.output_dir.mkdir(parents=True, exist_ok=True)
    themis = read_themis(args.themis_dir)
    symh = read_symh(range(2008, 2015))  # 2008 supplies early-2009 histories.
    data = make_arrays(themis, symh)
    public = data["year"] <= 2013
    hidden = data["year"] == 2014
    save_subset(args.output_dir / "public_2009_2013.npz", data, public)
    save_subset(args.output_dir / "hidden_2014.npz", data, hidden)
    hidden_indices = np.flatnonzero(hidden)
    hidden_times = data["timestamp"][hidden]
    hidden_histories = data["X"][hidden, :60]
    _, unique_at = np.unique(hidden_times, return_index=True)
    unique_indices = hidden_indices[unique_at]
    unique_histories = data["X"][unique_indices, :60]
    quiet_at = int(np.argmin(np.abs(unique_histories[:, -1])))
    disturbed_at = int(np.argmin(unique_histories[:, -1]))
    selected = unique_indices[[quiet_at, disturbed_at]]
    np.savez_compressed(
        args.output_dir / "reconstruction_contexts_2014.npz",
        symh_history=data["X"][selected, :60],
        timestamp=data["timestamp"][selected],
        label=np.asarray(["quiet", "disturbed"]),
    )
    print(f"Public rows: {int(public.sum()):,}")
    print(f"Hidden rows: {int(hidden.sum()):,}")


if __name__ == "__main__":
    main()
