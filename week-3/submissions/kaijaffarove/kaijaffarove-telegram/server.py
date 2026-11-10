# /// script
# requires-python = ">=3.11,<3.14"
# dependencies = ["mcp>=2.3,<3", "httpx>=0.27"]
# ///
"""Telegram MCP server: talk to ONE Telegram chat through a bot, by long polling.

Environment:
  TELEGRAM_BOT_TOKEN  the bot's token from @BotFather (a password: keep it in .env)
  TELEGRAM_CHAT_ID    the only chat this server will send to or accept messages from

Nothing here listens on the network: it polls Telegram's getUpdates.
Stdout is the MCP protocol channel, so every log line goes to stderr.
"""
import logging
import os
import sys
from datetime import datetime, timezone

import httpx
from mcp.server import MCPServer

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
API = os.environ.get("TELEGRAM_API_BASE", "https://api.telegram.org").rstrip("/")
MAX_LEN = 4096          # Telegram's limit per message
MAX_WAIT = 50           # seconds, cap for one long poll


# httpx logs each request URL, and Bot API URLs contain the token: never let it log.
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)


def log(*args):
    print("[telegram]", *args, file=sys.stderr, flush=True)


if not TOKEN or not CHAT_ID or TOKEN.startswith("${") or CHAT_ID.startswith("${"):
    log("TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must both be set (put them in .env). Exiting.")
    sys.exit(1)

mcp = MCPServer(
    "telegram",
    instructions="Send messages to the user's own Telegram chat and read their replies.",
)
state = {"offset": None}   # next update_id to ask for; None = not initialised yet


async def call(method: str, http_timeout: float = 15, **params):
    """Call one Bot API method; return its 'result' or raise with Telegram's message."""
    try:
        async with httpx.AsyncClient(timeout=http_timeout) as client:
            r = await client.post(f"{API}/bot{TOKEN}/{method}", json=params)
    except httpx.HTTPError as e:   # the message never includes the URL (it contains the token)
        raise RuntimeError(f"Could not reach Telegram ({e.__class__.__name__}). Check the internet connection.") from None
    data = r.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegram {method} failed: {data.get('description', r.status_code)}")
    return data["result"]


async def skip_backlog():
    """On first use, jump past old updates so messages sent while we were off never replay."""
    if state["offset"] is None:
        old = await call("getUpdates", offset=-1, timeout=0)
        state["offset"] = old[-1]["update_id"] + 1 if old else 0
        if old:
            log("skipped the backlog of old messages")


@mcp.tool()
async def send_message(text: str) -> str:
    """Send a text message to the user's Telegram chat (always the configured chat; you cannot choose another).

    Use it to reply to the user or to send a short progress update during a long task.
    The user reads it on a phone: keep it short and plain. Never send secrets, tokens or whole files.
    Texts longer than 4,096 characters are split into several messages.

    Args:
        text: the message, plain text, e.g. "Done: 3 files found."
    """
    if not text.strip():
        return "Nothing sent: the text was empty."
    parts = [text[i:i + MAX_LEN] for i in range(0, len(text), MAX_LEN)]
    for part in parts:
        await call("sendMessage", chat_id=CHAT_ID, text=part)
    return f"Sent {len(text)} characters in {len(parts)} message(s)."


@mcp.tool()
async def wait_for_messages(seconds: int = 30) -> dict:
    """Wait for new text messages from the user's Telegram chat and return them.

    Use it when you need the user's answer, e.g. after asking them a question with send_message.
    Each message is returned only once. Messages from anyone else are dropped and never returned.

    Args:
        seconds: how long to wait for a message, 1 to 50 (default 30). Returns as soon as one arrives.

    Returns: {"count": N, "messages": [{"date": "2026-10-20T21:05:00Z", "text": "..."}],
              "dropped_from_other_chats": M} (M messages from other chats were ignored).
    count 0 means no new messages arrived in that time; call again to keep waiting.
    """
    seconds = max(1, min(int(seconds), MAX_WAIT))
    await skip_backlog()
    updates = await call("getUpdates", http_timeout=seconds + 10, offset=state["offset"],
                         timeout=seconds, allowed_updates=["message"])
    messages, dropped = [], 0
    for u in updates:
        state["offset"] = u["update_id"] + 1
        msg = u.get("message") or {}
        chat = str((msg.get("chat") or {}).get("id", ""))
        if chat != CHAT_ID:
            sender = (msg.get("from") or {}).get("username", "unknown")
            log(f"DROPPED a message from chat {chat or '?'} (@{sender}): not the configured chat")
            dropped += 1
            continue
        date = datetime.fromtimestamp(msg.get("date", 0), timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        messages.append({"date": date, "text": msg.get("text") or "[a non-text message, ignored]"})
    return {"count": len(messages), "messages": messages, "dropped_from_other_chats": dropped}


if __name__ == "__main__":
    log("starting (stdio)")
    mcp.run()
