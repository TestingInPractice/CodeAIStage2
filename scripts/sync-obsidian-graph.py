#!/usr/bin/env python3
"""Bidirectional sync between Obsidian vault (docs/knowledge/) and graph-mem.

Usage:
    python3 sync-obsidian-graph.py md2graph    # Obsidian → Graph
    python3 sync-obsidian-graph.py graph2md    # Graph → Obsidian
    python3 sync-obsidian-graph.py status      # Show sync status
"""

import json
import re
import subprocess
import sys
from pathlib import Path

PROJECT_DIR = Path("/Users/halapinvv/Documents/Agents/CodeAIStage2")
KNOWLEDGE_DIR = PROJECT_DIR / "docs" / "knowledge"
GRAPH_DB = PROJECT_DIR / ".graphmem" / "graph.db"
TEMPLATES_DIR = KNOWLEDGE_DIR / "templates"


def graph_mem_cmd(args: list[str]) -> str:
    """Run a graph-mem CLI command and return stdout."""
    graphmem_bin = PROJECT_DIR / ".venv-graphmem" / "bin" / "graph-mem"
    cmd = [
        str(graphmem_bin),
        *args,
        "--project-dir", str(PROJECT_DIR),
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
    if result.returncode != 0:
        print(f"Error: {result.stderr}", file=sys.stderr)
        return ""
    return result.stdout


def parse_frontmatter(content: str) -> dict:
    """Extract YAML frontmatter from markdown."""
    match = re.match(r"^---\n(.*?)\n---\n", content, re.DOTALL)
    if not match:
        return {}
    fm = {}
    for line in match.group(1).split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            fm[key] = val
    return fm


def md_to_graph_entity(filepath: Path) -> dict | None:
    """Convert a markdown file to a graph entity dict."""
    content = filepath.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)
    if not fm.get("type") or fm["type"] in ("index",):
        return None

    name = filepath.stem
    entity_type = fm.get("type", "concept")
    source = fm.get("source", "")
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip("[]").split(",")]

    # Build description from frontmatter
    desc_parts = [entity_type.title()]
    if source:
        desc_parts.append(f"Source: {source}")
    description = " — ".join(desc_parts)

    # Extract observations from body
    body = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)
    observations = []
    for section in re.split(r"^##\s+", body, flags=re.MULTILINE)[1:]:
        lines = section.strip().split("\n")
        if lines:
            for line in lines[1:]:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("---"):
                    clean = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
                    clean = re.sub(r"\[\[([^\]]+)\]\]", r"\1", clean)
                    clean = re.sub(r"`([^`]+)`", r"\1", clean)
                    if len(clean) > 10:
                        observations.append(clean)
                        break
    if not observations:
        observations = [f"Entry: {name}"]

    # Extract related from frontmatter
    related = fm.get("related", [])
    if isinstance(related, str):
        related = [r.strip() for r in related.strip("[]").split(",") if r.strip()]

    return {
        "name": name,
        "entity_type": entity_type,
        "description": description,
        "observations": observations[:5],
        "tags": tags,
        "related": related,
    }


def md2graph():
    """Sync Obsidian .md files → graph-mem."""
    print("=== Obsidian → Graph sync ===\n")

    entities = []
    for md_file in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        if md_file.name == "INDEX.md" or "templates" in str(md_file):
            continue
        ent = md_to_graph_entity(md_file)
        if ent:
            entities.append(ent)
            print(f"  [md] {ent['name']} ({ent['entity_type']})")

    if not entities:
        print("No entities found.")
        return

    # Create/update entities via graph-mem MCP tools
    # We'll use a temp JSON import file
    import uuid
    import tempfile

    name_to_id = {}
    entities_json = []
    observations_json = []

    for ent in entities:
        eid = str(uuid.uuid4())
        name_to_id[ent["name"]] = eid
        entities_json.append({
            "id": eid,
            "name": ent["name"],
            "entity_type": ent["entity_type"],
            "description": ent["description"],
        })
        for obs in ent["observations"]:
            observations_json.append({
                "entity_id": eid,
                "content": obs,
                "source": "",
            })

    # Build relationships
    relationships_json = []
    for ent in entities:
        source_id = name_to_id.get(ent["name"])
        if not source_id:
            continue
        for rel_name in ent.get("related", []):
            target_id = name_to_id.get(rel_name)
            if target_id:
                relationships_json.append({
                    "source_id": source_id,
                    "target_id": target_id,
                    "relationship_type": "RELATES_TO",
                    "weight": 0.8,
                })

    import_data = {
        "version": "1.0.0",
        "entities": entities_json,
        "relationships": relationships_json,
        "observations": observations_json,
    }

    with tempfile.NamedTemporaryFile(mode="w", suffix=".json", delete=False) as f:
        json.dump(import_data, f, ensure_ascii=False)
        tmp_path = f.name

    result = graph_mem_cmd(["import", tmp_path])
    print(f"\n{result}")
    Path(tmp_path).unlink(missing_ok=True)


def graph2md():
    """Sync graph-mem → Obsidian .md files."""
    print("=== Graph → Obsidian sync ===\n")

    # Export graph
    export_json = graph_mem_cmd(["export", "--format", "json"])
    if not export_json:
        print("Failed to export graph.")
        return

    data = json.loads(export_json)
    entities = data.get("entities", [])
    observations = data.get("observations", [])
    relationships = data.get("relationships", [])

    # Build observation map
    obs_map = {}
    for obs in observations:
        eid = obs.get("entity_id", "")
        if eid not in obs_map:
            obs_map[eid] = []
        obs_map[eid].append(obs.get("content", ""))

    # Build relationship map
    rel_map = {}
    for rel in relationships:
        src = rel.get("source_id", "")
        tgt = rel.get("target_id", "")
        if src not in rel_map:
            rel_map[src] = []
        rel_map[src].append(tgt)

    # Entity ID → name mapping
    id_to_name = {e["id"]: e["name"] for e in entities}

    synced = 0
    for entity in entities:
        eid = entity["id"]
        name = entity["name"]
        etype = entity.get("entity_type", "concept")
        desc = entity.get("description", "")

        # Determine directory
        dir_map = {
            "article": "articles",
            "concept": "concepts",
            "video": "videos",
            "book": "books",
            "roadmap": "projects",
            "repo": "articles",
            "tool": "articles",
            "lib": "articles",
            "standard": "concepts",
            "docs": "articles",
            "skill": "articles",
        }
        subdir = dir_map.get(etype, "articles")
        target_dir = KNOWLEDGE_DIR / subdir
        target_dir.mkdir(parents=True, exist_ok=True)
        target_file = target_dir / f"{name}.md"

        # Skip if file already exists (don't overwrite Obsidian edits)
        if target_file.exists():
            continue

        # Build markdown
        obs_list = obs_map.get(eid, [])
        related_ids = rel_map.get(eid, [])
        related_names = [id_to_name[rid] for rid in related_ids if rid in id_to_name]

        md_lines = [
            "---",
            f"type: {etype}",
            f"date: 2026-07-25",
            f"tags: []",
            f"related: {related_names}",
            "---",
            "",
            f"# {name}",
            "",
            f"## Описание",
            desc,
            "",
        ]

        if obs_list:
            md_lines.append("## Ключевые факты")
            for obs in obs_list:
                md_lines.append(f"- {obs}")
            md_lines.append("")

        target_file.write_text("\n".join(md_lines), encoding="utf-8")
        print(f"  [created] {target_file.relative_to(PROJECT_DIR)}")
        synced += 1

    print(f"\nSynced {synced} new files.")


def show_status():
    """Show sync status."""
    print("=== Sync Status ===\n")

    # Graph stats
    status = graph_mem_cmd(["status"])
    print("Graph-mem:")
    print(status)

    # Obsidian stats
    md_files = list(KNOWLEDGE_DIR.rglob("*.md"))
    md_files = [f for f in md_files if f.name != "INDEX.md" and "templates" not in str(f)]
    print(f"Obsidian files: {len(md_files)}")
    for subdir in sorted(KNOWLEDGE_DIR.iterdir()):
        if subdir.is_dir() and subdir.name not in (".obsidian", "templates", "people", "tags"):
            count = len(list(subdir.glob("*.md")))
            if count > 0:
                print(f"  {subdir.name}/: {count} files")


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    if cmd == "md2graph":
        md2graph()
    elif cmd == "graph2md":
        graph2md()
    elif cmd == "status":
        show_status()
    else:
        print(f"Unknown command: {cmd}")
        print("Usage: sync-obsidian-graph.py [md2graph|graph2md|status]")
