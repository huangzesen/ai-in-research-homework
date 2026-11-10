"""Download one perihelion pass from NASA CDAWeb (HAPI): FIELDS MAG RTN (4 samples/cycle, binned to 4 s), SPAN-i L3 moments
and FIELDS QTN electron density. Usage: python fetch_pass.py OUT_DIR START_UTC [HOURS=144]; writes OUT_DIR/sweep.npz.
Passes used (OUT_DIR START HOURS): e10 2021-11-19T20:25 72, e14 2022-12-10T01:15 72, e18 2023-12-27T12:55 72,
e21 2024-09-27T00:00 144, e22 2024-12-21T12:00 144, e27 2026-03-10T06:05 72. Then run build_records.py."""
import csv, io, sys, time, urllib.parse, urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
import numpy as np

OUT = Path(sys.argv[1])
START = datetime.fromisoformat(sys.argv[2]).replace(tzinfo=timezone.utc)
STOP = START + timedelta(hours=float(sys.argv[3]) if len(sys.argv) > 3 else 144.0)
STEP = timedelta(hours=12)
DT = 4.0
T0 = START.timestamp()

def fmt(t): return t.strftime("%Y-%m-%dT%H:%M:%SZ")

def stream(ds, params, a, b):
    q = urllib.parse.urlencode({"id": ds, "parameters": params, "time.min": fmt(a), "time.max": fmt(b), "format": "csv"})
    url = "https://cdaweb.gsfc.nasa.gov/hapi/data?" + q
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=600) as r:
                return r.read().decode()
        except Exception as ex:
            print("retry", ds, a, ex, flush=True); time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"failed {ds} {a}")

def parse(text):
    if not text.strip():
        return None, None
    lines = text.splitlines()
    stamps = np.array([l[:l.index(",")].rstrip("Z") for l in lines], dtype="datetime64[ns]")
    t = stamps.astype(np.int64).astype(np.float64) * 1e-9
    vals = np.array([[float(x.strip('"')) if x.strip('"') else np.nan for x in l[l.index(",") + 1:].split(",")] for l in lines])
    return t, vals

nbin = int((STOP - START).total_seconds() / DT)
Bsum, Bcnt = np.zeros((nbin, 3)), np.zeros(nbin)
vt, vv, nt, nv = [], [], [], []
a = START
while a < STOP:
    b = min(a + STEP, STOP)
    tt = time.time()
    t, x = parse(stream("PSP_FLD_L2_MAG_RTN_4_SA_PER_CYC", "psp_fld_l2_mag_RTN_4_Sa_per_Cyc", a, b))
    nm = 0
    if t is not None:
        good = (np.abs(x) < 1e10).all(axis=1) & np.isfinite(x).all(axis=1)
        i = np.floor((t[good] - T0) / DT).astype(int); k = (i >= 0) & (i < nbin); i = i[k]
        for j in range(3): Bsum[:, j] += np.bincount(i, weights=x[good][k, j], minlength=nbin)
        Bcnt += np.bincount(i, minlength=nbin); nm = len(t)
    t, x = parse(stream("PSP_SWP_SPI_SF00_L3_MOM", "QUALITY_FLAG,VEL_RTN_SUN,EFLUX_VS_PHI,SUN_DIST,SC_VEL_RTN_SUN", a, b))
    nvv = 0
    if t is not None: vt.append(t); vv.append(x); nvv = len(t)
    raw = stream("PSP_FLD_L3_SQTN_RFS_V1V2", "electron_density,density_quality_flag", a, b)
    if raw.lstrip().startswith("{"):   # older QTN files have no quality flag: same rule as the oscillation project (0.1-99999.9 cm^-3 valid)
        t, x = parse(stream("PSP_FLD_L3_SQTN_RFS_V1V2", "electron_density", a, b))
        if t is not None: x = np.c_[x[:, 0], np.where((x[:, 0] >= .1) & (x[:, 0] <= 99999.9), 1., 0.)]
    else:
        t, x = parse(raw)
    nnn = 0
    if t is not None: nt.append(t); nv.append(x); nnn = len(t)
    print(fmt(a), "mag", nm, "vel", nvv, "qtn", nnn, f"{time.time()-tt:.0f}s", flush=True)
    a = b

with np.errstate(invalid="ignore", divide="ignore"):
    B = Bsum / Bcnt[:, None]
vt, vv = np.concatenate(vt), np.vstack(vv); nt, nv = np.concatenate(nt), np.vstack(nv)
for name, t in (("vel", vt), ("qtn", nt)):
    print(name, "monotonic:", bool(np.all(np.diff(t) > 0)))
np.savez_compressed(OUT / "sweep.npz", t0=T0, dt=DT, B=B, Bcnt=Bcnt,
    vel_t=vt, vel_flag=vv[:, 0], V=vv[:, 1:4], eflux_phi=vv[:, 4:12], sun_dist=vv[:, 12], sc_vel=vv[:, 13:16],
    qtn_t=nt, qtn_n=nv[:, 0], qtn_flag=nv[:, 1])
print("saved", (OUT / "sweep.npz").stat().st_size)
