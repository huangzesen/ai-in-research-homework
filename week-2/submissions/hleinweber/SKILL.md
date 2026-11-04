---
name: research-agent
description: Install, configure, run, and check research-agent, hleinweber's minimal agent harness for AI in Research Week 2, with local web chat and an approved bash tool.
---

# Research agent

Repository: https://github.com/hleinweber/research-agent

Install this small Python harness when the user asks to run research-agent. It uses an OpenAI-compatible Chat Completions API, one tool named `bash`, and a web interface served only on `127.0.0.1`. There are no Python package dependencies or agent frameworks.

## Install

Check `git --version` and `uv --version`. If Git is missing: on Windows the user runs `winget install --id Git.Git -e`; on macOS they run `git --version` and follow the developer-tools installation prompt; on Ubuntu/Debian they run `sudo apt-get install git`.

If uv is missing, use its official installer:

macOS/Linux:

```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Windows PowerShell:

```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

Reopen the terminal after installing so Git and uv are on PATH. Commands that request a password or interactive approval belong in the user's own terminal.

Choose a new folder under the user's home directory; preserve an existing clone and configuration if already installed. For a fresh install:

```sh
git clone https://github.com/hleinweber/research-agent.git
cd research-agent
```

uv obtains Python if needed; no `pip install` step is required.

## Configure

Create `.env` only if it does not already exist. On macOS/Linux:

```sh
cp .env.example .env
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

Have the user privately edit the file using a local text editor. Never ask them to paste a key into chat or print `.env`. The settings are:

```dotenv
BASE_URL=https://api.openai.com/v1
API_KEY=replace_with_your_key
MODEL=gpt-4.1-mini
```

Use the user's preferred provider and model if they already have them. The endpoint must support `/chat/completions` and the model must support tool calling. `BASE_URL` includes the provider's `/v1` path. Environment variables with these three names override `.env`. API requests may incur provider charges.

`.env` is already ignored by Git. Verify `git check-ignore .env` returns `.env`; never commit it.

## Run

In a separate terminal window, keep this command running:

```sh
uv run python web.py
```

It opens the browser automatically. The terminal remains occupied while the server runs; use your original terminal for other work. Ctrl+C stops the server.

For environments without automatic browser opening:

```sh
uv run python web.py --no-browser
```

Open `http://127.0.0.1:8765/`. The page sets a private session cookie; reload it after restarting. If research-agent already occupies that port, launching it again opens the existing page and returns the shell. If another program occupies port 8765, use `uv run python web.py --port 8766` and its printed link. Do not stop an unrelated process or expose the server to the network.

The working folder is the terminal's current directory, shown on the page. To work in another folder, run `uv run python` followed by the absolute path to the clone's `web.py` from that folder. On Windows, `bash` runs PowerShell commands; on macOS/Linux it runs bash.

On Windows, this launcher also works from outside the clone:

```powershell
& "$env:USERPROFILE\research-agent\start.ps1"
```

Adjust that path if you chose a different install folder. If local script policy blocks the launcher, use the documented `cd research-agent` and `uv run python web.py` commands instead.

The terminal alternative is `uv run python agent.py`; `/quit` exits.

## Check that it works

1. Wait for the page to show **Ready**. Ask **What files are in this folder?**
2. Expect a command card with **Approve** and **Deny** buttons. Let the user review and approve the listing command. Expect its output, exit code 0, and the model's reply.
3. Each model call displays input tokens, cached input if reported, and output tokens. Cached input is included in the input total.
4. Ask for another listing and deny it. Expect **The user declined to run this command.** and a model response without executing that command.
5. Optionally ask it to run `doesnotexist`; approve that missing program and check that the model receives and explains a nonzero exit code.

Approval is required for every command. Commands time out after 60 seconds; output is limited to the last 10,000 characters. There are at most 20 tool rounds per question. Tabs share one conversation; history is in memory, and **New conversation** resets it.

If Send is disabled and the page says **Disconnected**, keep the server running in its separate terminal and reload the page at the printed address. If the model request fails, check credentials, model access, billing, and connectivity without displaying secrets. Use **New conversation** after a failed or interrupted request to restart cleanly.
