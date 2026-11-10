# Week 3: kaijaffarove

Harness: **kai-agent**, https://github.com/kaijaffarove/kai-agent (both plugins live in its `plugins/` folder; the copies here are identical).

## kaijaffarove-telegram

An MCP server that lets an agent talk to my own Telegram chat through a bot, by long polling (nothing on my computer is reachable from the internet). Tools: `send_message(text)` (always to the configured chat, split over 4,096 characters) and `wait_for_messages(seconds)` (new messages from my chat, each returned once). Every message from any other chat is dropped and counted; old messages are skipped at startup so nothing replays; the HTTP library's request logging is silenced because Bot API URLs contain the token. Configured with `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` from `.env`.

## kaijaffarove-psp

A read-only MCP server for my research on Parker Solar Probe, using NASA CDAWeb's public HAPI service (no key). `solar_wind_summary(start, stop)` combines SWEAP/SPAN-i proton moments and FIELDS 1-minute magnetic field into a short summary (radial speed, speed, density, temperature in K, distance in R_sun and AU, |B| and Br, with medians, 5 to 95% ranges and times of extremes, quality-flag values), saving full tables as CSV. `describe_cdaweb_dataset` and `get_cdaweb_data` reach any CDAWeb dataset. The skill explains RTN, units, perihelion dates and caveats (SPAN-i partial moments, quality flags, data gaps). Tested on perihelion 22 (2024-12-24): closest approach 9.9 R_sun, median radial speed about 260 km/s.

## Run it in Telegram mode

```
git clone https://github.com/kaijaffarove/kai-agent.git
cd kai-agent
copy .env.example .env      # macOS/Linux: cp; then set TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID (and the model backend)
uv run app.py --telegram
```

The harness loads both plugins from `plugins/`, takes questions from Telegram, asks "Run this? ... Reply yes or no" before every `bash` command (anything but yes is a no), runs allow-listed MCP tools (`settings.json`) without asking, and sends the answer back. `/new` starts a fresh conversation. Second host: both plugins also work in Claude Code with `claude --plugin-dir kaijaffarove-telegram --plugin-dir kaijaffarove-psp`.
