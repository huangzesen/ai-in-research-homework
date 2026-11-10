"""Build tests/answer_key.json. Usage: make_key.py <detector_outputs_dir>
Run with GRADER_DIR set to the working folder G (default: current folder): labels from label_records.py; grade.measures is the same scoring as tests/test_outputs.py.
Definition-free: injected packets and decoys are known; a packet reported in real data only needs support from some method.
"supported" = intervals from the author's detector at 5 settings plus, from <detector_outputs_dir>, the reference solution
(k=4.5), the same at k=5, three band-excess detectors and the detector from an earlier practice agent run. "clear_nonwaves"
= islands the author's detector rejects at every setting. Limits: every good detector passes, with the margins in L below.
tests/answer_key.json is its output with decoys_max raised from 0 to 1, a margin of one like the other limits.
"""
import json, os, sys
from pathlib import Path

G = Path(os.environ.get("GRADER_DIR", ".")); sys.path.insert(0, str(G)); import grade
E = Path(sys.argv[1]); RECS = ("rec1", "rec2", "rec3", "rec4", "rec5"); VARIANTS = ("reference", "k3.5", "k4.5", "window6h", "window12h"); PAD = 300.0
truth = json.load(open(G / "injected_truth_enc.json"))
lab = {v: {r: json.load(open(G / "labels_enc" / v / r / "islands_seconds.json")) for r in RECS} for v in VARIANTS}
def ov(a0, a1, b0, b1): return max(0., min(a1, b1) - max(a0, b0))
def cat_labels(v): return {r: [dict(t=(i["start_s"] + i["end_s"]) / 2, a=i["start_s"], b=i["end_s"], p=i["period_s"], s=i["sigma_c"]) for i in lab[v][r] if i["decision"] == "pass"] for r in RECS}
def cat_dir(d): return {r: [dict(t=e["midpoint_s"], a=e["start_s"], b=e["end_s"], p=e["peak_period_s"], s=e["sigma_c"]) for e in json.load(open(d / f"{r}.json"))["packets"]] for r in RECS}
GOOD = {f"author {v}": cat_labels(v) for v in VARIANTS}
# "numpy k=4" (old rule without f_peak, below its own calibrated k=4.5) was dropped on 2026-11-09: on the polarity-correct null
# it reports 3 islands and 4 unsupported per record, which would loosen the null and unsupported limits for everyone.
for k, n in {"ref2": "numpy reference", "ref2_k5.0": "numpy k=5", "w20": "band-excess 20 min", "w30": "band-excess 30 min", "w60": "band-excess 60 min", "agent": "agent detector (adapted)"}.items():
    GOOD[n] = cat_dir(E / k)
WRONG = {d.name[6:]: cat_dir(d) for d in sorted(E.glob("wrong_*"))}

def nonwaves(r):
    """Islands the reference rejects (not borderline) and that no setting accepts."""
    out = []
    for i in lab["reference"][r]:
        if i["decision"] != "fail" or i["borderline"]: continue
        if any(ov(i["start_s"], i["end_s"], j["start_s"], j["end_s"]) > 0 and j["decision"] == "pass" for v in VARIANTS for j in lab[v][r]): continue
        out.append([i["start_s"], i["end_s"]])
    return out
def support(r, skip=None):
    s = [[i["start_s"], i["end_s"]] for v in VARIANTS for i in lab[v][r]]
    for n, c in GOOD.items():
        if n != skip and not n.startswith("author"): s += [[e["a"], e["b"]] for e in c[r]]
    return s
def key(skip=None):
    return dict(pad_s=PAD, period_tol_s=25, records={r: dict(null=(r == "rec5"), clear_nonwaves=nonwaves(r), supported=support(r, skip),
                injected=[dict(kind=x["kind"], t_s=x["t_s"], period_s=x["period_s"], fwhm_s=x["fwhm_min"] * 60, outward_sign=x["outward_sign"]) for x in truth[r]["signals"]]) for r in RECS})

rows = {n: grade.measures(c, key(skip=n)) for n, c in GOOD.items()}
rows.update({f"WRONG {n}": grade.measures(c, key()) for n, c in WRONG.items()})
good = [m for n, m in rows.items() if not n.startswith("WRONG")]
L = dict(packets_min=min(m["found"] for m in good) - 2, period_rate_min=.8, sign_rate_min=.95, decoys_max=max(m["decoys_listed"] for m in good),
         nonwave_max=max(m["nonwave_listed"] for m in good) + 1, null_max=max(m["null"] for m in good) + 1, unsupported_max=max(max(m["unsupported"].values()) for m in good) + 2)
K = key(); K["limits"] = L
K["source"] = "E10, E14, E18, E27 (72 h around perihelion, injected signals capped at 0.6|B|) and phase-scrambled E21; author detection_v2 (revised 2026-11-09: k=4.0 with the f_peak rule) labels at 5 settings; rec5 null polarity-rectified, scrambled in Alfven units"
print(f"{'detector':28s} packets  period sign  decoys  nonwave  null  unsupported/rec      verdict")
for n, m in rows.items():
    f = []
    if m["found"] < L["packets_min"]: f.append("packets")
    if m["found"] and m["period_ok"] / m["found"] < L["period_rate_min"]: f.append("periods")
    if not m["found"] or m["sign_ok"] / m["found"] < L["sign_rate_min"]: f.append("signs")
    if m["decoys_listed"] > L["decoys_max"]: f.append("decoys")
    if m["nonwave_listed"] > L["nonwave_max"]: f.append("non-waves")
    if m["null"] > L["null_max"]: f.append("null")
    if max(m["unsupported"].values()) > L["unsupported_max"]: f.append("unsupported")
    print(f"{n:28s} {m['found']:>2d}/{m['packets']:<4d} {m['period_ok']:>2d}    {m['sign_ok']:>2d}   {m['decoys_listed']:>2d}/{m['decoys']:<3d}  {m['nonwave_listed']:>2d}/{m['nonwave']:<3d} {m['null']:>3d}   {str(list(m['unsupported'].values())):16s} {'PASS' if not f else 'FAIL: ' + ', '.join(f)}")
print("limits:", L)
json.dump(K, open(G / "answer_key_enc.json", "w"), indent=1); print("written answer_key_enc.json")
