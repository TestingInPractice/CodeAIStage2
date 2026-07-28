---
name: godot-ui-children
description: Use when building user interfaces — Control nodes, themes, anchors, containers, and layout patterns
---

# Godot UI

## Goal

Build user interfaces in Godot 4.x: Control nodes, themes, anchors, containers, and layout patterns following best practices.

## Instructions

1. **Understand Control vs Node2D**:
   - `Control` — UI nodes with anchor-based layout, focus system, theme support
   - `Node2D` — World-space nodes with position/rotation/scale
   - Use Control for all UI elements

2. **Set up scene structure**:
   ```
   UI (Control)
   ├── MarginContainer
   │   └── VBoxContainer
   │       ├── Label
   │       ├── Button
   │       └── HBoxContainer
   ```

3. **Use containers** — Let containers arrange children automatically:
   - `VBoxContainer` — Vertical layout
   - `HBoxContainer` — Horizontal layout
   - `GridContainer` — Grid layout
   - `MarginContainer` — Add margins
   - `CenterContainer` — Center children

4. **Configure anchors** — Set how controls resize with parent:
   ```gdscript
   # Full screen
   set_anchors_preset(Control.PRESET_FULL_RECT)
   
   # Center
   set_anchors_preset(Control.PRESET_CENTER)
   ```

5. **Apply themes** — Use Theme resources for consistent styling:
   - Create Theme resource
   - Set colors, fonts, styleboxes for each control type
   - Apply theme to parent container (children inherit)

6. **Handle focus** — Configure keyboard/gamepad navigation:
   ```gdscript
   $Button.focus_mode = Control.FOCUS_ALL
   $Button.grab_focus()
   ```

## Constraints

- NEVER use Node2D for UI — always use Control nodes
- NEVER hardcode positions — use anchors and containers
- NEVER set anchors in `_ready()` — set in editor or use presets
- ALWAYS use containers for automatic layout
- ALWAYS set focus_mode for keyboard/gamepad navigation

## Examples

**Example 1: Main menu**
```
Input: "Create a main menu with play, settings, quit buttons"
Output:
- Control node with anchors_preset = PRESET_FULL_RECT
- VBoxContainer for vertical button layout
- Three Button nodes with labels
- Theme for consistent styling
- Focus navigation between buttons
```

**Example 2: HUD**
```
Input: "Add health bar and score display"
Output:
- CanvasLayer for HUD (separate from game world)
- HBoxContainer for horizontal layout
- ProgressBar for health
- Label for score
- Anchored to top-left corner
```

**Example 3: Responsive dialog**
```
Input: "Create a dialog box that centers on screen"
Output:
- CenterContainer with anchors_preset = PRESET_FULL_RECT
- PanelContainer for dialog background
- VBoxContainer for content
- Label for text
- HBoxContainer for buttons
```
