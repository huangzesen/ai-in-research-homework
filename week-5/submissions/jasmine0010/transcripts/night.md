# Week 5: the daytime replacement run (original overnight attempt incomplete)

Status: passed. Generated from the private append-only journal.

Window: 2026-11-03T10:57:49.821777-08:00 to 2026-11-03T18:58:02.411218-08:00.
Elapsed: 8.00 hours. Same continuously living service process verified: True.

One line per wake-up (local time; email and Telegram contents omitted):

- 2026-11-03T10:59:32.348233-08:00 | email | 1 reported turns / 1 request attempts | 5849 input + 482 output = 6331 reported tokens; 0 cached input (already included) | dollars unknown | completed=True
- 2026-11-03T11:00:15.602293-08:00 | schedule recovery-papers-check | 2 reported turns / 2 request attempts | 12918 input + 449 output = 13367 reported tokens; 8384 cached input (already included) | dollars unknown | completed=True
- 2026-11-03T16:53:50.716857-08:00 | telegram | 1 reported turns / 1 request attempts | 6960 input + 295 output = 7255 reported tokens; 0 cached input (already included) | dollars unknown | completed=True

Totals: 3 wake-ups; 4 admitted model request attempts; 26953 API-reported tokens. Dollars unknown; token budget enforced.
Model request attempts while asleep: 0.

Counts use usage and request-admission records, not the model-call-start marker before budget admission. Failed attempts without usage have no reported token count here; persistent budget estimates remain separate in state/usage.json.

Observed operational failures: {"email_watcher_failed": 123, "telegram_delivery_failed": 2, "telegram_watcher_failed": 1389}.
Requests from native children, if present, are grouped with their active parent wake. No cached tokens are double-counted.

The service requests idle wakefulness. Windows sleep/Modern Standby query: {"events": [], "queried": true}. Process lifetime alone does not prove the computer never suspended.
