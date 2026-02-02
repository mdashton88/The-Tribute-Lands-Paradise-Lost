# Tribute Lands NPC Database
## DiceForge Studios Ltd

A SQLite database and Python toolkit for managing NPCs across all five regional supplements, with direct export to Fantasy Grounds Unity XML format.

---

## Quick Start

```bash
# Initialise the database and seed with existing NPCs
python seed_data.py

# List all NPCs
python npc_manager.py list

# List by region or tier
python npc_manager.py list --region Ammaria
python npc_manager.py list --tier "Wild Card"
python npc_manager.py list --org Brotherhood

# Show NPC detail (by ID or name)
python npc_manager.py show 2
python npc_manager.py show "Jorin"

# Search across all text fields
python npc_manager.py search "smuggling"

# Production status report
python npc_manager.py status
python npc_manager.py status --region Ammaria
```

## Adding NPCs

```bash
# Interactive mode (prompts for all fields)
python npc_manager.py add

# Edit individual fields after creation
python npc_manager.py edit 1 quote "New quote here"
python npc_manager.py edit 1 edges_json "Charismatic, Block, Combat Reflexes"
python npc_manager.py edit 1 stat_block_complete yes

# Add skills and weapons
python npc_manager.py add-skill 1 Fighting 8
python npc_manager.py add-weapon 1
```

## Cross-Referencing

```bash
# Organisations
python npc_manager.py add-org "Moonstar Consortium" Ammaria Guild
python npc_manager.py link-org 1 "Moonstar" Member

# NPC connections
python npc_manager.py link-npc 1 4 ally

# Product appearances
python npc_manager.py appear 1 "AM_Week_03" Antagonist
```

## Fantasy Grounds Export

```bash
# Export a region as a complete FG module
python fg_export.py --region Ammaria --full-module -o ammaria_db.xml

# Export just the NPC section (for pasting into existing db.xml)
python fg_export.py --region Ammaria -o ammaria_npcs.xml

# Export a single NPC
python fg_export.py --npc "Jorin" -o single.xml

# Export all complete NPCs across all regions
python fg_export.py --all -o all_npcs.xml
```

## Stat Block Export (for Word documents)

```bash
# Formatted markdown stat block, ready for the module
python npc_manager.py export-statblock "Tam"
```

## File Structure

| File | Purpose |
|------|---------|
| `schema.sql` | Database schema — run once to initialise |
| `npc_manager.py` | CLI for all NPC operations |
| `fg_export.py` | Fantasy Grounds XML export |
| `seed_data.py` | Populate with existing NPCs |
| `tribute_lands_npcs.db` | The database file (auto-created) |

## Schema Overview

The database stores NPCs in a single main table with JSON fields for list data (edges, hindrances, gear) and separate tables for structured data that needs individual querying (skills, weapons) or cross-referencing (organisations, connections, appearances).

**Why this split?** FG XML needs individual `<skill>` and `<weaponlist>` entries with specific typed attributes. Edges and gear are just flat text strings in FG, so JSON storage is simpler and faster to maintain.

## Production Tracking

Each NPC has three status flags:

- `stat_block_complete` — All mechanical data entered and validated
- `narrative_complete` — Quote, description, background, motivation, secret
- `fg_export_ready` — Reviewed and approved for FG module inclusion

Use `python npc_manager.py list --incomplete` to find NPCs needing work.

---

*Up the Irons.*
