"""Checks a Unity game project set up by unity-game-kit and says what is missing (stdlib only).

    python doctor.py                 # table of checks, run from the repo root
    python doctor.py --json          # machine-readable
    python doctor.py --brief         # one line, for the session-start hook (silent outside a kit project)
    python doctor.py --write-status  # also writes the Setup table into PROJECT_STATUS.md

It reads gamekit.json (answers and skips) and automation/config.json, and looks at the real
project every time, so it notices things that broke since the last run. Checks listed in
gamekit.json "skip" are reported as skipped.
"""
import argparse
import importlib.util
import json
import os
import re
import shutil
import sys
import urllib.request
from pathlib import Path

HUB = Path(r"C:\Program Files\Unity\Hub\Editor")
START, END = "<!-- game-doctor:start -->", "<!-- game-doctor:end -->"


def read(path):
    try:
        return Path(path).read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def load_json(path):
    try:
        return json.loads(read(path) or "{}")
    except json.JSONDecodeError:
        return {}


class Doctor:
    def __init__(self, root):
        self.root = root
        self.kit = load_json(root / "gamekit.json")
        self.cfg = load_json(root / "automation" / "config.json")
        self.unity = root / self.kit.get("unityProject", self.cfg.get("unityProject", "Unity"))
        self.ident = self.kit.get("id", "")
        self.results = []

    def add(self, cid, title, status, detail, fix=""):
        if cid in self.kit.get("skip", []):
            status, fix = "skip", ""
        self.results.append({"id": cid, "check": title, "status": status, "detail": detail, "fix": fix})

    # --- checks -------------------------------------------------------------------------------
    def git(self):
        if not (self.root / ".git").exists():
            return self.add("git", "Git repo", "missing", "no .git folder", "git init, then commit")
        hook = self.root / ".git" / "hooks" / "pre-commit"
        if hook.exists():
            self.add("git", "Git repo and hooks", "ok", "repo with pre-commit hook")
        else:
            self.add("git", "Git repo and hooks", "warn", "no pre-commit hook",
                     "/kickoff:bootstrap with the unity profile")

    def editor(self):
        ver = re.search(r"m_EditorVersion: (\S+)", read(self.unity / "ProjectSettings" / "ProjectVersion.txt"))
        if not ver:
            self.add("unity-project", "Unity project", "missing", f"no ProjectSettings in {self.unity.name}/",
                     "create the project in Unity Hub (or /unity:new-unity-project) inside this folder")
            return None
        self.add("unity-project", "Unity project", "ok", f"Unity {ver.group(1)}")
        exe = Path(self.cfg["unityEditor"]) if self.cfg.get("unityEditor") else HUB / ver.group(1) / "Editor" / "Unity.exe"
        if os.name != "nt" and not self.cfg.get("unityEditor"):
            self.add("unity-editor", "Unity editor installed", "unknown", "only checked on Windows")
            return None
        if exe.exists():
            self.add("unity-editor", "Unity editor installed", "ok", str(exe))
            return exe.parent
        self.add("unity-editor", "Unity editor installed", "missing", f"{ver.group(1)} not found",
                 f"Unity Hub > Installs > Install {ver.group(1)}, or set unityEditor in automation/config.json")
        return None

    def android(self, editor_dir):
        if "android" not in self.kit.get("platforms", ["android"]):
            return
        if editor_dir is None:
            return self.add("android-module", "Android Build Support", "unknown", "editor not found")
        if (editor_dir / "Data" / "PlaybackEngines" / "AndroidPlayer").exists():
            self.add("android-module", "Android Build Support", "ok", "installed")
        else:
            self.add("android-module", "Android Build Support", "missing", "module not installed",
                     "Unity Hub > Installs > gear > Add modules > Android Build Support (with OpenJDK, SDK and NDK)")

    def packages(self):
        deps = load_json(self.unity / "Packages" / "manifest.json").get("dependencies", {})
        need = [p for p in ("com.unity.ugui", "com.unity.test-framework") if p not in deps]
        if need:
            self.add("packages", "Required packages", "missing", ", ".join(need),
                     "Window > Package Manager > Unity Registry, install " + ", ".join(need))
        else:
            self.add("packages", "Required packages", "ok", "ugui and test framework present")

    def kit_scripts(self):
        ed = self.unity / "Assets" / self.ident / "Editor"
        need = [p for p in ("AutomationCommands.cs", "AutomationAndroid.cs", "Checks/Checks.cs") if not (ed / p).exists()]
        if need:
            return self.add("kit-scripts", "Kit Editor scripts", "missing", ", ".join(need), "/game-setup (copies them)")
        dll = self.unity / "Library" / "ScriptAssemblies" / f"{self.ident}.Editor.Checks.dll"
        errors = re.findall(r"error CS\d+[^\"\\]{0,160}", read(self.unity / "Library" / "Bee" / "tundra.log.json"))
        if errors:
            self.add("kit-scripts", "Scripts compile", "missing", errors[-1], "fix this compile error (see the Unity Console)")
        elif not dll.exists():
            self.add("kit-scripts", "Scripts compile", "warn", "not compiled yet",
                     "open the project in Unity and wait for it to import")
        else:
            self.add("kit-scripts", "Scripts compile", "ok", "last compile had no errors")

    def scene(self):
        text = read(self.unity / "ProjectSettings" / "EditorBuildSettings.asset")
        if re.search(r"enabled: 1\s+path: \S+\.unity", text):
            self.add("scene", "Scene in Build Settings", "ok", "at least one enabled scene")
        else:
            self.add("scene", "Scene in Build Settings", "missing", "no enabled scene",
                     "File > Build Profiles > Scene List > Add Open Scenes, then File > Save Project")

    def player(self):
        a = self.cfg.get("android", {})
        if not a.get("productName"):
            self.add("player", "Android settings", "missing", "no android section in automation/config.json", "/game-setup")
        elif not a.get("packageId"):
            self.add("player", "Android settings", "warn", "packageId empty (dev builds only)",
                     "set android.packageId once the name is final; it can't change after the first Play upload")
        else:
            self.add("player", "Android settings", "ok", a["packageId"])

    def tests(self):
        asm = [p for p in (self.unity / "Assets").rglob("*.asmdef")
               if "UnityEditor.TestRunner" in read(p) and not p.name.endswith(".Editor.Checks.asmdef")]
        if not asm:
            return self.add("tests", "Edit Mode tests", "missing", "no test assembly",
                            "ask Claude to add Edit Mode tests for the game logic")
        res = load_json(self.root / "automation" / "reports" / "tests_latest.json")
        if res.get("failed"):
            self.add("tests", "Edit Mode tests", "warn", f"{res['failed']} failing at {res.get('finished')}", "/check")
        elif res:
            self.add("tests", "Edit Mode tests", "ok", f"{res.get('passed')} passed at {res.get('finished')}")
        else:
            self.add("tests", "Edit Mode tests", "warn", f"{len(asm)} test assembly, never run here", "/check")

    def unity_cli(self):
        if shutil.which("unity"):
            self.add("unity-cli", "Unity CLI", "ok", "on PATH")
        else:
            self.add("unity-cli", "Unity CLI", "missing", "not on PATH",
                     "PowerShell: $env:UNITY_CLI_CHANNEL='beta'; irm https://public-cdn.cloud.unity3d.com/hub/prod/cli/install.ps1 | iex ; then in Unity/: unity pipeline install")

    def python_deps(self):
        need = [m for m in ("PIL", "rembg") if importlib.util.find_spec(m) is None]
        if need:
            self.add("python", "Python packages", "missing", ", ".join(need), "pip install -r automation/requirements.txt")
        else:
            self.add("python", "Python packages", "ok", "pillow and rembg")

    def modules2d(self):
        mods = self.kit.get("modules", [])
        folder = Path(__file__).resolve().parent.parent / "skills" / "2d-pack-index" / "modules"
        unknown = [m for m in mods if not (folder / f"{m}.md").exists()]
        genres = [m for m in mods if m.startswith("genre-")]
        if unknown:
            self.add("modules", "2D modules", "warn", "unknown module(s): " + ", ".join(unknown), "fix the names in gamekit.json \"modules\" (see skills/2d-pack-index)")
        elif len(genres) > 1:
            self.add("modules", "2D modules", "warn", "more than one genre module: " + ", ".join(genres), "keep one genre-* module in gamekit.json")
        else:
            self.add("modules", "2D modules", "ok", ", ".join(mods) if mods else "core only")

    def comfyui(self):
        if self.kit.get("art", "comfyui") != "comfyui":
            return
        base = self.cfg.get("comfyUrl", "http://127.0.0.1:8188").rstrip("/")
        try:
            with urllib.request.urlopen(f"{base}/object_info/CheckpointLoaderSimple", timeout=3) as r:
                names = json.loads(r.read().decode())["CheckpointLoaderSimple"]["input"]["required"]["ckpt_name"][0]
        except Exception:  # noqa: BLE001
            return self.add("comfyui", "ComfyUI", "warn", f"not answering at {base}", "start ComfyUI Desktop (only needed for art)")
        ck = self.cfg.get("checkpoint", "")
        if ck in names:
            self.add("comfyui", "ComfyUI and checkpoint", "ok", f"{len(names)} checkpoints, using {ck}")
        else:
            self.add("comfyui", "ComfyUI and checkpoint", "missing", f"'{ck}' not installed ({len(names)} found)",
                     "set checkpoint in automation/config.json to one ComfyUI lists, or run /art-compare")

    def run(self):
        self.git()
        editor_dir = self.editor()
        if (self.unity / "ProjectSettings").exists():
            self.android(editor_dir)
            self.packages()
            self.kit_scripts()
            self.scene()
            self.tests()
        self.player()
        self.unity_cli()
        self.python_deps()
        self.modules2d()
        self.comfyui()
        return self.results


def table(results):
    rows = ["| Check | Status | Detail | Next step |", "|---|---|---|---|"]
    for r in results:
        cells = [r["check"], r["status"].upper(), r["detail"], r["fix"]]
        rows.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
    return "\n".join(rows)


def write_status(root, results):
    path = root / "PROJECT_STATUS.md"
    text = read(path)
    block = f"{START}\n## Setup\n\nFrom `/game-doctor`; regenerated on each run.\n\n{table(results)}\n{END}"
    if START in text and END in text:
        text = text[:text.index(START)] + block + text[text.index(END) + len(END):]
    else:
        text = text.rstrip("\n") + "\n\n" + block + "\n"
    path.write_text(text, encoding="utf-8", newline="\n")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", type=Path, default=Path.cwd())
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--brief", action="store_true")
    ap.add_argument("--write-status", action="store_true")
    args = ap.parse_args()
    root = args.root.resolve()
    if not (root / "gamekit.json").exists():
        if not args.brief:
            print("No gamekit.json here. Run /game-setup first (or pass --root).")
        return
    results = Doctor(root).run()
    todo = [r for r in results if r["status"] in ("missing", "warn")]
    if args.brief:
        if todo:
            print(f"unity-game-kit: {len(todo)} setup item(s) need attention ({', '.join(r['id'] for r in todo[:4])}). Run /game-doctor.")
        return
    if args.write_status:
        write_status(root, results)
    print(json.dumps(results, indent=2) if args.json else table(results))


if __name__ == "__main__":
    sys.exit(main())
