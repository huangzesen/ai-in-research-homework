# Demo 1: delegate inbox inspection

Real run on October 27, 2026. Private email subjects, senders and dates are omitted in this publication candidate. Full local logs remain private. No body reads or sends were authorized or performed.

## Main agent

- 2026-10-27T22:34:20.758548+00:00 — system
  Main system instructions and agent-type metadata; child system prompt not included.
- 2026-10-27T22:34:20.760202+00:00 — user
  Task: delegate to mail-reader; list at most five recent headers; no bodies, sends or bash.
- 2026-10-27T22:34:24.188246+00:00 — assistant
  Tool proposal: delegate
- 2026-10-27T22:35:41.333397+00:00 — tool
  Delegate result: report (private metadata omitted), [sa-1 · mail-reader · 2 turns · 2893 tokens · 77.14 s · idle]
- 2026-10-27T22:35:46.310839+00:00 — assistant
  Final summary: five recent messages checked; no class-agent reply among them. Private metadata omitted.

## mail-reader child

- 2026-10-27T22:34:24.189084+00:00 — system
  mail-reader system prompt; only email__check_inbox and email__read_message available.
- 2026-10-27T22:34:24.190690+00:00 — user
  Self-contained task passed by main; no main conversation supplied.
- 2026-10-27T22:34:27.858956+00:00 — assistant
  email__check_inbox {"unread_only":false,"limit":5}
- 2026-10-27T22:35:22.469094+00:00 — tool
  Raw inbox header result: [private metadata omitted for publication]. This result exists only in the child context/log.
- 2026-10-27T22:35:41.332479+00:00 — assistant
  Report: five recent messages checked; none from the class agent. Private metadata omitted.

## Verification

- One child was created; state after report: idle.
- Exactly one check_inbox call, unread_only=false, limit=5; succeeded.
- No read_message, send_message or bash call ran.
- Raw child tool-result strings are absent from main.messages.
- Main received only the report and statistics.
- Child: 2 model calls, 2893 total tokens, included in main session child-token totals.

This demo checks five recent inbox messages; it does not establish that all folders or all history contain no reply.
