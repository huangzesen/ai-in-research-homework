# Week 3 — WenyuZhang2001

Harness: https://github.com/WenyuZhang2001/ai-study-agent

## Plugins

**wenyuzhang2001-telegram** provides private-chat send and long-poll tools using the official MCP Python SDK. It accepts only the configured chat, skips queued updates at startup, and returns reply message IDs for approvals. The harness owns phone polling and requires linked, numbered yes/no approvals for bash and non-allowlisted tools, with expiry, reconnect handling and denial enforcement. Secrets are typed locally into an ignored .env and passed only through server environment variables.

**wenyuzhang2001-equity-research** supports read-only daily US tech/semiconductor/Tesla analysis: data inspection, trend/risk, a watchlist, an SMA control and five-session probability research with purged walk-forward validation and cost-aware simulations. Public breakout/pullback ideas are clearly labeled adaptations. Historical TSLA/NVDA checks did not demonstrate probability skill, and the agent reports that limitation. No brokerage access, orders, news/earnings inputs or daily scheduler is provided.

## Run from the phone

Clone the public harness, install uv (Python 3.11+), copy .env.example to .env, and enter BASE_URL, API_KEY, MODEL, TELEGRAM_BOT_TOKEN and the owner's TELEGRAM_CHAT_ID locally. Never paste secrets into AI chat.

```sh
uv sync
uv run server.py --telegram
```

Wait for the online message. Ask a question; reply to the corresponding numbered approval with exact English yes or no. /new resets the conversation. Only one receiver may run; keep the local process alive and stop with Ctrl+C. A standalone shell python3 can differ from the uv-managed interpreter.

Example accepted research question: "Check TSLA's five-session model as of 2025-10-17, compare with historical-up-frequency baseline and report simulated performance after 10 bps per side. Explain this is historical research, not a current forecast."

## Validation and safety

- 44 automated checks cover loop/tool dispatch, refusal, reply matching/expiry, reconnect, real fixture MCP lifecycle, environment isolation, web checks, and research timing/cost calculations.
- Phone acceptance passed: approved file listing, explicit refusal, complete research answer, sequential Python-version/disk-space task, deliberately nonmatching-chat filtering with observed drop log, and startup skipping of a marker verified present while stopped.
- Both plugins also worked in bundled Codex CLI 0.162.0-alpha.17.2 under ephemeral stdio configuration and built-in approval review: Telegram sent a fixed message, and research_swing returned the same historical TSLA result. No global Codex config was changed. Claude Code validation was unavailable and is not claimed.
- Only the owner's private chat is accepted. Every bash command asks; only Telegram sending is allowlisted by default. Telegram bot chats are not end-to-end encrypted. Never send secrets/whole files; revoke a leaked bot credential with BotFather /revoke.
- Research uses unofficial Yahoo/yfinance data and fractional adjusted units, with explicit costs and significant limitations. No live orders are placed. Generated market data, runtime receipts, caches and .env are not submitted.

## AI assistance

Codex helped implement both MCP plugins, the harness loader and Telegram approvals, write regression checks, debug network/approval issues, compare public strategy ideas, and prepare documentation. I created/configured the bot locally, chose the research scope, completed the phone acceptance tests and reviewed the model's failed validation result.
