---
name: godot-touch-input
description: "Expert blueprint for mobile platforms (Android/iOS) covering touch controls, virtual joysticks, responsive UI, safe areas (notches), battery optimization, and app store guidelines. Use when targeting mobile releases or implementing touch input. Keywords mobile, Android, iOS, touch, InputEventScreenTouch, virtual joystick, safe area, battery, app store, orientation."
---

# Mobile Touch Input

## Goal

Implement mobile touch input in Godot 4.x: touch controls, virtual joysticks, responsive UI, safe areas, battery optimization, and platform-specific features.

## Instructions

1. **Use touch events** — Never use mouse events for touch interaction:
   ```gdscript
   func _input(event: InputEvent) -> void:
       if event is InputEventScreenTouch:
           if event.pressed:
               on_touch_start(event.position)
           else:
               on_touch_end(event.position)
       elif event is InputEventScreenDrag:
           on_touch_drag(event.position, event.relative)
   ```

2. **Handle safe areas** — Query `DisplayServer.get_display_safe_area()` and offset critical UI:
   ```gdscript
   var safe_area = DisplayServer.get_display_safe_area()
   $UI.offset_top = safe_area.position.y
   $UI.offset_left = safe_area.position.x
   ```

3. **Implement virtual joystick** — Create a virtual joystick for movement:
   - Use `TouchScreenButton` or custom `Control`
   - Track touch position relative to center
   - Output normalized direction vector

4. **Optimize for mobile**:
   - Use Mobile or Compatibility renderer (not Forward+)
   - Enable ETC2/ASTC texture compression
   - Drop FPS when backgrounded: `Engine.max_fps = 1`

5. **Handle orientation** — Connect to `get_viewport().size_changed` signal:
   ```gdscript
   func _ready() -> void:
       get_viewport().size_changed.connect(_on_resize)
   ```

6. **Request permissions** — On Android, request permissions explicitly:
   ```gdscript
   OS.request_permission("VIBRATE")
   ```

## Constraints

- NEVER use `InputEventMouseButton` for touch — use `InputEventScreenTouch`
- NEVER ignore safe areas (notches/cutouts) — UI behind notch is unusable
- NEVER use Forward+ renderer for mobile — use Mobile or Compatibility
- NEVER maintain 60 FPS when backgrounded — drop to 1 FPS
- NEVER leave ETC2/ASTC disabled — uncompressed textures crash mobile
- NEVER assume Android permissions are automatic — request explicitly
- ALWAYS use `InputEventScreenTouch` and `InputEventScreenDrag` for multi-touch
- ALWAYS handle `size_changed` signal for orientation changes

## Examples

**Example 1: Basic touch input**
```
Input: "Add touch controls for mobile player"
Output:
- _input() handling InputEventScreenTouch and InputEventScreenDrag
- Touch start/end callbacks
- Touch drag with position tracking
- Movement based on touch position
```

**Example 2: Virtual joystick**
```
Input: "Create virtual joystick for movement"
Output:
- Custom Control node with touch handling
- Joystick base and knob sprites
- Normalized direction vector output
- Dead zone for small movements
```

**Example 3: Safe area UI**
```
Input: "Make UI work on notched phones"
Output:
- DisplayServer.get_display_safe_area() query
- UI offsets for top/bottom/left/right
- MarginContainer with safe area margins
- Test on different screen sizes
```
