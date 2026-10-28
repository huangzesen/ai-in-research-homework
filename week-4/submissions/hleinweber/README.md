# Week 4: Research Agent email and subagents

Harness: https://github.com/hleinweber/research-agent

Published implementation for this submission: https://github.com/hleinweber/research-agent/commit/ee4594c

Author: hleinweber. Agent: Research Agent. Model: gpt-4.1-mini. Interfaces: web, terminal, and Telegram. Research: InSight seismology and magnetometer observations on Mars.

## Hello and class reply confirmed

The required hello was sent October 27, 2026, approximately 17:49 America/Los_Angeles, from the agent's dedicated Gmail account to lingtai2026@gmail.com, subject `[AIR-2026 hello] hleinweber`. It used the required eight fields followed by an agent-written introduction under 100 words. Gmail SMTP accepted the send.

**Class reply received and read back:** the class agent replied October 27, 2026, at 20:40:28 America/Los_Angeles, thanking Research Agent for its hello and introducing it to other class agents. On October 28, the reply was retrieved from the dedicated Gmail inbox, read, and summarized to the student. This confirms hello receipt and completes the reply read-back requirement. No acknowledgement was sent. Private reply contents and other participants' contact details are omitted from this submission.

A separate self-addressed message was successfully sent/read back, and the student confirmed its arrival. Live harness inbox/read checks and send-approval denial checks passed. Credentials stay in the private environment or ignored .env and are not included here.

## Contents and use

- `hleinweber-email/`: plugin metadata, MCP configuration, IMAP/SMTP server, skill, and setup README. Copy into the harness's `plugins/` folder.
- `agents/`: restricted mail-reader and research-reader, plus stop-demo and limit-demo. Copy into the harness's `agents/` folder. The research type requires the InSight literature plugin from the harness.
- `transcripts/`: five reviewed demonstrations and a review index, with private inbox data redacted and scientific caveats documented.

The implementation lives in the linked harness (`subagents.py`, `agent.py`, `shell_tool.py`). Run `uv --system-certs run python web.py` or `uv --system-certs run python agent.py`; add `--telegram` for phone mode. Follow the harness and email READMEs for private configuration. No agent framework is used.

## How subagents run

Each worker runs the same loop in a daemon thread with a fresh private conversation, its type's system prompt, a follow-up inbox, and an enforced tool allow list. State lives in the session's in-memory Subagents manager. Workers share the existing MCP sessions through the loader's async bridge. `delegate(agent, task)` waits for a report; `subagent` exposes start, list, send, wait, read, and stop. At most four run at once, with a default 20-model-turn budget and ten-minute lifetime. Workers cannot start other workers. Idle workers resume their existing conversation on send; failed/stopped workers cannot resume. Serialized approval prompts identify the worker. Stop sets a cancellation event and kills the shell process tree using Windows taskkill /T /F or a POSIX process group. Logs record PID and confirmed exit. In-flight model/MCP requests may return at their normal timeout, but cannot trigger further tools after stop. Session shutdown stops workers.

Ignored private JSONL logs in `logs/<session>/` preserve main and worker conversations, tool calls/results, approvals, process events, state changes, token usage, session IDs, and UTC timestamps. A session-wide sequence orders the audit. Worker usage is tracked per worker and forwarded to the interface totals. Files survive restart; live agent state is not restored. Only reviewed exports appear here.

## Demonstration review and validation

1. Inbox: main delegates to read-only mail-reader; recent read/unread results and report return are logged. Private fields are withheld.
2. Fan-out: three background starts precede wait; active intervals overlap and the main agent combines the reports.
3. Follow-up: send resumes the same worker with no new tools. Its prior search found no magnetometer source, so the answer explains the evidence gap rather than a retrieved paper.
4. Stop: approval, running PID 24228, list/read, stop, confirmed termination, cancellation, and final stopped/non-running state are captured.
5. Limit: three successful calls exhaust a three-turn budget; the worker fails before the fourth call with max_turns exceeded and the main agent reports why.

Fourteen deterministic checks passed, covering restrictions, approvals, context preservation, logs, process cancellation, and limits. Plugin integration checks and live delegation/follow-up passed. These verify software behavior, not scientific claims. Transcript caveats distinguish source types, missing abstracts, search coverage, and unsupported generalizations.

## AI assistance

OpenAI Codex helped implement/debug the email plugin and plain subagent manager, diagnose SMTP connectivity, add audit logging/tests, review evidence, redact inbox details, and prepare submission files. The student configured credentials privately, approved sends/commands, confirmed delivery, ran the interactive demos, and reviewed outcomes. The harness demonstrations used gpt-4.1-mini.
