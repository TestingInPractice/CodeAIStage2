---
name: godot-tween-animation
description: Use when implementing tweens — property animation, method tweening, chaining, parallel sequences, easing, and common UI/gameplay motion recipes
---

# Tween Animation

## Goal

Implement code-driven animations in Godot 4.x using Tweens: property animation, method calls, chaining, parallel sequences, and common motion recipes.

## Instructions

1. **Choose Tween vs AnimationPlayer**:
   - Tween — Procedural motion, UI transitions, VFX (code-only, lightweight)
   - AnimationPlayer — Complex multi-track, artist-tuned animations (reusable resources)

2. **Create a tween** — Tweens auto-bind to the node. When the node is freed, the tween stops.
   ```gdscript
   var tween = create_tween()
   tween.tween_property($Sprite2D, "modulate:a", 0.0, 0.5)
   ```

3. **Chain tweens** — Sequential by default:
   ```gdscript
   tween.tween_property($Node, "position:x", 100, 0.5)
   tween.tween_property($Node, "position:y", 200, 0.5)
   ```

4. **Parallel tweens** — Use `set_parallel(true)`:
   ```gdscript
   tween.set_parallel(true)
   tween.tween_property($Sprite, "position:x", 100, 0.5)
   tween.tween_property($Sprite, "modulate", Color.RED, 0.5)
   ```

5. **Use easing curves** — Apply easing for smooth motion:
   ```gdscript
   tween.tween_property($Node, "position:x", 100, 0.5).set_ease(Tween.EASE_OUT).set_trans(Tween.TRANS_CUBIC)
   ```

6. **Method calls** — Use `tween_callback()` or `tween_method()`:
   ```gdscript
   tween.tween_callback(func(): print("Done!"))
   tween.tween_method(set_value, 0.0, 1.0, 1.0)
   ```

7. **Loop tweens** — Use `set_loops()` or `set_parallel()` with `chain()`.

## Constraints

- NEVER use `tween.stop()` inside `_process()` — tweens auto-stop when node is freed
- NEVER create tweens in `_process()` — create once and reuse or chain
- NEVER use `interpolate_property()` (Godot 3.x) — use `tween_property()` (Godot 4.x)
- ALWAYS use typed properties: `tween_property($Node, "position:x", 100, 0.5)`
- ALWAYS handle tween completion with `tween_callback()` or `finished` signal

## Examples

**Example 1: Fade in effect**
```
Input: "Fade in a UI element over 0.5 seconds"
Output:
- create_tween()
- tween_property(modulate:a, 0.0 → 1.0, 0.5)
- set_ease(EASE_OUT) for smooth finish
```

**Example 2: Bounce animation**
```
Input: "Bounce a sprite when collected"
Output:
- create_tween().set_loops(1)
- tween_property(scale, Vector2(1.5, 1.5), 0.15)
- tween_property(scale, Vector2(1, 1), 0.15)
- set_ease(EASE_OUT).set_trans(TRANS_ELASTIC)
```

**Example 3: UI slide transition**
```
Input: "Slide menu in from left"
Output:
- create_tween()
- position:x from -200 to 0, 0.3s
- set_ease(EASE_OUT).set_trans(TRANS_CUBIC)
- tween_callback(grab_focus) on completion
```
