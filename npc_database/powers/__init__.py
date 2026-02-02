"""
Powers Catalogue for the Tribute Lands NPC Database.

Modular structure — one file per source:
  - core.py             Savage Worlds core rules
  - fantasy_companion.py   Fantasy Companion additions
  - ammaria.py          Ammaria regional powers
  - saltlands.py        Saltlands regional powers
  - vinlands.py         Vinlands regional powers
  - concordium.py       Concordium regional powers

Each module exports: SOURCE, POWERS
"""

VERSION = {
    "version": "1.0.0",
    "updated": "2025-02-02",
    "changes": "Initial modular structure — 106 powers across 6 sources"
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
POWERS = []

for mod in _MODULES:
    POWERS.extend(_tag_items(mod.POWERS, mod.SOURCE))


def get_powers(source=None, rank=None):
    """Get powers, optionally filtered by source and/or rank."""
    results = POWERS
    if source and source != "All":
        results = [p for p in results if p["source"] == source]
    if rank and rank != "All":
        results = [p for p in results if p["rank"] == rank]
    return results
