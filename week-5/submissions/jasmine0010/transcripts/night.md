# Week 5: the daytime replacement run (original overnight attempt incomplete)

Status: incomplete. Generated from the private append-only journal; student review pending.

Window: 2026-11-03T10:57:49.821777-08:00 to 2026-11-03T11:07:27.036859-08:00.
Elapsed: 0.16 hours. Same continuously living service process verified: True.

One line per wake-up (local time; email and Telegram contents omitted):

- 2026-11-03T10:59:32.348233-08:00 | email | 1 reported turns / 1 request attempts | 5849 input + 482 output = 6331 reported tokens; 0 cached input (already included) | dollars unknown | completed=True
- 2026-11-03T11:00:15.602293-08:00 | schedule recovery-papers-check | 2 reported turns / 2 request attempts | 12918 input + 449 output = 13367 reported tokens; 8384 cached input (already included) | dollars unknown | completed=True

Totals: 2 wake-ups; 3 admitted model request attempts; 19698 API-reported tokens. Dollars unknown; token budget enforced.
Model request attempts while asleep: 0.

Counts use usage and request-admission records, not the model-call-start marker before budget admission. Failed attempts without usage have no reported token count here; persistent budget estimates remain separate in state/usage.json.

Observed operational failures: {"telegram_delivery_failed": 2, "telegram_watcher_failed": 56}.
Requests from native children, if present, are grouped with their active parent wake. No cached tokens are double-counted.

The service requests idle wakefulness. Windows sleep/Modern Standby query: {"events": [], "queried": true}. Process lifetime alone does not prove the computer never suspended.

Incomplete evidence:
- Fewer than eight hours have elapsed.

This is an early preflight snapshot. The full-duration report is scheduled for 18:58 Pacific on November 3.
