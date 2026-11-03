# Week 5 kill-switch demo

Date: November 2, 2026, America/Los_Angeles.

The student requested Start-Sleep -Seconds 600 and approved it using Telegram Reply on the approval prompt. /status showed command PID 40796. After /stop, the final /status showed asleep, task none, no command PID, no running subagents, zero queued messages, four wake-ups, four model calls and 6,604 tokens today.

Verified private log events (UTC):
- 2026-11-03T01:34:47.363359+00:00: process_started, PID 40796.
- 2026-11-03T01:35:16.835591+00:00: process_exited, PID 40796, exit_code 1, cancelled true.
- 2026-11-03T01:35:16.845346+00:00: process_stop_confirmed, PID 40796, exit_code 1.

A subsequent local Get-Process check found no process with PID 40796. Exit code 1 here records forced cancellation, not successful completion of the 600-second sleep.
