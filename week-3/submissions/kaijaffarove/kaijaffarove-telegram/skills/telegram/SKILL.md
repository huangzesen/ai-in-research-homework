---
name: telegram
description: Use when the user is talking to you through Telegram (from their phone), or asks you to send them a Telegram message. Covers how to write replies and progress updates for a phone screen.
---

# Talking through Telegram

The `telegram` MCP server sends messages to the user's own Telegram chat and reads their replies. It can only reach that one chat; messages from anyone else are dropped.

- **Replies are read on a phone.** Keep them short and plain: a few sentences, no tables, no long code blocks. Lead with the answer.
- **Long tasks:** send one short progress line with `send_message` (e.g. "Fetching PSP data for Dec 24, about 30 s...") so the user knows you are working. Don't send a message for every step.
- **Asking the user something:** send the question with `send_message`, then call `wait_for_messages` until a reply arrives (count 0 means nothing yet; call again).
- **Never send** secrets, tokens, passwords, the contents of `.env`, or whole files. Summarize instead, and give a file path if they need the full result on their computer.
- Telegram messages are not end-to-end encrypted. Don't ask the user to send anything secret through it.
