"""
Edges Catalogue for the Tribute Lands NPC Database.

Modular structure — one file per source:
  - core.py             Savage Worlds core rules
  - fantasy_companion.py   Fantasy Companion additions
  - ammaria.py          Ammaria regional edges
  - saltlands.py        Saltlands regional edges
  - vinlands.py         Vinlands regional edges
  - concordium.py       Concordium regional edges

Each module exports: SOURCE, EDGES
"""

VERSION = {
    "version": "1.0.0",
    "updated": "2025-02-02",
    "changes": "Initial modular structure — 193 edges across 6 sources"
}

from . import core
from . import fantasy_companion
from . import ammaria
from . import saltlands
from . import vinlands
from . import concordium

# All source modules in order
_MODULES = [core, fantasy_companion, ammaria, saltlands, vinlands, concordium]

# Source names for filtering
SOURCES = [m.SOURCE for m in _MODULES]


def _tag_items(items, source):
    """Add source tag to each item."""
    return [{**item, "source": source} for item in items]


# Combined catalogue with source tags
EDGES = []

for mod in _MODULES:
    EDGES.extend(_tag_items(mod.EDGES, mod.SOURCE))


def get_edges(source=None, rank=None, edge_type=None):
    """Get edges, optionally filtered by source, rank, and/or type."""
    results = EDGES
    if source and source != "All":
        results = [e for e in results if e["source"] == source]
    if rank and rank != "All":
        results = [e for e in results if e["rank"] == rank]
    if edge_type and edge_type != "All":
        results = [e for e in results if e["type"] == edge_type]
    return results
