<#
Nightly job: run the Edit Mode tests, then the game's own content check (contentCheckMethod in config.json, if set), then (optionally) build the Android APK.
Skips quietly if the Unity Editor has the project open.

Register once (runs every day at 02:00):
  schtasks /create /tn "__ID__ Nightly" /sc daily /st 02:00 /tr "powershell -ExecutionPolicy Bypass -File \"<project folder>\automation\scripts\nightly.ps1\""

Optional: add -WithClaude to have Claude Code read the report and write a short summary with suggested fixes
(uses your Claude plan; needs the claude command on PATH).
#>
param([switch]$Build, [switch]$WithClaude)

$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$config = Get-Content (Join-Path $root "automation\config.json") -Raw | ConvertFrom-Json
$lock = Join-Path (Join-Path $root $config.unityProject) "Temp\UnityLockfile"
if (Test-Path $lock) {
    Write-Host "Unity Editor has the project open; skipping nightly run."
    exit 0
}

& (Join-Path $PSScriptRoot "run_unity.ps1") -Method Tests
$tests = $LASTEXITCODE

$levels = 0
if ($config.contentCheckMethod) {
    & (Join-Path $PSScriptRoot "run_unity.ps1") -Method $config.contentCheckMethod
    $levels = $LASTEXITCODE
}

if ($Build) {
    & (Join-Path $PSScriptRoot "run_unity.ps1") -Method BuildAndroid
}

if ($WithClaude) {
    Push-Location $root
    claude -p "Read automation/reports/tests_latest.xml and any new report in automation/reports. Write automation/reports/summary_latest.md: what changed, what needs attention and one suggested fix for each. Do not edit any other file."
    Pop-Location
}
if ($tests -ne 0) { exit $tests }
exit $levels
