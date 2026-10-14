---
name: kai-agent
description: Install and run kai-agent, Kai Jaffarove's agent harness (AI in Research, week 2): a minimal agent loop with one bash tool (PowerShell on Windows), approval before every command, and a local web chat that shows token usage per call. Uses the installed Claude Code CLI (claude -p) as its model by default, or any OpenAI-compatible API.
---

# kai-agent

Repository: https://github.com/kaijaffarove/kai-agent

kai-agent is a small Python program (standard library only) that runs the agent loop itself. The model asks for a command by writing `<bash>command</bash>`; the harness asks the user, runs it, sends back the output and exit code, and calls the model again until it answers in plain text.

Never ask the user to paste an API key into the chat, and never print one. The user types secrets into `.env` themselves.

## Install

Requirements: `git` and [uv](https://docs.astral.sh/uv/). Check with `git --version` and `uv --version`.

If uv is missing:
- macOS / Linux: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Windows (PowerShell): `powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"`

Then open a new terminal so `uv` is on the PATH.

Clone the repository into the user's home folder:

```
cd ~
git clone https://github.com/kaijaffarove/kai-agent.git
cd kai-agent
```

There is nothing else to install: `uv run` fetches a suitable Python on first run, and the project has no third-party dependencies.

## Configure

Create `.env` from the template:
- macOS / Linux: `cp .env.example .env`
- Windows (PowerShell): `copy .env.example .env`

`.env` is in `.gitignore`; never commit it. Then choose one backend.

**Backend A: Claude Code (default, `BACKEND=claude-cli`).** Uses the Claude Code CLI with the user's own Claude subscription; kai-agent calls `claude -p` with Claude Code's built-in tools turned off, so it acts only as the model. No tokens are extracted and no proxy is involved.
1. Check `claude --version`. If missing, install Claude Code:
   - macOS / Linux: `curl -fsSL https://claude.ai/install.sh | bash`
   - Windows (PowerShell): `irm https://claude.ai/install.ps1 | iex` (Git for Windows is recommended: `winget install --id Git.Git -e`)
2. **(user does this)** Log in once in their own terminal: `claude auth login`. Verify with `claude auth status`.
3. In `.env`, keep `BACKEND=claude-cli` and set `CLAUDE_MODEL` to `haiku`, `sonnet`, `opus` or a full model ID. `haiku` uses the least of the subscription's limits.

**Backend B: any OpenAI-compatible API (`BACKEND=openai`),** for example OpenRouter.
1. **(user does this)** Create a key (for OpenRouter: https://openrouter.ai, then Keys) and type it into `.env` as `API_KEY=...` themselves.
2. In `.env`, set `BACKEND=openai`, `BASE_URL` (for OpenRouter `https://openrouter.ai/api/v1`) and `MODEL` (for example `anthropic/claude-haiku-5.5`).

Optional: `WORKDIR=<folder>` sets the folder commands run in (default: the folder kai-agent is started from). `PORT` changes the port (default 8765).

## Run

From the `kai-agent` folder:

```
uv run app.py
```

It prints `kai-agent running at http://127.0.0.1:8765/` and opens that page in the browser (served on 127.0.0.1 only). If no tab opens, the user opens the address themselves. The terminal stays busy while it runs; Ctrl+C stops it. Commands run with bash on macOS and Linux, and with PowerShell on Windows.

## Check that it works

**(user does this, in the browser page)**
1. Type `What files are in this folder?` and press Enter.
2. A grey box appears with the command the agent wants to run (`ls` or `Get-ChildItem`) and **Approve** / **Deny** buttons. Click **Approve**.
3. The command's output appears, then the agent's answer listing the files (`agent.py`, `app.py`, `index.html`, ...).
4. A gray line under each model call shows `call N · input … · cached … · output …`, and the footer shows totals for the chat. The input count grows with each call because the whole conversation is resent every time.
5. Ask something else and click **Deny**: the agent is told the user declined and should ask what to do instead.

If the page shows a red error instead:
- `The claude command was not found`: install Claude Code (Backend A, step 1), then open a new terminal and restart kai-agent.
- `claude -p failed` or a login message: run `claude auth login` in a terminal, then try again.
- An HTTP error with `BACKEND=openai`: check `BASE_URL`, `MODEL` and the key in `.env`, and that the model supports chat completions.
