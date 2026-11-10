---
name: game-setup
description: Set up a new or existing Unity game project with the unity-game-kit (Editor build and check scripts, Android pipeline, local ComfyUI art pipeline, docs and git). Use when the user starts a new Unity game, wants to add the kit to an existing one, or says "set up this project".
---

# /game-setup: from empty folder to first build

The kit's files are next to this skill: templates in `../../templates`, scripts in `../../scripts` (relative to this skill's base directory). Work from the repo root: the folder that holds (or will hold) `Unity/`.

Ask only what you can't find out, and keep every answer in `gamekit.json` so no session asks again.

## 1. Look before asking

- Is this a git repo? Is there a `Unity/` folder with `ProjectSettings/`? Or a Unity project at the root itself (then ask once whether to keep it there; the kit expects `Unity/`, set `unityProject` in `gamekit.json` and `automation/config.json` to `.` if they keep it).
- Is there already a `gamekit.json`? Then this is a re-run: skip to step 4 and only fill gaps.
- Any design docs, a README or a CLAUDE.md? Read them for the game's name and platforms.

## 2. Ask (one message, defaults marked)

1. Game name (display name). The C# id is made from it (`My Game` -> `MyGame`).
2. Platforms: Android first (default), iOS later.
3. Orientation: portrait (default) or landscape.
4. Art: local ComfyUI (default), or none.
5. 2D modules to turn on (default none): optional `2d-camera`, `2d-audio`, `2d-shaders`, `2d-physics-tuning`, `2d-ai-pathing`, `2d-procedural`; and at most one genre: `genre-puzzle`, `genre-platformer`, `genre-tower-defense`, `genre-roguelike`, `genre-card`. The core 2D skills are always on.
6. No Unity project yet: create one with `/unity:new-unity-project` if the Unity plugin is installed, else Unity Hub > New project > Universal 2D (or 3D), location = this folder, name `Unity`.

## 3. Apply the kit

1. `git init` if there is no repo; first commit of whatever exists.
2. If the kickoff plugin is installed, run `/kickoff:bootstrap` with profile `unity` (docs, budgets, PROJECT_STATUS.md, hooks). Otherwise say once that it adds docs and budgets, and go on.
3. `python ../../scripts/apply_template.py --root . --name "<name>" --dry-run`, show the user what will be written and kept, then run it without `--dry-run`. It never overwrites.
4. Merge what it printed as `claude_section` into `CLAUDE.md` (create it if missing). For each file listed as "kept", compare with the template and merge only what is missing, asking before changing anything the user wrote.
5. Write the answers into `gamekit.json` (`platforms`, `orientation`, `art`, `modules`) and `automation/config.json` (`android.productName`; `packageId` stays empty until the name is final).
6. Commit in small steps: kit Editor scripts; automation; gitignore and CLAUDE.md; gamekit.json.

## 4. Doctor

Run `/game-doctor`. Walk the user through the first missing item, then the next, re-running the doctor after each. The usual order: Unity editor and Android module, packages (ugui, test framework), open Unity once so the scripts compile, scene in Build Settings, Python packages, ComfyUI and checkpoint, Unity CLI.

Done when the doctor shows no MISSING items and the first development APK runs on the phone (`/build-android`).
