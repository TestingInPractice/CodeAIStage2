---
name: godot-2d-graphics
description: Use when working with 2D-specific systems — TileMaps, parallax scrolling, 2D lights and shadows, canvas layers, particles 2D, custom drawing, and 2D meshes in Godot 4.3+
---

# 2D Graphics

## Goal

Implement 2D graphics systems in Godot 4.x: TileMaps, parallax scrolling, 2D lighting, canvas layers, particles, and custom drawing following best practices.

## Instructions

1. **Set up canvas layers** — Use `CanvasLayer` for separate rendering layers (HUD, background, foreground). Higher `layer` values draw on top.

2. **Configure draw order** — Within a canvas layer, nodes draw in scene tree order. Use `z_index` to override without rearranging the tree.

3. **Implement TileMaps** — Use `TileMapLayer` (Godot 4.3+) for tile-based levels:
   - Create TileSet resource with tile definitions
   - Paint tiles in the editor
   - Use `set_cell()` for runtime modifications

4. **Add parallax scrolling** — Use `ParallaxBackground` and `ParallaxLayer` for depth effects:
   - Set `motion_scale` for speed difference
   - Configure `repeat_size` for infinite scrolling

5. **Set up 2D lighting** — Use `PointLight2D`, `DirectionalLight2D`, `LightOccluder2D`:
   - Add `CanvasModulate` for ambient light
   - Configure light textures and energy

6. **Add 2D particles** — Use `GPUParticles2D` or `CPUParticles2D`:
   - Configure emission shape, amount, lifetime
   - Set gravity, velocity, color parameters

7. **Custom drawing** — Override `_draw()` for procedural graphics:
   ```gdscript
   func _draw() -> void:
       draw_circle(Vector2.ZERO, 50, Color.RED)
   ```

## Constraints

- NEVER use old `TileMap` node — use `TileMapLayer` (Godot 4.3+)
- NEVER draw outside `_draw()` — all drawing must happen in this callback
- NEVER use `update()` (deprecated) — use `queue_redraw()` (Godot 4.x)
- ALWAYS use `z_index` for draw order instead of reordering scene tree
- ALWAYS configure parallax `repeat_size` for infinite scrolling

## Examples

**Example 1: TileMap level**
```
Input: "Create a platformer level with tiles"
Output:
- TileMapLayer with TileSet resource
- Ground, platforms, decorations tiles
- Collision shapes on solid tiles
- set_cell() for runtime tile changes
```

**Example 2: Parallax background**
```
Input: "Add scrolling mountain background"
Output:
- ParallaxBackground with ParallaxLayer
- motion_scale = Vector2(0.5, 0.5) for slower scroll
- repeat_size for infinite horizontal scrolling
- Background sprite with texture
```

**Example 3: 2D lighting**
```
Input: "Add torch lights to dungeon"
Output:
- PointLight2D with torch texture
- Light energy and color configuration
- LightOccluder2D for shadows
- CanvasModulate for ambient darkness
```
