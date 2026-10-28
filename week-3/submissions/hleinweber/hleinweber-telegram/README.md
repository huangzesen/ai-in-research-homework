# Telegram plugin

Two MCP tools send plain text and wait for new messages in the owner's private Telegram chat. Requires uv, Python 3.11+, and environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` (a private chat ID).

Keep credentials in the harness's ignored `.env`; other hosts must pass them through the environment. Never paste credentials into chat or commit them. Revoke leaked tokens with BotFather `/revoke`.

## Load

From the harness root, after privately loading the two environment variables:

```sh
claude --plugin-dir plugins/hleinweber-telegram
```

In the research-agent harness, keep this folder under `plugins/`, configure `.env`, and run `uv --system-certs run python agent.py --telegram` for phone mode. Use `uv --system-certs run python web.py` for local web chat. The loader expands `${CLAUDE_PLUGIN_ROOT}` and environment placeholders in `.mcp.json` and discovers tools through MCP.

Only one process may poll the bot: stop phone mode before testing another host. The uv script declares the official MCP SDK and httpx dependencies. Standard output is reserved for MCP; diagnostics go to stderr and HTTP URL logging is disabled.

## Safety and operation

The server long-polls Telegram; no inbound internet listener is required. It accepts only the configured private chat, logs dropped updates, skips old messages on startup and splits long outgoing text. The model cannot choose a destination chat. Telegram bot chats are not end-to-end encrypted; do not send secrets or whole files.

The host must approve every shell command. Phone mode owns polling, retains conversation history in memory, and accepts approval only through Telegram Reply to the current prompt with yes. Other answers decline; prompts expire after ten minutes. Send questions as new messages: replies to old prompts are ignored. `/new` resets the conversation.

## Validation status

SDK discovery and live sending passed. The student confirmed web-to-phone delivery, phone command approval and denial, separate approvals for a two-command task, research replies, and old-message skipping after restart. Simulated unauthorized private-chat and group updates were rejected and logged; a live second-account rejection test remains unperformed. Codex host validation passed: sending returned status sent (message ID 59), and incoming polling returned No new messages without an error. A fresh-message receive test in Codex remains inconclusive after its Telegram tool became unavailable; earlier phone-mode receive tests passed as documented above.
