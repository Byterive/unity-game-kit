# 2D shader effects (Unity URP)

Check the render pipeline (URP 2D vs Built-in) before writing; effects below are Shader Graph friendly.

- Tint/flash: multiply or lerp sprite colour; use `MaterialPropertyBlock` or per-renderer properties to avoid material instances (which break batching).
- Scrolling UVs: add `Time * speed` to UV; wrap with Repeat texture mode.
- Dissolve: sample a noise texture, `step(threshold, noise)` for alpha, add an emissive edge band just above the threshold.
- Outline: sample neighbour alpha at +/- texel offsets; needs padding in the sprite so the outline is not clipped.
- Keep effects cheap on mobile: few texture samples, no branching-heavy code, `half` precision where possible.
- Mind pivots and sprite atlas UVs: atlas sprites do not span 0-1 UV.
- Test on a real Android device; shader variants and precision differ from the Editor.
