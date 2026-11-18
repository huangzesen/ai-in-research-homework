# Prior agent regrade

Regraded 2026-11-16 local time with NumPy 2.1.3 / SciPy 1.14.1 in separate, offline Docker containers limited to 1 CPU and 2048 MB RAM. No model or Harbor run was performed.

| Grader | Passed windows | Failed windows | Failed component/window checks | Reward |
|---|---:|---:|---:|---:|
| Original grader | 629 / 647 | 18 | 24 | 0 |
| Revised exclusions, original event windows only | 542 / 559 | 17 | 22 | 0 |
| Current full-coverage grader | 2300 / 2340 | 40 | 51 | 0 |

The full-coverage pass fraction is 98.3%. The window sets differ; their pass fractions are not directly comparable as a measure of improved cleaning. The submitted record was held fixed while the grading changed.

Of the original 18 failed windows, 11 still fail and seven are no longer failing or are excluded. Six previously passing event windows now fail after canonicalization and removing excluded samples from the RMS denominator. Another 23 failures occur in newly scored regions. A total of 17 failures are in retained original event windows. Exclusions do not guarantee every retained score decreases: both the filter input and the RMS sample set change.

## Artifact provenance and limitation

No original saved cleaned.asc download was found. The candidate was reconstructed from the final deterministic pipeline in the published class trace, without making new cleaning decisions. The public trace redacts 551 characters from an intermediate run5.py definition. That boilerplate was restored using the later displayed pulse function and exact source strings in subsequent edits; the intermediate block loop was superseded by a fully published edit before execution. The final manual-region list was taken from the recorded final output. All remaining source edits were replayed with their assertions intact. This supports reproducibility but is not proof of byte identity with the unavailable original artifact.

The reconstructed candidate reproduces the published original 18-window / 24-component failure counts (629 passing windows). Input, trace, generated bootstrap, source, candidate, and grader hashes are recorded in prior-agent-regrade.json. The reconstructed candidate is preserved in reconstructed-prior-agent.npz under the `candidate` key. Replay code is regrade_published_agent.py. Per-window scores and zero-based stop-exclusive row ranges are in prior-agent-regrade.json. Raw reconstruction stdout is in prior-agent-reconstruction.log.

Source: https://class.xhelio.ai/homework/traces/insight-ifg-interference-cleaning.json
Original summary: https://class.xhelio.ai/homework/tasks/insight-ifg-interference-cleaning.json

## Interpretation

The revised grader still rejects this prior cleaning. This is a retrospective regrade: the agent was originally told that quiet intervals were unscored, and did not see the expanded grading instruction. It is not a fresh agent attempt against the revised task and should not be reported as one. After reviewing the failure plots, the scientist confirmed: "Ok the remaining failures are confirmed failures." This confirms that the 40 remaining failed windows represent unacceptable cleaning differences in this reconstructed candidate, rather than acceptable interpolation choices. No per-window physical cause was assigned in that confirmation. The conclusion relies on the scientist's review, not merely on reward zero.

These files record the retrospective regrade evidence. No task instruction, reference, or grading criterion changed during regrading.


## Scientist review

The scientist confirmed all remaining failures after the 40-window plot package was supplied. Scope: 40 failed windows / 51 failed component-window checks under the current full-coverage grader. Recorded from the user's explicit confirmation in this session. No reference values, exclusions, tolerances, or computed scores were changed. This supports a scientifically meaningful failure of this candidate under retrospective regrading; it does not substitute for a fresh agent run with the revised instructions or a fresh independent solvability review.
