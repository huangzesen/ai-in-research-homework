# Daily candidate (not promoted to the task)

The student requested calendar-quarter rounds with daily decisions. This isolated authoring prototype preserves the current monthly task and its independent review. No schedule, live agent, credentials, approvals or reward files are changed.

Run from this directory: `python3 calibrate.py` and `python3 validate.py`. Standard library only. Inputs are the official December 2024 French daily archives through 2024-12-31; original URL and hashes are in `evidence/provenance.json`. Only pre-2000 industry data are placed under this candidate's environment. Full data and factors remain under its tests directory. Do not copy the entire authoring folder into a solver environment.

See `instruction-draft.md` for the candidate contract. Daily close-to-close timing is idealized and not actual next-open execution. Quarterly settlement resets wealth, not prior observations. A 1,260-completed-day history cap bounds replay work; it is explicit and must be reviewed. Scores remain descriptive with `passed: null` until the student approves a defensible threshold after baseline calibration. There is no claim of a passing reference, frontier-agent failure or years of expert effort.

Calibration includes static industry holdings, daily equal-weight rebalancing, and two conventional daily momentum policies. It is not a hidden-data optimizer. Full-quarter details are recorded, including losses, so a high win fraction cannot hide their magnitude. These fixed author-inspected historical quarters are not a genuinely unseen future test.

## Measured checkpoint (2026-11-08)

All 6,289 chronology calls and 100 quarter settlements passed local validation. Daily equal-weight rebalancing won 53 quarters; top-three and top-four daily momentum each won 50; constant BusEq won 59. Win rate and economic payoff differ: constant Durbl won only 49 but had mean quarterly excess return about 1.411 percentage points, alongside a worst quarterly excess return about -44.636 percentage points. These are exploratory baseline comparisons on already-inspected data, not significance claims. Setting a hurdle just above the observed best baseline would be retrospective and would not yet have a demonstrated passing reference. Student scoring priorities and a defensible pass rule remain open.

## Primary objective selected

The student selected number/fraction of winning quarters as the primary objective. Payoff and drawdown are auxiliary disclosures, not hidden pass gates. No tie-break or binary hurdle has been approved. `select_training.py` selects once from a fixed 16-policy family using only visible 1980–1999 industry returns and a daily equal-weight proxy, with no market or post-1999 file access. The chosen policy (252 days, no skip, top three) won 53/80 training rounds against that proxy but only 45/100 final rounds against the actual market. Opponents differ, so the rates are not a matched train/test comparison. Preserve this negative result; do not claim a passing reference or retune on the final period.
