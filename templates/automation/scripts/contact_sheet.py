"""Builds one labelled review image from a folder of options.

    python automation/scripts/contact_sheet.py ArtReview/sprite_rook/v1
"""
import argparse
import math
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

THUMB = 384
LABEL_H = 44
GAP = 12


def checkerboard(size, cell=16):
    img = Image.new("RGB", size, (235, 235, 235))
    d = ImageDraw.Draw(img)
    for y in range(0, size[1], cell):
        for x in range(0, size[0], cell):
            if (x // cell + y // cell) % 2:
                d.rectangle([x, y, x + cell - 1, y + cell - 1], fill=(205, 205, 205))
    return img


def font(size):
    for name in ("arialbd.ttf", "Arial Bold.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default()


def build(folder: Path) -> Path:
    files = sorted(p for p in folder.glob("*.png") if p.stem != "contact")
    if not files:
        raise SystemExit(f"No PNG options in {folder}")
    cols = min(4, len(files))
    rows = math.ceil(len(files) / cols)
    first = Image.open(files[0])
    aspect = first.height / first.width
    tw, th = THUMB, int(THUMB * aspect)
    sheet = Image.new("RGB", (cols * (tw + GAP) + GAP, rows * (th + LABEL_H + GAP) + GAP), (30, 30, 34))
    draw = ImageDraw.Draw(sheet)
    f = font(28)
    for i, path in enumerate(files):
        r, c = divmod(i, cols)
        x = GAP + c * (tw + GAP)
        y = GAP + r * (th + LABEL_H + GAP)
        img = Image.open(path).convert("RGBA")
        img.thumbnail((tw, th))
        tile = checkerboard((tw, th))
        tile.paste(img, ((tw - img.width) // 2, (th - img.height) // 2), img)
        sheet.paste(tile, (x, y))
        draw.text((x + 8, y + th + 6), f"{folder.name} {path.stem}", fill=(255, 255, 255), font=f)
    out = folder / "contact.png"
    sheet.save(out)
    return out


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    print(build(ap.parse_args().folder))
