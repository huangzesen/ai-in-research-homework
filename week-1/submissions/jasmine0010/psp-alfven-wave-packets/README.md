# PSP Alfvén wave packets

**Author:** jasmine0010 · **Field:** physics / space-plasma-physics · **Class level:** 1 · **Agent budget:** 180 min

The solver gets six days of Parker Solar Probe magnetic field, proton velocity and electron density around the
December 2024 perihelion, and must write a detector program that finds genuine outward-propagating Alfvén wave packets
with 90–150 s periods. The program is graded on hidden records from other perihelion passes.

## Difficulty

The task is open-ended in the way the research is: nothing says what counts as a packet, how to separate a localized
wave packet from ordinary Alfvénic turbulence, how to set thresholds, or how to tell outward from inward propagation
when the field polarity flips. The solver decides for itself whether to calibrate against chance (a turbulence null),
how to test wave physics rather than band power alone (velocity–field correlation, low compressibility, propagation
sense relative to the local radial field), and how to make the detector generalize to unseen passes. The data are real
FIELDS and SPAN-ion measurements; only the injected test signals and the null record are synthetic. The setting
follows Huang et al. (2024, ApJL 977, L12) on two-minute oscillations near the Sun.

Data: public NASA CDAWeb datasets PSP_FLD_L2_MAG_RTN_4_SA_PER_CYC (FIELDS magnetic field),
PSP_SWP_SPI_SF00_L3_MOM (SWEAP SPAN-ion moments) and PSP_FLD_L3_SQTN_RFS_V1V2 (FIELDS QTN electron density), courtesy
of the FIELDS and SWEAP instrument teams.

AI assistance: the author designed the task (the 90–150 s question, the choice of perihelion passes and the
definition-free grading) and built the wavelet detector. Claude Code (Claude Opus 5.5)
wrote the remaining code: data pipeline, verifier, NumPy reference and audits.

## Reference solution

`solution/detect.py` is a NumPy/SciPy re-implementation of the author's wavelet-island detector, without its later
spectral-peak (f_peak) rule. It computes Morlet wavelet power of the magnetic field, marks pixels at least 4.5 times
the running 8-hour median at the same period, and
keeps connected islands that touch 90–150 s, have a local spectral peak in the band for at least 30% of their duration
and persist for at least two cycles. Each island must then be Alfvénic over 90–150 s: |σc| ≥ 0.75, Alfvén ratio 0.3–3,
magnetic compressibility ≤ 0.1, and outward propagation (σc · sign⟨B_R⟩ < 0) where |⟨B_R⟩|/⟨|B|⟩ ≥ 0.5.
`solve.sh` copies it to `/root/results/detect.py`.

## Verification

The verifier runs the submitted `detect.py` offline, as an unprivileged user who cannot read the tests, with 15
minutes per record, on the visible record and five hidden 72-hour records. Four are real passes (E10, E14, E18, E27)
with injected signals of known origin: 16 outward packets (short 4–7 min bursts and 15–35 min trains, near-linear,
with Alfvén ratios drawn from 0.6–1.05, the range of real packets in these records) and 16 non-wave decoys (compressive, transverse with no velocity response,
inward). The fifth is the E21 pass with fluctuations under two hours phase-scrambled jointly in B and V, in Alfvén
units and with the polarity sign removed first, so its spectra and cross helicity match the real data but coherent
packets are gone. It passes when all checks hold:

- it runs on every record and writes valid output;
- it finds at least 14 of 16 injected packets, at least 80% of them with `peak_period_s` within 25 s and at least 95%
  with the right σc sign;
- it reports at most 1 of 16 decoys and at most 1 of 14 clear non-wave events (islands the author's detector rejects
  at every setting);
- it reports at most 3 packets on the scrambled record;
- in each record, at most 5 reports are unsupported, that is, outside injection windows and not overlapping any interval
  reported by the author's detector at five settings or by six other detectors.

No single detector's catalogue of real packets is required, because detectors built in different reasonable ways agree
on few real packets. The limits were chosen so that every good detector passes: the author's detector at five settings
(k = 3.5, 4.0 and 4.5; 6 and 12 h windows), the reference at k = 4.5 and 5, three band-excess detectors and an earlier
agent's detector. Deliberately wrong variants of the reference fail: magnetic power only (16 decoys and 12 non-waves
reported), no propagation-direction test (7 inward decoys), σc required positive (11/16 packets), reversed direction
(0/16), and the older loudest-event background (9 reports on the scrambled record). A detector without the
compressibility test still passes, a known gap. Empty, crashing, hanging, network-dependent and whole-record or
every-hour submissions fail. The full table is in `authoring/evidence/verifier_calibration.txt`, the verifier runs in
`authoring/evidence/verifier_tests.md`, and `authoring/provenance/` has the scripts that fetched the data, built the
records and made the key.

Known limitations:
- Real packets are only checked for support, not for being real. The author's detector does not yet show more real
  90–150 s packets than intermittent turbulence produces (`authoring/evidence/reference_audit.md`).
- One 72-hour scrambled record is a weak false-alarm test: a detector with about one chance report per day passes it
  most of the time.
- The verifier enforces the 15-minute limit per record but not the 1 CPU and 2 GB stated in the instruction.
- The hidden records and key are public once merged, and the agent has internet access. The records are public CDAWeb
  data plus injections, so a determined agent could in principle find the key or reconstruct the injections.

## Attempts

See `authoring/attempts.md`.
