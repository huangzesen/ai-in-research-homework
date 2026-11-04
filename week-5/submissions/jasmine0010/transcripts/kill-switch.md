# Week 5: live phone kill switch

The owner requested the exact 600-second PowerShell sleep and approved its
execution by Telegram reply. The real model delegated the command to the
process-demo subagent. Owner /status showed the running sleep; owner /stop
then stopped the retained worker. The helper checked the recorded owned OS
process and found it gone. The main agent returned to asleep with an empty
queue. No main-agent shell process is claimed in this delegated run.

The owner confirmed receiving the subagent-stopped notice, the top-level stop
acknowledgement and the OS-check confirmation. This was a genuine phone /stop,
not a helper-injected command. The fresh preview used 4 model requests
and 13636 reported input/output tokens before the budget phase.

The first attempt expired without passing; its receipt is preserved separately.
The repaired helper detects both main and child processes. The current private
receipt is validation/week-5-controls-live.json; no chat ID, mailbox address or
private message body is included here. The tiny-budget demo also passed; see limit.md.
