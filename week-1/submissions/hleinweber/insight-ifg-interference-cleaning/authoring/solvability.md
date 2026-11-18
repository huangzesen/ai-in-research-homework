# Solvability review

Reviewed: 2026-11-17, commit 6081bd4 plus existing working-tree changes, by GPT-6 Codex using PowerShell and local Python, in a session that did not help build the task.
**Verdict: solvable** (conditional on an uncontaminated class run)

Reconsidered after the scientist reported that the October agent run did not use the online reference, which was already available. I did not independently audit that trace for retrieval, and the next runner's isolation is unverified. This verdict assumes the class run follows the instruction prohibiting task-specific online answers; the publicly accessible exact answer remains a concrete shortcut and any run using it cannot demonstrate scientific performance. Scientific solvability is qualified by the scientist's explicit confirmation that an acceptable cleaning is reachable from the supplied input and published knowledge, and by their confirmation that the reconstructed prior candidate's 40 failed windows are failures. The original method and its full input history remain unavailable; acceptance of a second independent valid cleaning has not been demonstrated. This verdict relies on the scientist's judgment rather than an independent reconstruction.

| # | Check | Answer | Reason and evidence |
|---|---|---|---|
| 1 | Information | yes | The output structure, filter, bridge rule and threshold in tests/test_outputs.py are stated in instruction.md. Provenance records the scientist's input-sufficiency confirmation. |
| 2 | Stated and hidden ranges | yes | The instruction distinguishes existing event windows from added windows of at most 120 samples. The verifier scores its stored windows; README.md and bridge-exclusion-validation.json document coverage and gap checks. I did not independently rebuild the window catalogue. |
| 3 | An honest reference | unclear | This is the permitted shipped-reference case: solution/solve.sh decompresses a precomputed scientist cleaning. I verified numerical equality with tests/reference.npz, not the production method. authoring/provenance/README.md records manual tuning and input sufficiency, but explicitly does not establish which auxiliary inputs were used originally. I could not run the requested isolated scratch-copy oracle under the read-only filesystem. |
| 4 | A right answer passes reliably | unclear | The reference passes with zero error. The scientist considers 1 nT sufficient, but no measurement-uncertainty calibration or independently acceptable full cleaning is supplied. Small synthetic perturbations documented in the earlier report do not establish scientific uncertainty. |
| 5 | A wrong answer fails reliably | yes | I reproduced 332 failing windows for the input and 368 for a constant field. The reconstructed prior candidate fails 40 windows and 51 component checks; prior-agent-scientist-review.json confirms these are failures. Its byte identity with the original candidate is unverified. |
| 6 | Identifiable | unclear | Abrupt and recurrent three-component signatures can provide evidence of interference, and the scientist confirms input sufficiency. No independent construction establishes identifiability of every retained correction; reference bridge interiors are excluded. |
| 7 | A defensible key | unclear | Bridge interiors are excluded and their differences interpolated before filtering, mitigating arbitrary bridge shapes. The scientist's confirmation rejects the particular prior candidate, but does not show that other acceptable reconstructions pass, especially at retained endpoints and short windows. |
| 8 | Not misleading by construction | unclear | The instruction warns against blanket smoothing and states the grading filter does not prescribe a cleaning method. No specific self-check trap is established, but the physical decomposition was not independently reproduced. |
| 9 | One fact does not decide it | yes | The record contains 200000 vector samples and many local windows; the numerical scoring procedure is specified in instruction.md. |
| 10 | No shortcut, no leak | unclear | The public repository contains solution/data/solution.asc.gz and tests/reference.npz, which provide the exact answer, and public network access is enabled in task.toml. The instruction prohibits task-specific online solutions, but does not prevent retrieval. The scientist reports the October run did not use the online answer; I did not independently audit its trace. The verdict assumes an uncontaminated class run, whose isolation is unverified; audit the new trace. |
| 11 | Limits | unclear | task.toml provides 18000 seconds, one CPU, 2048 MB and 4096 MB; NumPy and SciPy are installed. README.md explains that the 160-hour estimate concerns reading and method development, not measured runtime. Actual independent cleaning runtime and resource requirements are unverified. |

## What I ran

- Read the skill, instruction, task settings, verifier, oracle, Dockerfile, README, provenance, scientist confirmation, prior regrade, previous report and validation records. The working tree has substantial pre-existing changes, including this report.
- With local Python 3.12, NumPy 2.5.3 and SciPy 1.18.1, imported the actual numerical verifier functions with a minimal pytest decorator stub; this was not a pytest run. Loaded both gzip files and the verifier bundle in memory. The solution equals the reference numerically, the input timestamps match, and there are 200000 rows, 2340 windows and 21721 excluded samples. The shortest segment has 560 samples.
- Scored the reference (zero failures), input (332 failed windows, 475 component checks), constant field (368, 516) and reconstructed prior candidate (40, 51).
- Did not run Docker, Harbor, an isolated scratch-copy oracle, uncertainty calibration or a fresh agent. The filesystem is read-only; pytest is absent in the local Python environment. Previously recorded Docker and validation results were read, not independently rerun.

## Problems

1. The publicly accessible exact reference is an actionable shortcut. The task instruction prohibits its use, but the benchmark cannot establish scientific performance without monitoring retrieval and use.
2. Provenance does not establish all original inputs; the scientist confirms reachability from input and public knowledge but does not certify the original input history. The reference copy is not an independent construction.
3. The 1 nT threshold is a scientist judgment, not an empirical acceptance calibration. The confirmed 40 failures support rejection of that candidate, not acceptance of all defensible cleanings.

## Smallest fix

None required for the conditional verdict. Audit the class trace for successful retrieval and use of task-specific answers; if an answer is used, the run is contaminated and cannot establish scientific performance. Restricting access to answer-bearing sources would provide stronger assurance if feasible. The scientist has only the one cleaning; the 1 nT threshold remains expert judgment rather than independent calibration.

## What to check in a run's trace

Check successful retrieval or use of this repository or mirrors, solution/data/solution.asc.gz, tests/reference.npz, reference-derived authoring evidence, and the published prior trace at https://class.xhelio.ai/homework/traces/insight-ifg-interference-cleaning.json. Check mounts for solution, tests, authoring, host answer files or Docker sockets. Ordinary InSight publications are permitted; distinguish access to those from access to task-specific answers.


