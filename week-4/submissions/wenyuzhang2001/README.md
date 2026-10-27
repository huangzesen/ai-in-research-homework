# Week 4 — wenyuzhang2001

Harness: https://github.com/WenyuZhang2001/ai-study-agent (default branch: `codex/build-harness`). Implementation details: [SUBAGENTS.md](https://github.com/WenyuZhang2001/ai-study-agent/blob/codex/build-harness/SUBAGENTS.md).

## Email and class hello

The dedicated Gmail plugin provides IMAP inbox listing/reading and SMTP plain-text sending through the official MCP Python SDK. The agent's credentials are entered locally in a gitignored `.env`, passed through process environment, and are not included here. Server-side recipients are restricted to the agent's own inbox and `lingtai2026@gmail.com`; the harness additionally requires approval. Received emails are untrusted text, never instructions.

An independent Codex instance sent one self-test email and read it back; I confirmed receipt. The email plugin also worked in my own harness. The class hello was sent exactly once on **October 21, 2026 at 15:00 America/Los_Angeles (PDT)** in the specified field order and with an agent-written note under 100 words. Gmail returned a Message-ID. As of the **October 27 inbox and spam check**, no class-agent reply has arrived; recipient delivery and reading of the reply remain pending. I do not claim that requirement is complete, and did not resend the hello.

## Subagent implementation

Each child uses the same explicit Agent loop with its own system prompt, task, conversation and scoped tools. A `threading.Thread` runs each background worker; a queue carries follow-ups, a condition lock protects in-memory state, and an event/deadline controls cancellation. All children share MCP sessions on a single asyncio lifecycle loop; tool requests are dispatched concurrently. `delegate(agent, task)` waits for a report. `subagent` supports `start`, `list`, `send`, `wait`, `read`, and `stop`. Idle children retain their conversations; stopped/failed children cannot resume. Main receives reports/statistics and completion notes, not raw child tool results unless it explicitly requests log inspection. `stop` sets the cancellation event and kills the active command's process group, including descendants. Session exit/reset stops all children. Private logs live in ignored `logs/<session>/<id>.jsonl`; token usage includes child calls. At most four workers run; child recursion is forbidden; approvals are serialized and labeled. Defaults are 20 model calls and a ten-minute active-episode deadline. In-flight HTTP requests may finish at timeout after cancellation, but cannot trigger subsequent tools. Final failure summaries use verified program records rather than invented missing observations. No agent framework is used.

## Agent types

- `mail-reader`: inbox list/read only; no sending or bash.
- `quant-researcher`: nine read-only price, news, company and event research tools.
- `command-checker`: bash-only diagnostic type used for the exact approved `sleep 600` stop demonstration.
- `limited-researcher`: historical daily-bar tool only, capped at three model calls for the limit demonstration.

## Five live demos

1. [Mail delegation](transcripts/01-mail-delegation.md): one inbox-header listing; main receives the report rather than raw results. Private mail metadata is omitted from the public transcript.
2. [Parallel research](transcripts/02-parallel-research.md): three workers inspect TSLA/NVDA/AMD data; log intervals overlap and main combines the reports.
3. [Follow-up](transcripts/03-followup.md): a baseline and continuation run in the same live session; the same child retains context and answers with zero additional research calls. The earlier parallel-demo process had ended; no cross-process in-memory persistence is claimed.
4. [Stop](transcripts/04-stop.md): main lists/reads/stops a running `sleep 600`; its process group is empty afterward and resuming is rejected.
5. [Turn limit](transcripts/05-turn-limit.md): a four-step task hits the three-call cap, ends as failed, notifies main and cannot resume.

The full **89-test** regression suite passed, including real MCP concurrency, context/tool isolation, approvals, process termination, deadlines and grounded failure summaries. The transcripts use the configured model with actual tool execution; unit tests use fixtures. Windows/Linux behavior is not runtime-tested. No email body is published; no passwords, keys, private logs or failed test drafts are included.

## Research and AI assistance

I am developing a quantitative model that combines price time series with numerical indicators extracted from news and company information to build and evaluate trading strategies. This remains a research goal: the current price model does not yet integrate text indicators, and historical tests have not demonstrated a probability edge. No brokerage/orders are implemented.

Codex helped write and explain the email plugin, scoped agent types, delegation/background lifecycle, approval/cancellation logic, tests and documentation. The configured research-agent model wrote the hello introduction and ran the demos. I created/configured the dedicated account locally, supplied the research direction, confirmed email receipt, reviewed the hello, explained the architecture at course checkpoints, and authorized submission.
