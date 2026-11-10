---
name: content-check
description: Run the game's own content validator (for example a level solver or data checker) and report problems. Use after changing game data or logic, before a build, or when the user asks to verify levels or content.
---

# /content-check: the game's own checks

Read `gamekit.json` (`name`, `id`) and `automation/config.json` `contentCheckMethod`.

- **No method set:** say so once, and offer to write one: a static method on `<id>.EditorTools.Automation` (in a new file under `Unity/Assets/<id>/Editor/`) that validates the game's data, writes a short Markdown report to `automation/reports/`, and in batch mode exits with code 1 when something is wrong. Add a matching menu item under `<name>/Automation/`. Then set `contentCheckMethod`, so `nightly.ps1` runs it too.
- **Editor closed:** `powershell -ExecutionPolicy Bypass -File automation\scripts\run_unity.ps1 -Method <contentCheckMethod>`, then read the newest report in `automation/reports/` and the log in `automation/logs/`.
- **Editor open:** call its menu item through `unity command eval` with `UnityEditor.EditorApplication.ExecuteMenuItem("<name>/Automation/<item>")`, or ask the user to click it.

Report in two or three lines: what was checked, what failed, and the fix you suggest. Don't change game data without the user's go-ahead.
