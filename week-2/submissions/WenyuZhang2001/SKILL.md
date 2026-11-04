---
name: ai-study-agent
description: Install and run AI Study Agent, Wenyu Zhang's minimal Python agent harness for AI in Research week 2, with a local web chat and approved bash commands.
---
# AI Study Agent

Repository: https://github.com/WenyuZhang2001/ai-study-agent

The harness uses an OpenAI-compatible Chat Completions endpoint and one tool, `bash` (PowerShell on Windows). It displays token usage and requires approval before every command. No agent framework or third-party Python libraries are required.

## Install

Use Git and Python 3.10+ (or uv). Check `git --version` and `uv --version`; alternatively check `python3 --version` on macOS/Linux or `py --version` on Windows. If Git is missing, install it from https://git-scm.com/downloads; if both Python and uv are missing, install Python from https://www.python.org/downloads/ or uv following https://docs.astral.sh/uv/getting-started/installation/.

macOS / Linux:

```sh
cd ~
git clone https://github.com/WenyuZhang2001/ai-study-agent.git
cd ai-study-agent
cp .env.example .env
chmod 600 .env
```

Windows PowerShell:

```powershell
Set-Location $HOME
git clone https://github.com/WenyuZhang2001/ai-study-agent.git
Set-Location ai-study-agent
Copy-Item .env.example .env
```

If that folder already exists, inspect it first and reuse the intended clone; do not overwrite an existing `.env` or unrelated project.

## Configure

Have the user edit `.env` locally. Never ask them to paste a key in chat, print it, or commit the file. `.gitignore` excludes `.env`.

```dotenv
BASE_URL=https://openrouter.ai/api/v1
API_KEY=replace_with_your_private_key
MODEL=anthropic/claude-haiku-5.5
```

The user must create their own OpenRouter key and add credits, or choose another OpenAI-compatible API and model supporting tool calls. The model above was verified during development; if unavailable, consult that provider's current model list and choose a supported model. Use the `/v1` base URL, not the full `/chat/completions` URL. The three environment variables override values in `.env`.

## Run

From the cloned folder, on all platforms with uv:

```sh
uv run server.py
```

Without uv, on macOS/Linux:

```sh
python3 server.py
```

Without uv, on Windows:

```powershell
py server.py
```

Open http://127.0.0.1:8765 if the browser does not open automatically. The service binds only to `127.0.0.1`; do not expose it to a network. Use `--port 8766` if the port is occupied, or `--no-browser` to avoid opening a browser. Stop it with Ctrl+C.

## Check that it works

1. In the chat, ask “What files are in this folder? Use bash.” Expect a command card with Approve and Deny buttons. Review and approve the listing command. Expect command output, exit code, and a model reply naming files.
2. Ask “Run `printf hello`” on macOS/Linux, or “Run `Write-Output hello`” on Windows. Click Deny. Expect “The user declined to run this command.” in the command result and an assistant response respecting the denial. No command should run.
3. Confirm every API call displays input and output token counts, plus cached input when reported. Cost is shown when the API reports it.
4. Click New conversation after the turn ends; the chat should clear.

Commands run in the project folder with the server's local permissions, require approval, have a 60-second timeout and truncated output, and allow at most 20 tool rounds per question. The session is single-user and in memory. Review commands before approving them. Do not approve commands that read `.env` or credentials.

For setup errors, check local configuration without exposing keys. HTTP 401/403 usually means credentials or access; 402 may indicate credits. Stop and restart the server after code changes. Windows and Linux instructions are provided, but runtime testing for this submission was on macOS.

## Validation record

Fresh-clone installation, chat, approved file listing, denied command, token usage and reset were verified on macOS. Additional real API tests verified sequential tool calls and failed commands in a disposable sample folder. The student chose not to scan the home directory. No Linux/Windows runtime testing or positive prompt-cache hit is claimed.
