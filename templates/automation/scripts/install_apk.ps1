<#
Installs the development APK on a phone connected over USB and starts the game.
The phone needs USB debugging on, and you must accept the "Allow USB debugging" prompt on it once.

  powershell -ExecutionPolicy Bypass -File automation\scripts\install_apk.ps1
  powershell -ExecutionPolicy Bypass -File automation\scripts\install_apk.ps1 -Apk Builds\Android\__ID__.apk

adb comes from "adb" in automation\config.json, then PATH, then the SDK Unity installs with Android Build Support.
#>
param([string]$Apk = "")

$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$config = Get-Content (Join-Path $root "automation\config.json") -Raw | ConvertFrom-Json
$project = Join-Path $root $config.unityProject
if (-not $Apk) { $Apk = Join-Path $root "Builds\Android\__ID__.apk" }
if (-not (Test-Path $Apk)) { throw "No APK at $Apk. Build one first: run_unity.ps1 -Method BuildAndroid" }

$adb = $config.adb
if (-not $adb) { $adb = (Get-Command adb -ErrorAction SilentlyContinue).Source }
if (-not $adb) {
    $found = Get-ChildItem "C:\Program Files\Unity\Hub\Editor\*\Editor\Data\PlaybackEngines\AndroidPlayer\SDK\platform-tools\adb.exe" -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending | Select-Object -First 1
    if ($found) { $adb = $found.FullName }
}
if (-not $adb) { throw "adb not found. Install Android Build Support in Unity Hub, or set adb in automation\config.json." }

$devices = & $adb devices | Select-Object -Skip 1 | Where-Object { $_ -match "\S+\s+device$" }
if (-not $devices) {
    Write-Host "No phone ready. Connect it over USB, turn on USB debugging and accept the prompt on the phone."
    Write-Host "APK: $Apk ($([math]::Round((Get-Item $Apk).Length / 1MB, 1)) MB)"
    & $adb devices
    exit 2
}

# The package id Unity built with, from ProjectSettings.asset (applicationIdentifier > Android).
$settings = Get-Content (Join-Path $project "ProjectSettings\ProjectSettings.asset") -Raw
$match = [regex]::Match($settings, "applicationIdentifier:\s*\r?\n(?:\s+\S+: \S+\r?\n)*?\s+Android: (\S+)")
$package = if ($match.Success) { $match.Groups[1].Value } else { "com.__LOWER__.dev" }

Write-Host "Installing $Apk ($([math]::Round((Get-Item $Apk).Length / 1MB, 1)) MB) as $package"
& $adb install -r $Apk
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
& $adb shell monkey -p $package -c android.intent.category.LAUNCHER 1 | Out-Null
Write-Host "Started $package on the phone."
