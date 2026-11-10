---
name: 2d-code-hygiene
description: "Use when writing or reviewing C# gameplay code in a 2D Unity game: MonoBehaviour habits, ScriptableObject data, seeded RNG, allocation-free updates."
---

# 2D code hygiene (Unity C#)

Read `ProjectSettings/ProjectVersion.txt` first and keep that version's APIs; do not migrate unless asked. Verify engine-specific claims against current Unity docs.

## MonoBehaviours
- Cache `GetComponent` in `Awake`; subscribe in `OnEnable`, unsubscribe in `OnDisable`.
- `[SerializeField] private` over public fields; `CompareTag` over string ==.
- Per-frame motion scales by `Time.deltaTime`; physics work in `FixedUpdate`; camera follow in `LateUpdate`.
- Disabling a component does not stop its coroutines; deactivating the GameObject does.
- No allocations in `Update` (no LINQ, string concat, closures, `new` collections).

## ScriptableObjects
- Use for shared config and designer-tunable data (levels, tuning, palettes); not for per-instance state or save data.
- Runtime edits persist in the Editor but not in builds. With Reload Domain off, `OnEnable` may not run on Play: reset mutable values from an explicit bootstrap.

## Randomness and logic
- Use a dedicated seeded RNG instance (not `UnityEngine.Random` globally) wherever results must be reproducible or testable.
- Keep game logic in plain C# classes separate from MonoBehaviours so EditMode tests can run it without scenes.

## Done checklist
Logic separated from visuals and tested; seeded RNG; no per-frame allocations; events unsubscribed; verified on a device.
