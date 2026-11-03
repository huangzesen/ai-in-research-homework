# Week 5 Windows Task Scheduler restart demo

The service was registered as ResearchAgentAlwaysOn for the logged-in Windows user,
with InteractiveToken logon and least privilege (no stored password). A hidden
PowerShell wrapper launches the venv Python and propagates its exit code. Normal
always-on mode and the existing conversation journal are used.

The first live test terminated the service tree, and Windows recorded exit code 1,
but native RestartOnFailure did not relaunch it within 100 seconds. A repeating
one-minute recovery trigger was added alongside the logon trigger. IgnoreNew prevents
an additional instance when the task is already running. Stop now disables the task;
Start re-enables it. The recovery trigger makes no model calls itself.

Verified second test:

- old_pid: 7172
- new_pid: 38572
- seconds: 42.59
- ready: True
- recorded_at: 2026-11-03T03:26:40.3186529Z

The test checked the tracked PID's command line, repository and process creation
time before terminating only that agent tree. A different run ID reached ready,
which is recorded after plugin startup and conversation restoration. Task state
was checked afterward. This verifies restart during the current logged-in session;
a fresh login trigger has not been tested by logging out and back in.

The student subsequently confirmed phone /status responded. The completed 12h 34m overnight window is documented in night.md.
