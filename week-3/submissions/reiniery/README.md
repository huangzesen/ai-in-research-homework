# Week 3 — Reiniery

Harness: https://github.com/Reiniery/reiniery-agent-harness

`reiniery-telegram` is a stdio MCP server for one authorized private Telegram chat.
It sends split plain-text replies, receives new messages, ignores other chats, and
skips queued messages at startup. The harness loads it as a plugin and owns polling
in phone mode. Every shell command still requires approval; approvals are tied to
their own Telegram prompt or short code, expire after five minutes, and denial stops
the remaining tools in the turn.

`reiniery-themis-density` is a read-only MCP server for local THEMIS THA/THD/THE
13-column DAT files. Three tools describe coverage, summarize sample-weighted density
in cm^-3 by UTC interval and inside/outside plasmapause region, and report sampling
gaps. It preserves region semantics (0 inside, 1 outside); the flag is not a quality
indicator. Real research data stay local. The bundled four-row example is synthetic.

## Run the harness

```sh
git clone https://github.com/Reiniery/reiniery-agent-harness.git
cd reiniery-agent-harness
uv sync
cp .env.example .env
```

Enter the model API settings, Telegram bot token and private chat ID in local `.env`.
Set `THEMIS_DATA_DIR` to the local folder of `den-scpot-YYYYMMDD-tha-1.dat` files
(or leave it blank for the synthetic THA demo). Never paste tokens into AI chat.
Then run:

```sh
uv run python main.py --telegram --model openrouter/free
```

The run-specific model override worked during testing when the saved NVIDIA model
returned a provider 404; model availability can change. Reply directly to each
approval message with yes/no, or send its displayed yes CODE/no CODE. `/new` resets
history; `/stop` stops the agent. Do not send secrets: bot chats are not end-to-end
encrypted. Keep the computer running and use only one Telegram polling host.

## Validation

Both plugins passed stdio MCP checks in the harness and Codex. Codex reproduced the
THA June 1, 2008 comparison: 50 inside records with median 695.6 cm^-3 and 139 outside
records with median 2.342 cm^-3, then sent the compatibility greeting to Telegram.
The student confirmed phone approval, denial and the research answer. A real queued
phone message was rejected with a deliberately wrong chat ID, then skipped by normal
startup initialization. Sixteen automated regression tests pass in the harness;
VALIDATION.md there records the details and scientific limitations.

The model receives MCP tool schemas next to bash and skill names/descriptions/paths
in the system prompt. It reads full skills on demand through approved bash calls.
Credentials go to plugin processes and are not automatically included in model context.
Each plugin README includes loading instructions for Claude Code and Codex.

## AI assistance and license

OpenAI Codex helped implement both MCP servers, the plugin loader, Telegram mode,
permission handling, documentation, and tests. I configured the bot locally, explained
the research data fields, reviewed the scientific result, and tested from my phone.
This submission contains code/documentation and synthetic data only; it is submitted
under the class repository's MIT license.
