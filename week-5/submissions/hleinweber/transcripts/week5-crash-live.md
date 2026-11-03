# Week 5 live interrupted-tool and email recovery

Evidence: student reports plus inspected main journal and matching outbox records.

## Interrupted command

The initial Write-Output crash-test request produced an ordinary chat approval
question, so there was no pending tool to interrupt. The corrected request called
bash and left the harness approval unanswered. After a forced crash and restart,
the agent reported an interrupted telegram-owner task and tools not re-run.
The student then received: "The Write-Output crash-test command was interrupted by
a restart and was not re-run. Its effects should be checked before attempting to
run it again. I will not run it or use any tools as you instructed."
The journal records the bash call and a matching interrupted/not-rerun result.
No command approval was bypassed.

## Email after SMTP, before done

The student armed an exact-content test, approved the email tool and crashed the
agent tree in the delivered-awaiting-done window. Inspection found intent only
and a restart with interrupted true. No done record existed at that point.
The first reconciliation request produced a chat confirmation question instead of
a tool call. After an explicit request to call the tool with unchanged arguments,
the agent reported already sent, prior delivery found and recovered, with no new send.
Later inspection confirmed matching intent and done records with recovered true.
The student independently confirmed exactly one copy in the receiving inbox.
Recipient addresses and message contents are omitted here.

This demonstrates live manual restart recovery and send-once reconciliation.
Automatic restart under Task Scheduler is recorded in week5-service-restart.md: the replacement process reached ready in 42.59 seconds. The student confirmed phone /status afterward.
