## Unity game kit

- `Unity/` is the Unity project; game code in `Unity/Assets/__ID__`. Open `Unity/` in Unity Hub and the repo root in Claude Code.
- `gamekit.json` holds this game's setup answers; `automation/config.json` holds build and art settings. Change settings there, not in ProjectSettings.asset.
- Run `/game-doctor` when something about the setup seems off; it checks the real project and says what is missing.
- Run `/check` before saying a change is done.
- Never put generated art into `Unity/` until the user names the final option (`/asset`).
- Commit in small steps, one logical change each, on a branch per feature or asset.
- Don't hand-edit .meta, .unity or .prefab YAML without asking; don't delete or rename assets; don't upgrade Unity or packages without asking.
- Never commit keystores, passwords or tokens.
- Batch-mode Unity (`automation/scripts/run_unity.ps1`) only works with the Editor closed; with it open use the __NAME__ > Automation menu or `unity command eval`.
