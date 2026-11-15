# Reviewed Week 4 demo transcripts

These transcripts replace the earlier excerpts with persistent main/worker audit evidence from the reruns on October 27, 2026 (America/Los_Angeles). Timestamps are UTC. They preserve actual call arguments, correlated tool results, approval evidence, and process events while omitting duplicate UI events and private inbox contents.

| Demo | Review |
| --- | --- |
| 1. Inbox delegation | PASS: delegate, read-only inbox call, report return, and main response recorded; private fields redacted. |
| 2. Three-way fan-out | PASS: corrected rerun starts three background workers before wait; their active intervals overlap and the main agent combines their reports. Scientific caveats qualify the recorded claims. |
| 3. Follow-up | PASS for preserved context and no new tools. Search had found no magnetometer source, so paper-specific scientific discussion was unavailable. |
| 4. Stop | PASS: background start, approval, PID, running list/read, stop, confirmed termination, cancellation, final stopped list. |
| 5. Limit | PASS: three successful calls, enforced failure before fourth, main-agent notification. |

## Remaining before submission

All five lifecycle demonstrations have supporting main/worker audit records. Demo 3 remains a context-reuse example about a search that found no source; a follow-up to a retrieved paper would provide a richer scientific example but is not needed to prove conversation continuation. The class-agent reply was received and read back on October 28, 2026; see the submission README. Final publication remains to be done.

The scientific reports are model outputs with limitations, not independently validated research conclusions. No email addresses, inbox subjects/bodies, credentials, or browser cookies are included in these exports. Private raw logs remain ignored by Git. Class hello receipt and reply read-back are confirmed. Nothing here has been published.
