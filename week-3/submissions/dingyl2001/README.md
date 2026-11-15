# dingyl2001 — week 3

Harness repository: https://github.com/dingyl2001/psp-agent-harness-ding

## Plugins

**`dingyl2001-telegram`** — a Telegram MCP server: `send_message` and a
long-polling `wait_for_messages`, both scoped to exactly one configured
chat (messages from any other chat are dropped and logged). Used by the
harness's `--telegram` mode so approvals happen by replying "yes"/"no"
on a phone instead of typing into a terminal.

**`dingyl2001-energyflux`** — a research MCP server wrapping a
multi-species (proton + alpha + electron-coupling) MHD solar wind
energy-flux model, generalizing Belcher (1971) and Halekas et al.
(2023) — both single-species/proton-only — to track alpha particles as
their own species (own kinetic+enthalpy term, own gravitational term,
own ambipolar-electric term with charge number Z=2, and alpha mass
contributing to the Alfvén speed). Three tools: `compute_energy_budget`,
`alpha_density_from_quasineutrality`, and
`compare_alpha_density_assumptions`. Validated against real PSP
Encounter 10 SWEAP data.

## Run in Telegram mode

```
git clone https://github.com/dingyl2001/psp-agent-harness-ding.git
cd psp-agent-harness-ding
uv sync
cp .env.example .env   # fill in BASE_URL, API_KEY, MODEL, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
uv run harness.py --telegram
```

Message the bot from Telegram; approval requests for `bash` or any
plugin tool call arrive as replies to approve ("yes") or deny ("no").

Tested: plugin auto-discovery (both plugins load with zero harness code
changes), both the approve and deny paths over a live Telegram
round-trip, multi-step tool chains, and the energy-flux model's output
checked for scientific correctness against the original (non-plugin)
validation run.
