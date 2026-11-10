# 2D camera (Unity)

- Smoothing must be frame-rate independent: `pos = Vector3.Lerp(pos, target, 1 - Mathf.Exp(-k * Time.deltaTime))` (not a fixed per-frame lerp).
- Deadzone around the target reduces nausea; look-ahead leads in the movement direction.
- Clamp the view to level bounds using orthographic size and aspect (half-width = size * aspect), not just the center point.
- Follow in `LateUpdate` (after the target moved) to avoid jitter. Cinemachine is the usual route; use its Confiner 2D and Impulse for bounds and shake.
- Shake is an additive offset applied last (see 2d-game-feel), never moves the simulation.
- Pixel art: use the 2D Pixel Perfect Camera component or snap to pixel grid to avoid shimmer.
- Portrait mobile: set orthographic size from the board/world height and test the narrowest and tallest aspect ratios.
- Test at several frame rates, near walls, at level edges.
