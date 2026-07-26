#!/usr/bin/env python3
"""Import knowledge from docs/knowledge/ and docs/sources.json into graph-mem."""

import json
import os
import re
from pathlib import Path

PROJECT_DIR = Path("/Users/halapinvv/Documents/Agents/CodeAIStage2")
KNOWLEDGE_DIR = PROJECT_DIR / "docs" / "knowledge"
SOURCES_FILE = PROJECT_DIR / "docs" / "sources.json"
OUTPUT_FILE = PROJECT_DIR / ".graphmem" / "import.json"
GRAPHMEM_BIN = PROJECT_DIR / ".venv-graphmem" / "bin" / "graph-mem"


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
            # Handle lists like [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            fm[key] = val
    return fm


def parse_wikilinks(content: str) -> list[str]:
    """Extract [[wikilinks]] from markdown."""
    return re.findall(r"\[\[([^\]]+)\]\]", content)


def extract_observations(content: str, frontmatter: dict) -> list[str]:
    """Extract key observations from markdown content."""
    observations = []
    # Skip frontmatter
    body = re.sub(r"^---\n.*?\n---\n", "", content, flags=re.DOTALL)

    # Extract section headers as context
    sections = re.split(r"^##\s+", body, flags=re.MULTILINE)
    for section in sections[1:]:  # skip first (before any header)
        lines = section.strip().split("\n")
        if lines:
            header = lines[0].strip()
            # Get first meaningful paragraph
            for line in lines[1:]:
                line = line.strip()
                if line and not line.startswith("#") and not line.startswith("|") and not line.startswith("---"):
                    # Clean markdown formatting
                    clean = re.sub(r"\*\*(.*?)\*\*", r"\1", line)
                    clean = re.sub(r"\[\[([^\]]+)\]\]", r"\1", clean)
                    clean = re.sub(r"`([^`]+)`", r"\1", clean)
                    if len(clean) > 10:
                        observations.append(clean)
                        break
    return observations[:5]  # max 5 observations per file


def md_to_entity(filepath: Path) -> dict | None:
    """Convert a markdown file to a graph-mem entity."""
    content = filepath.read_text(encoding="utf-8")
    fm = parse_frontmatter(content)

    if not fm.get("type"):
        return None

    name = filepath.stem
    entity_type = fm.get("type", "concept")
    source = fm.get("source", "")
    tags = fm.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.strip("[]").split(",")]

    description = f"{entity_type.title()}: {name}"
    if source:
        description += f" (source: {source})"

    observations = extract_observations(content, fm)
    if not observations:
        observations = [f"Entry about {name} in category {entity_type}"]

    # Get related entries
    related = fm.get("related", [])
    if isinstance(related, str):
        related = [r.strip() for r in related.strip("[]").split(",") if r.strip()]

    return {
        "name": name,
        "type": entity_type,
        "description": description,
        "observations": observations,
        "tags": tags,
        "related": related,
        "source": source,
    }


def sources_to_entities(sources_file: Path) -> list[dict]:
    """Convert sources.json entries to graph-mem entities."""
    if not sources_file.exists():
        return []

    data = json.loads(sources_file.read_text(encoding="utf-8"))
    entities = []

    for src in data.get("sources", []):
        name = src.get("name", "unknown")
        slug = re.sub(r"[^a-z0-9-]", "-", name.lower()).strip("-")
        source_type = src.get("type", "tool")
        url = src.get("url", "")
        description = src.get("description", f"{source_type}: {name}")
        tags = src.get("tags", [])
        category = src.get("category", "")

        observations = []
        if url:
            observations.append(f"URL: {url}")
        if category:
            observations.append(f"Category: {category}")
        if description:
            observations.append(description)

        entities.append({
            "name": slug,
            "type": source_type,
            "description": description,
            "observations": observations[:3],
            "tags": tags if isinstance(tags, list) else [],
            "related": [],
            "source": url,
        })

    return entities


def build_import_json(md_entities: list[dict], source_entities: list[dict]) -> dict:
    """Build the graph-mem import JSON."""
    import uuid

    all_entities = md_entities + source_entities
    entities_json = []
    relationships_json = []
    observations_json = []
    seen_names = set()
    name_to_id = {}

    # Deduplicate by name, assign IDs
    for ent in all_entities:
        name = ent["name"]
        if name in seen_names:
            continue
        seen_names.add(name)

        entity_id = str(uuid.uuid4())
        name_to_id[name] = entity_id

        entities_json.append({
            "id": entity_id,
            "name": name,
            "entity_type": ent["type"],
            "description": ent["description"],
        })

    # Add observations with entity IDs
    for ent in all_entities:
        name = ent["name"]
        if name not in name_to_id:
            continue
        entity_id = name_to_id[name]

        for obs_text in ent.get("observations", []):
            observations_json.append({
                "entity_id": entity_id,
                "content": obs_text,
                "source": "",
            })

    # Add relationships with entity IDs
    for ent in all_entities:
        name = ent["name"]
        if name not in name_to_id:
            continue
        source_id = name_to_id[name]

        for related_name in ent.get("related", []):
            if related_name and related_name in name_to_id:
                target_id = name_to_id[related_name]
                relationships_json.append({
                    "source_id": source_id,
                    "target_id": target_id,
                    "relationship_type": "RELATES_TO",
                    "weight": 0.8,
                })

    return {
        "version": "1.0.0",
        "entities": entities_json,
        "relationships": relationships_json,
        "observations": observations_json,
        "skipped": [],
    }


def main():
    # Parse markdown files (skip templates and INDEX.md)
    md_entities = []
    for md_file in sorted(KNOWLEDGE_DIR.rglob("*.md")):
        if md_file.name == "INDEX.md" or "templates" in str(md_file):
            continue
        ent = md_to_entity(md_file)
        if ent:
            md_entities.append(ent)
            print(f"  [md] {ent['name']} ({ent['type']})")

    # Parse sources.json
    source_entities = sources_to_entities(SOURCES_FILE)
    for ent in source_entities:
        print(f"  [src] {ent['name']} ({ent['type']})")

    # Build import JSON
    import_data = build_import_json(md_entities, source_entities)

    # Write output
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(json.dumps(import_data, indent=2, ensure_ascii=False), encoding="utf-8")

    print(f"\nImport file ready: {OUTPUT_FILE}")
    print(f"  Entities: {len(import_data['entities'])}")
    print(f"  Relationships: {len(import_data['relationships'])}")
    print(f"  Observations: {len(import_data['observations'])}")


if __name__ == "__main__":
    main()
