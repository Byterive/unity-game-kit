# 2D AI and pathfinding

Separate three layers: decide (what to do), steer (how to move), path (where through the map).
- Start with a finite state machine (idle, patrol, chase, attack); move to behaviour trees only when states explode. Multi-frame actions return RUNNING; add stuck timeouts.
- Steering: seek, arrive (slow near target), simple separation. Steer toward the next waypoint, not the final goal.
- Grid games: A* with an admissible heuristic (Manhattan for 4-way, Chebyshev/octile for 8-way); cache paths and re-plan on change, never every frame.
- Unity: NavMesh is 3D-oriented; for 2D use grid A* or a 2D-aware package. Verify packages against the project's Unity version.
- Keep AI decisions deterministic given a seed so they are testable.
- Tune with debug draws (paths, state labels).
