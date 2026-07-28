---
name: godot-audio
description: Use when implementing audio — audio buses, AudioStreamPlayer, spatial audio, music management, SFX pooling, and dynamic mixing
---

# Audio System

## Goal

Implement audio systems in Godot 4.x: background music, sound effects, spatial audio, bus management, and adaptive music following best practices.

## Instructions

1. **Set up audio buses** — Create Master, Music, SFX buses at minimum. Add sub-bus groups for fine-tuning (Footsteps, Weapons, UI).

2. **Choose the right node**:
   - `AudioStreamPlayer` — Non-positional: music, UI sounds, global SFX
   - `AudioStreamPlayer2D` — 2D positional: footsteps, gunfire, environmental
   - `AudioStreamPlayer3D` — 3D positional: same as 2D but in 3D space

3. **Configure audio resources**:
   - Music: OGG Vorbis (small files, good quality)
   - Short SFX: WAV (no decode latency)
   - Looping: Configure on the AudioStream resource, not in code

4. **Implement music manager** — Use an autoload singleton for crossfading between tracks. Manage two AudioStreamPlayer nodes and tween their volume_db.

5. **Implement SFX pool** — Pre-instantiate a fixed pool of AudioStreamPlayer nodes. `play_sfx(stream)` finds the next free player and plays. Avoids per-shot instancing churn.

6. **Wire volume controls** — Use `linear_to_db()` / `db_to_linear()` for UI sliders. Persist settings with ConfigFile.

7. **Add spatial audio** — Set `max_distance`, `attenuation`, `panning_strength` on positional players. Use AudioListener2D/3D only when needed.

## Constraints

- NEVER use `get_node()` inside `_process()` — cache references with `@onready`
- NEVER use MP3 for timing-critical SFX — use WAV (MP3 adds encoder padding)
- NEVER set volume to 0.0 with `linear_to_db(0.0)` — it returns `-inf`. Mute the bus instead
- NEVER create new AudioStreamPlayer nodes dynamically — use an SFX pool
- NEVER configure looping in code — configure on the AudioStream resource
- NEVER use stereo files for 3D spatial audio — use Force Mono in Import tab
- ALWAYS assign the correct `bus` property on all AudioStreamPlayer nodes
- ALWAYS use OGG for music, WAV for short SFX

## Examples

**Example 1: Basic audio playback**
```
Input: "Add background music and jump sound effect"
Output:
- AudioStreamPlayer for music (bus = "Music")
- AudioStreamPlayer2D for SFX (bus = "SFX")
- Music autoload to survive scene changes
- play_jump_sound() function with preload()
```

**Example 2: Volume control**
```
Input: "Add volume slider for music and SFX"
Output:
- HSlider nodes for Music and SFX
- set_bus_volume_linear() using linear_to_db()
- ConfigFile persistence for saved settings
- Near-zero values mute the bus
```

**Example 3: Spatial audio**
```
Input: "Enemy footsteps should be positional in 2D"
Output:
- AudioStreamPlayer2D as child of enemy
- max_distance = 1000.0
- attenuation = 1.0
- max_polyphony = 4 for overlapping steps
```
