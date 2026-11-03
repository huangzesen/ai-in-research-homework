# Week 5: always-on research agent

Student: **hleinweber**. AI assistance: **Codex**.

Harness: [research-agent, Week 5 release](https://github.com/hleinweber/research-agent/tree/week-5-always-on).
Implementation revision: [`b987129`](https://github.com/hleinweber/research-agent/commit/b98712924eb351d7b50fb26672163eae305ed84d).

A small Python harness with its own model/tool loop, MCP plugins and subagents; no agent framework.
I used Codex to implement the outer loop, scheduler, controls, compaction, recovery,
outbox, Windows service, tests and draft documentation. I performed the phone approvals,
message/email tests and overnight run; checked one received email after recovery;
explained why idle watchers need no model calls; and reviewed summary information loss.

Run installation and service commands from the linked harness checkout on branch `week-5-always-on`, not from this evidence-only class submission folder.

## How it runs

- **Service:** Windows Task Scheduler, ResearchAgentAlwaysOn, running under my logged-in
  account with least privilege and no stored Windows password. A hidden wrapper launches
  the venv Python with agent.py --always-on, absolute paths and an explicit uv PATH.
  It appends stdout/stderr under logs/. The task starts at login; a one-minute recovery
  trigger and IgnoreNew recover missing instances without duplicating a running agent.
  Native one-minute failure retry is also configured, but did not fire in the first test.
  Stop disables the task, and Start re-enables it. A workspace lock excludes a second
  manual plugin host. Keep this Windows laptop awake with its lid open and remain logged in.
- **Watchers:** Telegram long-polls for 20 seconds; email checks the newest 50 inbox UIDs
  every 90 seconds via MCP, without marking mail read; schedule checks/reloads every 60
  seconds. Watchers enqueue timestamped events without asking the model to check.
  Code handles /status, /stop, /pause and /resume directly from the configured owner's chat.
- **Research job:** morning-papers, cron `0 8 * * 1-5`, an 08:00 weekday InSight/Mars
  seismology or magnetometer-calibration literature digest. Model-added jobs require
  approval; maximum ten jobs, each at least hourly. Missed schedule occurrences are skipped.
- **Compaction:** 20,000 reported main-input tokens normally; keep the last two user-message
  groups intact. The demo used 2,000 and one group. A normal approved-tools turn first
  saves durable details to private memory/MEMORY.md (under 200 lines), then one summary
  call keeps Goal/Done/Open/Decisions/Exact/People. Standing rules and memory reload
  every wake. Summary logs distinguish estimates from actual API-reported token counts.
- **Limits:** 20 model calls and 10 minutes per wake, 250,000 input-plus-output tokens per
  local day, three email send attempts per recipient per day, 2,048 output tokens per call.
  Main and workers share daily accounting. Tokens are enforced instead of dollars because
  model prices are not configured. Commands require approval; unanswered prompts expire
  after ten minutes. Automatic/list-mail senders cannot receive replies through the send tool.
- **Recovery:** append/flush/fsync logs/main.jsonl, replay from the latest compaction,
  reconstruct interrupted tool results as not re-run, restore undelivered queued events,
  notify the owner and await review of interrupted effects. Old subagents are not relaunched.
- **Email:** state/outbox.jsonl holds intent/done with a content-derived key and stable
  Message-ID. Pending intent searches Gmail Sent, with a recent-content fallback if the
  provider rewrites Message-ID. Confirmed delivery returns already sent; unresolved
  delivery is held rather than automatically resent. Normal approval and reply caps apply.

## Five required demonstrations

| Demo | Evidence |
|---|---|
| Night | [night.md](transcripts/night.md): 12h 34m 30s, two wake-ups, five model calls, 22,942 tokens, zero calls while idle. Morning job ran at 08:00:49 and finished at 08:01:07. |
| Compaction | [compaction](transcripts/week5-compaction.md): saved summary, before/after metrics, MARS-739 recall and student-confirmed loss of circular-buffer/linked-list examples. |
| Kill switch | [kill switch](transcripts/week5-kill-switch.md): approved 600-second sleep, /status PID, /stop, cancellation and process exit. |
| Limit | [daily limit](transcripts/week5-daily-limit.md): one-token cap held the next request with the model-call count unchanged; normal cap restored. Exact warning text was not supplied in my confirmation. |
| Crash | [interrupted tools and email](transcripts/week5-crash-live.md), plus [automatic service restart](transcripts/week5-service-restart.md): no blind rerun; recovered done; one received email; replacement ready in 42.59 seconds. |

Supporting message, scheduling, pause/resume, graceful-restart and isolated-crash
transcripts are included. [failures.md](failures.md) records bugs and test mistakes,
the Windows memory encoding failure, native retry failure and the overnight email-watcher error.

## Validation and limitations

The reviewed release passes **70 offline tests** across scheduler, controls, compaction,
recovery/outbox, real isolated process-death helpers, service and night accounting. These
use fake models and mail services except the fixed local process tests. The transcripts
separately identify live checks performed with the real agent and email account.

One RuntimeError from the email watcher was logged at 00:22:20 during the night;
the underlying cause was not retained. The service stayed running and no later watcher
errors were logged, which does not prove a later inbox check succeeded. No new machine
login was performed to exercise the login trigger; recovery was tested in the existing session.
Already-submitted API requests may cross a token cap; subsequent calls are stopped.
The email window/UIDVALIDITY and schedule-state-to-queue crash gap are documented harness
limitations. Unconfirmed SMTP delivery may need manual review instead of an automatic retry.

## Files and privacy

schedule.toml, limits.toml and compaction.toml are the actual configurations used.
service/ResearchAgentAlwaysOn.xml is a privacy-reviewed export from the registered task;
Windows machine SIDs were replaced with my local/public username. Its machine-specific
paths identify this checkout. The helper scripts show installation and management;
regenerate the definition for a different account or location.

No .env, credentials, runtime state, inbox contents, addresses or raw private journal is
submitted. The summary excerpt omits Telegram message IDs and an exact owner-message
timestamp. Demo process IDs and timestamps remain as local execution evidence.
