---
name: store-shots
description: Capture and frame store screenshots of the game for Google Play and the App Store. Use when the user asks for store screenshots, marketing images or a feature graphic.
---

# /store-shots: screenshots for the stores

Read `gamekit.json` at the repo root first: `name` is the game's menu root (`<name>/Automation/...`), `id` its C# namespace and folder (`Unity/Assets/<id>`), `envPrefix` the prefix of its environment variables. If there is no `gamekit.json`, run `/game-setup` first.

1. Agree on 4 to 6 moments with the user (for example: the first minute of play, a hard moment, a win screen, a menu or map, a special mode). Suggest five that fit this game.
2. For each moment, with the Editor open: set the Game view or Device Simulator to a tall phone (1080 x 1920 or 1290 x 2796). Enter Play Mode with the menu item `<name>/Automation/Enter Play Mode` (through `unity command eval` and `EditorApplication.ExecuteMenuItem`, as in the `check` skill, or ask the user to click it). Get to the moment (load the right level or state, drive input through `eval` if needed), then call `<id>.EditorTools.Checks.Screenshot("<moment>", 2)` through `eval`, or the menu item `<name>/Automation/Take Screenshot`. PNGs land in `automation/reports/screenshots/`.
3. Frame them with Pillow in a short script under `automation/scripts/` (keep it for next time): background from the art bible palette, the screenshot inset with rounded corners, one caption of 2 to 5 words on top in a bold font.
4. Save to `StoreAssets/<date>/` at the store sizes: Google Play phone 1080 x 1920, App Store 6.9" 1290 x 2796. Open the folder for the user.
5. Captions should sell the idea, for example a 2 to 5 word promise of the core fun, the hook, and the amount of content.
