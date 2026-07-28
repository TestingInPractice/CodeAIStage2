---
name: godot-game-dev
description: >
  Godot game development assistance — GDScript coding, scene setup,
  physics, UI, shaders, and project organization. Helps with Godot 4.x
  best practices and common patterns.
---

# Godot Game Development

## Goal

Provide expert assistance for Godot 4.x game development: GDScript coding, scene architecture, physics, UI, shaders, and project organization following best practices.

## Instructions

1. **Analyze the request** — Understand what game mechanic, feature, or problem the user needs help with.

2. **Check existing code** — Before writing new code, examine current scripts and scenes to understand the project structure and conventions.

3. **Follow Godot conventions**:
   - Use typed GDScript (`var speed: int = 200`, `func move() -> void:`)
   - Prefer `@onready` for node references over `get_node()` in `_ready()`
   - Use signals for inter-node communication ("signal up, call down")
   - Keep scenes small and focused on one responsibility

4. **Implement the solution**:
   - Write clean, typed GDScript
   - Use appropriate node types (CharacterBody2D for players, Area2D for triggers, etc.)
   - Add `@export` for configurable values
   - Follow the script structure: signals → enums → exports → vars → lifecycle → public → private

5. **Validate** — Ensure the code follows Godot 4.x patterns and doesn't use deprecated APIs.

6. **Test guidance** — Remind the user to test in the Godot editor and check the debugger for errors.

## Constraints

- NEVER use `get_node()` inside `_process()` — cache references with `@onready`
- NEVER use string-based signal connections (`connect("signal", ...)`) — use Callable references
- NEVER use `yield()` — use `await` (Godot 4.x)
- NEVER mix `@onready` and `@export` on the same variable
- NEVER use `InputEventMouseButton` for mobile touch — use `InputEventScreenTouch`
- NEVER use Forward+ renderer for mobile — use Mobile or Compatibility
- ALWAYS use typed GDScript for performance and error detection
- ALWAYS follow "signal up, call down" pattern for node communication

## Examples

**Example 1: Player movement with typed GDScript**
```
Input: "Make a platformer player that can run and jump"
Output:
- CharacterBody2D with CollisionShape2D
- Player.gd with SPEED, JUMP_VELOCITY constants
- _physics_process(delta) with gravity, movement, and move_and_slide()
- Input mapping for ui_left, ui_right, ui_accept
```

**Example 2: Signal communication**
```
Input: "Enemy should notify parent when player enters detection zone"
Output:
- Area2D with CollisionShape2D for detection zone
- signal player_detected(player: Node2D) declaration
- _on_body_entered() emitting the signal
- Parent connecting to the signal in _ready()
```

**Example 3: State machine pattern**
```
Input: "Add a state machine for enemy AI (idle, patrol, chase)"
Output:
- State base class with enter(), exit(), tick() methods
- StateMachine node managing current_state
- Individual state scripts (IdleState, PatrolState, ChaseState)
- State transitions via transition_to() method
```
