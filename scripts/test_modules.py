#!/usr/bin/env python3
"""Tests for the 2D modules (stdlib only): skill files, module files, gamekit.json switch, doctor check.
Usage: python scripts/test_modules.py   (exit 1 on any failure)
"""
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
MODS = SKILLS / "2d-pack-index" / "modules"
CORE = ["2d-code-hygiene", "2d-game-feel", "2d-ui-touch-mobile", "2d-performance-android", "2d-save-systems", "2d-art-pipeline", "2d-level-pacing-prototype"]
OPTIONAL = ["2d-camera", "2d-audio", "2d-shaders", "2d-physics-tuning", "2d-ai-pathing", "2d-procedural"]
GENRE = ["genre-puzzle", "genre-platformer", "genre-tower-defense", "genre-roguelike", "genre-card"]
fails = []


def check(name, ok, detail=""):
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  {str(detail)[:300]}"))
    if not ok:
        fails.append(name)


def front(path):
    t = path.read_text(encoding="utf-8").replace("\r\n", "\n")
    m = re.match(r"---\n(.*?)\n---\n", t, re.S)
    return dict(re.findall(r"^(\w+):\s*(.+)$", m.group(1), re.M)) if m else None


for n in ["2d-pack-index"] + CORE:
    f = front(SKILLS / n / "SKILL.md") if (SKILLS / n / "SKILL.md").exists() else None
    check(f"skill {n}: frontmatter has name equal to the folder and a description", bool(f) and f.get("name") == n and bool(f.get("description")), f)

check("the 11 modules exist and are not skills", sorted(p.stem for p in MODS.glob("*.md")) == sorted(OPTIONAL + GENRE)
      and not any((SKILLS / m).exists() for m in OPTIONAL + GENRE))
check("modules carry no frontmatter (they are loaded by the index, not by Claude)", all(not p.read_text(encoding="utf-8").startswith("---") for p in MODS.glob("*.md")))
idx = (SKILLS / "2d-pack-index" / "SKILL.md").read_text(encoding="utf-8")
check("the index names every module", all(m in idx for m in OPTIONAL + GENRE))
check("the index reads gamekit.json, not a separate pack file", "gamekit.json" in idx and "2d-pack.json" not in idx)
tpl = json.loads((ROOT / "templates" / "project" / "gamekit.json").read_text(encoding="utf-8"))
check("gamekit.json template has an empty modules list", tpl.get("modules") == [], tpl)
check("game-setup asks for modules and records them", "2d-camera" in (SKILLS / "game-setup" / "SKILL.md").read_text(encoding="utf-8") and "`modules`" in (SKILLS / "game-setup" / "SKILL.md").read_text(encoding="utf-8"))
phys = (MODS / "2d-physics-tuning.md").read_text(encoding="utf-8")
check("physics module uses the current API names", "linearVelocity" in phys and "linear damping" in phys and "OverlapCircleNonAlloc" not in phys.replace("instead of the old `...NonAlloc` calls", ""), phys)
check("overlaps point at the kit's own skills", "/asset" in (SKILLS / "2d-art-pipeline" / "SKILL.md").read_text(encoding="utf-8") and "/build-android" in (SKILLS / "2d-performance-android" / "SKILL.md").read_text(encoding="utf-8"))
check("the performance skill dates its Play numbers", "2026-11-04" in (SKILLS / "2d-performance-android" / "SKILL.md").read_text(encoding="utf-8"))


def doctor(modules):
    with tempfile.TemporaryDirectory() as d:
        kit = dict(tpl, modules=modules)
        (Path(d) / "gamekit.json").write_text(json.dumps(kit), encoding="utf-8")
        r = subprocess.run([sys.executable, str(ROOT / "scripts" / "doctor.py"), "--root", d, "--json"], capture_output=True, text=True)
        rows = json.loads(r.stdout) if r.stdout.strip().startswith("[") else []
        return next((x for x in rows if x["id"] == "modules"), None), r


row, r = doctor(["2d-camera", "genre-puzzle"])
check("doctor: valid modules are ok", bool(row) and row["status"] == "ok", (row, r.stderr))
row, r = doctor(["2d-camera", "nope"])
check("doctor: an unknown module is a warning", bool(row) and row["status"] == "warn" and "nope" in row["detail"], row)
row, r = doctor(["genre-puzzle", "genre-card"])
check("doctor: two genres is a warning", bool(row) and row["status"] == "warn" and "genre" in row["detail"], row)
row, r = doctor([])
check("doctor: no modules means core only", bool(row) and row["status"] == "ok" and "core only" in row["detail"], row)

print(f"\n{len(fails)} failure(s)")
sys.exit(1 if fails else 0)
