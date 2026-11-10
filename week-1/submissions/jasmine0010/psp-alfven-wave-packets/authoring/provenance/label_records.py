"""Label rec1-rec5 with the author's wavelet-island detector (oscillation.detection_v2, revised 2026-11-09: k=4.0 with the f_peak
rule) at five settings. Needs the author's oscillation project importable. Run with GRADER_DIR set to the working folder (default: current folder), which holds
hidden_enc/ (the records from build_records.py) and injected_truth_enc.json. Labels feed make_key.py."""
import csv, json, os, sys, time
from pathlib import Path
import numpy as np
from oscillation.detection_v2 import DetectionConfig, ArraySource, identify_two_minute_islands

ROOT = Path(os.environ.get("GRADER_DIR", "."));   # working folder with hidden_enc/ and injected_truth_enc.json
OUT = ROOT / "labels_enc"; OUT.mkdir(exist_ok=True)
truth = json.load(open(ROOT / "injected_truth_enc.json"))
VARIANTS = {"reference": {}, "k3.5": dict(island_power_threshold=3.5), "k4.5": dict(island_power_threshold=4.5),   # revised detection_v2: default k=4.0 with the f_peak rule
            "window6h": dict(reference_window_hours=6.0), "window12h": dict(reference_window_hours=12.0)}
only = sys.argv[1:] or list(VARIANTS)
summary = {}
for var in only:
    cfg = DetectionConfig.for_cadence(4.0, **VARIANTS[var])
    for rec in ("rec1", "rec2", "rec3", "rec4", "rec5"):
        z = np.load(ROOT / "hidden_enc" / f"{rec}.npz"); start = np.datetime64(truth[rec]["start_utc"], "ns")
        start = start - (start - np.datetime64("1970-01-01", "ns")) % np.timedelta64(10, "s")   # ten-second boundary
        t = start + np.arange(len(z["time_s"])) * np.timedelta64(4, "s")
        out = OUT / var / rec; t0 = time.time()
        identify_two_minute_islands(t[0], t[-1] + np.timedelta64(4, "s"), label=f"{var}-{rec}", config=cfg, output_dir=out,
                                    source=ArraySource(t, z["B_RTN_nT"], z["V_RTN_kms"], z["electron_density_cm3"], label=rec), snapshots=False)
        try: rows = list(csv.DictReader(open(out / "islands.csv", encoding="utf-8")))
        except FileNotFoundError: rows = []
        islands = []
        for r in rows:
            a = (np.datetime64(r["start_utc"].replace("Z", "")) - start) / np.timedelta64(1, "s"); b = (np.datetime64(r["end_utc_exclusive"].replace("Z", "")) - start) / np.timedelta64(1, "s")
            fl = lambda k: None if r.get(k) in (None, "", "None") else float(r[k])
            islands.append(dict(start_s=float(a), end_s=float(b), period_s=fl("median_period_s"), cycles=fl("persistent_cycles"), decision=r["alfven_decision"],
                                reasons=r["alfven_reasons"], borderline=r["alfven_borderline"], sigma_c=fl("sigma_c"), alfven_ratio=fl("alfven_ratio"),
                                compressibility=fl("compressibility"), propagation=r["propagation"]))
        json.dump(islands, open(out / "islands_seconds.json", "w"), indent=1)
        summary[f"{var}/{rec}"] = dict(islands=len(islands), passing=sum(x["decision"] == "pass" for x in islands), seconds=round(time.time() - t0))
        print(var, rec, summary[f"{var}/{rec}"], flush=True)
json.dump(summary, open(OUT / f"summary_{'_'.join(only)}.json", "w"), indent=1)
