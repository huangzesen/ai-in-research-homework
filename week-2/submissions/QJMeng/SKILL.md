---
name: qimeng-agent
description: Install and run Qimeng's qimeng-agent for AI in Research week 2, a Python agent with local web or terminal chat, one bash tool, command approval, and token usage reporting.
---
# qimeng-agent

Repository: https://github.com/QJMeng/qimeng-agent

## Install

Use a new folder outside other projects. Check `git --version` and `uv --version`. If Git is missing, install it with Xcode Command Line Tools on macOS, `winget install --id Git.Git -e` on Windows, or `sudo apt-get install -y git` on Ubuntu. Let the user complete any OS password prompts.

If uv is missing:

macOS / Linux:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
source "$HOME/.local/bin/env"
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Restart PowerShell after installation. Clone and install on all platforms:

```sh
git clone https://github.com/QJMeng/qimeng-agent.git
cd qimeng-agent
uv sync --locked
```

uv provides Python 3.11 or newer if necessary. Do not install dependencies into system Python.

## Configure

macOS / Linux:

```sh
cp .env.example .env
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
```

Have the user edit `.env` locally, supplying:

- `BASE_URL`: `https://api.openai.com/v1` for OpenAI, or another OpenAI-compatible Chat Completions endpoint.
- `API_KEY`: their own provider key; never ask them to paste it into chat or print it.
- `MODEL`: a model available to their account that supports tool calling. The template uses `gpt-4.1-mini`.

The user completes account login and billing setup themselves. API calls use their account and may incur charges. Never commit `.env`; only `.env.example` is public. The current implementation reads settings from the local `.env` file next to the code.

## Run

Recommended web interface, from the cloned folder:

```sh
uv run web.py
```

Open http://127.0.0.1:8765. Keep the server terminal open. The page has a chat box, model replies, Approve and Deny buttons, command output, and per-call token usage. The server binds only to 127.0.0.1. Approvals time out after five minutes and default to denial. Ctrl+C in the terminal stops the server; restarting clears in-memory history.

Alternative terminal chat:

```sh
uv run main.py
```

Enter `y` to approve a command, any other response to deny, and `/exit` to quit.

Commands start in the directory where the program was launched. Each command starts there; `cd` does not persist. The tool uses bash on macOS / Linux and PowerShell on Windows. It returns combined stdout/stderr and exit code, limits execution to 60 seconds, and retains the last 10,000 output characters. It allows up to 20 tool rounds per question. The working directory is not a sandbox: review each command before approval, and do not expose private data through tool output sent to the API. Windows has not been tested by the author.

## Check that it works

1. Ask `What files are in this folder?`. Approve the listing command. Expect repository files such as `main.py` and `web.py`, a successful exit code, a model explanation, and token counts.
2. Ask `Remember the label seismic-demo-729`, then `What label did I give you?`. Expect the same label, using conversation history.
3. Ask `Run doesnotexist and explain the error; do not try other commands`. Approve it. Expect a nonzero exit code and the model's explanation, not a crash.
4. Ask `Run printf hello` on macOS / Linux, or `Run Write-Output hello` on Windows. Deny the proposed command. Expect a user-declined tool result and acknowledgment; the command must not execute.

An optional automated live test on macOS / Linux is `uv run test_live.py`. It incurs API usage and supplies approval responses for two exact test commands; the normal interfaces still require user approval.

## Troubleshooting

- `uv: command not found`: restart the terminal, or on macOS / Linux run `source "$HOME/.local/bin/env"`; alternatively use `$HOME/.local/bin/uv`.
- Python cannot import `encodings`: check for conflicting `PYTHONHOME` / `PYTHONPATH` values. In the current macOS / Linux shell, run `unset PYTHONHOME PYTHONPATH` and retry. In PowerShell, remove conflicting values from the current process with `Remove-Item Env:PYTHONHOME, Env:PYTHONPATH -ErrorAction SilentlyContinue`.
- Certificate errors: run through `uv run` so the certifi dependency is available. Do not disable TLS verification.
- Port 8765 already in use: stop the previous instance before starting another; do not terminate unrelated programs.
- API authentication, quota, or unavailable-model errors: have the user check their key, billing, and model access locally without revealing credentials.
