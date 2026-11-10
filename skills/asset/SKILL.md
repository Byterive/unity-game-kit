---
name: asset
description: Make or redo a game art asset (block, background, icon) with the local ComfyUI, show options for review, iterate on the user's pick, and put the approved one into the Unity project. Use when the user asks for new art, art options, or changes to an existing sprite.
---

# /asset: art from idea to in-game, all local

Read `gamekit.json` at the repo root first: `name` is the game's menu root (`<name>/Automation/...`), `id` its C# namespace and folder (`Unity/Assets/<id>`), `envPrefix` the prefix of its environment variables. If there is no `gamekit.json`, run `/game-setup` first.

The user only does three things: asks, picks, approves. You do the rest. Never put an asset into the Unity project until the user has said which option is final.

## Before the first run in a session

1. Read `automation/art-bible.md` (style and palette) and `automation/asset-types.json` (sizes, prompt templates, target paths).
2. Check ComfyUI is up: `python automation/scripts/comfy_run.py --help` works and `http://127.0.0.1:8188/system_stats` answers (use `curl -s`). If ComfyUI is not running, tell the user to start ComfyUI Desktop and stop.
3. Check `automation/config.json` `checkpoint` matches a model the user has. If unsure, ask ComfyUI: `curl -s http://127.0.0.1:8188/object_info/CheckpointLoaderSimple` lists installed checkpoints.

## 1. Brief, then prompt

The user can describe the asset in as much plain language as they like, and may drop reference images into `automation/refs/`. Turn that into a brief before prompting:

1. Write `ArtReview/<type>_<name>/brief.md`: subject, silhouette/shape, material, main colour (from the art bible palette, with hex), lighting, camera/view, mood, must-have details, and an avoid-list. Keep the user's own words where they are specific. Reuse and update this brief on every later version.
2. Compress it into the positive prompt: most important words first, under about 60 words in total (SDXL reads 75-token chunks and weights early words most). Weight the one or two things that matter most, for example `(castle tower symbol:1.2)`. End with the art bible's style line. Put the avoid-list into `--negative`.
3. Show the user the brief in two or three lines only when it adds something they didn't say; otherwise just generate.

## 2. Generate options

Turn the request into: `--type` (sprite, background, icon, or a type you add to asset-types.json), `--name` (short, e.g. `hero`), and `--subject` (a few concrete words: material, colour from the palette, symbol or shape). Default 4 options.

```
python automation/scripts/comfy_run.py --type sprite --name hero --subject "red gem with a star symbol" --count 4
```

Pass the prompt from the brief with `--prompt "<prompt>"` and the avoid-list with `--negative "<terms>"`; `--subject` stays a short label.

Before showing the sheet, look at it yourself against the brief. If an option clearly misses (wrong shape, text in the image, cropped), say so, and if all four miss, rerun once with a reworded prompt before showing anything. Then open the contact sheet so the user sees it: `start "" "<contact path>"` (Windows), and reply with one line per option only if something stands out. Say: "Pick one (for example v1 B), say what to change, or ask for fresh options."

## 3. Iterate

- "B but warmer / thicker outline / less shiny": update the brief, then rerun with `--source ArtReview/<type>_<name>/<version>/<letter>.png`, the subject updated with the change, `--denoise 0.35` for small tweaks, `0.5` for clear changes, `0.65` for big ones.
- "fresh options" or "none of these": rerun without `--source`, rewording the subject. Mention what you changed.
- "same as B but for bishop": reuse B's seed from `meta.json` with `--seed` and a new `--name` and subject, so the set stays consistent.

Each run makes a new version folder; never delete earlier ones.

## 4. Approve and integrate

Only after the user names the final option (for example "final v2 B"):

1. `git status` must be clean or only contain this asset's earlier work; if not, ask before going on. Create a branch: `git checkout -b art/<type>-<name>` (skip if not a git repo and say so).
2. Finalize: `python automation/scripts/finalize_asset.py --type <type> --name <name> --pick <file>`. It removes the background, trims, resizes, backs up the old file and writes the PNG to the target path.
3. If the target is a new file the game does not load yet (for example a new icon), wire it in the code (find how the game loads sprites, for example `Resources.Load` by name) and say what you changed.
4. Unity: if the Editor is open, the asset imports automatically. Run the tests, enter Play Mode and take a screenshot the way the `check` skill does (steps 2 and 4), look at the screenshot, and check the asset looks right at game size. If the Editor is closed, tell the user to open it and press Play.
5. Commit: `git add -A && git commit -m "Art: <type> <name> from <version> <letter>"`.
6. Reply with the screenshot path, what was replaced and the backup path, and how to undo (`git checkout main` or revert the commit).

## Batch sets

For "make the whole piece set": generate one block first, get it approved, then generate the others with the approved seed and the same wording pattern, and show all of them on one contact sheet before finalizing any.
