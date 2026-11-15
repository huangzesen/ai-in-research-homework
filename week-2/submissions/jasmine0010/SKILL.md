---
name: jasmines-agent
description: Install, configure, run, and check Jasmine's Agent, jasmine0010's AI in Research Week 2 harness with local web chat, saved conversations, one approved bash tool, and per-call token usage. Use when asked to install or run this harness.
---
# Jasmine's Agent

Repository: https://github.com/jasmine0010/jasmines-agent

This repository contains the Week 2 version with one approved shell tool. Installation does not authorize creating a repository, pushing code, or submitting a pull request. If cloning fails, report the error and stop.

## Install

Requires Git and uv. Check `git --version` and `uv --version`. Install missing tools using https://git-scm.com/downloads and https://docs.astral.sh/uv/getting-started/installation/; the user completes interactive OS prompts. uv obtains Python 3.11+ if needed. There are no third-party Python dependencies or agent frameworks.

In a new folder on macOS, Linux, or Windows PowerShell:

```sh
git clone https://github.com/jasmine0010/jasmines-agent.git
cd jasmines-agent
uv sync --locked
```

If the destination exists, inspect and reuse the intended clone; do not overwrite other work or an existing `.env`.

## Configure

Create `.env` only if it does not already exist.

macOS / Linux:

```sh
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

The user enters their own key in a local editor. Never ask for it in chat, print it, or commit it.

```dotenv
BASE_URL=https://openrouter.ai/api/v1
API_KEY=replace_with_your_own_key
MODEL=openrouter/free
```

Other OpenAI-compatible Chat Completions APIs work with a tool-capable model. `BASE_URL` includes the provider's version path, not `/chat/completions`. The example uses a free model router whose availability and quotas can vary; do not silently switch to a paid model. Environment variables override `.env` values when using the commands below.

Verify `git check-ignore .env` prints `.env`. Local chat history under `history/` and command workspace files under `workspace/` are also ignored by Git.

## Run

From the clone, on all supported platforms:

```sh
uv run --env-file .env python web.py
```

Keep that terminal running and open http://127.0.0.1:8765. The server binds only to `127.0.0.1`. If the port belongs to another program, use `uv run --env-file .env python web.py --port 8766`; do not stop unrelated programs. Ctrl+C stops the server. Reload the page after restarting to reconnect.

The sidebar opens saved chats. New chat preserves earlier chats; Rename changes the selected title; Delete asks for confirmation. Chats persist in `history/chats.sqlite3`. An interrupted turn is marked on reopening and commands are never resumed automatically.

Terminal alternative: `uv run --env-file .env python agent.py --chat`; type `/quit` to exit. Terminal history lasts for its current process only.

## Check that it works

1. Ask **What files are in this folder? Use bash.** Expect a proposed command with Approve and Deny buttons. Have the user review and approve the listing command. Expect its output, exit code, and a model answer based on that output. Commands begin in `workspace/`; an empty listing is valid on a fresh install.
2. Ask it to run `Write-Output hello` on Windows, or `printf hello` on macOS/Linux, and choose Deny. Expect a declined tool result and a model reply respecting the denial; no command should execute.
3. Start a new chat so the failure check is independent of the earlier denial. Ask it to run `doesnotexist` once and explain the error. Approve that deliberate failure. Expect a nonzero exit code and an explanation, without a crash.
4. Confirm each API call shows input, output, and cached-input tokens when reported. Cached tokens are part of the input count.
5. Rename a chat, create another, then reopen the earlier chat and refresh. Its title and messages should remain.

Commands use PowerShell on Windows and bash on macOS/Linux, require approval, time out after 60 seconds, and return at most 10,000 characters of output. Each question permits 20 tool rounds. The working folder is not a sandbox: approved commands retain the local user's permissions, and command output is sent to the configured model provider.

Offline checks, requiring no API key:

```sh
uv run --locked python -m unittest discover -s tests -v
```

Optional live checks make API requests and approve only exact synthetic test commands in a disposable folder:

```sh
uv run --env-file .env python tests/live_checks.py
```

These cover listing, sequential commands, intentional command failure, denial, and token reporting without scanning the home directory. Results are written to `validation/live-checks.json`.

## Troubleshooting and validation scope

HTTP 401/403 suggests credentials or access; 402 or 429 can indicate credits or quotas. Check configuration and provider access locally without exposing keys. A model request timeout can be retried with a new message. Refresh after a server restart; saved conversations remain available.

Runtime checks were performed on Windows. macOS/Linux commands are provided but have not been runtime-tested. A fresh local-clone installation passed locked setup, offline tests, live listing/denial/failure checks, token usage, and saved-chat checks. A fresh clone from the public URL also passed locked setup, all 12 offline checks, and localhost web startup. Live model checks passed on the same Week 2 implementation before publication; they were not repeated in the public clone because the free model quota was exhausted.
