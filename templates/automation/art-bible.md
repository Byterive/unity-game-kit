---
title: Art bible
summary: Style line, palette, model and rules the /asset skill uses to build every ComfyUI prompt for __NAME__.
keywords: [art, style, comfyui, prompts, asset]
status: draft
updated: __DATE__
---

# __NAME__ art bible

Edit this file to change the look of every generated asset. The `/asset` skill reads it before each run and builds the `{style}` part of the prompt from the **Style line**. Keep the style line under about 30 words: SDXL pays most attention to the first words of a prompt.

## Style line

clean stylized mobile game art, soft studio lighting from top left, bold readable shapes

## Palette

| Role | Material | Main colour |
| --- | --- | --- |
| Main object | | |
| Accent | | |
| Background | | |

## Model

Set by `/art-compare`: the winning checkpoint, LoRA and settings, with the grid that chose them.

## Rules

- Every game object is readable at its smallest on-screen size: one strong silhouette, no fine detail.
- Objects differ by shape or symbol, not only colour (colour-blind players).
- Light comes from the same side on every asset.
- No letters or numbers in generated art; the game draws text itself.
- Keep the same seed family for one set so the pieces look related.
