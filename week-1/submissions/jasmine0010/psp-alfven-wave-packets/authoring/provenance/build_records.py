"""Build the task's records from CDAWeb sweeps made by fetch_pass.py.

Usage: python build_records.py SWEEPS_DIR OUT_DIR
  SWEEPS_DIR/<enc>/sweep.npz for e10, e14, e18, e21, e22 and e27 (fetch_pass.py)
Writes OUT_DIR/pass.npz (the visible December 2024 record, environment/data), OUT_DIR/rec1-rec5.npz (the hidden records,
tests/data) and OUT_DIR/injected_truth.json.

Each record is on a uniform 4 s grid. Magnetic field: 4 s bin means. SPAN-i velocity and QTN density: interpolated onto the
grid after quality rejection. Hidden records rec1-rec4 are 72 h around the E10, E14, E18 and E27 perihelia with injected
90-150 s signals at the fixed sample indices in SLOTS: two short and two long outward packets (spherical, near-linear, slight frequency
wander, velocity response sqrt(r_A) of the Alfvenic value with r_A drawn from 0.6-1.05, the 10-90% range of the Alfven ratio
of real packets the author's detector finds in these records) and four non-wave decoys (compressive, transverse with no velocity,
and two inward). rec5 is a null record: 72 h of E21 with fluctuations under ~2 h phase-scrambled jointly in B and V,
polarity-rectified and in Alfven units, so spectra and cross helicity are kept but coherent packets are destroyed."""
import json, sys
from pathlib import Path
import numpy as np
from scipy import signal

DT = 4.0
MP, MU0 = 1.67262192369e-27, 4e-7 * np.pi
REJECT = sum(1 << b for b in (0, 2, 3, 8, 10, 11))           # SPAN-i QUALITY_FLAG bits treated as bad
SO = signal.butter(4, [1 / 150., 1 / 90.], btype="band", fs=1 / DT, output="sos")
SOURCES = {"rec1": "e10", "rec2": "e14", "rec3": "e18", "rec4": "e27"}
# Injection slots (sample indices). They were chosen on 2026-11-08 as the earliest non-overlapping 4 h windows, every 10 min,
# with >= 98% usable B, V and n over 1 h, |<B_R>|/<|B|> >= 0.6, 90-150 s band power below the record's 60th percentile, and
# at least 25 min from any island of the author's 1 Hz detection_v2 run. Those island files have since been regenerated,
# so the slots are fixed here to reproduce the shipped records exactly.
SLOTS = {"rec1": [3600, 7350, 14850, 21750, 25650, 33600, 38400, 42150], "rec2": [3600, 7350, 11100, 15900, 20250, 24000, 30150, 47100],
         "rec3": [3600, 7350, 12150, 15900, 41400, 47550, 51900, 55800], "rec4": [3600, 7350, 12750, 21450, 25950, 42600, 46350, 51450]}
KINDS = ["packet_short", "packet_short", "packet_long", "packet_long", "compressive", "transverse", "inward", "inward"]


def load(path):
    """Sweep file -> grid start, grid, B, V, N, usable masks for each, and closest approach in solar radii."""
    Z = np.load(path); T0e = float(Z["t0"]); grid = T0e + DT * (np.arange(len(Z["B"])) + .5)
    def tg(t, y, good, mg):
        t, y = t[good], y[good]; i = np.searchsorted(t, grid); ok = (i > 0) & (i < len(t)); gap = np.full(len(grid), np.inf); gap[ok] = t[i[ok]] - t[i[ok] - 1]
        out = np.interp(grid, t, y) if y.ndim == 1 else np.column_stack([np.interp(grid, t, y[:, j]) for j in range(y.shape[1])])
        return out, gap <= mg
    B, mB = tg(grid, np.nan_to_num(Z["B"]), Z["Bcnt"] > 0, 60.)
    fl = np.nan_to_num(Z["vel_flag"], nan=65535).astype(np.int64); gv = np.isfinite(Z["V"]).all(axis=1) & (fl != 65535) & ((fl & REJECT) == 0)
    V, mV = tg(Z["vel_t"], Z["V"], gv, 60.)
    qf, qn = Z["qtn_flag"], Z["qtn_n"]; N, mN = tg(Z["qtn_t"], qn, np.isin(qf, [1, 2, 4]) & (qn > 0) & (qn < 1e10), 120.)
    return T0e, grid, B, V, N, mB, mV, mN, float(np.nanmin(Z["sun_dist"]) / 695700)


def save(path, B, V, N):
    np.savez_compressed(path, time_s=(np.arange(len(B)) + .5) * DT, B_RTN_nT=B.astype(np.float32), V_RTN_kms=V.astype(np.float32), electron_density_cm3=N.astype(np.float32))


def band_rms_ratio(B, i, half):
    """Band-limited |dB| amplitude around sample i relative to the surrounding +-4 h (excluding the window)."""
    w = int(4 * 3600 / DT); a, b = max(i - w, 0), min(i + w, len(B)); fb = signal.sosfiltfilt(SO, signal.detrend(B[a:b], axis=0), axis=0)
    env = np.sqrt((fb ** 2).sum(1)); j = i - a; core = env[max(j - half, 0):j + half]; ring = np.r_[env[:max(j - 3 * half, 0)], env[j + 3 * half:]]
    return float(np.sqrt((core ** 2).mean() / (ring ** 2).mean()))


def build(name, enc, seed, sweeps, out_dir):
    T0e, grid, B, V, N, mB, mV, mN, Rmin = load(sweeps / enc / "sweep.npz"); rng = np.random.default_rng(seed)
    chosen = SLOTS[name]
    # with fewer slots, keep one short and one long packet plus one of each decoy type before the extras
    core = ["packet_short", "packet_long", "compressive", "transverse", "inward", "inward"]; extra = ["packet_short", "packet_long"]
    kinds = list(rng.permutation(core + extra[:len(chosen) - 6])); Bi, Vi, Ni, truth = B.copy(), V.copy(), N.copy(), []
    for i, kind in zip(sorted(chosen), kinds):
        period = float(rng.uniform(95, 145)); fw = float(rng.uniform(4, 7) if kind == "packet_short" else rng.uniform(15, 35))
        sl = slice(i - int(2 * 3600 / DT), i + int(2 * 3600 / DT)); t = (np.arange(sl.start, sl.stop) - i) * DT; e = np.exp(-.5 * (t / (fw * 60 / 2.355)) ** 2)
        wander = np.convolve(rng.normal(size=len(t)), np.hanning(int(600 / DT)), "same"); wander = wander / wander.std() * .03
        ph = np.cumsum(2 * np.pi / period * (1 + wander)) * DT; ph = ph - ph[len(t) // 2] + rng.uniform(0, 6.28)
        th = rng.uniform(0, np.pi); ell = rng.uniform(.1, .4); u = np.array([0, np.cos(th), np.sin(th)]); v = np.array([0, -np.sin(th), np.cos(th)])
        s = slice(i - int(900 / DT), i + int(900 / DT)); bhat = B[s].mean(0); bhat /= np.linalg.norm(bhat)
        target = {"packet_short": rng.uniform(3.5, 6), "packet_long": rng.uniform(3.5, 6), "compressive": rng.uniform(5, 9), "transverse": rng.uniform(5, 9), "inward": rng.uniform(6, 10)}[kind]
        half = max(int(fw * 60 / 2 / DT), 30)
        def applied(A):
            if kind == "compressive": return B[sl] + (A * e * np.cos(ph))[:, None] * bhat
            q = B[sl] + (A * e * np.cos(ph))[:, None] * u + (A * ell * e * np.sin(ph))[:, None] * v
            return q * (np.linalg.norm(B[sl], axis=1) / np.linalg.norm(q, axis=1))[:, None]
        cap = .6 * float(np.median(np.linalg.norm(B[s], axis=1))); lo, hi = 0., cap      # keep dB/B physical
        for _ in range(30):
            m = .5 * (lo + hi); q = B.copy(); q[sl] = applied(m); lo, hi = (m, hi) if band_rms_ratio(q, i, half) < target else (lo, m)
        A = .5 * (lo + hi); Bi[sl] = applied(A); dB = Bi[sl] - B[sl]; q = B.copy(); q[sl] = Bi[sl]; achieved = band_rms_ratio(q, i, half)
        sgn = -np.sign(B[s, 0].mean()); to_v = 1e-9 / np.sqrt(MU0 * MP * N[sl, None] * 1e6) / 1e3; rA = float(rng.uniform(.6, 1.05)); r = np.sqrt(rA)   # one draw, as before, so all other parameters are unchanged
        if kind.startswith("packet"): Vi[sl] += sgn * r * dB * to_v
        elif kind == "inward": Vi[sl] += -sgn * r * dB * to_v
        elif kind == "compressive": Ni[sl] = N[sl] * (1 - A * e * np.cos(ph) / np.linalg.norm(B[sl], axis=1))
        truth.append(dict(kind=kind, t_s=float((i + .5) * DT), period_s=period, fwhm_min=fw, cycles=fw * 60 / period, amplitude_nT=float(A), band_rms_ratio=float(achieved),
                          target_ratio=float(target), alfven_ratio=rA, dB_over_B=float(A / (cap / .6)), outward_sign=float(sgn)))
    save(out_dir / f"{name}.npz", Bi, Vi, Ni)
    return dict(source=enc, start_utc=str(np.datetime64(int(T0e), "s")), min_R_Rs=Rmin, signals=truth)


def null_record(sweeps, out_dir, seed=99):
    T0e, grid, B, V, N, *_ = load(sweeps / "e21" / "sweep.npz")
    a = int(((np.datetime64("2024-09-28T17:15") - np.datetime64(int(T0e), "s")) / np.timedelta64(1, "s")) / DT); n = int(72 * 3600 / DT)
    B, V, N = B[a:a + n], V[a:a + n], N[a:a + n]; lp = lambda x, s: signal.sosfiltfilt(signal.butter(4, 1 / s, btype="low", fs=1 / DT, output="sos"), x, axis=0)
    trendB, trendV = lp(B, 7200.), lp(V, 7200.); pol = np.where(trendB[:, :1] >= 0, 1., -1.); sN = np.sqrt(lp(N, 1200.))[:, None]
    X = np.fft.rfft(np.c_[(B - trendB) * pol / sN, V - trendV], axis=0); ph = np.exp(1j * np.random.default_rng(seed).uniform(0, 2 * np.pi, X.shape[0])); ph[0] = 1
    Y = np.fft.irfft(X * ph[:, None], n=n, axis=0)
    save(out_dir / "rec5.npz", trendB + Y[:, :3] * pol * sN, trendV + Y[:, 3:], N)
    return dict(source="e21 phase-scrambled (polarity-rectified, Alfven units)", start_utc=str(np.datetime64(int(T0e) + int(a * DT), "s")), signals=[])


if __name__ == "__main__":
    sweeps, out = Path(sys.argv[1]), Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
    T0e, grid, B, V, N, *_ = load(sweeps / "e22" / "sweep.npz"); save(out / "pass.npz", B, V, N)     # 2024-12-21T12:00Z, 6 days, no injections
    truth = {k: build(k, v, 8000 + i, sweeps, out) for i, (k, v) in enumerate(SOURCES.items())}
    truth["rec5"] = null_record(sweeps, out)
    json.dump(truth, open(out / "injected_truth.json", "w"), indent=1)
    print("written", sorted(p.name for p in out.iterdir()))
