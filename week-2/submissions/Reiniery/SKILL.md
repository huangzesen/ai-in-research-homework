---
name: reiniery-agent-harness
description: Install and run Reiniery Agent Harness, Reiniery Villalta's minimal AI agent harness for UCLA AI in Research week 2, with a local web chat and approval-gated Bash commands.
---

# Reiniery Agent Harness

Repository: https://github.com/Reiniery/reiniery-agent-harness

This harness uses an OpenAI-compatible Chat Completions API, keeps the full
conversation history, and gives the model one tool: `bash`. Every command needs
the user's approval before it runs.

## Install

Check that Git and uv are available:

```bash
git --version
uv --version
```

If uv is missing, install it on macOS or Linux:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

On Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Open a new terminal after installing uv. Then clone and install the harness:

```bash
git clone https://github.com/Reiniery/reiniery-agent-harness.git
cd reiniery-agent-harness
uv sync
```

The same `git clone`, `cd`, and `uv sync` commands work in PowerShell.

## Configure

On macOS or Linux:

```bash
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Edit `.env` and set these three values:

```dotenv
BASE_URL=https://openrouter.ai/api/v1
API_KEY=replace-with-your-own-key
MODEL=nvidia/nemotron-3-super-120b-a12b:free
```

The endpoint may be any OpenAI-compatible `/v1/chat/completions` API, and the
model must support tool calling. The user must enter the API key themselves;
never ask them to paste it into chat, display it, or commit `.env`.

## Run

Start the local web chat:

```bash
uv run python web.py
```

Open http://127.0.0.1:8000 in a browser. The server binds only to `127.0.0.1`,
so it is available only on the same computer. Stop it with `Ctrl+C`.

For the terminal interface instead:

```bash
uv run python main.py
```

Type `/exit` to leave the terminal chat.

## Check that it works

In the web chat, ask:

> What files are in this folder? Use bash to check.

The page should show an API-call token count and a proposed `ls` command with
**Approve** and **Deny** buttons. Approve it. The page should then show the
command output, its exit code, a second API-call token count, and the model's
answer. Deny a later command to verify that it does not run and that the model
receives "The user declined to run this command."
