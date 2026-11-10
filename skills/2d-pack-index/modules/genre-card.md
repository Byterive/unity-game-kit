# Genre: card games

- Card data as ScriptableObjects describing effects; code interprets effect specs.
- Zones (deck, hand, discard, board): each card in exactly one zone; moving a card is one atomic operation.
- Draw with automatic reshuffle of discard; seeded shuffle.
- Turn as explicit phases; resource costs; effects resolve in a defined order using a queue/stack.
- Pitfalls: duplicated cards, unseeded shuffles, non-atomic play, effect chains that skip validation.
- Unit-test rules without scenes (see 2d-code-hygiene).
