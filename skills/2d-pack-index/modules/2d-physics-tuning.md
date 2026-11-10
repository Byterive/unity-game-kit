# 2D physics tuning (Unity)

- 2D uses `Rigidbody2D`/`Collider2D`, separate from 3D. Many match/puzzle games need no physics: prefer tweens.
- Physics runs in `FixedUpdate` (default 0.02 s). Read input in `Update`, store it, apply in `FixedUpdate`.
- Move dynamic bodies with forces or `linearVelocity` (named `velocity` before Unity 6), not by setting `transform.position`; use `MovePosition` for kinematic bodies.
- Jitter: enable Rigidbody2D Interpolate; keep cameras following in `LateUpdate`.
- Tunnelling: Collision Detection = Continuous for fast bodies; avoid thin colliders.
- Use layers and the 2D Layer Collision Matrix to prune checks; in hot paths use the `Physics2D.OverlapCircle(point, radius, contactFilter, results)` overload with a preallocated `Collider2D[]` (it returns the count) instead of the old `...NonAlloc` calls.
- Tune gravity scale, linear damping (named linear drag before Unity 6) and mass together; derive jump from height/time (gravity = 2h/t^2, velocity = 2h/t).
- Merge tilemap colliders with `CompositeCollider2D` and a static Rigidbody2D.
- Debug with the Physics 2D debugger and gizmos.
