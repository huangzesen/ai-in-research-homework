# Solvability review

Reviewed: 2026-11-08, base commit `dc9d83e` plus the current uncommitted historical-audit revision, by Codex using local Python 3.12 and shell tools, in an independent session that did not help build the task.
**Verdict: solvable**

This verdict covers the current top-level historical audit, not the archived strategy-discovery tasks. It assesses reproducible accounting on supplied historical observations, not investment merit, pristine holdout performance, or research difficulty. Only this report was written in the repository; no student approval commands were run.

| # | Check | Answer | Reason and evidence |
|---|---|---|---|
| 1 | Information | yes | `instruction.md` specifies histories, daily timing, fees including entry/exit, proportional fee deduction, contribution dates, unitized NAV, CPI months, flags, summary fields and tolerances. `environment/policy_runtime.py` supplies exact policy semantics, including top-k ties by column index. Every assertion in `tests/test_outputs.py` maps to the output contract, apart from a harmless 2 MB artifact cap well above the required output size. |
| 2 | Stated and hidden ranges | yes | The full historical inputs are visible. Confirmed 4,026 aligned industry/market dates, 2009-01-02–2024-12-31, and 193 CPI months, December 2008–December 2024. The scorer covers exactly 16 quarters and 160 scenario/method/quarter rows. There is no hidden forecast window or positive-performance threshold. |
| 3 | Honest reference | yes | `solution/solve.py` and `solution/analysis.py` read only public CSVs, frozen policies and the public interpreter. Ran a copied reference with `tests/` and `authoring/` excluded in a fresh subprocess; both original verifier checks passed. This is a computed reference, not a shipped precomputed-answer exception. |
| 4 | Correct answer passes reliably | yes | An independently written account loop reproduced all 160 rows' wealth, fees, drawdown, inflation floor and purchasing-power gain; maximum absolute difference was 2.22e-16. Reversed rows and quarterly numbers rounded to 12 significant digits still passed both checks. Fixed rounded historical inputs imply deterministic arithmetic tolerances, not measurement-noise or statistical-confidence intervals; regenerating seeds is inapplicable. |
| 5 | Wrong answer fails reliably | yes | Independently exercised no output, zero costs, early availability of future monthly deposits, zero drawdown, ignored inflation, constant-negative conclusions, NaN wealth, a flipped flag, duplicate rows and missing summary fields. Every incorrect submission failed at least one mandatory check. See results below. |
| 6 | Identifiable | yes | All scoring returns, CPI levels, fixed policy sources and interpreter are supplied. Prior-day windows determine targets; explicit accounting determines each output. No latent policy, selected future strategy, private benchmark or grader-only scientific choice must be inferred. |
| 7 | Defensible key | yes | Independent bookkeeping agrees with the reference; source reconciliation confirms the exported archive observations. The key applies explicit conventions rather than an unstated investment judgment. It correctly charges daily target turnover, entry and terminal liquidation, matches deposits and removes their effect from drawdown. No invented daily CPI or interpolation is required. |
| 8 | Not misleading by construction | yes | `instruction.md` and `environment/data/README.md` identify exploratory frozen policies, fully visible retrospective outcomes, French broad market, frictionless RF, research fills and monthly CPI endpoints. Passing does not require any strategy to win. The arithmetic self-checks reward the stated conventions. |
| 9 | One fact does not decide it | yes | The task requires integrating policy timing, multiple cash-flow scenarios, cost-aware holdings, NAV, inflation and comparison aggregation. All specialized conventions are supplied; success does not hinge on recalling one obscure finance fact. |
| 10 | No shortcut or leak | yes | No expected audit outputs appear in the agent-visible input files. Both artifacts and all specified numbers/flags are checked, so generic positive/negative claims cannot pass. Frozen policies are expressly inputs, not answer leaks. The public repository's `tests/`, `solution/` and archived audit evidence remain an external answer-retrieval risk; internet access cannot enforce the instruction's prohibition. Trace review is essential, as described below. |
| 11 | Limits | yes | The public-input reference ran in about 4.47 seconds locally with standard-library Python; 3,600 seconds, one CPU, 2 GB RAM and 4 GB storage provide substantial margin. Agent dependencies and offline verifier dependencies are pinned in their Dockerfiles. README honestly calls the 1.5-hour estimate provisional and does not claim years of expert research. Docker/Harbor integration remains untested here because Docker is unavailable; this does not obscure a computational feasibility concern. |

## What I ran

Read the current instruction, task configuration, agent/verifier Dockerfiles, both verifier assertions and recursive comparison helper, expected fixture structure, complete reference and public policy runtime, all three frozen strategies, current provenance and calibration source/results. Archived development materials were used only as provenance, not as task requirements. No calibration script that writes repository evidence was executed.

Scratch directory: `/tmp/sector-audit-review/`; removed after writing this report. The independent `review.py` script copied the task excluding `tests`, `authoring`, `.git` and bytecode caches. It invoked:

```text
PYTHONDONTWRITEBYTECODE=1 DATA_DIR=<isolated>/environment/data
PUBLIC_RUNTIME_DIR=<isolated>/environment RESULTS_DIR=<scratch>/results
python3 <isolated>/solution/solve.py
```

These environment assignments were passed together to a fresh subprocess. The original verifier's two test functions were loaded read-only and called directly against scratch artifacts; no reward file, approval, schedule or task artifact was changed. This tests verifier logic, not its Docker/pytest/CTRF wrapper.

| Submission/check actually run | Quarterly check | Summary check |
|---|---|---|
| Isolated reference | pass | pass |
| Correct outputs, reversed quarterly rows and 12-significant-digit quarterly numbers | pass | pass |
| No output | reject | reject |
| Recomputed zero transaction costs | reject | reject |
| Recomputed monthly deposits all available at quarter start | reject | reject |
| Correct outputs except drawdown replaced with zero | reject | pass |
| Recomputed with constant CPI, ignoring inflation | reject | reject |
| Correct outputs except all majority conclusions false | pass | reject |
| NaN terminal wealth | reject | pass |
| One flipped joint-win flag | reject | pass |
| One duplicated quarterly row | reject | pass |
| Empty summary object | pass | reject |

The drawdown probe changes only quarterly drawdown values, so it demonstrates rejection of that output error rather than a full recomputation of a deposit-masked NAV method. The actual recomputed wrong-accounting probes are zero fees, premature deposits and ignored inflation. Overall acceptance requires **both** tests; a pass in one column does not accept an incorrect analysis.

My independent account loop used the supplied interpreter for fixed-policy weights but independently maintained holdings, fee scaling, cash issuance and the NAV series, using `math.fsum` for sums. It compared five primary numerical quantities for all 160 rows against reference outputs; maximum absolute difference was 2.22e-16. Reference aggregation and exact flags were also inspected against the instruction; fixture verification then checked every output field. This is independent accounting validation, not a claim to have independently reimplemented the restricted interpreter.

Additional read-only Python checks verified all seven recorded input SHA-256 hashes. Re-parsing the first value-weighted French industry table reproduced all 4,026 supplied industry rows, and parsing the factor archive reproduced all market and RF rows (absolute tolerance 1e-14). CPI bytes matched the preserved source snapshot. An initial reconciliation command accidentally sliced industry rows to 4,025 and failed its length assertion; correcting that scratch-only slice to the actual 4,026 rows passed. No input data correction was needed.

No internet source refresh, full Docker build, Harbor integration, frontier-model attempt, new random-data draw or student approval command was run. This review validates the supplied historical snapshots rather than independently authenticating their original downloads. It is not financial advice or an assessment of future returns.

## Problems

No blocking solvability defect found in the current audit.

1. Public answer retrieval remains possible: the public repository includes fixtures, reference code and earlier computed audit evidence. Correct artifacts alone cannot prove an agent performed the analysis. This is an evaluation-integrity limitation, not an ambiguity in the deterministic question.
2. End-to-end container/artifact transfer and CTRF/reward plumbing are not locally demonstrated. The direct verifier logic passes; the shell wrapper and pinned Dockerfiles were inspected only.
3. The verifier assesses the specified structured conclusions, not free-text reasoning, actual causal execution traces or compliance with the prohibition on strategy fitting. This is adequate for the current artifact contract but should not be described as proof of research process or scientific significance.
4. The 1.5-hour estimate is explicitly provisional. This audit is computationally small and establishes no claim of a year of expert difficulty.

## Smallest fix

None required for the current deterministic historical-audit contract. Before claiming a fully validated benchmark run, execute the unchanged Docker/Harbor path and inspect the run trace for prohibited task-specific retrieval. No task edits or student approvals were made in this review.

## What to check in a run's trace

Check for fetches of this repository's `tests/expected_quarterly.csv`, `tests/expected_summary.json`, `solution/`, `authoring/evidence/`, and `authoring/daily-prototype/post2008-study/evidence/benchmark_comparison.json`, or copied task-specific online answers/hints. Inspect whether the agent derives results from the supplied inputs rather than these artifacts. Also check for modified/reselected policies, same-day/future return access in policy decisions, unavailable future deposits, and replacing French market/RF/CPI with external series. All scoring observations are intentionally visible; retrospective outcome inspection alone is not leakage or cheating in this task. Do not interpret a successful historical audit as evidence of investable execution, lower risk, statistical significance or future superiority.
