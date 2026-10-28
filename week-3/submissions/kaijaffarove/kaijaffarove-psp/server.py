# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["mcp>=2.3,<3", "httpx>=0.27"]
# ///
"""Parker Solar Probe data MCP server, read-only, using NASA CDAWeb's public HAPI service.

No API key needed. Full tables are saved as CSV files (in PSP_DATA_DIR, default ~/psp_data);
tools return short summaries plus the file path. Logs go to stderr (stdout is the MCP channel).
"""
import csv
import logging
import math
import os
import re
import statistics
import sys
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path

import httpx
from mcp.server import MCPServer

HAPI = os.environ.get("CDAWEB_HAPI", "https://cdaweb.gsfc.nasa.gov/hapi").rstrip("/")
OUT_DIR = Path(os.environ.get("PSP_DATA_DIR", "~/psp_data")).expanduser()
MAX_DAYS = 7
R_SUN_KM = 695_700.0
AU_KM = 149_597_870.7
EV_TO_K = 11_604.518

SPAN_I = "PSP_SWP_SPI_SF00_L3_MOM"      # SWEAP SPAN-i proton partial moments
MAG_1MIN = "PSP_FLD_L2_MAG_RTN_1MIN"    # FIELDS magnetic field, RTN, 1-minute

logging.getLogger("httpx").setLevel(logging.WARNING)
mcp = MCPServer("psp", instructions="Read-only Parker Solar Probe data from NASA CDAWeb.")


def log(*args):
    print("[psp]", *args, file=sys.stderr, flush=True)


class UserError(Exception):
    """An error whose message tells the caller what to try next."""


# ---------------------------------------------------------------- helpers

def parse_time(text: str, name: str) -> datetime:
    t = text.strip().replace(" ", "T").rstrip("Z")
    for fmt in ("%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%dT%H", "%Y-%m-%d"):
        try:
            return datetime.strptime(t, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            pass
    raise UserError(f"{name}={text!r} is not a time I understand. Use UTC ISO 8601, e.g. 2024-12-24 or 2024-12-24T06:00.")


def time_range(start: str, stop: str) -> tuple[str, str]:
    a, b = parse_time(start, "start"), parse_time(stop, "stop")
    if b <= a:
        raise UserError("stop must be after start.")
    if b - a > timedelta(days=MAX_DAYS):
        raise UserError(f"That range is {(b - a).days} days; the limit is {MAX_DAYS}. Split it into shorter ranges.")
    iso = lambda d: d.strftime("%Y-%m-%dT%H:%M:%SZ")
    return iso(a), iso(b)


def hapi_get(endpoint: str, params: dict, timeout: float = 90) -> httpx.Response:
    try:
        r = httpx.get(f"{HAPI}/{endpoint}", params=params, timeout=timeout)
    except httpx.TimeoutException:
        raise UserError("CDAWeb did not answer in time. Try a shorter time range, or try again in a minute.")
    except httpx.HTTPError as e:
        raise UserError(f"Could not reach CDAWeb ({e.__class__.__name__}). Check the internet connection.")
    if r.headers.get("content-type", "").startswith("application/json") or r.status_code >= 400:
        try:
            status = r.json().get("status", {})
        except ValueError:
            status = {"code": r.status_code, "message": r.text[:200]}
        code = status.get("code")
        if code == 1201:
            raise UserError("CDAWeb has no data for that time range. Check the dates; PSP data arrive weeks to months after downlink.")
        if code is not None and code != 1200:
            raise UserError(f"CDAWeb error {code}: {status.get('message')}. Check the dataset ID and parameter names with describe_cdaweb_dataset.")
    return r


def dataset_info(dataset_id: str) -> dict:
    r = hapi_get("info", {"id": dataset_id}, timeout=30)
    info = r.json()
    if "parameters" not in info:
        raise UserError(f"Unknown dataset {dataset_id!r}. Dataset IDs look like {SPAN_I}.")
    return info


def column_names(p: dict) -> list[str]:
    size = (p.get("size") or [1])[0]
    if size == 1:
        return [p["name"]]
    if size == 3 and "RTN" in p["name"].upper():
        return [f"{p['name']}_{c}" for c in "RTN"]
    return [f"{p['name']}_{i}" for i in range(size)]


def fetch_table(dataset_id: str, wanted: list[str], start: str, stop: str):
    """Return (header, rows of floats/None, times, units per column) for the chosen parameters."""
    info = dataset_info(dataset_id)
    params = [p for p in info["parameters"] if p["name"] in wanted]   # HAPI wants dataset order
    missing = set(wanted) - {p["name"] for p in params}
    if missing:
        names = ", ".join(p["name"] for p in info["parameters"][1:])
        raise UserError(f"Unknown parameter(s) {sorted(missing)} in {dataset_id}. Available: {names}")
    log(f"fetching {dataset_id} {start}..{stop} {wanted}")
    r = hapi_get("data", {"id": dataset_id, "time.min": start, "time.max": stop,
                          "parameters": ",".join(p["name"] for p in params), "format": "csv"})
    header, units, fills = ["time"], [""], [None]
    for p in params:
        cols = column_names(p)
        header += cols
        units += [p.get("units") or ""] * len(cols)
        fills += [p.get("fill")] * len(cols)
    times, rows = [], []
    for line in csv.reader(r.text.splitlines()):
        if not line or line[0].startswith("#"):
            continue
        times.append(line[0])
        row = []
        for value, fill in zip(line[1:], fills[1:]):
            try:
                x = float(value)
            except ValueError:
                x = math.nan
            bad = math.isnan(x) or abs(x) >= 1e30 or (fill not in (None, "NaN") and x == float(fill))
            row.append(None if bad else x)
        rows.append(row)
    if not rows:
        raise UserError("CDAWeb returned no data for that range. Check the dates.")
    return header, rows, times, units


def save_csv(name: str, header: list[str], times: list[str], rows: list[list]) -> Path:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / (re.sub(r"[^A-Za-z0-9_.-]", "", name.replace(":", "")) + ".csv")
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for t, row in zip(times, rows):
            w.writerow([t] + ["" if v is None else f"{v:.6g}" for v in row])
    return path


def stats(values: list, times: list[str]) -> dict | None:
    pairs = [(v, t) for v, t in zip(values, times) if v is not None]
    if not pairs:
        return None
    vals = sorted(v for v, _ in pairs)
    lo, hi = min(pairs), max(pairs)
    pct = lambda q: vals[min(len(vals) - 1, int(q * (len(vals) - 1) + 0.5))]
    return {"n": len(vals), "min": lo[0], "min_time": lo[1], "max": hi[0], "max_time": hi[1],
            "mean": statistics.fmean(vals), "median": statistics.median(vals), "p05": pct(0.05), "p95": pct(0.95)}


def fmt(s: dict | None, unit: str, scale: float = 1.0, digits: int = 3) -> str:
    if s is None:
        return "no valid data"
    g = lambda x: f"{x * scale:.{digits}g}"
    return (f"median {g(s['median'])}, mean {g(s['mean'])}, 5-95% range {g(s['p05'])} to {g(s['p95'])}, "
            f"min {g(s['min'])} ({s['min_time'][:19]}), max {g(s['max'])} ({s['max_time'][:19]}) {unit}  [{s['n']} samples]")


# ---------------------------------------------------------------- tools

@mcp.tool()
def solar_wind_summary(start: str, stop: str) -> str:
    """Summarize the solar wind measured by Parker Solar Probe between two UTC times.

    Use this first for questions like "how fast was the solar wind at PSP on 2024-12-24?" or
    "what was the density near perihelion 22?". It combines SWEAP/SPAN-i proton moments
    (density, velocity, temperature, distance from the Sun) with the FIELDS 1-minute magnetic field,
    returns median/mean/min/max with times, and saves the full table as a CSV file.

    Args:
        start: UTC start, ISO 8601, e.g. "2024-12-24" or "2024-12-24T06:00".
        stop: UTC stop, after start; at most 7 days later, e.g. "2024-12-25".
    """
    try:
        a, b = time_range(start, stop)
        header, rows, times, _ = fetch_table(SPAN_I, ["QUALITY_FLAG", "DENS", "VEL_RTN_SUN", "TEMP", "SUN_DIST"], a, b)
        col = {name: [r[i - 1] for r in rows] for i, name in enumerate(header) if i}
        positive = lambda xs: [x if x is not None and x > 0 else None for x in xs]
        dropped = sum(1 for x in col["DENS"] if x is not None and x <= 0) + \
                  sum(1 for x in col["TEMP"] if x is not None and x <= 0)
        col["DENS"], col["TEMP"] = positive(col["DENS"]), positive(col["TEMP"])   # unphysical values
        vr, vt, vn = col["VEL_RTN_SUN_R"], col["VEL_RTN_SUN_T"], col["VEL_RTN_SUN_N"]
        speed = [math.sqrt(x * x + y * y + z * z) if None not in (x, y, z) else None for x, y, z in zip(vr, vt, vn)]
        flags = Counter(int(q) for q in col["QUALITY_FLAG"] if q is not None)
        total = sum(flags.values())
        common = ", ".join(f"{q} ({100 * n / total:.0f}%)" for q, n in flags.most_common(3)) if total else "none"
        path = save_csv(f"psp_solar_wind_{a}_{b}", header + ["SPEED"], times, [r + [s] for r, s in zip(rows, speed)])
        dist = stats(col["SUN_DIST"], times)
        lines = [
            f"PSP solar wind, {a} to {b} (SWEAP/SPAN-i proton partial moments, {SPAN_I}):",
            f"- Radial speed Vr: {fmt(stats(vr, times), 'km/s')}",
            f"- Speed |V|: {fmt(stats(speed, times), 'km/s')}",
            f"- Proton density: {fmt(stats(col['DENS'], times), 'cm^-3')}",
            f"- Proton temperature: {fmt(stats(col['TEMP'], times), 'K', EV_TO_K)}",
        ]
        if dist:
            lines.append(f"- Distance from Sun: {dist['min'] / R_SUN_KM:.1f} to {dist['max'] / R_SUN_KM:.1f} R_sun "
                         f"({dist['min'] / AU_KM:.3f} to {dist['max'] / AU_KM:.3f} AU); closest at {dist['min_time'][:19]}")
        lines.append(f"- QUALITY_FLAG (bit flags; nonzero is common and not bad by itself), most common values: {common}.")
        if dropped:
            lines.append(f"- Dropped {dropped} unphysical values (density or temperature <= 0) before the statistics.")
        try:
            mh, mrows, mtimes, _ = fetch_table(MAG_1MIN, ["psp_fld_l2_mag_RTN_1min"], a, b)
            bmag = [math.sqrt(sum(v * v for v in r)) if None not in r else None for r in mrows]
            br = [r[0] for r in mrows]
            mpath = save_csv(f"psp_mag_{a}_{b}", mh + ["B_MAG"], mtimes, [r + [m] for r, m in zip(mrows, bmag)])
            lines.append(f"- |B| (FIELDS, 1-min): {fmt(stats(bmag, mtimes), 'nT')}")
            lines.append(f"- Br: {fmt(stats(br, mtimes), 'nT')}")
            lines.append(f"Saved: {path} and {mpath}")
        except UserError as e:
            lines.append(f"(Magnetic field unavailable: {e})")
            lines.append(f"Saved: {path}")
        return "\n".join(lines)
    except UserError as e:
        return f"Error: {e}"


@mcp.tool()
def describe_cdaweb_dataset(dataset_id: str) -> str:
    """List a CDAWeb dataset's time coverage and parameters (names, units, sizes).

    Use it before get_cdaweb_data to find parameter names. Useful PSP dataset IDs:
    PSP_SWP_SPI_SF00_L3_MOM (SPAN-i proton moments), PSP_FLD_L2_MAG_RTN_1MIN (FIELDS B in RTN, 1-min).
    Any CDAWeb dataset ID works (e.g. OMNI_HRO_1MIN for near-Earth solar wind).

    Args:
        dataset_id: the CDAWeb dataset ID, e.g. "PSP_FLD_L2_MAG_RTN_1MIN".
    """
    try:
        info = dataset_info(dataset_id.strip())
        lines = [f"{dataset_id}: data from {info.get('startDate', '?')[:19]} to {info.get('stopDate', '?')[:19]}"]
        for p in info["parameters"][1:]:
            size = (p.get("size") or [1])[0]
            desc = (p.get("description") or "").strip()
            lines.append(f"- {p['name']} [{p.get('units') or '-'}]{f' x{size}' if size > 1 else ''}: {desc}")
        return "\n".join(lines)
    except UserError as e:
        return f"Error: {e}"


@mcp.tool()
def get_cdaweb_data(dataset_id: str, parameters: str, start: str, stop: str) -> str:
    """Download chosen parameters of any CDAWeb dataset for a UTC time range, save them as CSV, return statistics.

    Use it when solar_wind_summary doesn't cover what you need (other parameters or datasets).
    Find parameter names with describe_cdaweb_dataset first. Vectors are split into components
    (_R, _T, _N for RTN vectors). Fill values and NaN are skipped in the statistics and left blank in the CSV.

    Args:
        dataset_id: CDAWeb dataset ID, e.g. "PSP_SWP_SPI_SF00_L3_MOM".
        parameters: comma-separated parameter names, e.g. "DENS,TEMP".
        start: UTC start, ISO 8601, e.g. "2024-12-24T00:00".
        stop: UTC stop, at most 7 days after start, e.g. "2024-12-24T12:00".
    """
    try:
        a, b = time_range(start, stop)
        wanted = [p.strip() for p in parameters.split(",") if p.strip()]
        if not wanted:
            raise UserError("Give at least one parameter name, e.g. parameters=\"DENS\".")
        header, rows, times, units = fetch_table(dataset_id.strip(), wanted, a, b)
        path = save_csv(f"{dataset_id}_{a}_{b}", header, times, rows)
        lines = [f"{dataset_id}, {a} to {b}, {len(rows)} records:"]
        for i, name in enumerate(header[1:]):
            lines.append(f"- {name}: {fmt(stats([r[i] for r in rows], times), units[i + 1])}")
        lines.append(f"Saved: {path}")
        return "\n".join(lines)
    except UserError as e:
        return f"Error: {e}"


if __name__ == "__main__":
    log("starting (stdio)")
    mcp.run()
