"""Compares checkpoints, LoRAs and LoRA strengths on one fixed prompt, and makes a labelled grid.

    python automation/scripts/compare_models.py automation/compare/rook-round1.json --dry-run
    python automation/scripts/compare_models.py automation/compare/rook-round1.json

The matrix file (JSON) says what to try; see automation/compare/example.json:
    name          folder name under ArtReview/compare/
    type          key in automation/asset-types.json (sets size and prompt template)
    subject       what to draw (goes into the type's prompt template), or
    prompt        a full positive prompt instead of the template; negative is optional
    seeds         the same seeds are used for every combination
    checkpoints   file names, or ["all"] for every checkpoint ComfyUI has
    loras         file names and/or null for "no LoRA", or ["all"]
    loraStrengths strengths to try for each LoRA (default [0.8])
    overrides     per-file settings, e.g. {"x_lightning.safetensors": {"steps": 6, "cfg": 1.5}}
    workflow      optional: an API-format workflow you exported from ComfyUI (Workflow > Export (API)),
                  for models the built-in SDXL workflow can't load (FLUX.2, Z-Image, GGUF). Title its
                  prompt nodes "Positive" (and "Negative" if it has one). The script swaps the model file
                  (unet_name or ckpt_name), the prompt text and the seed; steps and CFG stay as saved.
                  "checkpoints" then lists diffusion model files; LoRAs are not swapped.

Settings for each file come from overrides, then automation/model-settings.json, then config.json.
A LoRA is skipped on a checkpoint of another family (an SDXL LoRA on SD 1.5, say) when both families are known.
Images that already exist are kept, so an interrupted run continues where it stopped.
Output: ArtReview/compare/<name>/ with one PNG per image, results.json and grid_<n>.png sheets
(one row per combination, one column per seed).
"""
import argparse
import itertools
import json
import re
import sys
import time
from pathlib import Path

from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
import comfy_run  # noqa: E402
from contact_sheet import font  # noqa: E402

THUMB = 256
LABEL_W = 420
ROWS_PER_SHEET = 12
# Families that share the SDXL architecture; their LoRAs mostly load on each other.
SDXL_LIKE = {"sdxl", "pony", "illustrious", "noobai"}


def family_group(name):
    name = (name or "").lower()
    return "sdxl" if name in SDXL_LIKE else name


def installed(base, node, field):
    info = comfy_run.http_json(f"{base}/object_info/{node}")
    return list(info[node]["input"]["required"][field][0])


def slug(s):
    return re.sub(r"[^A-Za-z0-9]+", "-", Path(s).stem if s else "none").strip("-")[:40]


def combos(matrix, base, known):
    ckpts = matrix.get("checkpoints", ["all"])
    loras = matrix.get("loras", [None])
    if ckpts == ["all"]:
        ckpts = (installed(base, "UNETLoader", "unet_name") if matrix.get("workflow")
                 else installed(base, "CheckpointLoaderSimple", "ckpt_name"))
    if loras == ["all"]:
        loras = [None] + installed(base, "LoraLoader", "lora_name")
    strengths = matrix.get("loraStrengths", [0.8])
    out, skipped = [], []
    for ckpt, lora in itertools.product(ckpts, loras):
        cf = family_group(known.get(ckpt, {}).get("family"))
        lf = family_group(known.get(lora, {}).get("family")) if lora else ""
        if lora and cf and lf and cf != lf:
            skipped.append(f"{lora} ({lf}) on {ckpt} ({cf})")
            continue
        for strength in (strengths if lora else [None]):
            out.append((ckpt, lora, strength))
    return out, skipped


def custom_workflow(path, model, positive, negative, seed):
    wf = json.loads(Path(path).read_text(encoding="utf-8"))
    swapped = False
    for node in wf.values():
        inputs, title = node.get("inputs", {}), node.get("_meta", {}).get("title", "")
        for key in ("unet_name", "ckpt_name"):
            if key in inputs and not swapped:
                inputs[key], swapped = model, True
        for key in ("seed", "noise_seed"):
            if key in inputs and not isinstance(inputs[key], list):
                inputs[key] = seed
        if "text" in inputs and title == "Positive":
            inputs["text"] = positive
        if "text" in inputs and title == "Negative":
            inputs["text"] = negative
    if not swapped:
        raise SystemExit(f"{path} has no node with unet_name or ckpt_name to swap")
    return wf


def settings_for(ckpt, lora, cfg, known, overrides):
    s = {k: cfg.get(k) for k in ("steps", "cfg", "sampler", "scheduler")}
    for source in (known.get(ckpt, {}), overrides.get(ckpt, {}), overrides.get(lora or "", {})):
        s.update({k: v for k, v in source.items() if k in s})
    return s


def build_grids(out_dir, rows, seeds):
    sheets = []
    f, small = font(22), font(18)
    for page in range(0, len(rows), ROWS_PER_SHEET):
        chunk = rows[page:page + ROWS_PER_SHEET]
        w = LABEL_W + len(seeds) * (THUMB + 8) + 8
        h = 40 + len(chunk) * (THUMB + 8) + 8
        sheet = Image.new("RGB", (w, h), (30, 30, 34))
        d = ImageDraw.Draw(sheet)
        for j, seed in enumerate(seeds):
            d.text((LABEL_W + 8 + j * (THUMB + 8), 10), f"seed {seed}", fill=(200, 200, 200), font=small)
        for i, row in enumerate(chunk):
            y = 40 + i * (THUMB + 8)
            d.text((10, y + 10), f"{page + i + 1}. {Path(row['checkpoint']).stem[:30]}", fill=(255, 255, 255), font=f)
            lora = f"{Path(row['lora']).stem[:30]} @ {row['strength']}" if row["lora"] else "no LoRA"
            d.text((10, y + 42), lora, fill=(190, 190, 190), font=small)
            d.text((10, y + 70), f"{row['steps']} steps, cfg {row['cfg']}, {row['sampler']}", fill=(150, 150, 150), font=small)
            for j, seed in enumerate(seeds):
                p = out_dir / row["files"].get(str(seed), "")
                if p.is_file():
                    img = Image.open(p).convert("RGB")
                    img.thumbnail((THUMB, THUMB))
                    sheet.paste(img, (LABEL_W + 8 + j * (THUMB + 8), y))
        path = out_dir / f"grid_{page // ROWS_PER_SHEET + 1}.png"
        sheet.save(path)
        sheets.append(str(path))
    return sheets


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("matrix", type=Path)
    ap.add_argument("--dry-run", action="store_true", help="List the combinations and the image count, generate nothing")
    args = ap.parse_args()

    matrix = json.loads(args.matrix.read_text(encoding="utf-8"))
    cfg = common.load_config()
    settings_path = common.AUTOMATION / "model-settings.json"
    known = json.loads(settings_path.read_text(encoding="utf-8")) if settings_path.exists() else {}
    overrides = matrix.get("overrides", {})
    base = cfg["comfyUrl"].rstrip("/")
    try:
        comfy_run.http_json(f"{base}/system_stats")
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"ComfyUI is not reachable at {base} ({e}). Start ComfyUI first.")

    t = common.load_asset_types()[matrix.get("type", "sprite")]
    positive = matrix.get("prompt") or t["prompt"].format(subject=matrix["subject"], style=common.style_line())
    negative = matrix.get("negative", t["negative"])
    seeds = matrix.get("seeds", [101, 202])
    todo, skipped = combos(matrix, base, known)
    total = len(todo) * len(seeds)
    print(f"{len(todo)} combinations x {len(seeds)} seeds = {total} images")
    for s in skipped:
        print(f"  skipped (family mismatch): {s}")
    if args.dry_run:
        for ckpt, lora, strength in todo:
            print(f"  {ckpt}  {lora or 'no LoRA'}  {strength or ''}")
        return

    out_dir = common.review_dir(cfg) / "compare" / slug(matrix.get("name", args.matrix.stem))
    out_dir.mkdir(parents=True, exist_ok=True)
    rows, done, started = [], 0, time.time()
    for ckpt, lora, strength in todo:
        s = settings_for(ckpt, lora, cfg, known, overrides)
        run_cfg = dict(cfg, checkpoint=ckpt, lora=lora or "", loraStrength=strength or 0, **s)
        row = {"checkpoint": ckpt, "lora": lora, "strength": strength, **s, "files": {}}
        for seed in seeds:
            name = f"{slug(ckpt)}__{slug(lora)}__{strength or 0}__s{seed}.png"
            path = out_dir / name
            done += 1
            if not path.exists():
                if matrix.get("workflow"):
                    wf = custom_workflow(common.ROOT / matrix["workflow"], ckpt, positive, negative, seed)
                else:
                    wf = comfy_run.build_workflow(run_cfg, positive, negative, t["genWidth"], t["genHeight"], seed)
                print(f"[{done}/{total}] {ckpt} | {lora or 'no LoRA'} {strength or ''} | seed {seed}", flush=True)
                comfy_run.run_one(base, wf, path)
            row["files"][str(seed)] = name
        rows.append(row)

    sheets = build_grids(out_dir, rows, seeds)
    result = {"matrix": str(args.matrix), "positive": positive, "negative": negative, "seeds": seeds,
              "minutes": round((time.time() - started) / 60, 1), "skipped": skipped, "rows": rows, "grids": sheets}
    (out_dir / "results.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps({"folder": str(out_dir), "grids": sheets, "minutes": result["minutes"]}, indent=2))


if __name__ == "__main__":
    main()
