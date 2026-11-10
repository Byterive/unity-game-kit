"""Turns a picked option into a game-ready PNG and puts it in the Unity project.

    python automation/scripts/finalize_asset.py --type sprite --name rook --pick ArtReview/sprite_rook/v2/B.png

Steps: remove the background (sprite and icon types), trim, pad to square, resize,
save as a real PNG at the target path from asset-types.json. The file it replaces is
copied to ArtReview/<type>_<name>/replaced_<time>.png first, so nothing is lost.
Add --dry-run to write the result only to ArtReview/<type>_<name>/final.png.
"""
import argparse
import json
import shutil
import sys
import time
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common  # noqa: E402


def remove_background(img: Image.Image) -> Image.Image:
    try:
        from rembg import remove  # pip install rembg onnxruntime  (first run downloads the model once)
        return remove(img.convert("RGBA"))
    except ImportError:
        print("rembg not installed, using flood fill from the corners instead", file=sys.stderr)
        return flood_fill_alpha(img.convert("RGBA"))


def flood_fill_alpha(img: Image.Image, tolerance=28) -> Image.Image:
    """Makes the flat background transparent by filling inward from the four corners."""
    w, h = img.size
    px = img.load()
    seen = bytearray(w * h)
    stack = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    refs = [px[x, y][:3] for x, y in stack]

    def close(c):
        return any(sum(abs(c[i] - r[i]) for i in range(3)) <= tolerance * 3 for r in refs)

    while stack:
        x, y = stack.pop()
        i = y * w + x
        if seen[i]:
            continue
        seen[i] = 1
        c = px[x, y]
        if not close(c):
            continue
        px[x, y] = (c[0], c[1], c[2], 0)
        if x > 0: stack.append((x - 1, y))
        if x < w - 1: stack.append((x + 1, y))
        if y > 0: stack.append((x, y - 1))
        if y < h - 1: stack.append((x, y + 1))
    return img


def fit_square(img: Image.Image, size, padding) -> Image.Image:
    bbox = img.getchannel("A").getbbox()
    if bbox:
        img = img.crop(bbox)
    side = int(max(img.size) / (1 - 2 * padding)) if padding < 0.5 else max(img.size)
    canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
    canvas.paste(img, ((side - img.width) // 2, (side - img.height) // 2), img)
    return canvas.resize(tuple(size), Image.LANCZOS)


def fit_cover(img: Image.Image, size) -> Image.Image:
    tw, th = size
    scale = max(tw / img.width, th / img.height)
    img = img.resize((round(img.width * scale), round(img.height * scale)), Image.LANCZOS)
    left, top = (img.width - tw) // 2, (img.height - th) // 2
    return img.crop((left, top, left + tw, top + th))


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--type", required=True)
    ap.add_argument("--name", required=True)
    ap.add_argument("--pick", required=True, type=Path, help="The option you approved")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    cfg = common.load_config()
    t = common.load_asset_types()[args.type]
    folder, safe = common.asset_folder(args.type, args.name, cfg)
    folder.mkdir(parents=True, exist_ok=True)

    img = Image.open(args.pick)
    if t.get("removeBackground"):
        img = fit_square(remove_background(img), t["outputSize"], t.get("padding", 0.06))
    else:
        img = fit_cover(img.convert("RGB"), t["outputSize"])

    final = folder / "final.png"
    img.save(final, format="PNG")
    result = {"final": str(final), "pick": str(args.pick)}

    if not args.dry_run:
        target = common.unity_project(cfg) / t["target"].format(name=safe)
        target.parent.mkdir(parents=True, exist_ok=True)
        if target.exists():
            backup = folder / f"replaced_{time.strftime('%Y%m%d-%H%M%S')}.png"
            shutil.copy2(target, backup)
            result["backup"] = str(backup)
        img.save(target, format="PNG")
        result["target"] = str(target)
        (folder / "approved.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
