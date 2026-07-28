---
name: godot-animation
description: Use when implementing animations — AnimationPlayer, AnimationTree, blend trees, state machines, sprite animation, and code-driven animation
---

# Animation System

## Goal

Implement animations in Godot 4.x: keyframe animation, blending, state machines, sprite animation, and code-driven animation following best practices.

## Instructions

1. **Choose the right node**:
   - `AnimationPlayer` — Simple playback, one-shot effects (low complexity)
   - `AnimationTree` — Blending, transitions, layered animation (medium-high complexity)
   - Start with AnimationPlayer. Add AnimationTree when you need blending (walk/run blend, directional movement, layered upper/lower body).

2. **Set up scene structure**:
   ```
   Character (CharacterBody2D)
   ├── Sprite2D
   └── AnimationPlayer
   ```

3. **Create animation clips** — Add tracks in the Animation panel: keyframe properties, method calls, audio playback.

4. **Trigger from code**:
   - AnimationPlayer: `$AnimationPlayer.play("walk")`
   - AnimationTree: `$AnimationTree["parameters/blend_position"] = velocity`

5. **Use AnimationTree for blending**:
   - Set `TreeRoot` to `AnimationNodeStateMachine` or `AnimationNodeBlendTree`
   - Connect to AnimationPlayer via `AnimationMixer.root_animation`
   - Use `travel()` for state machine transitions

6. **Sprite animation** — Use AnimatedSprite2D for frame-by-frame animation. Set `sprite_frames` resource with animation definitions.

## Constraints

- NEVER use `AnimationPlayer.play()` inside `_process()` — use `_ready()` or signal triggers
- NEVER forget to set `AnimationTree.active = true` — animations won't play without it
- NEVER mix `AnimationPlayer` and `AnimationTree` on the same node — use one or the other
- NEVER use deprecated `play_backwards()` — use `play("anim", -1.0)` for reverse playback
- ALWAYS use typed animation names: `$AnimationPlayer.play("walk")` not `$AnimationPlayer.play(0)`
- ALWAYS call `animation_finished` signal for cleanup logic

## Examples

**Example 1: Basic AnimationPlayer**
```
Input: "Add idle and walk animations for player"
Output:
- AnimationPlayer with "idle" and "walk" clips
- Sprite2D with SpriteFrames resource
- GDScript: play("walk") on movement, play("idle") when stopped
- animation_finished signal for one-shot cleanup
```

**Example 2: AnimationTree state machine**
```
Input: "Blend between walk and run based on speed"
Output:
- AnimationTree with AnimationNodeStateMachine
- States: Idle → Walk → Run
- Parameters: blend_position (Vector2)
- Code: $AnimationTree["parameters/blend_position"] = velocity
```

**Example 3: Sprite frame animation**
```
Input: "Animated character with frame-by-frame sprite animation"
Output:
- AnimatedSprite2D with SpriteFrames
- Animations: idle (4 frames), walk (6 frames), jump (3 frames)
- play("walk") on movement
- Frame connections for sound effects
```
