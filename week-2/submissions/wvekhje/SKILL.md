---
name: mini-harness
description: Install and run mini-harness, Patrick Russell's agent harness (AI in Research, week 2) - a hand-written agent loop with one bash tool that asks before every command, talking to any OpenAI-compatible API, with a local web chat (or terminal chat).
---
# mini-harness

Repository: https://github.com/wvekhje/mini-harness

A small Python program: it chats with a model through an OpenAI-compatible `/v1/chat/completions` API and gives the model one tool, `bash`. The user approves or denies every command. Each API call's token usage (input, cached input, output) is shown.

Never ask the user to paste an API key into the chat, and never print `.env`. The user types the key into `.env` themselves.

## Install

Needs `git` and [uv](https://docs.astral.sh/uv/). Check with `git --version` and `uv --version`. If uv is missing:

- macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`, then open a new terminal.
- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`, then open a new terminal.

Clone it into the home folder and install its dependencies (uv also installs a suitable Python if needed):

```bash
cd ~
git clone https://github.com/wvekhje/mini-harness.git
cd mini-harness
uv sync
```

On Windows, run these in PowerShell; the same commands work.

## Configure (BASE_URL, API_KEY, MODEL; never commit .env)

Create `.env` from the example. It is listed in `.gitignore`, so it is never committed.

- macOS / Linux: `cp .env.example .env`
- Windows (PowerShell): `Copy-Item .env.example .env`

Then the user (not the agent) opens `.env` in a text editor and fills in:

```
BASE_URL=https://openrouter.ai/api/v1
API_KEY=<their key>
MODEL=openai/gpt-4.1-mini
```

Any OpenAI-compatible endpoint works (OpenRouter, OpenAI, a local sub2api at `http://127.0.0.1:8080/v1`, ...), as long as `MODEL` supports tool calling. OpenRouter's tool-capable models: https://openrouter.ai/models?supported_parameters=tools. A paid OpenRouter model needs credits on the account; otherwise the API returns `402 Insufficient credits` (use a `:free` model or add credits).

Check the configuration (one plain call, then one call that must come back as a `bash` tool call):

```bash
uv run check_api.py
```

Expected: a short greeting, a `usage:` line, and `tool call: bash {"command": "ls ..."}`. If it prints `NO tool call came back`, choose a different `MODEL`.

## Run

Web chat (recommended). It serves on `127.0.0.1` only, so no other computer can reach it:

```bash
uv run web.py
```

Then open http://127.0.0.1:8765. Set `PORT` (e.g. `PORT=9000 uv run web.py`; on Windows `$env:PORT=9000; uv run web.py`) if 8765 is taken. Stop it with Ctrl-C.

Terminal chat instead: `uv run harness.py` (type a question; answer `y` or `n` before each command; Ctrl-D, or Ctrl-Z then Enter on Windows, to quit). `uv run harness.py --yes` approves every command automatically; don't use it unless the user asks.

Commands run in the folder the harness is started from. To work in another folder, `cd` there and run `uv run --project ~/mini-harness ~/mini-harness/web.py`.

Platforms: on macOS and Linux commands run in `/bin/bash`. On Windows they run in `cmd.exe`, so the model must use Windows commands (`dir`, not `ls`); running the harness inside WSL gives it bash instead.

## Check that it works

Start the web chat and open http://127.0.0.1:8765. Ask:

> What files are in this folder, and how many lines does harness.py have?

The user should see:

1. A gray `[tokens] in … (cached …) · out …` line for the first API call.
2. A command such as `$ ls -la`, with **Approve** and **Deny** buttons. Click **Approve**; its output and `exit code: 0` appear under it.
3. Probably a second command (e.g. `wc -l harness.py`) to approve, then a text answer listing the files (README.md, harness.py, web.py, ...) and the line count. Every API call has its own token line, and the input count grows with each one because the whole conversation is resent.

Then ask anything that needs a command and click **Deny**: the model is told "The user declined to run this command." and answers without running it.

An agent can run the same check without a browser, with the server running in the background (`uv run web.py &` on macOS/Linux):

```bash
curl -s -X POST http://127.0.0.1:8765/send -d '{"text": "What files are in this folder?"}'
sleep 3; curl -s "http://127.0.0.1:8765/events?since=0"
```

The events include `{"kind": "approve", "data": {"id": "<id>", "command": "..."}}`. Approve it with:

```bash
curl -s -X POST http://127.0.0.1:8765/approve -d '{"id": "<id>", "ok": true}'
```

Poll `/events` again until a `{"kind": "done"}` event arrives: before it there should be a `result` event starting with `exit code: 0`, `usage` events, and a `text` event with the answer. Send `"ok": false` instead to check that denying works. Stop the server afterwards.
