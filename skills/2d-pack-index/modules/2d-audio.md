# Audio (Unity)

- Route sounds through group buses (Music, SFX, UI) in an AudioMixer; never tweak individual clips for volume settings.
- Volume sliders: map 0-1 to dB (`Mathf.Log10(Mathf.Max(v, 0.0001f)) * 20`) and set the exposed mixer parameter. Leave master headroom.
- Duck music under important sounds: fast attack, slow release.
- Adaptive music: layers or segments that respond to state (menu, play, danger, win); crossfade on bar boundaries.
- Randomize repeated SFX slightly (pitch +/-5%, volume, 3+ variants) and cap simultaneous instances of one sound.
- Time beats from `AudioSettings.dspTime`, not frame delta.
- Loop clips must be seamless; test the loop point. Compress for mobile (Vorbis, Load Type by length).
- Mute on focus loss/phone call; respect a mute setting and save it.
