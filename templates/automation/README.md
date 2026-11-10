# __NAME__ local automation

Everything here runs on your PC: Claude Code, ComfyUI and Unity. Set up by the unity-game-kit plugin; run `/game-doctor` to see what is still missing.

| You type | What happens |
| --- | --- |
| `/asset <what to draw>` | ComfyUI makes 4 options, you pick one, it goes into the game after you approve |
| `/art-compare <models to try>` | Same prompt and seeds on each checkpoint and LoRA, one labelled grid per round |
| `/check` | Console, tests, play-mode screenshot |
| `/build-android` | APK built and installed on your phone over USB |
| `/store-shots` | Store screenshots captured and framed |
| `/content-check` | The game's own content validator, if it has one |

| File | Does |
| --- | --- |
| `config.json` | ComfyUI address, model and sampler settings, Android settings, content check method |
| `art-bible.md` | Style line, palette, model and art rules |
| `asset-types.json` | Sizes, prompt templates and target paths per asset type |
| `model-settings.json` | Family and recommended settings per checkpoint and LoRA |
| `compare/*.json` | Model comparison matrices |
| `android-builds.md` | Android setup, signing and release |
| `scripts/comfy_run.py`, `contact_sheet.py`, `finalize_asset.py`, `compare_models.py` | Art pipeline |
| `scripts/run_unity.ps1` | Unity batch mode (Editor closed): builds, tests, your own methods |
| `scripts/install_apk.ps1` | Installs the APK on a USB phone and starts it |
| `scripts/nightly.ps1` | Tests, content check and optional build; its header has the Task Scheduler line |

Python packages: `pip install -r automation/requirements.txt`.
