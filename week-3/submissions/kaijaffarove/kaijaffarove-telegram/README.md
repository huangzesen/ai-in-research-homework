# kaijaffarove-telegram

An MCP server, packaged as a Claude Code plugin, that lets an agent talk to **your own Telegram chat** through a bot.
It uses long polling (`getUpdates`), so nothing on your computer is reachable from the internet.

## Tools

| Tool | What it does |
|---|---|
| `send_message(text)` | Sends `text` to your chat (always the configured chat; the model can't pick another). Splits messages over 4,096 characters. |
| `wait_for_messages(seconds=30)` | Waits up to `seconds` (max 50) and returns new text messages from your chat, each once. |

Every message from any other chat is **dropped** and logged to stderr. On first use it skips the backlog, so messages sent while it was off never replay as fresh orders.

The skill `skills/telegram/SKILL.md` tells an agent how to write for a phone screen.

## Configure

1. In Telegram, message [@BotFather](https://t.me/BotFather): `/newbot`, pick a name and a username ending in `bot`. It gives you a token.
2. Send your bot any message, then find your chat ID:
   - macOS/Linux: `curl -s "https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getUpdates"` and read `message.chat.id`
   - Windows PowerShell: `(Invoke-RestMethod "https://api.telegram.org/bot$env:TELEGRAM_BOT_TOKEN/getUpdates").result.message.chat.id`
3. Set two environment variables (in your harness's `.env`; never commit it):
   ```
   TELEGRAM_BOT_TOKEN=123456789:AA...
   TELEGRAM_CHAT_ID=123456789
   ```

Requires [uv](https://docs.astral.sh/uv/); `.mcp.json` starts the server with `uv run --script server.py`, which installs its two dependencies (`mcp`, `httpx`) automatically.

## Load it

- **kai-agent** (https://github.com/kaijaffarove/kai-agent): it loads every folder in `plugins/` automatically.
- **Claude Code**: with the two variables set in your shell, `claude --plugin-dir path/to/kaijaffarove-telegram`, then `/mcp` should list `telegram`.
  PowerShell example: `$env:TELEGRAM_BOT_TOKEN="..."; $env:TELEGRAM_CHAT_ID="..."; claude --plugin-dir plugins\kaijaffarove-telegram`

## Safety

A bot connected to an agent with a shell has all three legs of the [lethal trifecta](https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/): your files, messages from the internet, and a way to send things out.
- Only your chat ID gets in. Anyone can find a bot and message it.
- Keep command approval on in the agent.
- The bot token is a password: keep it in `.env`, never commit it, never paste it into an AI chat. If it leaks, send `/revoke` to @BotFather.
- Bot messages are not end-to-end encrypted. Don't send secrets through them.
