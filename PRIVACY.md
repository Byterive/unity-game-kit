---
title: unity-game-kit privacy policy
summary: What unity-game-kit reads, writes and sends, how long data is kept, and how to contact us.
keywords: [unity-game-kit, privacy, data, policy]
status: confirmed
updated: 2026-11-13
---

# unity-game-kit privacy

This page says what unity-game-kit does with your data. It applies to unity-game-kit version 0.2 and later releases of that line, until a newer version of this file replaces it. Date: 2026-11-13.

## What it reads
On session start, a hook runs `scripts/doctor.py --brief`, which uses only the Python standard library. In a project with a `gamekit.json` it reads your project files and checks whether ComfyUI answers at `http://127.0.0.1:8188`. It prints one line if setup items need attention, and stays silent in any other project.

The Android build reads your signing keystore path, alias and passwords from environment variables that you set in your own PowerShell window. The build guide says to keep passwords out of the project and out of git.

## What it writes and where
Assets and screenshots go into your Unity project when you approve them. Setup copies the kit's Editor scripts, `automation/`, `gamekit.json` and `.gitignore` lines, and never overwrites an existing file. The doctor prints install hints as text and never runs them.

Models and the pip packages `rembg` and `onnxruntime` are installed by you, not by the plugin.

## What it sends and to whom
Nothing leaves your machine through the plugin. Art generation talks only to a ComfyUI running on your own computer, at the address set in `automation/config.json` (default `127.0.0.1:8188`).

## How long data is kept
Everything the plugin writes stays in your project folder until you delete it. The plugin keeps nothing anywhere else.

## Who it is for
We do not design unity-game-kit for people under 18, and we do not knowingly collect data from them.

## Other software
unity-game-kit runs inside Claude Code. Claude Code and the other tools it works with handle your data under their own terms. This page covers only unity-game-kit.

## Contact
Use the contact details on [byterive.com](https://byterive.com). We do not publish an email address for privacy questions yet.

Unity, ComfyUI, Android and Google Play are trademarks of their owners; this project is not affiliated with them.

*Independent project by Byterive. Not affiliated with or endorsed by Anthropic.* · [byterive.com](https://byterive.com)
