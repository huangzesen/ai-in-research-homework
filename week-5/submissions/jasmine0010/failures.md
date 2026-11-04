# Week 5 failures

## 2026-11-02: script entrypoint used a separate agent module

What happened: `python agent.py --telegram` initialized PLUGINS on __main__,
while the interface imported a separate agent module. The new --always-on
entrypoint exposed the same existing problem.

How noticed: a fresh-process offline regression failed with
`AssertionError: CLI and interface imported different agent modules` for both
entrypoints, despite passing in-process tests.

Changed: alias the script module as agent before main starts. Both interfaces
now share the connected runtime. Keep the fresh-process regression.

## 2026-11-02: inbox watcher would miss arrivals beyond one page

What happened: the existing check_inbox returned only the newest 20 headers;
polling the same newest page could hide earlier messages in a larger burst.

How noticed: inspected the existing plugin while building the watcher.

Changed: added an optional after_id UID cursor, oldest-first pages, more and
next_after_id fields, plus UIDVALIDITY so mailbox replacement cannot reuse IDs.
Tests cover 25 arrivals in two pages and IMAP's N:* reverse-range behavior.

## 2026-11-02: network sandbox could not fetch the assignment

What happened: the web reader could not open homework.md; the sandboxed shell
reported `No such host is known.`

How noticed: opening the user-provided assignment URL failed.

Changed: fetched the public assignment with an approved network-capable shell;
read the full course guide and located the existing local harness.

## 2026-11-02: routine email notification asked for approval

What happened: the email wake-up offered the model telegram__send_message,
although the harness already delivers final answers. The owner received an
approval prompt for an ordinary arrival notice, followed by the notice.

How noticed: the owner reported the exact prompt after the real email test.
The log confirms one email wake-up, two model calls and 6,906 reported tokens;
no email reply was sent.

Changed: hide Telegram send and poll tools from the always-on model and its
children. The harness owns reply delivery; the model returns plain text.
Regression checks cover blocked fabricated transport calls and one final
email-arrival notification without approval. The original live observation
is preserved rather than described as a post-fix demonstration.

## 2026-11-02: proposed recurring job repeated unchanged data

What happened: the first suggested weekday job reran diagnostics on fixed
PSP intervals, so it would mostly repeat the same numbers.

How noticed: the owner asked whether this was the best task and whether it
recurred. The scheduler was sound, but the proposed recurring work had little
new information value.

Changed: the owner chose a weekday 8 a.m. digest of new matching papers.
Added a bounded public arXiv feed tool, cross-list deduplication and local
delivered-paper bookkeeping. The saved-data check remains available on demand.

## 2026-11-02: main commands did not expose a cancellable process handle

What happened: the older main-agent shell path called run_bash without its
Agent object, whereas children already owned their process handles. That
could not support the new top-level phone kill switch.

How noticed: inspected main/child dispatch before implementing Step 3.

Changed: controlled main calls use the worker-aware shell path, with the
deadline, stop flag and process-tree handling. A real offline 600-second sleep
was killed before completion, and no second model call occurred.

## 2026-11-02: stop-test assertion mishandled a valid tool-call message

What happened: the process-stop assertions passed, but the final test assertion
raised TypeError because an assistant tool-call message had content=None.

How noticed: unittest reported that NoneType was not iterable while checking
for the saved control note.

Changed: the assertion treats null content as empty text. The full suite then
passed; this was a test assertion error, not a failed OS termination.

## 2026-11-02: allowlist review found overly broad child-label stripping

What happened: the first control implementation stripped any bracketed prefix
before checking a read-only command, although only real worker labels should
be treated as harness metadata.

How noticed: code review of the exact-command approval boundary.

Changed: strip only a registered child's exact id/type label. The regression
rejects an arbitrary prefix and still accepts a real registered worker label.
No unapproved prefixed command was executed in a live test.

## 2026-11-02: first live control preview expired and missed delegated work

What happened: the real sleep request arrived near the end of the original
20-minute preview. The model delegated it to process-demo, but the helper
watched only the main process. The preview stopped at 8:06 p.m. Pacific with
no credited phone stop or budget demo. The owner reported no /status or /stop
reply; the first run did not log command arrival times, so their delivery
relative to shutdown cannot be established.

How noticed: inspected the incomplete_timeout receipt, the real main/child
trajectory and the owner's report. The child was stopped by session cleanup;
that is not a successful owner /stop demonstration.

Changed: the helper now observes the main and child processes; /status shows
child actions; command arrivals are logged without message bodies or chat IDs.
The initial waiting window is 30 minutes, extends with owner activity and has
a one-hour cap. Expiry sends an explicit stopped notice. A real delegated
sleep regression verifies status visibility and top-level process termination.
The failed receipt is preserved privately as the first attempt. The repaired live attempt passed with owner
confirmation; the original incomplete attempt remains documented.

## 2026-11-02: compaction preserved values but mislabeled their importance

What happened: the real summary kept the demo code and interval correctly, but
one Decisions sentence called the important identifiers nonessential. The
memory checkpoint also read memory despite it already being supplied in the
system prompt, adding a redundant long-context model/tool round.

How noticed: compared the untouched generated summary and retained tool turn
with the original explicitly synthetic fixture. The real recall answer was
correct; semantic priority and workflow efficiency were separate shortcomings.

Changed: tightened future summary prompts to preserve owner-designated
importance. Kept the original output and the redundant read in the evidence,
and did not claim the prompt change guarantees correct prioritization.
The compaction demo cost seven requests / 139,088 reported tokens including
repeated long-context calls; estimates are labeled separately from API counts.

## 2026-11-02: Windows venv launcher PID differed from Python PID

The live crash controller assumed its Popen PID equaled os.getpid() inside the
child script. SMTP had accepted the approved self-email, then that guard failed.
Cleanup force-killed the owned launcher tree, leaving intent without done.
An OS check found no surviving fixture process. A harmless subprocess reproduced
the redirector behavior: different launcher and interpreter PIDs.

The controller now always kills the Popen tree it created, without selecting
a target from the receipt. A Windows regression retains an OS process handle
and verifies the actual sleeping interpreter exits. A recovery-only invocation
then resumed the original accepted intent: one Sent match, no second send,
missing tool result marked interrupted. The original incident remains recorded.

## 2026-11-02: sandboxed uv status check could not persist its cache

A read-only receipt check unnecessarily launched uv in the restricted shell.
It retried a cache write and reported Access is denied. That status command was
stopped; plain PowerShell read the receipt without touching the Python cache.
This did not affect the separate live agent or resend email. Use plain file
reads for status and the authorized harness environment for Python checks.

## 2026-11-02: task export sanitizer had an invalid raw string

The separate export script ended a raw string with a backslash and failed with
SyntaxError before generating public XML. The running service was unaffected.
The string was corrected, compilation and export validation passed, and the
sanitized export excludes local user paths and SID.

## 2026-11-02: the real sleep had a PowerShell wrapper

The model used powershell -Command around the requested Start-Sleep. The
observer's exact matcher missed it. OS ancestry confirmed both PowerShell
processes belonged to this service. The observer was stopped and corrected to
recognize that simple wrapper; the existing approval was not repeated.

## 2026-11-02: first service retry failed; cleanup and startup were slower than expected

The service was force-stopped during the approved sleep. The five-second handle
check timed out; later OS enumeration showed the service and sleep gone. The
first retry-only configuration did not produce an automatic restart before a
manual repair roughly four minutes later. The task had been updated mid-run;
that as a cause remains unproven. No automatic recovery success is claimed for
this attempt. A native minute repetition trigger was added, retaining IgnoreNew
and the failure retry settings, so Windows can restart a missing instance.

In the second real reply-task test all ten retained handles signaled exit after
10.055 seconds and a new process started automatically in 16.410 seconds.
The observer's three-minute watcher-readiness window expired; a later real
watcher-ready event and fresh owner status confirmed functionality. Process
start and phone readiness are recorded separately. Default BelowNormal task
priority was changed to Normal for the task and its verified descendants;
faster startup has not been measured. The observer now records individual wait
codes and allows 30 seconds for asynchronous process cleanup.

## 2026-11-02: restart model asked to repeat interrupted sleep

After the manual repair, the model requested approval to repeat the prior
sleep. The owner declined it, so it did not execute. Recovery turns now hide
shell, delegation, schedule, memory and send tools in code and defer compaction;
the model can explain the interruption and ask for a fresh owner request.
The regression also verifies that a fresh owner event restores normal tools.

The first version of that regression accidentally mutated a tool-call fixture
already stored in old history. The append-only checkpoint correctly rejected
that unlogged mutation. Separate fixture objects fixed the test; this was a
test-construction error, not a live history corruption.

## 2026-11-02: transport failures retried during service checks

The journal recorded email/Telegram watcher RuntimeErrors. The Telegram server
reported that it could not reach Telegram or parse its response; the exact
network cause is unknown. Watchers retained their cursor and retried. Later
owner approvals, messages and fresh /status demonstrated working Telegram.
No model action or email send was retried because of the transport errors.

## 2026-11-02: overnight wake answered with an acknowledgement

The owner requested the exact phrase "Week 5 overnight wake works". A real
Telegram wake completed with 5715 reported tokens, but the student reported
the phone reply as "acknowledged". Event routing and model wake-up succeeded;
exact instruction following did not. This remains a model-behavior limitation
for review, with no claim that a prompt change has fixed it. The overnight
service was left running so the real duration and scheduled digest can be
observed. The student confirmed receiving the acknowledgement.

## 2026-11-03: AC-only task stopped before the morning job

The first night report was incomplete: 8.99 wall-clock hours, one message wake,
5715 reported tokens, zero idle model requests, and no completed scheduled wake.
The service run ID had changed. Windows Kernel-Power event 105 recorded
AcOnline=false at 07:04:56 Pacific and AcOnline=true at 08:08:31. The registered
task had DisallowStartIfOnBatteries and StopIfGoingOnBatteries set true. That
power-source interval explains why it stopped while the computer stayed awake
and skipped the 08:00 job. The owner's pasted 08:08 messages were restart
notices, not a digest. Later Modern Standby/lid events started at 08:21.

The task and installer now allow starting/continuing on battery. The failed
report is retained as night-attempt-1.md and its original private metadata was
archived. No global power plan was changed. The user requested a new eight-hour
daytime run, starting 10:57:49 with a local report due 18:58 on November 3.

## 2026-11-03: Telegram DNS failure aborted the whole plugin startup

The current network could not resolve api.telegram.org. Public arXiv requests
succeeded; changing certificate stores did not help, and no TLS settings were
changed. The Telegram startup backlog request raised RuntimeError, causing
plugin startup and the service to exit repeatedly. The user will restore
network connectivity later; no DNS/proxy or other system network settings
were modified.

Telegram startup now yields a transport with pending backlog initialization
after that error. The phone watcher retries it, skips old backlog on its first
successful retry, and then accepts fresh updates. Other event sources remain
available while Telegram is offline. Two new synthetic tests cover startup and
recovery, including no secret values in logs. The live service now stays alive;
phone reconnection cannot be claimed until the network works again.

## 2026-11-03: network outage during the replacement run

The run passed its audit, but the computer could not reliably reach Telegram
for most of it. The journal recorded 1389 Telegram watcher failures (10:57 to
16:29, then two at 17:10), 123 email watcher failures (intermittent, 11:56 to
16:28) and 2 Telegram delivery failures. Those were the 10:59 email notice and
the 11:00 scheduled answer, so neither reached the phone. The exact network
cause is unknown.

How noticed: the journal's failure counts and a DNS check. The audit does not
check delivery, so "passed" does not mean every answer arrived.

Changed: no settings were changed; the watchers retried. A real owner message
at 16:53 woke the agent after the network returned, and the student confirmed
the reply reached the phone. Undelivered answers are not resent, which remains
a known limitation.

## Status

Steps 1-6 and their student checkpoints are complete. The original overnight
attempt is honestly incomplete and preserved in transcripts/night-attempt-1.md.
The eight-hour daytime replacement passed its audit (8.00 hours, same live
service run, no Windows sleep events, three completed wake-ups, zero idle model
requests); see transcripts/night.md.
