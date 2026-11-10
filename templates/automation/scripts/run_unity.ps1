<#
Runs a __NAME__ editor command headless (Unity batch mode).
The Unity Editor must be CLOSED for this project, because Unity locks an open project.
While the Editor is open, use the __NAME__ > Automation menu or the Unity CLI (unity command eval) instead.

  powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method BuildAndroid
  powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method BuildAndroidRelease
  powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method ApplyPlayerSettings
  powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method <YourMethod> -Extra "-someArg"
  powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method Tests   (Edit Mode tests -> automation\reports\tests_latest.xml)
#>
param(
    [Parameter(Mandatory = $true)][string]$Method,  # BuildAndroid, BuildAndroidRelease, ApplyPlayerSettings, Tests, or any static method on Automation
    [string]$Extra = ""
)

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$config = Get-Content (Join-Path $root "automation\config.json") -Raw | ConvertFrom-Json
$project = Join-Path $root $config.unityProject

$unity = $config.unityEditor
if (-not $unity) {
    # Prefer the editor version the project was saved with, else the newest Unity 6 from Unity Hub.
    $version = (Select-String -Path (Join-Path $project "ProjectSettings\ProjectVersion.txt") -Pattern "m_EditorVersion: (\S+)").Matches[0].Groups[1].Value
    $exact = "C:\Program Files\Unity\Hub\Editor\$version\Editor\Unity.exe"
    if (Test-Path $exact) { $unity = $exact }
    else {
        $candidates = Get-ChildItem "C:\Program Files\Unity\Hub\Editor\6*\Editor\Unity.exe" -ErrorAction SilentlyContinue |
            Sort-Object { $_.Directory.Parent.Name } -Descending
        if (-not $candidates) { throw "Unity $version not found. Set unityEditor in automation\config.json to the full path of Unity.exe." }
        $unity = $candidates[0].FullName
        Write-Host "Unity $version not found; using $unity"
    }
}

$logDir = Join-Path $root "automation\logs"
New-Item -ItemType Directory -Force -Path $logDir | Out-Null
$log = Join-Path $logDir "$Method.log"

if ($Method -eq "Tests") {
    # Unity's own test runner flags; -runTests quits by itself, so no -quit.
    $results = Join-Path $root "automation\reports\tests_latest.xml"
    New-Item -ItemType Directory -Force -Path (Split-Path $results) | Out-Null
    $unityArgs = @("-batchmode", "-nographics", "-projectPath", "`"$project`"", "-runTests", "-testPlatform", "EditMode",
              "-testResults", "`"$results`"", "-logFile", "`"$log`"")
} else {
    $unityArgs = @("-batchmode", "-nographics", "-quit", "-projectPath", "`"$project`"",
              "-executeMethod", "__ID__.EditorTools.Automation.$Method", "-logFile", "`"$log`"")
}
if ($Method -like "BuildAndroid*") { $unityArgs += @("-buildTarget", "Android") }
if ($Extra) { $unityArgs += $Extra.Split(" ") }

Write-Host "Running $Method with $unity (log: $log)"
$p = Start-Process -FilePath $unity -ArgumentList $unityArgs -Wait -PassThru -NoNewWindow
Write-Host "$Method finished with exit code $($p.ExitCode)"
if ($p.ExitCode -ne 0) {
    Write-Host "Last log lines:"
    Get-Content $log -Tail 40
}
exit $p.ExitCode
