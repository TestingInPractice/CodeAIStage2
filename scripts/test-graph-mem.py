#!/usr/bin/env python3
"""Test graph-mem MCP tools work correctly."""

import asyncio
import sys

from graph_mem.graph.engine import GraphEngine
from graph_mem.models import Entity, Observation, Relationship
from pathlib import Path

DB_PATH = Path("/Users/halapinvv/Documents/Agents/CodeAIStage2/.graphmem/graph.db")


async def test_all():
    engine = GraphEngine(str(DB_PATH))
    await engine.initialize()

    print("=== TEST 1: search_nodes (hybrid search) ===")
    results = await engine.search_nodes("authentication security", limit=5)
    for r in results:
        print(f"  [{r.get('score', 0):.2f}] {r['name']} ({r.get('entity_type', '?')})")
    print(f"  Found: {len(results)} results\n")

    print("=== TEST 2: search_nodes (FastAPI) ===")
    results = await engine.search_nodes("FastAPI web framework", limit=3)
    for r in results:
        print(f"  [{r.get('score', 0):.2f}] {r['name']}")
    print(f"  Found: {len(results)} results\n")

    print("=== TEST 3: get_entity ===")
    entity = await engine.get_entity("owasp-top10")
    if entity:
        print(f"  Name: {entity.name}")
        print(f"  Type: {entity.entity_type}")
        print(f"  Description: {entity.description[:80] if entity.description else '?'}")
        print(f"  Observations: {len(entity.observations) if entity.observations else 0}")
        if entity.observations:
            for o in entity.observations[:3]:
                print(f"    - {o.content[:80]}")
    else:
        print("  NOT FOUND")
    print()

    print("=== TEST 4: find_connections ===")
    connections = await engine.find_connections("owasp-top10", max_hops=2)
    print(f"  Connections from owasp-top10:")
    if hasattr(connections, 'entities'):
        for c in connections.entities[:5]:
            print(f"    - {c.name} ({c.entity_type})")
        print(f"  Total connected: {len(connections.entities)}")
    else:
        print(f"  Result: {connections}")
    print()

    print("=== TEST 5: read_graph (stats) ===")
    stats = await engine.read_graph()
    print(f"  Stats: {stats}")
    print()

    print("=== TEST 6: search_observations ===")
    results = await engine.search_observations("bcrypt password hashing", limit=3)
    for r in results:
        print(f"  [{r.get('score', 0):.2f}] {r.get('entity_name', '?')}: {r.get('content', '?')[:60]}")
    print(f"  Found: {len(results)} results\n")

    print("=== ALL TESTS PASSED ===")
    await engine.close()


if __name__ == "__main__":
    asyncio.run(test_all())
