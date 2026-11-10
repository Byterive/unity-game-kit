---
name: game-doctor
description: Check what a unity-game-kit project is missing (Unity editor and modules, packages, compiled kit scripts, scene, tests, Unity CLI, Python, ComfyUI, Android settings) and guide the user through fixing it step by step. Use when the user asks what's missing, what to do next with setup, or when the session-start line says setup items need attention.
---

# /game-doctor: what's missing, and the next step

1. From the repo root run: `python <this skill's base directory>/../../scripts/doctor.py --write-status`. It reads `gamekit.json` and `automation/config.json`, checks the real project, prints a table and writes it into the Setup section of `PROJECT_STATUS.md`.
2. Reply with the MISSING and WARN rows only, one line each, then the single next step in full: what to click or run, exactly. Don't list every fix at once.
3. When the user says it's done, re-run the doctor and move to the next item.
4. Remember the user's decisions in `gamekit.json`:
   - "Skip ComfyUI" or "no art pipeline" -> add the check id (for example `comfyui`) to `skip`.
   - Facts worth keeping (test phone model, where the keystore lives, not its password) -> `notes` or the matching field.
5. Checks marked UNKNOWN can't be read from here (for example the editor outside Windows); ask the user once and note the answer.

Never write passwords, keystores or tokens into `gamekit.json` or any file in the repo.
