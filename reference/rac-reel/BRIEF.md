---
workflow: general-video
flow: automation
storyboard: yes
---

# RAC reel: "Ek berth, do ajnabi"

Vertical Instagram reel for Indian viewers, Hinglish voiceover, new account, goal is followers.
Story: two strangers pay full fare for half a berth, and that is the plan, not a mistake.

- Format: 720×1280, 30 fps for now, about 1:30. Render in software mode (`--no-browser-gpu`).
- Voice: ElevenLabs "Kanika - Soft and Vibrant" (female, Hindi), speed 1.1. Pauses only at full stops and new lines.
- Look: navy blueprint 3D world, glowing yellow and red berth, glass cards, progress rail. See `frame.md`.
- Sound: voice and low free-licence music only, no sound effects.
- No paid services. Header shows only the series label.

## Assets

- `assets/audio/voiceover.wav`: the voiceover in use.
- `assets/audio/voiceover-alt-hf_alpha.wav`: the other female voice, for comparison.
- `assets/audio/voiceover.lines.json`: sentence start and end times.
- `assets/audio/voiceover.words.json`: word times from Whisper.

## Customizations

- English words stay in Latin script for ElevenLabs; initials and numbers are spelled out in Devanagari.
