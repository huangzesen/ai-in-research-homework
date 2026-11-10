[CmdletBinding()]
param([Parameter(Mandatory=$true)][string]$UvDirectory, [switch]$Check)
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$pythonPath = Join-Path $repoRoot '.venv\Scripts\python.exe'
$runnerPath = Join-Path $repoRoot 'service_runner.py'
$launchArguments = @('-u','-B',('"' + $runnerPath + '"'),'--uv-dir',('"' + $UvDirectory + '"'))
if ($Check) { $launchArguments += '--check' }
try {
    $process = Start-Process -FilePath $pythonPath -ArgumentList $launchArguments -WorkingDirectory $repoRoot -WindowStyle Hidden -PassThru
    $process.WaitForExit()
    $process.Refresh()
    exit $process.ExitCode
} catch {
    $logDirectory = Join-Path $repoRoot 'logs'
    $null = New-Item -ItemType Directory -Path $logDirectory -Force
    Add-Content -LiteralPath (Join-Path $logDirectory 'service-stderr.log') -Value ('Service wrapper failed: ' + $_.Exception.GetType().Name) -Encoding UTF8
    exit 1
}
