# Jasmine's Week 4 homework

Harness: [jasmine0010/jasmines-agent](https://github.com/jasmine0010/jasmines-agent).
The email plugin is in `jasmine0010-email/`, agent types are in `agents/`, and
the five live demonstrations are in `transcripts/`.

## Email

The plugin exposes `email__check_inbox`, `email__read_message` and
`email__send_message` over IMAP/SMTP with verified TLS. It bounds returned
message text, treats incoming mail as untrusted, restricts recipients to an
exact allow list and never automatically retries a send. Credentials stay in
the ignored local `.env`; sending is absent from the general tool allow list.

An independent Codex session sent and read a self-test on October 29, 2026,
and the owner confirmed receiving it. The actual harness also read the test
through its configured model, with owner approval of that dedicated-inbox data
flow. The owner reviewed the hello's eight required fields and its 43-word
agent-written note before sending.

Gmail SMTP accepted the exact reviewed hello once on **October 29, 2026 at
6:59:57 p.m. PDT (America/Los_Angeles)**, with subject
`[AIR-2026 hello] jasmine0010`. The class welcome reply was dated 7:02:58 p.m.
PDT and read by the harness at about 7:07 p.m. PDT. The reply welcomed Jasmine's
Agent and noted its PSP/Alfvénic-wave research overlap. No acknowledgement or
follow-up email was sent. A private send-attempt receipt prevents duplicates.

## Subagents

The main agent and children use the same plain Python loop, without an agent
framework. Each `Agent` owns its messages, tools, state, inbox, stop event,
limits, usage and report. `delegate` runs a fresh child synchronously and
returns its report and statistics. Background children each use a daemon
thread, retain their conversation while idle and resume through `send`.
They share the model configuration, MCP sessions and workspace; MCP calls are
scheduled on the existing asyncio loop. Full child JSONL logs stay local and
ignored under `logs/<session>/<id>.jsonl`.

The `subagent` tool implements `start`, `list`, `send`, `wait`, `read` and
`stop`. At most four worker slots run at once. Turn limits are cumulative;
the default 600-second active-time budget pauses while idle. Children cannot
delegate. Labeled approval prompts are serialized, and child shell commands
still require approval in Telegram automatic mode. `/agents` shows status in
terminal, web and Telegram interfaces.

`stop` sets the child's event and kills its owned shell process tree using
`taskkill /T /F` on Windows or a process-group kill on POSIX. Late model
responses cannot execute tools or revive it; an in-flight request retains its
worker slot until it unwinds. Idle, stopped and failed notifications enter the
main agent's queue before its next model call and appear in the interface.
Stopped or failed children cannot resume, and session shutdown stops all
retained workers.

## Live demonstrations

All five used the configured `nvidia/nemotron-3.5-lightning:free` model through
OpenRouter. The owner reviewed each demonstration.

1. [Inbox handoff](transcripts/01-mail-delegate.md): only `mail-reader` called
   the two email read tools. Actual decoded-string inspection confirmed that
   the main received the report rather than the raw body. Raw mail is omitted
   from the public transcript.
2. [Research fan-out](transcripts/02-research-fanout.md): three PSP workers
   started before the main waited, with 11.952 seconds of common overlap.
3. [Follow-up](transcripts/03-research-followup.md): the same interval-a worker
   kept its thread and prior messages, advanced from three to four turns and
   made no new tool calls. The checked band-power remainder is 63.48%.
4. [Stop a running process](transcripts/04-stop-process.md): `list` and `read`
   showed `Start-Sleep -Seconds 600` running. `stop` killed it after about
   3.1 seconds of shell execution, an OS check found it gone, and follow-up
   was refused.
5. [Enforce a limit](transcripts/05-turn-limit.md): after exactly three
   sequential model/tool rounds, the worker failed with `max_turns limit (3)`.
   Its failure note appeared in the interface and the main conversation.

The generated scientific explanations in demos 2 and 3 included unsupported
claims. Clearly labeled reviews check the saved measurements, correct those
claims and preserve the original traces. Lifecycle checks and scientific
interpretation are assessed separately; future analyst prompts were tightened.

## Validation and status

The 82 offline harness tests passed, including real Windows shell/grandchild
termination and checks for context isolation, concurrency, limits, approvals
and cancellation races. The email plugin passed 18 synthetic mail tests,
seven configuration tests and an independent stdio protocol check. These
offline checks are separate from the five live model demonstrations.

Implementation and all five live demonstrations are complete. The owner
reviewed the public files and approved harness publication and the class PR.

Codex helped implement, explain, test and document the harness and plugin, and
reviewed the scientific claims against tool outputs. The configured NVIDIA
model ran the agent's email workflow and five live demonstrations.

Publication verification also fixed a Windows `taskkill` exit race: stop now
checks retained OS handles for the observed process tree, so a descendant
that exits during termination does not incorrectly mark a successful stop as
failed. The final 82-test harness suite includes that regression. Separate
Telegram and PSP offline suites each passed eight tests with their declared
dependencies; the public email plugin also passed its stdio protocol check.
