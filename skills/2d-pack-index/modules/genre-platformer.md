# Genre: platformer

- Coyote time: allow a jump 0.08-0.12 s after leaving a ledge. Jump buffer: remember a press 0.10-0.15 s before landing.
- Variable jump: cut upward velocity to 0.4-0.5x when the button is released early.
- Jump shape: apex ~3-4 tiles in 0.30-0.40 s; gravity = 2h/t^2, jump velocity = 2h/t; fall gravity 1.5-2.0x rise gravity.
- Run on the fixed physics tick (or fixed-step custom controller) so jump height is frame-rate independent.
- Corner correction (~4 px nudge), one-way platforms, slope handling.
- Camera: smoothed follow with deadzone (see 2d-camera). Level pacing: see 2d-level-pacing-prototype; require jumps at ~70% of max distance.
- Prefer a kinematic custom controller over a dynamic Rigidbody2D for precise feel.
