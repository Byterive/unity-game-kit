---
title: Android builds
summary: How to set up, build, install and sign __NAME__ for Android, from a development APK on your phone to a release bundle for Google Play.
keywords: [android, apk, aab, keystore, adb, google play, build]
status: draft
updated: __DATE__
platform: android
---

# Android builds

## One-time setup

1. **Android module.** Unity Hub > Installs > <editor version> > gear > Add modules > **Android Build Support**, with **OpenJDK** and **Android SDK & NDK Tools** ticked.
2. **Phone.** Settings > About phone > tap **Build number** seven times. Then Developer options > turn on **USB debugging**. Plug it in and accept the "Allow USB debugging" prompt.
3. **Settings.** The `android` section of `automation/config.json` is applied before every build:

| Field | Now | Meaning |
|---|---|---|
| `productName` | __NAME__ | Name under the icon |
| `companyName` | empty (left as is) | Shown in Player Settings only |
| `packageId` | empty | Empty means development builds use `com.__LOWER__.dev`; release builds refuse to run. It can't change after the first Play upload, so set it once the name is final |
| `version` | 0.1.0 | Version players see |
| `versionCode` | 1 | Must go up by at least 1 for every Play upload |

Every build also sets portrait, IL2CPP and ARM64 (Google Play requires 64-bit). To apply them without building: **__NAME__ > Automation > Apply Android Player Settings**.

## Development APK on your phone

- Editor open: **__NAME__ > Automation > Build Android APK**.
- Editor closed: `powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method BuildAndroid`.
- Output: `Builds\Android\__ID__.apk` (development build). Log: `automation\logs\BuildAndroid.log`.
- Install and start it: `powershell -ExecutionPolicy Bypass -File automation\scripts\install_apk.ps1`. Exit code 2 means no phone was ready.

`/build-android` runs these steps for you.

## Release bundle for Google Play

1. **Make an upload key once**, outside the repo, and back it up (if it is lost, Google Play support must reset the upload key):
   ```
   & "C:\Program Files\Unity\Hub\Editor\<editor version>\Editor\Data\PlaybackEngines\AndroidPlayer\OpenJDK\bin\keytool.exe" -genkeypair -v -keystore <keys folder outside the repo>\__LOWER__-upload.keystore -alias upload -keyalg RSA -keysize 2048 -validity 10000
   ```
   Or use Player Settings > Publishing Settings > Keystore Manager.
2. **Tell the build where it is.** In the PowerShell window you build from (passwords stay out of the project and out of git):
   ```
   $env:__ENV___KEYSTORE = "<keys folder outside the repo>\__LOWER__-upload.keystore"
   $env:__ENV___KEY_ALIAS = "upload"
   $env:__ENV___KEYSTORE_PASS = "<keystore password>"
   $env:__ENV___KEY_PASS = "<key password, if different>"
   ```
   For the menu item, set them with `setx` instead and restart Unity Hub (this stores them in your Windows user profile).
3. Set `packageId`, raise `versionCode`, then run `run_unity.ps1 -Method BuildAndroidRelease` (or **Build Android Release (AAB)**).
4. Output: `Builds\Android\__ID__-<version>.aab`. Upload it in Play Console > Testing > Internal testing. The build clears the keystore path from Player Settings afterwards.

## When a build fails

Read the log from the end and fix the first error. Usual causes: Android module missing, SDK or NDK path not set (Preferences > External Tools), package id, or a missing keystore variable.
