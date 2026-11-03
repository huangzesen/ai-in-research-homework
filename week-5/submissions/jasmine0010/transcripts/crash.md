# Week 5: crash recovery and send-once evidence

This combines the real SMTP crash gap and the separate real Windows service
restart test. Their failures and different scopes are retained.

# Week 5: real SMTP crash gap and journal replay

The attended fixture used a real model task, the normal Telegram owner approval,
the real dedicated Gmail account and the production always-on outbox wrapper.
Only one harmless email to the agent's own inbox was approved. Addresses,
mail content, chat IDs and raw conversation records are excluded here.

Evidence, in order (UTC timestamps; field excerpts are sanitized):

1. logs/main.jsonl line 9, 2026-11-03T05:19:05.772902+00:00: the assistant
   requested email__send_message. Its tool-call ID was durably recorded before
   execution. This is a real model tool request, not a fabricated replay.
2. state/outbox.jsonl, 2026-11-03T05:19:30.574886+00:00: `kind=intent`, a deterministic
   content key and Message-ID were flushed before the SMTP attempt.
3. Gmail accepted one SMTP attempt at 2026-11-03T05:19:33.377276+00:00. The test-only
   after-accept hook paused before writing done. The first controller then
   rejected a PID equality check: Windows venv python.exe was a redirector,
   whose Popen PID differed from the actual Python PID. Its cleanup force-killed
   the owned launcher tree. An OS check confirmed no fixture process remained.
   The intent remained without done. No second email was approved or sent.
4. A fresh process was launched in recovery-only mode. logs/main.jsonl line
   10, 2026-11-03T05:21:16.316759+00:00, added the missing tool result:
   "Interrupted by a restart; not re-run. Check its effects before trying again."
5. Sent reconciliation found exactly one message by the deterministic
   Message-ID. state/outbox.jsonl, 2026-11-03T05:21:19.372398+00:00: `kind=done`,
   `reconciled=true`, `match=message_id`, `count=1`.
6. Startup told the owner on Telegram that one unfinished call was marked
   interrupted and one pending intent checked. The owner confirmed receiving
   that restart notice. The model then continued from the repaired conversation.
7. A repeated request through the same outbox returned `already_sent`, with
   no new approval, reply-budget reservation or SMTP call. The restarted process
   made 0 SMTP attempts. Final Sent count:
   1. The preview stopped at 2026-11-03T05:22:14.697466+00:00.

The controller was fixed to kill its owned Popen process tree without assuming
the launcher and interpreter have the same PID; a real Windows process-tree
regression checks that the actual sleeping interpreter exits. This run did not
test Task Scheduler. The service restart demo is still required in Step 6.

The initial journal bootstrap is explicitly labeled a retrospective import of
the earlier control checkpoint. It is not presented as real-time logging of
the previous demos. New messages, usage and compaction markers are append-only.

Student explanation of restart:

> Intent is saved before sending to act as the foundation of the request/command and ensure reliability. It sends the email but crashes before marking it as done. After restarting, the agent checks intent and continues workflow, finds that email is sent, so marks it as done. The repeat request sees that and does not send a second email

The student correctly described intent, Sent reconciliation, done and duplicate
suppression. Step 5 and its learning checkpoint are complete.


# Week 5: Windows service restart

Task: JasminesAgent-AlwaysOn, current-user interactive login, limited privileges.
The real registration exports one-minute failure retries, no runtime limit,
IgnoreNew and a one-minute native recovery trigger. The trigger does not call
the model. Public service/windows-task.xml is a sanitized actual export; the
ignored local export retains the installed identity and paths.

Attempt 1 failed and is preserved privately. The owner approved a real
Start-Sleep -Seconds 600 wrapped in a second PowerShell. An exact matcher first
missed that wrapper. After the matcher was corrected, the observer terminated
only the verified service interpreter at 2026-11-03T07:01:00Z. Its five-second
process-handle check failed. A subsequent OS inventory found the old service
and sleep absent. Task Scheduler recorded exit 15 but no automatic restart was
observed before the manual repair start around 07:04:59Z. That manual repair is
not counted as a successful automatic restart. The installed task definition
had been updated while its first instance ran; whether that caused the missed
retry is unproven. A native minute recovery trigger was added after this failure.

On that repair start, the model asked for approval to repeat the interrupted
sleep. The owner declined it; no repeated command executed. Recovery turns now
hide shell execution, delegation, schedule changes, memory writes and email
sends in code. A fresh owner request restores normal permissions. A focused
test checks both the rejection during recovery and normal fresh-owner behavior.

Attempt 2 used a genuine fresh Telegram reply task, with no new shell approval
or email send. Its request and API text response were recorded. The observer
killed the verified service while that reply task was finishing; its wake had
not logged completion. It did not kill in the middle of the HTTP request: the
API response was already in the journal. The task's final phone delivery was
not established by that interrupted turn.

- Force termination: 2026-11-03T07:11:32.349562+00:00.
- Old owned process handles: 10; all signaled exited.
- Observed cleanup time: 10.055 seconds.
- New service interpreter: 2026-11-03T07:11:48.759886+00:00.
- Automatic process-start latency: 16.41 seconds.
- Manual Start-ScheduledTask during this second recovery: none.
- Watchers ready: 2026-11-03T07:15:36.685050+00:00.
- Watcher readiness after the kill: 244.335 seconds.

The observer's three-minute watcher-readiness deadline expired. The real later
ready event is preserved above; process start and phone readiness are separate.
The default task priority was observed as BelowNormal (setting 7). The task and
its verified live descendants were changed to Normal (setting 5); a faster
future restart has not been measured, so that change is not claimed as a proven
fix for the slow startup.

The saved owner request survived in the append-only journal. The previous
send-once outbox remains durable; this test sent no email. The separate SMTP
crash-gap transcript proves one Sent match and zero resend attempts after its
restart. Both parts are needed to describe the crash demo honestly.

The student confirmed a restart notice and a fresh Telegram /status:
asleep, no current action, zero queued events and no running subagents.
Daily usage was 11 wake-ups, 21 model requests and 193451 reported tokens,
with zero estimates/reservations; dollars unknown. The next job was daily-papers
at 2026-11-03 08:00 -08:00. This is the completed Step 6 checkpoint.

The service stays running. The eight-hour evidence window starts at the verified
ready event above; it is not yet an eight-hour success. The log-derived report
is scheduled separately for 08:15 Pacific on November 3.
