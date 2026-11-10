"""Generates asset options with the local ComfyUI and saves them for review.

New options (text to image):
    python automation/scripts/comfy_run.py --type sprite --name rook --subject "ruby rook tower" --count 4

Iterate on a picked option (image to image, keeps the composition):
    python automation/scripts/comfy_run.py --type sprite --name rook --subject "ruby rook tower, warmer, thicker outline" \
        --source ArtReview/sprite_rook/v1/B.png --denoise 0.45 --count 4

Each run writes ArtReview/<type>_<name>/v<N>/A.png, B.png ... plus meta.json and contact.png.
ComfyUI must be running (ComfyUI Desktop, or python main.py) at comfyUrl in automation/config.json.
"""
import argparse
import copy
import json
import random
import string
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402
import contact_sheet  # noqa: E402


def http_json(url, payload=None):
    data = None if payload is None else json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return json.loads(r.read().decode())


def upload_image(base, path: Path):
    boundary = uuid.uuid4().hex
    body = (
        f"--{boundary}\r\nContent-Disposition: form-data; name=\"image\"; filename=\"{path.name}\"\r\n"
        f"Content-Type: image/png\r\n\r\n"
    ).encode() + path.read_bytes() + f"\r\n--{boundary}\r\nContent-Disposition: form-data; name=\"overwrite\"\r\n\r\ntrue\r\n--{boundary}--\r\n".encode()
    req = urllib.request.Request(f"{base}/upload/image", data=body,
                                 headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    with urllib.request.urlopen(req, timeout=60) as r:
        info = json.loads(r.read().decode())
    return f"{info['subfolder']}/{info['name']}" if info.get("subfolder") else info["name"]


def find(wf, class_type, title=None):
    for nid, node in wf.items():
        if node["class_type"] == class_type and (title is None or node.get("_meta", {}).get("title") == title):
            return nid
    raise SystemExit(f"Workflow has no {class_type} node" + (f" titled '{title}'" if title else ""))


def add_lora(wf, lora, strength):
    ckpt = find(wf, "CheckpointLoaderSimple")
    wf["100"] = {"class_type": "LoraLoader", "_meta": {"title": "LoRA"},
                 "inputs": {"lora_name": lora, "strength_model": strength, "strength_clip": strength,
                            "model": [ckpt, 0], "clip": [ckpt, 1]}}
    for nid, node in wf.items():
        if nid == "100":
            continue
        for key, val in node["inputs"].items():
            if isinstance(val, list) and val[0] == ckpt and val[1] in (0, 1):
                node["inputs"][key] = ["100", val[1]]


def build_workflow(cfg, positive, negative, width, height, seed, source_name=None, denoise=1.0):
    name = "sdxl_img2img_api.json" if source_name else "sdxl_txt2img_api.json"
    wf = json.loads((common.AUTOMATION / "comfy" / name).read_text(encoding="utf-8"))
    wf[find(wf, "CheckpointLoaderSimple")]["inputs"]["ckpt_name"] = cfg["checkpoint"]
    wf[find(wf, "CLIPTextEncode", "Positive")]["inputs"]["text"] = positive
    wf[find(wf, "CLIPTextEncode", "Negative")]["inputs"]["text"] = negative
    ks = wf[find(wf, "KSampler")]["inputs"]
    ks.update(seed=seed, steps=cfg.get("steps", 28), cfg=cfg.get("cfg", 6.0),
              sampler_name=cfg.get("sampler", "dpmpp_2m"), scheduler=cfg.get("scheduler", "karras"), denoise=denoise)
    if source_name:
        wf[find(wf, "LoadImage")]["inputs"]["image"] = source_name
    else:
        lat = wf[find(wf, "EmptyLatentImage")]["inputs"]
        lat.update(width=width, height=height, batch_size=1)
    if cfg.get("lora"):
        add_lora(wf, cfg["lora"], cfg.get("loraStrength", 0.8))
    return wf


def run_one(base, wf, out_path: Path, timeout=600):
    client = uuid.uuid4().hex
    try:
        pid = http_json(f"{base}/prompt", {"prompt": wf, "client_id": client})["prompt_id"]
    except urllib.error.HTTPError as e:
        raise SystemExit(f"ComfyUI rejected the workflow: {e.read().decode(errors='replace')}")
    start = time.time()
    while time.time() - start < timeout:
        hist = http_json(f"{base}/history/{pid}")
        if pid in hist:
            entry = hist[pid]
            status = entry.get("status", {})
            if status.get("status_str") == "error":
                raise SystemExit(f"ComfyUI job failed: {json.dumps(status.get('messages', []))[:2000]}")
            for node_out in entry.get("outputs", {}).values():
                for img in node_out.get("images", []):
                    q = urllib.parse.urlencode({"filename": img["filename"], "subfolder": img.get("subfolder", ""),
                                                "type": img.get("type", "output")})
                    with urllib.request.urlopen(f"{base}/view?{q}", timeout=60) as r:
                        out_path.write_bytes(r.read())
                    return
        time.sleep(1.0)
    raise SystemExit(f"Timed out after {timeout}s waiting for ComfyUI job {pid}")


def next_version(folder: Path):
    n = 1
    while (folder / f"v{n}").exists():
        n += 1
    return f"v{n}"


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True, help="Key in automation/asset-types.json, e.g. sprite, background, icon")
    ap.add_argument("--name", required=True, help="Asset name, e.g. rook")
    ap.add_argument("--subject", required=True, help="What to draw, in a few words (kept in meta.json)")
    ap.add_argument("--prompt", default=None, help="Full positive prompt written from the asset brief; replaces the type's template")
    ap.add_argument("--negative", default=None, help="Extra negative terms, added to the type's negative prompt")
    ap.add_argument("--count", type=int, default=4)
    ap.add_argument("--seed", type=int, default=None, help="First seed; the rest follow it. Random if omitted")
    ap.add_argument("--source", type=Path, default=None, help="Picked option to iterate on (image to image)")
    ap.add_argument("--denoise", type=float, default=0.45, help="How far to move from --source (0.2 subtle .. 0.7 big)")
    args = ap.parse_args()

    cfg = common.load_config()
    types = common.load_asset_types()
    if args.type not in types:
        raise SystemExit(f"Unknown type '{args.type}'. Known: {', '.join(types)}")
    t = types[args.type]
    base = cfg["comfyUrl"].rstrip("/")
    try:
        http_json(f"{base}/system_stats")
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"ComfyUI is not reachable at {base} ({e}). Start ComfyUI first.")

    folder, safe = common.asset_folder(args.type, args.name, cfg)
    version = next_version(folder)
    out_dir = folder / version
    out_dir.mkdir(parents=True, exist_ok=True)

    positive = args.prompt or t["prompt"].format(subject=args.subject, style=common.style_line())
    negative = t["negative"] + (f", {args.negative}" if args.negative else "")
    source_name = upload_image(base, args.source.resolve()) if args.source else None
    seed0 = args.seed if args.seed is not None else random.randint(1, 2**31 - 1)

    options = []
    for i in range(args.count):
        label = string.ascii_uppercase[i]
        seed = seed0 + i
        wf = build_workflow(cfg, positive, negative, t["genWidth"], t["genHeight"], seed,
                            source_name, args.denoise if source_name else 1.0)
        path = out_dir / f"{label}.png"
        print(f"Generating {version} {label} (seed {seed}) ...", flush=True)
        run_one(base, wf, path)
        options.append({"label": label, "file": path.name, "seed": seed})

    meta = {"type": args.type, "name": safe, "version": version, "subject": args.subject,
            "positive": positive, "negative": negative, "checkpoint": cfg["checkpoint"], "lora": cfg.get("lora", ""),
            "source": str(args.source) if args.source else None,
            "denoise": args.denoise if args.source else None, "options": options}
    (out_dir / "meta.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")
    sheet = contact_sheet.build(out_dir)
    print(json.dumps({"folder": str(out_dir), "contact": str(sheet), "options": options}, indent=2))


if __name__ == "__main__":
    main()
