# Week 5: the overnight run

Status: incomplete. Generated from the private append-only journal; student review pending.

Window: 2026-11-02T23:15:36.685050-08:00 to 2026-11-03T08:15:00.332866-08:00.
Elapsed: 8.99 hours. Same continuously living service process verified: False.

One line per wake-up (local time; email and Telegram contents omitted):

- 2026-11-02T23:23:22.080799-08:00 | telegram | 1 reported turns / 1 request attempts | 5683 input + 32 output = 5715 reported tokens; 4192 cached input (already included) | dollars unknown | completed=True

Totals: 1 wake-ups; 1 admitted model request attempts; 5715 API-reported tokens. Dollars unknown; token budget enforced.
Model request attempts while asleep: 0.

Counts use usage and request-admission records, not the model-call-start marker before budget admission. Failed attempts without usage have no reported token count here; persistent budget estimates remain separate in state/usage.json.

Observed operational failures: {"email_watcher_failed": 5, "telegram_watcher_failed": 1}.
Requests from native children, if present, are grouped with their active parent wake. No cached tokens are double-counted.

Power was kept awake by the service request. Manual sleep, lid closure or logout must be reviewed with the student; process lifetime alone cannot prove the computer never suspended.

Incomplete evidence:
- The original live service process was not verified; review restarts or downtime.
- The scheduled daily-papers wake has not completed.

Morning diagnosis: Windows Kernel-Power event 105 recorded AcOnline=false at
07:04:56 Pacific and AcOnline=true at 08:08:31. The task's AC-only conditions
stopped it across that interval, covering the 08:00 paper job. Missed jobs are
skipped by design. The student pasted the 08:08 restart notices; these were not
a paper digest. Later lid/Modern Standby events began at 08:21 and are separate
from the overnight power-source interruption. No eight-hour success is claimed.
The task is now allowed to start and continue on battery; no global power-plan
settings or TLS checks were disabled.
