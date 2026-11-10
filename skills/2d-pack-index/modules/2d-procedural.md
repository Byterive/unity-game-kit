# Procedural generation

- One seed reproduces the same world. Use a dedicated RNG instance per system; log the seed with bug reports.
- Noise: fractal (octaves, lacunarity, persistence); uncorrelated seeds per layer to avoid matching patterns.
- Loot: weighted tables; test distribution over thousands of seeds.
- Dungeons: place rooms, reject overlaps, connect with corridors; always verify connectivity (flood fill) and that required items are reachable.
- Bound every loop (max attempts); fall back to a safe layout.
- Puzzle levels: verify solvability and difficulty by running a solver over generated boards.
- Sweep seeds when tuning; save a few known-good seeds as regression tests.
