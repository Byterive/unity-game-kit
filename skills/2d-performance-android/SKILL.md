---
name: 2d-performance-android
description: Use when profiling or optimizing a 2D Unity game, or preparing an Android release build (IL2CPP, ARM64, AAB, keystore).
---

# 2D performance and Android release

## Performance
- Profile a development build on a real device; Editor numbers lie. Find the single biggest bottleneck (CPU vs GPU), fix it, re-measure.
- Budget 16.7 ms at 60 fps, 33 ms at 30 fps; leave thermal headroom.
- Pool frequently spawned objects (tiles, particles, popups). Avoid per-frame allocations.
- Sprite Atlases per screen to cut draw calls; ASTC textures on Android; watch texture memory; Read/Write off.
- Set `Application.targetFrameRate` deliberately with vSync off.
- Prefer algorithmic fixes over micro-optimizations; set asset budgets so gains hold.

## Android release
Building and signing is `/build-android` (APK for the phone, signed bundle for Play); this skill only keeps the rules in mind.
- IL2CPP and ARM64 are required for Play; ship an AAB, use an APK only for local tests.
- Play also sets a minimum target API level for new apps and updates. As of 2026-11-04 it is API 36 (Android 16) since 2026-08-31. It rises every year, so check the current number on Google's "Target API level requirements" page before a release. Native code may also need 16 KB page-size support; check the same page.
- Release minify/strip on; add `link.xml` if stripping breaks reflection.
- Keystore and passwords stay outside the repo; back them up. Never commit them.
- Launch the built output on a device before calling it done.
- Personal Play accounts created after 2023-11-13 must run a closed test with at least 12 testers opted in for 14 days before they can ask for production access. Check Play Console for the current rule.
