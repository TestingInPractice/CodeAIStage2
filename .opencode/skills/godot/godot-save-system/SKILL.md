---
name: godot-save-system
description: Use when implementing save/load systems — ConfigFile, JSON, Resource serialization, save game architecture
---

# Save / Load Systems

## Goal

Implement save/load systems in Godot 4.x: settings persistence, game state serialization, and save file management following best practices.

## Instructions

1. **Choose the right strategy**:
   - `ConfigFile` — Settings, simple key-value data (INI-style, built-in)
   - `JSON` — Game saves, flexible structures (cross-platform, version-migratable)
   - `Resource .tres/.res` — Editor-integrated data (NOT secure for user data)

2. **Set up save architecture**:
   ```
   SaveManager (Autoload singleton)
   ├── save_game(slot: int) → void
   ├── load_game(slot: int) → void
   └── get_save_slots() → Array[String]
   ```

3. **Implement ConfigFile for settings**:
   ```gdscript
   var config = ConfigFile.new()
   config.set_value("audio", "music_volume", 0.8)
   config.save("user://settings.cfg")
   ```

4. **Implement JSON for game saves**:
   ```gdscript
   var save_data = {"level": 5, "score": 1200, "inventory": [...]}
   var file = FileAccess.open("user://save_1.json", FileAccess.WRITE)
   file.store_string(JSON.stringify(save_data))
   ```

5. **Handle version migration** — Add version field to save data. On load, check version and migrate if needed.

6. **Persist settings** — Save audio, video, controls settings on game launch and settings change.

## Constraints

- NEVER load Resource files (.tres/.res) from untrusted sources — they execute arbitrary GDScript
- NEVER use `File` class (deprecated) — use `FileAccess` (Godot 4.x)
- NEVER block the main thread for large file I/O — use background threads on mobile
- NEVER save to `res://` — use `user://` for save files
- ALWAYS add version field to save data for migration
- ALWAYS handle FileAccess open errors gracefully

## Examples

**Example 1: Basic save/load**
```
Input: "Save and load player progress (level, score, inventory)"
Output:
- SaveManager autoload singleton
- save_game(slot) and load_game(slot) functions
- JSON serialization with version field
- Error handling for missing/corrupt files
```

**Example 2: Settings persistence**
```
Input: "Save audio and video settings"
Output:
- ConfigFile with sections: audio, video, controls
- get_value() with defaults for first launch
- Settings menu connected to save/load
- Auto-save on settings change
```

**Example 3: Save slot system**
```
Input: "Multiple save slots with preview"
Output:
- Save slot selection UI
- save_1.json, save_2.json, save_3.json
- Preview shows level, playtime, timestamp
- Overwrite confirmation dialog
```
