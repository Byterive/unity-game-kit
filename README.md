# unity-game-kit

The same Unity setup every time, and it tells you what is missing.

Version 0.2.0 · MIT · Works with Claude Code

## What it does

We built unity-game-kit to set up a Unity game project the same way every time and then check what is still missing. It adds Editor build and check scripts, an Android build and install pipeline, a local ComfyUI art pipeline with model comparison, seven 2D game skills with optional modules, and a doctor that names the next missing step.

Scope: Windows, Unity 6, Android.

## Install

```
/plugin marketplace add Byterive/kit
/plugin install unity-game-kit@byterive-kit
```

Pick **project** scope inside each game. After a new version is released: `/plugin marketplace update byterive-kit`.

## What you get

| skill | what it does | result |
|---|---|---|
| `/game-setup` | Asks name, platforms, orientation, art style and 2D modules; copies the kit; runs the doctor | Editor scripts, `automation/`, `gamekit.json`, `.gitignore` lines; existing files are never overwritten |
| `/game-doctor` | Checks the real project: Unity modules, packages, kit scripts, scene, tests, Unity CLI, Python, ComfyUI, Android settings | a table and the next missing step |
| `/check` | Compile errors, tests, level check, play-mode screenshot | pass or fail plus a screenshot |
| `/content-check` | Runs the game's own validator, if it has one | problems found, or clean |
| `/asset` | Art brief, ComfyUI options, you pick, iterate, the approved asset goes into the project | a placed asset |
| `/art-compare` | Checkpoint, LoRA and strength grid on one fixed prompt | labelled grids and a pick |
| `/build-android` | Development APK over USB, or a signed AAB for Google Play | an installed build or a bundle |
| `/store-shots` | Captures and frames store screenshots and the feature graphic | store-ready images |

**2D skills:** `2d-code-hygiene`, `2d-game-feel`, `2d-ui-touch-mobile`, `2d-performance-android`, `2d-save-systems`, `2d-art-pipeline` and `2d-level-pacing-prototype` are always on. `2d-pack-index` loads the optional modules a game lists in `gamekit.json` (camera, audio, shaders, physics tuning, AI pathing, procedural, and at most one genre). The Google Play figures in the pack are dated 2026-11-04; check them before you release.

On session start, a project with a `gamekit.json` gets one line if setup items need attention. More in the [how-to](https://github.com/Byterive/kit/blob/main/docs/howto/02-unity-game-kit.md).

## Needs and limits

- Windows, Unity 6, Python 3, and an Android phone for builds.
- Art generation needs a local ComfyUI and models you download yourself under their own licences; `reference/comfyui-models.md` lists models for a 12 GB GPU and has a licences section.
- Version 1 covers Windows and Android only.

## Tests

```
python scripts/test_modules.py
```

## Licence

License: MIT. Copyright (c) 2026 Junaid Iqbal (Byterive).

Unity, ComfyUI, Android and Google Play are trademarks of their owners; this project is not affiliated with them.

*Independent project by Byterive. Not affiliated with or endorsed by Anthropic.* · [byterive.com](https://byterive.com)
