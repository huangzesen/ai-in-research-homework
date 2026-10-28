# /// script
# requires-python = ">=3.11"
# dependencies = ["mcp>=1.28,<2", "httpx>=0.28,<0.29"]
# ///
"""Private Telegram MCP server. Stdout is reserved for MCP."""
import asyncio
import os
import sys
import ssl
import logging
from contextlib import asynccontextmanager
import httpx
from mcp.server.fastmcp import FastMCP


class Telegram:
    def __init__(self):
        token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
        chat = os.environ.get("TELEGRAM_CHAT_ID", "")
        if not token or not chat:
            raise ValueError("Set TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in the host environment.")
        try:
            self.chat_id = int(chat)
        except ValueError:
            raise ValueError("TELEGRAM_CHAT_ID must be an integer.") from None
        if self.chat_id <= 0:
            raise ValueError("Use your private Telegram chat ID, not a group chat.")
        self.client = httpx.AsyncClient(base_url="https://api.telegram.org/bot" + token + "/", timeout=65, verify=ssl.create_default_context())
        self.offset = 0
        self.lock = asyncio.Lock()

    async def request(self, method, **payload):
        try:
            response = await self.client.post(method, json=payload)
            response.raise_for_status()
            body = response.json()
            if not body.get("ok"):
                raise ValueError("Telegram rejected the request; check bot configuration.")
            return body["result"]
        except (httpx.HTTPError, ValueError):
            # Do not expose exceptions containing the token-bearing URL.
            raise ValueError("Telegram request failed. Check connection, token and chat ID; run only one poller.") from None

    async def skip_backlog(self):
        updates = await self.request("getUpdates", offset=-1, timeout=0, allowed_updates=["message"])
        if updates:
            self.offset = updates[-1]["update_id"] + 1
            await self.request("getUpdates", offset=self.offset, timeout=0, allowed_updates=["message"])

    def accept(self, updates):
        messages = []
        for update in updates:
            self.offset = max(self.offset, update["update_id"] + 1)
            message = update.get("message", {})
            chat = message.get("chat", {})
            if chat.get("id") != self.chat_id or chat.get("type") != "private":
                print("Dropped update from an unauthorized chat.", file=sys.stderr)
                continue
            if isinstance(message.get("text"), str):
                messages.append({"message_id":message["message_id"], "text":message["text"], "reply_to_message_id":message.get("reply_to_message", {}).get("message_id")})
        return messages

    async def wait(self, seconds):
        async with self.lock:
            updates = await self.request("getUpdates", offset=self.offset, timeout=max(0,min(50,seconds)), allowed_updates=["message"])
            return self.accept(updates)

    async def send(self, text):
        if not text.strip():
            raise ValueError("Provide nonempty message text.")
        # Telegram counts UTF-16 units; 2000 code points also fits emoji.
        ids = []
        for start in range(0,len(text),2000):
            sent = await self.request("sendMessage", chat_id=self.chat_id, text=text[start:start+2000])
            ids.append(sent["message_id"])
        return {"status":"sent", "message_ids":ids}


telegram = None

@asynccontextmanager
async def lifespan(server):
    global telegram
    telegram = Telegram()
    try:
        await telegram.skip_backlog()
        yield {}
    finally:
        await telegram.client.aclose()
        telegram = None

mcp = FastMCP("hleinweber-telegram", lifespan=lifespan)

@mcp.tool()
async def send_message(text: str) -> dict:
    """Send plain text to the owner's configured private Telegram chat only. Use for brief replies or progress; never send secrets or whole files. Long text is split automatically."""
    return await telegram.send(text)

@mcp.tool()
async def wait_for_messages(seconds: int = 30) -> list[dict] | str:
    """Wait 0-50 seconds for new text messages from the owner's private chat. Returns message IDs and text, once each, or No new messages. The harness owns this tool in Telegram mode."""
    return await telegram.wait(seconds) or "No new messages."

if __name__ == "__main__":
    # SDK configures logging on startup; silence HTTP URL logs containing credentials.
    logging.getLogger("httpx").disabled = True
    logging.getLogger("httpcore").disabled = True
    mcp.run(transport="stdio")
