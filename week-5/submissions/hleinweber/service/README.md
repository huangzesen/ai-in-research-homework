# Windows Task Scheduler service

Prepared for this checkout by service/manage.ps1. ResearchAgentAlwaysOn runs as the
current logged-in user at least privilege. It stores no Windows password. Locking
the screen or a screen saver does not end that login session; logging off does.
The laptop still needs its lid open and must remain awake, as agreed for the night.

The action starts a hidden PowerShell wrapper, which starts the absolute venv
Python path with service_runner.py. The wrapper waits and propagates Python's exit
code. The runner uses the absolute repository as its working directory, adds the
prepared uv directory and venv Scripts to PATH, and launches agent.py --always-on.
The normal application loads its own local configuration. No credentials are in
the task XML or command arguments. stdout/stderr append to logs/service-stdout.log
and logs/service-stderr.log. The hidden window does not replace phone approvals.

Settings: logon trigger for this user plus a repeating one-minute recovery trigger, one minute between failure retries (up to
255 retries), ExecutionTimeLimit PT0S, IgnoreNew for duplicate task starts, and
continued operation on battery. Plugging in is still recommended for the night.
IgnoreNew makes recovery triggers no-ops while the task is already running; these triggers do not call the model. A workspace OS lock also refuses a second manual web/terminal/plugin host before
it can initialize Telegram. Stop the scheduled task before using another mode.
The lock is released by the OS if the owning process dies.

From the repository folder, invoke management using:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File service/manage.ps1 ACTION

Actions: Prepare (generate reviewable XML only), Install (register without starting),
Start, Stop, Status, Export, Update (requires stopped task), Uninstall (requires stopped task), CrashTest.
The process-scoped PowerShell execution policy option allows these local scripts;
it does not grant administrator rights or change machine policy.

CrashTest verifies the tracked agent PID's command line, repository and creation
time, then terminates only that service tree. It waits up to 100 seconds for a new
run ID in ready state. Evidence goes to private state/service-restart-test.json.
The child interpreter's nonzero exit propagates through the wrapper to Task Scheduler. The one-minute recovery trigger also relaunches a missing task because the first live test showed the native failure retry alone did not fire on this computer.
Do not use Stop to test automatic failure restart: an explicitly stopped task is
not a failed run. /stop in Telegram cancels current agent work; it does not disable
the scheduled service. Stop disables the task before terminating it, so the recovery trigger respects an intentional shutdown. Start re-enables it. Use Stop before editing/running the agent manually.

ResearchAgentAlwaysOn.xml is a privacy-reviewed export from the actual registered task. Machine SIDs have been replaced with the equivalent local username hleinweber; regenerate it with Prepare for another machine.
It contains machine-specific paths and the account identity, but no credentials.
Review regenerated exports before publication: Prepare/Export uses this machine's account SID. The published copy has already been sanitized. This service has no scheduled
heartbeat/model call. Application watchers remain in charge of wake-ups.

Offline checks use fake providers/models and do not load credentials. An intentional
bad-uv-directory check can appear in the stderr log from setup; that synthetic
failure verifies nonzero exit propagation and is not a live service failure.

These scripts are copied here as submission evidence. Run them from the linked harness checkout, which contains service_runner.py and the venv; this class folder does not contain the full runnable harness.
