# Windows service

From an installed harness, run `uv sync --locked` once, configure its ignored
`.env` locally, then invoke `service/install-windows.ps1 -Start` in PowerShell.
The script registers `JasminesAgent-AlwaysOn` for the current logged-in user,
with limited privileges and an at-login trigger. It does not store a Windows
password. The action uses absolute paths to `.venv/Scripts/pythonw.exe` and
`service_runner.py`, with the harness as its working directory. Pythonw keeps
the agent in the background without a console window; the task remains visible
in Task Scheduler. A duplicate installer invocation refuses to replace it.

Task Scheduler restarts failed actions every minute, for up to 999 attempts,
with no runtime limit and `IgnoreNew` for overlapping starts. The first live
failure-retry-only test did not restart, so a native time trigger also attempts
a start once per minute indefinitely. A running instance causes that attempt
to be skipped. This is an OS service-recovery trigger; it does not enqueue a
model task or change the weekday 8 a.m. research schedule. Priority 5 uses normal
process priority; the first installed default was below normal. The local
`state/telegram.lock` also prevents another phone-mode process in this checkout
from connecting a second poller. Stop terminal phone previews before starting
the service. After the first night exposed an AC-only stop, the task now
allows starting and continuing on battery. Keep the computer charged, logged
in, awake, and with its lid open for the evidence run.

`service_runner.py` reads the root `.env` using python-dotenv with literal
values and no variable interpolation. The service uses the local file rather
than depending on the launching shell's environment. The ordinary agent CLI
also reads that exact path, preserving explicitly inherited values. The runner
sets its working directory and tool PATH, appends stdout/stderr to private
`logs/service.stdout.log` and `logs/service.stderr.log`, and writes only process
metadata to private `state/service.json`. Plugin script environments may need
network access on their first cold start; later restarts reuse their cache.

An owned Windows job uses `KILL_ON_JOB_CLOSE`: when the service interpreter
dies, its descendants, including MCP servers and shell commands, die with it.
Task Scheduler owns the restart; the runner has no private restart loop. A
continuous `ES_SYSTEM_REQUIRED` request prevents idle sleep while it runs.
It releases on exit and does not override manual sleep, lid closure or logout.
The screen may turn off normally.

These settings follow the official documentation for
[scheduled-task restart settings](https://learn.microsoft.com/en-us/powershell/module/scheduledtasks/new-scheduledtasksettingsset),
[job objects](https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects),
and [power requests](https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-setthreadexecutionstate).

The installer saves an actual export as `windows-task.local.xml`, ignored by
Git. `export_public.py` validates that export and creates `windows-task.xml`
with owner SID and user-specific paths replaced by explicit placeholders. The
public XML is a sanitized export, not a directly runnable registration. Use
the installer on another computer to generate its correct paths and identity.

To inspect the task: `Get-ScheduledTask -TaskName JasminesAgent-AlwaysOn`.
To stop the service intentionally, first run `Disable-ScheduledTask -TaskName JasminesAgent-AlwaysOn`,
then `Stop-ScheduledTask -TaskName JasminesAgent-AlwaysOn`. Disabling it prevents
the recovery trigger from starting it again. To start it again, run
`Enable-ScheduledTask -TaskName JasminesAgent-AlwaysOn`, then
`Start-ScheduledTask -TaskName JasminesAgent-AlwaysOn`.
Telegram `/stop` cancels current work; `/pause` holds queued work. Those phone
commands keep the service alive.

`tests/check_service_live.py` is an attended observer. It waits for an owner-
approved main-agent `Start-Sleep -Seconds 600`, kills only the verified service
interpreter, retains OS process handles to check that the sleep exits, and
waits for Task Scheduler to produce a new run. It does not poll Telegram,
restart the task manually, reset budgets, or send any email.

The first attempt is preserved as a failure. After repair,
`tests/check_service_message_restart.py` watches a fresh owner reply task and
force-stops the verified service. It retains handles for the old process tree
and measures automatic recovery without any manual task start. Process-start
latency and later plugin/phone readiness are separate measurements. The initial
three-minute observer readiness window proved too short; the actual ready
event from the journal is recorded even when it arrives later.

On a restart event the agent can review its saved context, but shell commands,
delegation, schedule changes, memory writes and email sends are unavailable.
This prevents a model from turning a recovery review into an approval request
to repeat interrupted work. A fresh owner event enables normal approved work.

For a later overnight run, verify `/status`, run `python night_report.py --start`
from the harness, then invoke `service/install-night-report.ps1`. The report
task reads the private start metadata and runs once the following morning at
08:15 local time. It makes no network or model calls. This assignment's current
window is already initialized; starting a second one refuses to overwrite it.

The first overnight attempt failed its scheduled wake after AC was lost. The
current replacement is explicitly daytime, beginning November 3 at 10:57:49
and ending no earlier than 18:57:49. The report task is scheduled for 18:58.
