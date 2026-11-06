---
name: pedro-agent
description: Install and run Pedro Agent, Pedro's AI in Research Week 2 harness with a local web chat and one approval-gated shell tool.
---

# Pedro Agent

Repository: https://github.com/Caltz27/pedro-agent

## Install

Requires Git and Python 3.10 or newer. The harness uses only the Python standard library; no agent framework or package installation is needed. Check `git --version`. If Git is missing, install it using the operating system's package manager (Windows: `winget install --id Git.Git -e`; macOS: `xcode-select --install`; Ubuntu: `sudo apt-get install git`).

Clone into a new folder; preserve any existing checkout:

```sh
git clone https://github.com/Caltz27/pedro-agent.git
cd pedro-agent
```

Use `uv --version` if uv is available. Otherwise check `python --version` on Windows or `python3 --version` on macOS/Linux. If Python 3.10+ is missing, install uv using https://docs.astral.sh/uv/getting-started/installation/ and let `uv run` provision Python.

## Configure

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
notepad .env
```

On macOS/Linux:

```sh
cp .env.example .env
${EDITOR:-nano} .env
```

Only copy the example when `.env` does not already exist. Have the user enter their key locally; never ask them to paste it into chat or print it. Configure:

- `BASE_URL`: OpenRouter uses `https://openrouter.ai/api/v1`; other OpenAI-compatible Chat Completions APIs also work.
- `API_KEY`: the user's API key. OpenRouter keys can be created at https://openrouter.ai/settings/keys.
- `MODEL`: a model with tool calling. The example uses `cohere/north-mini-code:free`, tested for this submission; availability and free quotas may change. If unavailable, choose a tool-capable model from https://openrouter.ai/models?supported_parameters=tools.

These settings are read into environment variables; pre-existing environment variables take precedence. Never commit `.env`. Verify `git check-ignore .env` prints `.env`.

## Run

With uv, on any supported platform:

```sh
uv run check_api.py
uv run server.py
```

Or with an installed Python 3.10+ interpreter, on Windows:

```powershell
python check_api.py
python server.py
```

On macOS/Linux:

```sh
python3 check_api.py
python3 server.py
```

On Pedro's computer, activate `Calimero` in the same shell before Python or uv commands: `conda activate Calimero`. This environment is not required on other computers.

Open http://127.0.0.1:8765. The server binds only to loopback; keep it local. Stop with Ctrl+C. If port 8765 is occupied, stop the previous Pedro Agent server before starting another instance. Restarting clears the in-memory conversation.

## Check that it works

`check_api.py` should report PASS for plain chat and a valid `bash` tool call, with token usage. It never executes a command. HTTP 401 suggests a bad key; 402 or 429 may indicate credit or rate limits. If there is no tool call, select another tool-capable model.

In the web chat, ask “What files are in this folder?” The user should see a proposed command and Approve/Deny buttons. Have them approve it: the page should show the command, output, exit code, final model answer, and input/cached/output token counts per API call. Cached tokens may be zero or not reported.

Ask another filesystem question and deny its command; no command should execute and the model should receive the denial. Ask it to run `doesnotexist` once and explain the error; approve that deliberate failure and check the nonzero exit code and model explanation. Commands run in the repository folder, using PowerShell on Windows or bash on macOS/Linux. Approval expires after five minutes; execution times out after 60 seconds; output retains the last 10,000 characters; each question allows 20 tool rounds.

For local deterministic checks, run `uv run python -m unittest test_agent` (or `python -m unittest test_agent`, using `python3` on macOS/Linux).
