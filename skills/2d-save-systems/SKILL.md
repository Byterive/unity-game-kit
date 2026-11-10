---
name: 2d-save-systems
description: Use when designing save/load for a Unity game: versioned schema, migrations, atomic writes, backups, autosave.
---

# Save systems (Unity)

- Save plain serializable data only (DTOs/JSON); rebuild objects on load. No scene references or UnityEngine.Object in saves.
- Stamp a schema `version` int. Migrate step by step to current; refuse saves from newer builds.
- Atomic write: write temp file, flush, replace target, keep a `.bak`; on parse/validation failure load the backup.
- Path: `Application.persistentDataPath` (Android/iOS safe). `PlayerPrefs` only for small settings.
- Autosave: throttled, own slot, at safe points (level end), never mid-resolve.
- Persist input bindings and settings through the same system.
- Test: corrupt file, empty file, old version, future version, interrupted write.
- If cloud save or analytics are added, update the privacy policy / data safety form.
