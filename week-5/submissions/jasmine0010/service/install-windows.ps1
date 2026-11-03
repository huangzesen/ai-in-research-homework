param([switch]$Start)
$ErrorActionPreference = 'Stop'
$agentRoot = [System.IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pythonPath = Join-Path $agentRoot '.venv\Scripts\pythonw.exe'
$entryPath = Join-Path $agentRoot 'service_runner.py'
$taskName = 'JasminesAgent-AlwaysOn'
foreach ($requiredPath in @($pythonPath, $entryPath, (Join-Path $agentRoot '.env'))) {
    if (-not (Test-Path -LiteralPath $requiredPath -PathType Leaf)) { throw 'Service prerequisites are missing; run uv sync and configure .env locally.' }
}
if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
    throw 'The service task already exists. Inspect it before replacing its definition.'
}
$ownerName = [System.Security.Principal.WindowsIdentity]::GetCurrent().Name
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument ('"' + $entryPath + '"') -WorkingDirectory $agentRoot
$trigger = New-ScheduledTaskTrigger -AtLogOn -User $ownerName
$recoveryTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddSeconds(5) -RepetitionInterval (New-TimeSpan -Minutes 1)
$principal = New-ScheduledTaskPrincipal -UserId $ownerName -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -RestartCount 999 -RestartInterval (New-TimeSpan -Minutes 1) -ExecutionTimeLimit ([TimeSpan]::Zero) -MultipleInstances IgnoreNew -StartWhenAvailable -Priority 5 -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
$task = New-ScheduledTask -Action $action -Trigger @($trigger, $recoveryTrigger) -Principal $principal -Settings $settings -Description 'Week 5 event-driven research agent; phone controls and budgets enforced in code. Minute recovery trigger skips starts while already running.'
Register-ScheduledTask -TaskName $taskName -InputObject $task | Out-Null
$exportPath = Join-Path $PSScriptRoot 'windows-task.local.xml'
Export-ScheduledTask -TaskName $taskName | Set-Content -LiteralPath $exportPath -Encoding Unicode
Write-Output ('Registered ' + $taskName + '; exported task definition locally.')
if ($Start) {
    Start-ScheduledTask -TaskName $taskName
    Write-Output 'Started service task.'
}
