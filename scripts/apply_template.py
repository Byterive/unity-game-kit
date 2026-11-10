"""Copies the unity-game-kit templates into a game project, filling in the game's name.

    python apply_template.py --root "F:/Games/My Game" --name "My Game" --dry-run
    python apply_template.py --root "F:/Games/My Game" --name "My Game"

Never overwrites: files that already exist are listed as "kept" so Claude can merge by hand.
Fills __NAME__ (display name), __ID__ (C# namespace and folder, e.g. MyGame), __LOWER__ (mygame),
__ENV__ (environment variable prefix, e.g. MYGAME) and __DATE__ in file names and contents.
Also adds missing .gitignore lines, writes gamekit.json if there is none, and prints
CLAUDE.section.md for Claude to merge into the project's CLAUDE.md.
"""
import argparse
import datetime
import json
import re
from pathlib import Path

KIT = Path(__file__).resolve().parents[1]
TEMPLATES = KIT / "templates"


def kit_version():
    return json.loads((KIT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]


def default_id(name):
    parts = re.findall(r"[A-Za-z0-9]+", name)
    ident = "".join(p[:1].upper() + p[1:] for p in parts) or "Game"
    return ident if not ident[0].isdigit() else "Game" + ident


def tokens(name, ident, env):
    return {"__NAME__": name, "__ID__": ident, "__LOWER__": ident.lower(), "__ENV__": env,
            "__DATE__": datetime.date.today().isoformat(), "__KIT_VERSION__": kit_version()}


def fill(text, toks):
    # __ENV__ before __ID__ etc. does not matter: tokens never contain each other.
    for k, v in toks.items():
        text = text.replace(k, v)
    return text


def copy_tree(src, root, toks, dry):
    written, kept = [], []
    for path in sorted(src.rglob("*")):
        if path.is_dir() or "__pycache__" in path.parts:
            continue
        rel = Path(fill(str(path.relative_to(src)), toks))
        dest = root / rel
        if dest.exists():
            kept.append(str(rel))
            continue
        written.append(str(rel))
        if not dry:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(fill(path.read_text(encoding="utf-8"), toks), encoding="utf-8", newline="\n")
    return written, kept


def merge_gitignore(root, dry):
    wanted = (TEMPLATES / "project" / "gitignore.txt").read_text(encoding="utf-8").splitlines()
    path = root / ".gitignore"
    have = set(path.read_text(encoding="utf-8").splitlines()) if path.exists() else set()
    missing = [l for l in wanted if l and not l.startswith("#") and l not in have]
    if missing and not dry:
        with path.open("a", encoding="utf-8", newline="\n") as f:
            f.write("\n# Added by unity-game-kit\n" + "\n".join(missing) + "\n")
    return missing


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, required=True, help="Repo root (the folder that holds Unity/)")
    ap.add_argument("--name", required=True, help="Display name, e.g. 'My Game'")
    ap.add_argument("--id", help="C# identifier, default from the name (My Game -> MyGame)")
    ap.add_argument("--env", help="Environment variable prefix, default the id in capitals")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    root = args.root.resolve()
    ident = args.id or default_id(args.name)
    toks = tokens(args.name, ident, args.env or ident.upper())
    report = {"root": str(root), "id": ident, "written": [], "kept": []}
    for part in ("Unity", "automation"):
        w, k = copy_tree(TEMPLATES / part, root / part, toks, args.dry_run)
        report["written"] += [f"{part}/{p}" for p in w]
        report["kept"] += [f"{part}/{p}" for p in k]
    gk = root / "gamekit.json"
    if gk.exists():
        report["kept"].append("gamekit.json")
    else:
        report["written"].append("gamekit.json")
        if not args.dry_run:
            gk.write_text(fill((TEMPLATES / "project" / "gamekit.json").read_text(encoding="utf-8"), toks),
                          encoding="utf-8", newline="\n")
    report["gitignore_added"] = merge_gitignore(root, args.dry_run)
    report["claude_section"] = fill((TEMPLATES / "project" / "CLAUDE.section.md").read_text(encoding="utf-8"), toks)
    report["dry_run"] = args.dry_run
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
