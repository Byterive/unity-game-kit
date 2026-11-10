---
name: 2d-pack-index
description: Use at the start of any 2D Unity game task to see which optional 2D modules (camera, audio, shaders, physics, AI pathing, procedural, one genre) this game has turned on, and load only those.
---

# 2D pack index

The seven core skills (`2d-code-hygiene`, `2d-game-feel`, `2d-ui-touch-mobile`, `2d-performance-android`, `2d-save-systems`, `2d-art-pipeline`, `2d-level-pacing-prototype`) are always available. The rest are modules in the `modules/` folder next to this file, loaded only when the game turns them on.

1. Read `ProjectSettings/ProjectVersion.txt` (in the Unity project folder) and keep that version's APIs; do not migrate unless asked.
2. Read `gamekit.json` at the repo root, key `modules` (a list of names; empty or missing means none).
3. For each name listed, read `modules/<name>.md` next to this file and use it. At most one `genre-*` module per game; if two are listed, ask which one.
4. If the task needs a module that is not listed, say so and ask before adding it to `modules` in `gamekit.json`.

Modules: optional `2d-camera`, `2d-audio`, `2d-shaders`, `2d-physics-tuning`, `2d-ai-pathing`, `2d-procedural`; genre `genre-puzzle`, `genre-platformer`, `genre-tower-defense`, `genre-roguelike`, `genre-card`.

Numbers in these notes (touch sizes, Play requirements, timings) change over time; re-check them against current Unity and Google Play docs when a release depends on them.
