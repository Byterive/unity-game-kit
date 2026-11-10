---
name: check
description: "Check that the game still works after a change: compile errors, tests, level verification, and a play-mode screenshot. Use before saying any change is done, or when the user asks to check, test or review the game locally."
---

# /check: is the game still OK?

Read `gamekit.json` at the repo root first: `name` is the game's menu root (`<name>/Automation/...`), `id` its C# namespace and folder (`Unity/Assets/<id>`), `envPrefix` the prefix of its environment variables. If there is no `gamekit.json`, run `/game-setup` first.

Run what applies, in this order, and stop at the first failure to fix it.

Editor open: drive it with the Unity CLI. Run `unity status` (must show the Editor connected) and `unity command` once to see how `eval` takes code, then call the game's menu items with `UnityEditor.EditorApplication.ExecuteMenuItem("<path>")`. If the CLI isn't installed or connected, ask the user to click the same menu items under **<name> > Automation**.
Editor closed: use `automation\scripts\run_unity.ps1`.

1. **Compile and console**: read the end of `%LOCALAPPDATA%\Unity\Editor\Editor.log` (Editor open) or `automation\logs\<Method>.log` (batch). Look for `error CS`. Fix errors before anything else.
2. **Tests**:
   - Editor open: menu `<name>/Automation/Run Edit Mode Tests`, then read `automation/reports/tests_latest.json` (`passed`, `failed`, `failures`). Wait until its `finished` time is newer than when you started.
   - Editor closed: `run_unity.ps1 -Method Tests`, then read `automation/reports/tests_latest.xml` (NUnit format; the `test-run` element has `passed` and `failed`).
3. **Content**: if the game has a content check (`contentCheckMethod` in `automation/config.json`) and its data or logic changed, run `/content-check` and make sure it passes.
4. **Play** (Editor open only): menu `<name>/Automation/Enter Play Mode`, wait a few seconds, then `<name>/Automation/Take Screenshot`. The PNG lands in `automation/reports/screenshots/`. Look at it: board visible, sprites (not letters) on blocks, buttons inside the safe area. Then `<name>/Automation/Exit Play Mode`.
5. **Report** in two or three lines: what passed, what you fixed, the screenshot path.

For a phone check, use the `build-android` skill.
