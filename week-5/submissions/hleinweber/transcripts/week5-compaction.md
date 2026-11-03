# Week 5 compaction demo

Date: November 2, 2026. Evidence: saved summary, private session log and student report.

- Demo mode: 2,000-token trigger, one recent user-message group retained.
- Triggering ordinary call input: 3,099 reported tokens.
- Summary call input before replacement: 2,516 reported tokens.
- Summary output: 193 reported tokens.
- Replacement history size: approximately 1,976 tokens (JSON UTF-8 bytes / 4 estimate, not an API measurement).
- Next ordinary call input: 2,526 reported tokens, including refreshed system files, tools and the new question. It is not directly comparable to the bytes/4 estimate or the summary-only request's inputs.
- Summary file: logs/compactions/20261102-180256-436d890c.md.
- The student confirmed receiving the compaction notification before asking for the test code.
- The student reported the answer: "Your test project code is MARS-739."

The summary retained the project code and memory file path. Its headings were Goal, Done, Open, Decisions, Exact and People. It described the completed event-queue explanation and reported saving memory; that description is the model's summary, not an independent validation of every statement in the explanation.

Student-confirmed omission: the original explanation explicitly described circular buffers and linked lists as queue storage structures. The summary only says it covered implementation details; it does not retain either data structure. The student confirmed the circular-buffer and linked-list omission and discussed why compaction intentionally drops explanatory detail.

The initial live attempt failed because a PowerShell write produced UTF-16 memory; BOM-aware reading fixed the crash. The rerun completed compaction and recall. Subsequent restart/send-once tests and the completed overnight run are documented in week5-crash-live.md, week5-service-restart.md and night.md.


## Saved summary (privacy-reviewed excerpt)

Telegram message IDs and the exact owner-message timestamp have been omitted; the summary text below is otherwise retained.

```text
# Goal
Explain event queues in about 800 words. Remember the test project code is MARS-739.

# Done
- Provided an approximately 800-word detailed explanation of event queues covering concept, structure, roles in event-driven systems, types, implementation details, use cases, advantages, and challenges.
- Sent a concise Telegram message summarizing the explanation.
- Saved the remembered information (test project code MARS-739 and explanation details) into memory/MEMORY.md.

# Open
- None currently. No outstanding questions or pending tasks.

# Decisions
- Use MARS-739 as the project/test code for context or reference if needed.

# Exact
- Test project code: MARS-739
- Memory file path: memory/MEMORY.md

# People
- Owner via Telegram [exact message timestamp omitted]
```
