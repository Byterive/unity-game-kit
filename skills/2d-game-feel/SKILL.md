---
name: 2d-game-feel
description: "Use when adding juice to a 2D game: feedback stacking, hit-stop, camera shake, easing, squash and stretch, with reduce-motion options."
---

# 2D game feel (juice)

Adds polish to an existing mechanic; it does not implement the mechanic.

- Stack 2-3 feedback channels per event first (scale pop, particles, sound, flash); add more only until the event reads clearly. A strong hit is 5-8 small responses within ~100 ms.
- Pop tween ~0.18 s with overshoot easing. Squash and stretch preserves volume (scale x up, y down).
- Hit-stop 0.05-0.12 s, using unscaled time/real-time waits, triggered once per impact (never stack).
- Camera shake: a decaying "trauma" value (decay ~1.2/s), squared so small hits barely move; smooth noise not per-frame random; shake the camera, not the simulated bodies.
- Ease nearly all motion; everything returns to rest.
- Scale feedback by importance with small/medium/large presets so big moments stand out.
- Accessibility: offer reduce-shake and reduce-flash settings; never flash faster than 3 Hz; feedback must never block or delay input.

Unity notes: tweens via a tween library or coroutines with `AnimationCurve`; hit-stop via `Time.timeScale` plus `WaitForSecondsRealtime`; shake via Cinemachine impulse or a camera-offset hook.

Verify: trigger the event repeatedly; feedback decays, nothing gets stuck, input still registers.
