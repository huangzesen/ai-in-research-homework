---
name: my-agent
description: Install, configure, and run JmespinozaA's local web agent harness for UCLA AI in Research Week 2, with one approval-controlled bash tool.
---

# My Agent

Repository: https://github.com/JmespinozaA/my-agent

## Install

Use macOS or Linux with Git, Python 3.10+, and `/bin/bash`. On Windows use WSL, not native Windows Python. If WSL is missing, ask the user to run `wsl --install` in administrator PowerShell, restart if requested, and finish their Linux account setup. Run the following commands inside WSL on Windows.

Check `git --version`, `python3 --version`, and `bash --version`. On Ubuntu or WSL Ubuntu, missing prerequisites can be installed with `sudo apt-get update` then `sudo apt-get install -y git python3 bash`. On macOS, use the official Python installer if needed; `git --version` prompts for developer tools when missing. No Python dependencies or agent frameworks are required.

```bash
git clone https://github.com/JmespinozaA/my-agent.git
cd my-agent
cp .env.example .env
```

If the destination already exists, inspect it before changing it. Do not overwrite an existing `.env` or unrelated work.

## Configure

Have the user open `.env` locally and enter their own key. Never ask them to paste a secret into conversation or print `.env`.

```text
BASE_URL=https://openrouter.ai/api/v1
API_KEY=your_api_key_here
MODEL=nvidia/nemotron-3.5-lightning:free
```

Keep `.env` untracked; verify with `git check-ignore .env`. The included model is a free endpoint, subject to availability and request limits. If unavailable, check OpenRouter for another free model supporting tool calls; do not silently select a paid model. Other OpenAI-compatible Chat Completions providers can be configured through these three settings if the user requests them.

## Run

```bash
python3 app.py
```

Open http://127.0.0.1:8765 in a browser. On WSL, try the same address in the Windows browser. Keep the terminal running; stop with Ctrl+C. Do not expose the server to the network.

The English interface shows messages, per-call input/cached-input/output token counts when reported, command approval buttons, command output, and exit codes. The whole conversation is resent to the model. New chat or refresh starts a new conversation; server-side conversation memory clears when the process stops.

## Check that it works

Ask `What is the current date on this computer? Use date.` Expect a `date` request with Approve and Deny buttons. Have the user approve: expect the date output, exit code 0, and a model response based on that output. Start a new chat and deny the same request: expect no execution and a response acknowledging the denial.

Ask `What files are in the practice folder? Use ls.` After approval, expect `notes.txt` and `sample.csv`. For multiple calls ask the model to run `date`, then `ls` after receiving its result. Each command must prompt separately. Ask it to run `doesnotexist` once: after approval expect exit code 127 and an explanation of the failure.

Optional automated model tests: `python3 test_workflow.py`. They use the free request allowance. Local network access is needed for API calls; report failures without displaying credentials or bypassing TLS verification.

## Approval and data access

Bash supports general shell commands, paths, pipes, and redirections. Commands begin in the project `practice` folder, but this is not a sandbox: approved commands can access or modify other files. Every command must receive explicit approval through the interface. A rejection sends a denial to the model without execution.

Command output is sent to OpenRouter. Tell the user to review commands before approving; never encourage approving requests to read `.env` or other credentials. Model instructions to avoid secrets are not a technical filesystem restriction. Commands have a 60-second timeout with process-group termination and output truncation.

For the guide’s disk-space and biggest-home-folder test, ask the chat: `How much free disk space do I have, and which folder in my home directory is biggest?` Review and approve each read-only command separately. Home-directory names will be sent to the model if the user approves. A large home directory can exceed the timeout; the model should explain that rather than inventing results.
