---
name: art-compare
description: Compare ComfyUI checkpoints, LoRAs and LoRA strengths on one fixed prompt and pick the best combination for the game's art. Use when the user wants to try models, checkpoints or LoRAs, or asks which model makes the best assets.
---

# /art-compare: find the best model combination

Same prompt, same seeds, only the model changes, so the grid shows the model and nothing else.

1. **Check ComfyUI** is up (`curl -s http://127.0.0.1:8188/system_stats`). List what is installed:
   `curl -s http://127.0.0.1:8188/object_info/CheckpointLoaderSimple` and `.../object_info/LoraLoader`.
   Read `automation/model-settings.json` for each file's family and recommended steps, CFG, sampler and scheduler. Files missing from it: ask the user or look up the model page, then add them.
2. **Write the matrix** in `automation/compare/<asset>-round<N>.json` (see `automation/compare/example.json`) from what the user said. Plain words like "all SDXL checkpoints with the icon LoRA at two strengths" become the lists.
3. **Run in rounds**, never everything at once:
   - Round 1: checkpoints only (`"loras": [null]`), 2 seeds. The user picks the top 3.
   - Round 2: LoRAs on those 3 (include `null` as the baseline). The user picks the top 2.
   - Round 3: strengths and steps on the winners.
4. Always `--dry-run` first and tell the user the image count and rough time (about 15 to 25 seconds per 1024 px SDXL image on an RTX 3060; Lightning or Turbo models much less). Over about 60 images, ask before running.
5. Run: `python automation/scripts/compare_models.py automation/compare/<file>.json`. Interrupted runs continue where they stopped.
6. Open the grids (`start "" "<grid path>"`) and look at them yourself: say which rows best match the art bible (clean shape at small size, palette colour, no text or artefacts). The user decides.
7. **Save the winner**: set `checkpoint`, `lora`, `loraStrength`, `steps`, `cfg`, `sampler`, `scheduler` in `automation/config.json`, add a line to `automation/art-bible.md` under a "Model" heading with the grid path, and commit both.

The built-in workflow loads checkpoints (SD 1.5, SDXL, Pony, Illustrious, all-in-one files). For FLUX.2, Z-Image or GGUF models, ask the user to build one working workflow in ComfyUI, title its prompt node "Positive", export it with Workflow > Export (API) into `automation/comfy/`, and set `"workflow"` in the matrix; the script then swaps the model file, prompt and seed. Model downloads and licenses: the plugin's `reference/comfyui-models.md` (next to this skill: `../../reference/`). Before an asset ships, check its model's license there.
