# Week 5 — Jasmine's always-on research agent

Harness: https://github.com/jasmine0010/jasmines-agent

Status: local draft, pending a completed eight-hour replacement and student
review. Week 5 harness changes have not yet been published. The original
overnight attempt is preserved as incomplete in transcripts/night-attempt-1.md.
The student requested a daytime replacement beginning November 3, 10:57:49
Pacific, with a report due 18:58. See transcripts/night.md for actual evidence;
elapsed wall-clock time is not presented as verified continuous operation.

The Windows Task Scheduler service starts at login, uses limited interactive
user privileges, and restarts a missing instance through a native minute
recovery trigger plus one-minute failure retries. It has no runtime limit and
IgnoreNew prevents duplicate instances. The Python runner loads its own .env,
uses absolute paths, logs privately and owns descendants with a Windows job.
The task now continues on battery after the failed AC-only first night. The
public XML is a sanitized export; use install-windows.ps1 for real local paths
and identity. No credential, SID or private mailbox is included here.

Watchers run in code: Telegram long polling uses a one-second wait, email is
checked every 60 seconds, and the scheduler checks once a minute. All events
feed one queue; no model call occurs while it is empty. Startup Telegram DNS
failure no longer aborts other event sources. Phone connectivity is currently
unavailable on the computer's network; the user will restore it. Transport
retries do not wake the model. Shell commands require owner approval except
the exact Get-Location, Get-ChildItem and Get-Date allowlist.

The recurring research task is a weekday 08:00 Pacific digest of new arXiv
PSP/Alfven-wave/solar-wind-switchback announcements. It uses a read-only keyword-
filtered feed tool, labels preprints and bases relevance on abstracts. A
temporary recovery-papers-check runs that task inside the replacement window;
it was removed after its wake completed. Missed jobs are skipped, not caught up.

Compaction triggers at 20000 API-reported input tokens, keeps two recent whole
turns within 24000 bytes, saves approved memory first and never splits tool
calls/results. AGENTS.md and private memory are refreshed at every wake. The
demo measured input dropping from 26262 to 2331; the student identified omitted
padding rows. The actual synthetic summary and its priority-labeling mistake
are included in transcripts/compaction.md.

limits.toml enforces 20 model requests per wake, 15 minutes per wake, 250000
daily tokens and two replies per sender per day. Cached input is not counted
twice. Dollars remain unknown; unreported-use estimates are tracked separately.
/status, /stop, /pause and /resume run in code. /stop kills owned command trees
and subagents; an unanswered approval expires after ten minutes. Robot mail
cannot receive replies. Recovery turns cannot repeat state-changing actions.

The append-only main journal records messages/usage and compaction markers.
Startup repairs missing tool results without executing them. Email outbox
intent/done records and deterministic Message-ID allow Sent reconciliation
after a crash, with no blind resend when delivery remains uncertain.

The five demo transcripts are night.md, compaction.md, kill-switch.md, limit.md
and crash.md. failures.md preserves failures and repairs, including the first
night, missed retry, slow readiness, model acknowledgement and repeated-sleep
request. Raw .env, state, logs, memory, addresses and chat IDs remain private.

AI assistance: OpenAI Codex helped implement, debug and test the harness,
review logs and prepare these artifacts. The student chose the research job
and approval policy, performed real phone/email checks, explained event
waking and recovery, and reviewed the compaction summary. No agent framework
was used. Publication and final PR require the student's evidence/privacy
review; this draft does not claim the replacement run has already completed.

Replacement preflight is verified: the genuine email wake and temporary
scheduled paper check completed with three model requests and 19698 reported
tokens. The temporary job is removed; schedule.toml contains the normal
recurring digest. Telegram delivery remains unavailable on this network.
The remaining runtime requirement cannot be inferred from these short checks;
the full report is scheduled for 18:58 Pacific. No push or PR has been made.
