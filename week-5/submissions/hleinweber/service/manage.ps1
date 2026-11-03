[CmdletBinding()]
param(
    [ValidateSet('Prepare','Install','Update','Start','Stop','Status','Export','Uninstall','CrashTest')]
    [string]$Action = 'Prepare'
)
$ErrorActionPreference = 'Stop'
$taskName = 'ResearchAgentAlwaysOn'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$taskXml = Join-Path $PSScriptRoot ($taskName + '.xml')
$powershellPath = Join-Path $env:SystemRoot 'System32\WindowsPowerShell\v1.0\powershell.exe'
$wrapper = Join-Path $PSScriptRoot 'run.ps1'
$pythonConsole = Join-Path $repoRoot '.venv\Scripts\python.exe'
$runner = Join-Path $repoRoot 'service_runner.py'
$identity = [Security.Principal.WindowsIdentity]::GetCurrent()

function New-AgentDefinition {
    if (-not (Test-Path -LiteralPath $pythonConsole)) { throw 'Create the project venv first.' }
    $uvPath = (Get-Command uv -ErrorAction Stop).Source
    $uvDirectory = Split-Path -Parent $uvPath
    $scheduler = New-Object -ComObject 'Schedule.Service'
    $scheduler.Connect()
    $definition = $scheduler.NewTask(0)
    $definition.RegistrationInfo.Description = 'Always-on research agent. Owner-approved tools, persistent recovery and code-enforced budgets.'
    $definition.Principal.UserId = $identity.User.Value
    $definition.Principal.LogonType = 3 # InteractiveToken: no stored password.
    $definition.Principal.RunLevel = 0 # Least privilege.
    $trigger = $definition.Triggers.Create(9) # At user logon.
    $trigger.UserId = $identity.User.Value
    $trigger.Enabled = $true
    $recovery = $definition.Triggers.Create(1) # One-minute recovery trigger; IgnoreNew prevents a second instance.
    $recovery.StartBoundary = (Get-Date).AddMinutes(1).ToString('yyyy-MM-ddTHH:mm:ss')
    $recovery.Repetition.Interval = 'PT1M'
    $recovery.Repetition.StopAtDurationEnd = $false
    $recovery.Enabled = $true
    $settings = $definition.Settings
    $settings.Enabled = $true
    $settings.ExecutionTimeLimit = 'PT0S'
    $settings.RestartInterval = 'PT1M'
    $settings.RestartCount = 255
    $settings.MultipleInstances = 2 # IgnoreNew.
    $settings.StartWhenAvailable = $true
    $settings.DisallowStartIfOnBatteries = $false
    $settings.StopIfGoingOnBatteries = $false
    $settings.AllowDemandStart = $true
    $settings.Hidden = $false # Visible in Task Scheduler; launcher windows are hidden.
    $exec = $definition.Actions.Create(0)
    $exec.Path = $powershellPath
    $exec.Arguments = '-NoLogo -NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File "' + $wrapper + '" -UvDirectory "' + $uvDirectory + '"'
    $exec.WorkingDirectory = $repoRoot
    return $definition
}

function Save-TaskXml([string]$xmlText) {
    [IO.File]::WriteAllText($taskXml, $xmlText, [Text.Encoding]::Unicode)
}

function Get-AgentTask {
    Get-ScheduledTask -TaskName $taskName -TaskPath '\' -ErrorAction SilentlyContinue
}

function Assert-NoManualHost {
    $hosts = @(Get-CimInstance Win32_Process | Where-Object {
        $_.Name -match '^pythonw?\.exe$' -and $_.CommandLine -and
        $_.CommandLine -match '(agent\.py|web\.py)' -and
        ($_.CommandLine -match [regex]::Escape($repoRoot) -or $_.CommandLine -match '(?:^|\s)(agent\.py|web\.py)(?:\s|$)')
    })
    if ($hosts.Count) { throw 'Close the manual web/Telegram/always-on agent before starting the task.' }
}

switch ($Action) {
    'Prepare' {
        $definition = New-AgentDefinition
        Save-TaskXml $definition.XmlText
        Write-Output ('Prepared: ' + $taskXml)
        Write-Output ('Runs as: ' + $identity.Name + ' (logged-in user, least privilege, no stored password)')
        Write-Output ('Executable: ' + $powershellPath + ' (hidden wrapper around ' + $pythonConsole + ')')
        Write-Output 'At login plus a one-minute recovery trigger; failure retry every minute; no execution time limit.'
        Write-Output 'No task was registered or started.'
    }
    'Install' {
        if (Get-AgentTask) { throw 'Task already exists. Inspect it before changing or uninstalling it.' }
        $definition = New-AgentDefinition
        Save-TaskXml $definition.XmlText
        $scheduler = New-Object -ComObject 'Schedule.Service'
        $scheduler.Connect()
        $folder = $scheduler.GetFolder('\')
        $null = $folder.RegisterTaskDefinition($taskName, $definition, 2, $identity.Name, $null, 3, $null)
        Save-TaskXml (Export-ScheduledTask -TaskName $taskName -TaskPath '\')
        Write-Output 'Installed ResearchAgentAlwaysOn. It has not been started in this session.'
    }
    'Update' {
        $existing = Get-AgentTask
        if (-not $existing) { throw 'Install the task first.' }
        if ($existing.State -eq 'Running') { throw 'Stop the task before updating it.' }
        if ($existing.Actions.Arguments -notlike ('*' + $wrapper + '*')) { throw 'Existing task is not this checkout; refusing to replace it.' }
        $definition = New-AgentDefinition
        $definition.Settings.Enabled = $existing.Settings.Enabled
        Save-TaskXml $definition.XmlText
        $scheduler = New-Object -ComObject 'Schedule.Service'
        $scheduler.Connect()
        $folder = $scheduler.GetFolder('\')
        $null = $folder.RegisterTaskDefinition($taskName, $definition, 6, $identity.Name, $null, 3, $null)
        Save-TaskXml (Export-ScheduledTask -TaskName $taskName -TaskPath '\')
        Write-Output 'Updated the verified task definition.'
    }
    'Start' {
        if (-not (Get-AgentTask)) { throw 'Install the task first.' }
        Assert-NoManualHost
        $null = Enable-ScheduledTask -TaskName $taskName -TaskPath '\'
        Start-ScheduledTask -TaskName $taskName -TaskPath '\'
        Write-Output 'Start requested. Use Status and send /status to the bot.'
    }
    'Stop' {
        $null = Disable-ScheduledTask -TaskName $taskName -TaskPath '\'
        Stop-ScheduledTask -TaskName $taskName -TaskPath '\'
        Write-Output 'Task disabled and stopped. Start re-enables it. /stop only cancels a task inside the agent; it does not stop this service.'
    }
    'Status' {
        $task = Get-AgentTask
        if (-not $task) { Write-Output 'Task is not installed.'; break }
        $info = Get-ScheduledTaskInfo -TaskName $taskName -TaskPath '\'
        $statePath = Join-Path $repoRoot 'state\service.json'
        $state = $null
        $process = $null
        if (Test-Path -LiteralPath $statePath) {
            $state = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
            $process = Get-Process -Id $state.pid -ErrorAction SilentlyContinue
        }
        [pscustomobject]@{
            TaskName=$task.TaskName; State=[string]$task.State;
            LastRunTime=$info.LastRunTime; LastTaskResult=$info.LastTaskResult;
            NextRunTime=$info.NextRunTime; AgentPID=$state.pid;
            Phase=$state.phase; ProcessExists=[bool]$process
        } | Format-List
    }
    'Export' {
        Save-TaskXml (Export-ScheduledTask -TaskName $taskName -TaskPath '\')
        Write-Output ('Exported: ' + $taskXml)
    }
    'Uninstall' {
        $task = Get-AgentTask
        if ($task -and $task.State -eq 'Running') { throw 'Stop the task before uninstalling.' }
        Unregister-ScheduledTask -TaskName $taskName -TaskPath '\' -Confirm:$false
        Write-Output 'Task removed. Code, logs and state are preserved.'
    }
    'CrashTest' {
        $task = Get-AgentTask
        if (-not $task -or $task.State -ne 'Running') { throw 'Start the scheduled task before the crash test.' }
        $statePath = Join-Path $repoRoot 'state\service.json'
        $before = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
        if ($before.phase -ne 'ready') { throw 'Wait until the agent reports ready before testing.' }
        $target = Get-CimInstance Win32_Process -Filter ('ProcessId = ' + [int]$before.pid)
        if (-not $target -or $target.CommandLine -notmatch [regex]::Escape($runner)) { throw 'PID is not this service runner; refusing to terminate it.' }
        if ($before.root -ne $repoRoot) { throw 'Service state belongs to a different directory.' }
        $started = [DateTimeOffset]::FromUnixTimeSeconds([long][math]::Floor($before.started_at)).UtcDateTime
        if ([math]::Abs(($target.CreationDate.ToUniversalTime() - $started).TotalSeconds) -gt 15) { throw 'PID creation time does not match service startup; refusing to terminate it.' }
        $watch = [Diagnostics.Stopwatch]::StartNew()
        & taskkill.exe /PID ([string]$before.pid) /T /F
        if ($LASTEXITCODE -ne 0) { throw 'Could not terminate the verified service process tree.' }
        Write-Output 'Verified agent tree terminated. Waiting for Task Scheduler to restart it (up to 100 seconds).'
        $deadline = [DateTime]::UtcNow.AddSeconds(100)
        while ([DateTime]::UtcNow -lt $deadline) {
            Start-Sleep -Milliseconds 500
            $after = Get-Content -LiteralPath $statePath -Raw | ConvertFrom-Json
            if ($after.run_id -ne $before.run_id -and $after.phase -eq 'ready') {
                $report = [ordered]@{ old_pid=$before.pid; new_pid=$after.pid; seconds=[math]::Round($watch.Elapsed.TotalSeconds,2); ready=$true; recorded_at=[DateTime]::UtcNow.ToString('o') }
                $report | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $repoRoot 'state\service-restart-test.json') -Encoding UTF8
                $report | ConvertTo-Json
                break
            }
        }
        if ($after.run_id -eq $before.run_id -or $after.phase -ne 'ready') { throw 'No ready replacement observed. Inspect service logs and Task Scheduler result.' }
    }
}
