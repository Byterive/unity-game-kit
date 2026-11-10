---
name: build-android
description: Build the game's Android APK and install it on the user's phone over USB for local review, or a signed release bundle for Google Play. Use when the user wants to try the game on their phone, needs a build to share, or asks for a Play Store build.
---

# /build-android: APK on the phone

Read `gamekit.json` at the repo root first: `name` is the game's menu root (`<name>/Automation/...`), `id` its C# namespace and folder (`Unity/Assets/<id>`), `envPrefix` the prefix of its environment variables. If there is no `gamekit.json`, run `/game-setup` first.

Setup, settings and signing are in `automation/android-builds.md`. Player Settings come from the `android` section of `automation/config.json`; change them there, not in ProjectSettings.asset.

1. Run `/check` first; do not build a broken game.
2. Build a development APK:
   - Editor **closed**: `powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method BuildAndroid`
   - Editor **open**: ask the user to use **<name> > Automation > Build Android APK**, or with the Unity CLI: `unity command eval "<id>.EditorTools.Automation.BuildAndroidMenu(); return 0;"`.
   The APK goes to `Builds/Android/<id>.apk`. If it fails, read `automation/logs/BuildAndroid.log` (or the Editor console) from the end and fix the first error.
3. Install: `powershell -ExecutionPolicy Bypass -File automation\scripts\install_apk.ps1`. Exit code 2 means no phone is ready; tell the user to plug it in with USB debugging on and accept the prompt.
4. Reply with the APK size and whether it was installed. If no phone is connected, say where the APK is.

Release bundle (only when the user asks for a Play build): needs `android.packageId` set and the `<envPrefix>_KEYSTORE*` variables in the user's shell. Ask the user to raise `versionCode`, then run `run_unity.ps1 -Method BuildAndroidRelease`. Never write keystore passwords into any file.
