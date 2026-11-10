# Genre: puzzle (grid)

- Board = plain data grid, the single source of truth; visuals follow the model.
- Resolve loop: find matches -> score by chain step -> clear -> gravity -> refill from seeded RNG -> repeat until stable. Resolving once misses cascades.
- Validate moves before applying; ignore input while resolving. Detect deadlocks and reshuffle or end.
- Undo: snapshot board + score + moves (or command pattern on large boards).
- Level progression: move limits, goals, grid shape; teach one rule per level; check generated boards are solvable; watch for difficulty spikes.
- Feedback for each step of a cascade (see 2d-game-feel); keep logic unit-testable (see 2d-code-hygiene).
- Pitfalls: logic mixed into visuals, unseeded refill, incomplete undo, accepting input mid-resolve.
