# Week 3 — QJMeng

Harness repository: https://github.com/QJMeng/qimeng-agent

## Telegram plugin

`qjmeng-telegram` is a stdio MCP server for sending and receiving text in one
configured private Telegram chat. It uses long polling, ignores other chats,
skips queued messages on startup, and keeps the bot token in environment
variables. Its skill explains phone-friendly replies and safe handling of
secrets. It was tested through the student's own harness, the official MCP
SDK client, and Codex CLI; phone receipt and replies were confirmed.

## Seismology plugin

`qjmeng-seismic` provides five tools to query USGS catalogs, summarize depths,
inspect events, classify available two-plane focal mechanisms, and estimate
Gutenberg–Richter b with a user-specified Mc. The validation case is a 100 km
circle centered at 33.3 N, 115.8 W from 2021-10-21T00:00:00Z through
2026-10-21T00:00:00Z, M>=3.0 and Mc=3.0. It returned 205 events and an
exploratory pooled b of 0.966 +/- 0.060 (approximate 1-sigma sampling error).
Mixed magnitude scales, completeness, clustering and mechanism-quality
limitations are explicit. Full public data stays local and is removed when
the MCP session ends. The student accepted the phone-delivered result.

## Run the harness from Telegram

Clone the linked harness repository and run the following in its root:

```sh
uv sync --locked
cp .env.example .env
# Edit .env locally: BASE_URL, API_KEY, MODEL,
# TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID. Never share or commit secrets.
uv run main.py --telegram
```

Wait for the online message and send a research question to the bot. Every
bash command and every MCP tool outside settings.json's explicit allow list
requires a fresh `yes` reply after the approval prompt; other replies and
timeouts deny execution. The harness owns polling and hides its receive tool
from the model. `/new` starts a new conversation and `/stop` stops the agent.
Only one polling host should run per bot. The computer must remain running.
Bot messages are not end-to-end encrypted; never send secrets or whole files.
The working directory is not a sandbox. Keep command approval enabled.

## Validation and AI assistance

Both plugins worked in Codex CLI and the custom harness. The phone tests
covered receipt, replies, approval, explicit refusal, chat filtering, startup
backlog skipping, and a multi-step research query invoking four dependent
tools. Eighteen harness tests, four Telegram-plugin tests and ten research-
plugin tests passed. Automatic result cleanup was also verified in a live run.
Claude Code was not installed, so its plugin validator was not used.

OpenAI Codex assisted with implementation, documentation, debugging and tests.
The student chose the research question and parameters, configured credentials
locally, performed phone tests, explained context and skill disclosure, and
reviewed the research result. No credentials, raw catalogs, virtual environments
or local audit logs are included in this submission.
