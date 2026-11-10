# Genre: tower defense

- Systems: path/lane, wave spawner (data-driven wave definitions), tower targeting (first, last, strongest, nearest), projectiles, gold economy, lives.
- Balance levers: enemy HP growth vs income growth vs tower cost; tune with a spreadsheet or simulation, not by feel alone.
- Pitfalls: trivially dominant tower, no counterplay to a wave type, maze-blocking paths (always keep a valid path), spiking difficulty.
- Use pooling for enemies/projectiles; seeded randomness for reproducible wave tests.
- See 2d-ai-pathing and 2d-performance-android.
