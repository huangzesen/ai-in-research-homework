---
name: psp-agent-harness-ding
description: Install and run psp-agent-harness-ding, Yuliang Ding's agent harness (AI in Research, week 2) - a minimal agent loop with one bash tool, approval before every command, and a local web chat interface.
---
# psp-agent-harness-ding

Repository: https://github.com/dingyl2001/psp-agent-harness-ding

An agent harness with exactly one tool, `bash`. It talks to any
OpenAI-compatible Chat Completions API, runs the agent loop (send the
conversation, run any tool calls the model asks for, feed the results
back, repeat until it replies in plain text), asks for approval before
every command, and shows token usage per call. Interface: a local web
page with a chat box and Approve/Deny buttons for each command.

## Install

Requires [uv](https://docs.astral.sh/uv/) and `git`.

macOS / Linux:
```
git clone https://github.com/dingyl2001/psp-agent-harness-ding.git
cd psp-agent-harness-ding
uv sync
```

Windows (PowerShell):
```
git clone https://github.com/dingyl2001/psp-agent-harness-ding.git
cd psp-agent-harness-ding
uv sync
```

## Configure

Copy the example env file and fill in three values:

macOS / Linux:
```
cp .env.example .env
```

Windows (PowerShell):
```
copy .env.example .env
```

Edit `.env` (any text editor) and set:
- `BASE_URL` — the API's base URL, e.g. `https://openrouter.ai/api/v1`
- `API_KEY` — your API key for that provider
- `MODEL` — a model name that supports tool calling, e.g.
  `nvidia/nemotron-3-super-120b-a12b:free` (a free OpenRouter model)

Never commit `.env` — it is already gitignored.

## Run

```
uv run app.py
```

Then open **http://127.0.0.1:5050** in a browser. (A terminal-only
alternative also exists: `uv run harness.py`.)

## Check that it works

In the chat box, ask:

> What files are in this current folder?

You should see:
1. A pulsing "Thinking..." indicator appear briefly.
2. A card showing the command the model wants to run (e.g. `ls -la`)
   with **Approve** and **Deny** buttons.
3. After clicking **Approve**, the command's real output appears, then
   the model's final answer describing the files — using that real
   output, not a guess.
4. A small `[tokens: ... in, ... cached, ... out]` line after each API
   call.

If you click **Deny** instead, the model should get back "The user
declined to run this command." and respond accordingly (e.g. asking
what to do instead), rather than crashing.
