---
name: 2d-ui-touch-mobile
description: "Use when building touch UI and input for a 2D Unity mobile game: uGUI scaling, safe areas, touch targets, Input System, buffering, rebinding."
---

# 2D UI, touch and input (Unity)

Check Unity version and installed packages first. Verify numbers against current docs.

## UI (uGUI)
- Canvas Scaler: Scale With Screen Size, portrait reference (e.g. 1080x1920), Match ~0.5 (1.0 for height-critical HUDs). Anchor everything.
- Apply `Screen.safeArea` to a root panel; re-apply on resolution/orientation change.
- Touch targets at least 48 x 48 dp (about 9 mm) with at least 8 dp between them; primary actions in thumb reach (lower half).
- One screen stack/manager; HUD updates via events, not polling.
- Split Canvases by update frequency; disable Raycast Target on non-interactive graphics.
- Test on the smallest and the tallest/narrowest phones.

## Input
- Input System package: one action asset, touch/pointer action, read via `performed`; unsubscribe in `OnDisable`. Active Input Handling must be New or Both.
- Grid games: `Camera.ScreenToWorldPoint` -> cell; ignore input while animating/resolving.
- Name actions, never read raw keys in gameplay. Edge vs held reads; radial deadzones on sticks.
- Input buffering: remember a press for ~0.1-0.15 s so a slightly early press still counts.
- Rebinding (PC/gamepad builds): detect conflicts and save bindings with the save system. No hover on mobile.
