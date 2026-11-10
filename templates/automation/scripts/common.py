"""Shared paths and settings for the __NAME__ automation scripts."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
AUTOMATION = ROOT / "automation"


def load_config():
    return json.loads((AUTOMATION / "config.json").read_text(encoding="utf-8"))


def load_asset_types():
    return json.loads((AUTOMATION / "asset-types.json").read_text(encoding="utf-8"))


def unity_project(config=None):
    config = config or load_config()
    return (ROOT / config["unityProject"]).resolve()


def review_dir(config=None):
    config = config or load_config()
    return ROOT / config.get("reviewDir", "ArtReview")


def style_line():
    """The line under '## Style line' in art-bible.md."""
    text = (AUTOMATION / "art-bible.md").read_text(encoding="utf-8")
    m = re.search(r"^## Style line\s*\n+(.+?)\s*$", text, re.MULTILINE)
    return m.group(1).strip() if m else ""


def asset_folder(asset_type, name, config=None):
    safe = re.sub(r"[^a-z0-9_]+", "_", name.lower()).strip("_")
    return review_dir(config) / f"{asset_type}_{safe}", safe
