---
name: godot-game-dev
description: >
  Godot game development assistance — GDScript coding, scene setup,
  physics, UI, shaders, and project organization. Helps with Godot 4.x
  best practices and common patterns.
license: MIT
compatibility:
  claude-code: ">=1.0.0"
  opencode: ">=1.0.0"
---

# Godot Game Development

## When to use
- User is working on a Godot project
- Need help with GDScript, scenes, or nodes
- Physics, UI, or shader questions
- Project structure and organization

## Capabilities

### GDScript
- Script writing and debugging
- Node references and signals
- State machines and patterns
- Performance optimization

### Scenes & Nodes
- Scene tree structure
- Node types and usage
- Instancing and delegation
- Export variables

### Physics
- CharacterBody2D/3D
- RigidBody2D/3D
- Area detection
- Collision layers

### UI
- Control nodes layout
- Theme customization
- Responsive design
- Input handling

### Shaders
- CanvasItem shaders
- Spatial shaders
- Visual shader tips
- Performance considerations

## Workflow

1. **Understand the goal** — What game mechanic or feature?
2. **Check existing code** — Look at current scripts and scenes
3. **Implement** — Write GDScript or suggest scene changes
4. **Test** — Remind to test in Godot editor

## Best Practices

- Use signals for communication
- Prefer composition over inheritance
- Keep scenes small and focused
- Use @export for configurable values
- Name nodes descriptively

## Common Patterns

- State pattern for player/enemy AI
- Event bus for global signals
- Autoload for singletons
- Resource for data objects