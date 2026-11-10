---
name: 2d-art-pipeline
description: Use when planning, validating or importing 2D game art (sprites, icons, UI, tiles) into Unity. Generating art with ComfyUI is /asset and /art-compare.
---

# 2D art pipeline

Generation is done by `/asset` (one asset, with options and your pick) and `/art-compare` (models and LoRAs on one prompt); the style and palette live in `automation/art-bible.md`. This skill is the checklist around them.

- Style bible first: palette, outline weight, lighting, silhouette rules, reference images. Reuse the same references for every asset so the set stays cohesive.
- Without generated art, use licensed assets or greybox placeholders. Record the model and licence (commercial-use status) per asset set.
- Before import: exact dimensions and frame counts; real alpha (no baked backgrounds, labels or mockup chrome); no clipped content; stable pivots; consistent scale between characters.
- Pixel art: enforce the grid and palette; point filtering; no compression artifacts.
- Tilesets: repair seams; test a repeated 3x3 tiling.
- Icons: view at the smallest in-game size; the silhouette must still read.
- Optional scripted checks (Pillow): size, alpha, max colours, contact sheet.
- Unity import: Sprite Mode and Pixels Per Unit consistent; Sprite Atlas per screen; per-platform compression; Read/Write off.
- Keep sources (PSD, ComfyUI recipes) outside Assets; commit only final imports; do not commit huge generated batches.
