# Jasmine's Week 3 plugins

`jasmine0010-telegram` provides two MCP tools to send messages to one configured
private Telegram chat and poll for new owner messages. It rejects other chats,
skips startup backlog, splits long messages, and returns message IDs so the
harness can bind an approval to a particular Telegram reply. Credentials are
environment variables entered locally; no token is part of this submission.

`jasmine0010-psp-waves` wraps my Week 1 Parker Solar Probe wave analysis with
three read-only tools: list the two public intervals, analyze one, or compare
both. It calculates five-minute and two-minute magnetic energy fractions and
signed cross helicity from bundled public measurements for December 24, 2024.
The skill documents units, flags, interpolation limits, normalization, and the
absence of a polarity flip. All 11 checked measurements match the Week 1
acceptance ranges. It needs no research API key or network data retrieval.

## Harness and running

Harness repository: [jasmine0010/jasmines-agent](https://github.com/jasmine0010/jasmines-agent).
The Week 2 version is public on `main`. This local submission draft uses the
prepared `week-3` release branch, which is awaiting final phone verification and
publication approval. No Week 3 submission PR has been opened.

After the release branch is published, install the Week 3 version with:

```sh
git clone --branch week-3 https://github.com/jasmine0010/jasmines-agent.git
cd jasmines-agent
```

In the harness folder, install uv and configure the ignored `.env` from
`.env.example`: `BASE_URL`, `API_KEY`, `MODEL`, `TELEGRAM_BOT_TOKEN`,
`TELEGRAM_CHAT_ID`, and the nonsecret `PSP_PYTHON` interpreter selector.
Enter credentials locally, never in chat. Send `/start` to the bot first.
Stop any other process using the same bot, then run:

```sh
uv sync --locked
uv run --locked --env-file .env python agent.py --telegram
```

The harness discovers both plugins under `plugins/`, starts their MCP servers,
and offers tool schemas beside its built-in shell tool. The system prompt lists
skill metadata; skill bodies are read only when needed through an approved shell
call. The harness owns polling and delivers final answers in phone mode.

In the default manual mode, use Telegram's Reply action on each approval request and type `yes` or `no`.
Only `yes` approves; another reply or a three-minute timeout declines. Old replies
cannot approve a new action. Every shell command asks in manual mode. The owner explicitly
trusted the three read-only PSP tools, so those do not ask repeatedly; other
model-requested MCP actions still ask. `/new` resets phone conversation history.
Ctrl+C stops the process. Bot messages are not end-to-end encrypted, and command
approval is not an operating-system sandbox.

## Validation status

Both plugins worked in Codex and through independent SDK stdio clients.
The owner confirmed Telegram delivery from Codex and the normal harness web chat,
then phone command approval, denial, and free-space reporting. There are 36
passing harness checks, eight Telegram plugin checks, and eight research checks.
Claude Code is unavailable on the test machine, so its plugin validator was not run.

The PSP comparison was resumed through the Telegram interface after a model
timeout; its MCP call succeeded and Telegram accepted the expected answer.
Owner receipt confirmation is pending. The underlying research calculation and
second-host answer passed.
Live owner filtering and restart tests
also passed: a message with a mismatched receiver ID was rejected, an actual
pre-start message was skipped, and a fresh message arrived exactly once. Receipts
are saved in the harness's validation folder. This draft must be updated
with the final phone result before submission.

Codex helped implement the MCP servers, plugin loader, phone interface, tests,
and documentation. I selected the research task, completed the phone checkpoints,
and chose agreement with my Week 1 acceptance ranges as the scientific check.

After the manual approval and denial demonstrations, the owner requested
automatic execution for local Telegram use. Set `"telegram_auto_approve": true`
in the harness settings.json and restart to enable it; all phone-requested shell
and MCP actions then run without prompts. The release default is false so the
assignment's approval-by-reply behavior can be demonstrated.
