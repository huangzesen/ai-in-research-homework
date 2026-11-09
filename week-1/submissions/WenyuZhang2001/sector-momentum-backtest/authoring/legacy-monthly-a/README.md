# Industry strategy versus a hidden market return series — prototype A

**Author:** Wenyu Zhang · **Field:** quantitative finance · **Status:** local prototype, not independently re-reviewed or submitted.

The solver receives monthly industry returns through December 1999 and submits a frozen strategy in a documented restricted Python language. A separate offline verifier interprets that strategy sequentially on January 2000–December 2024. Future rows and the market series are not available to the strategy; completed industry rows become available after each decision. The goal is final net wealth greater than the disclosed Kenneth French broad U.S. market benchmark, not the S&P 500 or Nasdaq.

## Difficulty

The method is no longer prescribed. The solver must choose a policy using earlier data, with a language supporting lag windows, return/volatility summaries, vector arithmetic, ranking and allocations. However, calibration demonstrates that static equal weighting already beats this benchmark. Prototype A is therefore an operational scoring prototype, not evidence of hard scientific reasoning or of more than a year of expert effort. The previous 1.5-hour estimate is retained as an unvalidated implementation estimate; no years-long estimate is claimed. No frontier model has attempted this revised task.

## Reference solution

`solution/solve.py` installs `solution/strategy.py` as the sole artifact. It ranks eleven compounded monthly returns ending one month before the latest available month and allocates equally to three industries. It does not read the verifier data. The reference and an alternative top-four implementation pass locally. The restricted interpreter parses source rather than executing it, eliminating submitted Python access to verifier files, globals or network. This is a small policy language, not unrestricted machine learning code; expanding the allowed models would require a new interface and review.

## Verification

Every monthly target must have twelve finite nonnegative weights summing to one within 1e-10; shorting, leverage and cash are excluded. The verifier computes gross weighted returns, drifted pretrade weights, absolute traded notional and 10 bp per unit turnover. Both portfolios begin fresh in January 2000, so the benchmark pays its first purchase cost then. Pass requires strategy final wealth greater than benchmark final wealth plus 1e-10. This epsilon distinguishes numerical equality; it is not a statistical significance threshold. No risk hurdle was added.

Run `python3 authoring/evidence/calibrate.py` from this task folder. `authoring/evidence/calibration.json` records the actual results: reference and top-four pass, static equal weight also passes, reversal fails, and invalid zero weights are rejected. `authoring/evidence/validate.py` checks reference artifact dispatch, no-op rejection, chronological history boundaries, interpreter restrictions and an independent accounting cross-check. Local checks do not substitute for the full Docker/Harbor pipeline, which has not been run.

## Data and limitations

`environment/data/train.csv` contains only July 1926–December 1999 industry returns, converted from percent to decimal. Original archive files are under `tests/data/`, copied only to the verifier. The benchmark series is withheld, but its identity and all grading rules are public. See `authoring/provenance/data_sources.md` for archive URLs, original and LF-normalized hashes.

These are public historical observations, already inspected by the authors. They are withheld from the solving container, not newly unseen author data or a prospective experiment. Public repositories, mirrors and model memory remain leakage risks. Repeated feedback can overfit a fixed benchmark. One passing interval says nothing about future outperformance, statistical significance or comparable risk. Industry research portfolios are not executable ETFs; taxes, market impact and other costs beyond the specified model are omitted.

The original independent report `authoring/solvability.md` applies to the old task and is intentionally preserved; a fresh final review is required. Student instruction/window/publication approvals are required again before submission. Nothing has been published for Week 6.
