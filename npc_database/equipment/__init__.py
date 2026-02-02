"""
Equipment Catalogue for the Tribute Lands NPC Database.

Modular structure — one file per source:
  - core.py            Savage Worlds core rules
  - fantasy_companion.py  Fantasy Companion additions
  - ammaria.py         Ammaria regional equipment
  - saltlands.py       Saltlands regional equipment
  - vinlands.py        Vinlands regional equipment
  - concordium.py      Concordium regional equipment

Each module exports: SOURCE, WEAPONS, ARMOR, GEAR
"""

VERSION = {
    "version": "1.0.0",
    "updated": "2025-02-02",
    "changes": "Initial modular structure — 168 items across 6 sources"
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


# Combined catalogues with source tags
WEAPONS = []
ARMOR = []
GEAR = []

for mod in _MODULES:
    WEAPONS.extend(_tag_items(mod.WEAPONS, mod.SOURCE))
    ARMOR.extend(_tag_items(mod.ARMOR, mod.SOURCE))
    GEAR.extend(_tag_items(mod.GEAR, mod.SOURCE))


def get_weapons(source=None):
    """Get weapons, optionally filtered by source."""
    if source and source != "All":
        return [w for w in WEAPONS if w["source"] == source]
    return WEAPONS


def get_armor(source=None):
    """Get armour, optionally filtered by source."""
    if source and source != "All":
        return [a for a in ARMOR if a["source"] == source]
    return ARMOR


def get_gear(source=None):
    """Get gear, optionally filtered by source."""
    if source and source != "All":
        return [g for g in GEAR if g["source"] == source]
    return GEAR
