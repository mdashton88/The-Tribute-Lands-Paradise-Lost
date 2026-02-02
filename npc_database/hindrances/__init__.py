"""
Hindrances Catalogue for the Tribute Lands NPC Database.

Modular structure — one file per source:
  - core.py             Savage Worlds core rules
  - fantasy_companion.py   Fantasy Companion additions
  - ammaria.py          Ammaria regional hindrances
  - saltlands.py        Saltlands regional hindrances
  - vinlands.py         Vinlands regional hindrances
  - concordium.py       Concordium regional hindrances

Each module exports: SOURCE, HINDRANCES
"""

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
HINDRANCES = []

for mod in _MODULES:
    HINDRANCES.extend(_tag_items(mod.HINDRANCES, mod.SOURCE))


def get_hindrances(source=None, severity=None):
    """Get hindrances, optionally filtered by source and/or severity."""
    results = HINDRANCES
    if source and source != "All":
        results = [h for h in results if h["source"] == source]
    if severity and severity != "All":
        results = [h for h in results if h["severity"] == severity]
    return results
