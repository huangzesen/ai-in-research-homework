# Week 5 — WenyuZhang2001

Harness (validated Week 5 commit): https://github.com/WenyuZhang2001/ai-study-agent/tree/e9c9c59069377d57122cea60d2ce93605d9c83a9

Own synchronous Python model/tool loop; no agent framework. Codex helped inspect the migrated harness, implement and test watchers, controls, scheduling, compaction/memory, durable recovery/outbox and launchd, and summarize private logs into these reviewed evidence transcripts. The student performed real Telegram/mail tests, approved the self-email, reviewed summary loss and explained intent/done recovery.

## Running

Install with uv sync and fill local .env from .env.example (never commit secrets). Run `.venv/bin/python server.py --always-on`; production uses the macOS user launchd service generated/installed by service_control.py. Only one receiver is allowed per workspace; stop the service before an interactive plugin-enabled run. The service reads the existing local .env, uses absolute venv/PATH/CA paths, logs privately and holds caffeinate assertions on AC. It restarts on exit; observed idle SIGKILL recovery: 11.391 seconds. See service/.

## Behavior and configuration

- One durable SQLite event queue. Telegram watcher uses 1-second long polling with a 0.01-second loop wait; email headers every 90 seconds; schedule checks every 60 seconds. These run in code with no idle model calls. Email is labelled untrusted. Durable Telegram acknowledgement follows enqueue.
- Weekday stock research at 08:00 America/Los_Angeles, cron `0 8 * * 1-5`, using completed-day data. Temporary Sunday verification task has been removed. Missed/paused schedule occurrences are skipped, not caught up. At most 10 jobs, no more than hourly per job; add/remove require approval.
- Compaction after a completed wake at 20000 API-reported input tokens, keeping 2 complete user turns; this is the selected course demonstration threshold. Structured memory checkpoint requires approval; maintenance preserves existing notes. Rules and memory refresh every wake. Actual before/next-request input: 21583 → 1344. See compaction transcript for the failed memory write and repair.
- Limits: 8 shared model requests, 5 minutes per wake, 1000000 tokens per local day, 2 sending attempts per recipient/day. Shared reservations include children and maintenance. API cost is usage-reported, not an independent billing audit.
- Owner-only /status, /stop, /pause, /resume are code paths, outside model work. /stop kills owned process groups and children. Unanswered approvals decline after 10 minutes. Robot mail cannot receive replies.
- Append-only fsynced journal, interrupted-tool repair, verified orphan cleanup, persistent FIFO/cursors/pause. Interrupted claimed tasks are not replayed. Outbox intent precedes SMTP; done follows it. Intent-only mail is reconciled read-only against Sent; uncertain delivery is never automatically resent. This favors at-most-once attempts over guaranteed delivery.

## Evidence

Five required demos: transcripts/night.md, compaction.md, kill-switch.md, limit.md, crash.md. Additional service.md records automatic restart. Night: 17.39 elapsed UTC hours across daylight-saving fallback, one scheduled and one message wake, 3 model requests, 31925 tokens, API-reported $0 and zero idle calls. PID and launchd run count unchanged.

SMTP crash/reconciliation and automatic idle launchd restart were separate real tests; a combined SMTP-under-launchd crash is not claimed. Full regression run at service acceptance: 189 tests passed. Historical transcript caps/pending states are annotated with final status.

Private .env, state/, logs/, memory/, addresses, chat IDs and raw mailbox contents are excluded. Exported service paths use AGENT_USER; generate locally before installing. See failures.md for actual bugs and limitations.
