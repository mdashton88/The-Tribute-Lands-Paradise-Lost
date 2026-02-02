#!/usr/bin/env python3
"""
Tribute Lands NPC Database Manager
DiceForge Studios Ltd

Command-line tool for managing NPCs across all regional modules.
Designed for quick data entry during writing sessions.

Usage:
    python npc_manager.py add
    python npc_manager.py list [--region REGION] [--tier TIER] [--org ORG]
    python npc_manager.py show <name_or_id>
    python npc_manager.py search <query>
    python npc_manager.py edit <id> <field> <value>
    python npc_manager.py add-skill <npc_id> <skill_name> <die>
    python npc_manager.py add-weapon <npc_id> (interactive)
    python npc_manager.py add-org <org_name> <region> [type]
    python npc_manager.py link-org <npc_id> <org_name> [role]
    python npc_manager.py link-npc <npc_id_a> <npc_id_b> <relationship>
    python npc_manager.py appear <npc_id> <product> [role]
    python npc_manager.py status [--region REGION]
    python npc_manager.py export-statblock <name_or_id>
    python npc_manager.py init
"""

import sqlite3
import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime

DB_PATH = Path(__file__).parent / "tribute_lands_npcs.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"

# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db():
    conn = get_db()
    with open(SCHEMA_PATH, 'r') as f:
        conn.executescript(f.read())
    conn.commit()
    conn.close()
    print(f"Database initialised at {DB_PATH}")

# ============================================================
# DICE HELPERS
# ============================================================

def die_str(value):
    """Convert integer die value to string: 8 -> 'd8'"""
    if value and value > 0:
        return f"d{value}"
    return "—"

def parse_die(s):
    """Convert die string to integer: 'd8' -> 8, '8' -> 8"""
    s = str(s).strip().lower().replace('d', '')
    return int(s)

# ============================================================
# ADD NPC (Interactive)
# ============================================================

def add_npc_interactive():
    conn = get_db()
    print("\n=== ADD NEW NPC ===\n")
    
    name = input("Name: ").strip()
    if not name:
        print("Name required.")
        return
    
    title = input("Title/Role (e.g. 'Professional Fixer'): ").strip() or None
    
    print("\nRegions: Ammaria, Saltlands, Vinlands, Concordium, Glasrya, Global")
    region = input("Region: ").strip()
    if region not in ('Ammaria', 'Saltlands', 'Vinlands', 'Concordium', 'Glasrya', 'Global'):
        print(f"Invalid region: {region}")
        return
    
    print("\nTiers: Wild Card, Extra, Walk-On")
    tier = input("Tier: ").strip()
    if tier not in ('Wild Card', 'Extra', 'Walk-On'):
        print(f"Invalid tier: {tier}")
        return
    
    archetype = input("Archetype (combat/social/criminal/scholarly/maritime/wilderness/spellcaster): ").strip() or None
    
    print("\nRanks: Novice, Seasoned, Veteran, Heroic, Legendary (or blank)")
    rank = input("Rank guideline: ").strip() or None
    
    quote = input("\nSignature quote: ").strip() or None
    
    print("\n--- Attributes (enter die size: 4, 6, 8, 10, 12 — or 0 to skip) ---")
    agi = int(input("  Agility: ") or 0)
    sma = int(input("  Smarts: ") or 0)
    spi = int(input("  Spirit: ") or 0)
    stre = int(input("  Strength: ") or 0)
    vig = int(input("  Vigor: ") or 0)
    
    pace = int(input("\nPace [6]: ") or 6)
    parry = int(input("Parry [2]: ") or 2)
    tough = int(input("Toughness [5]: ") or 5)
    tough_arm = int(input("Toughness (armor) [0]: ") or 0)
    
    bennies = 0
    if tier == 'Wild Card':
        bennies = int(input("Bennies [3]: ") or 3)
    
    source = input("\nSource document (e.g. '201_Ammaria'): ").strip() or None
    
    cursor = conn.execute("""
        INSERT INTO npcs (name, title, region, tier, archetype, rank_guideline,
                         quote, agility, smarts, spirit, strength, vigor,
                         pace, parry, toughness, toughness_armor, bennies,
                         source_document)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (name, title, region, tier, archetype, rank, quote,
          agi, sma, spi, stre, vig, pace, parry, tough, tough_arm,
          bennies, source))
    
    npc_id = cursor.lastrowid
    conn.commit()
    
    print(f"\n✓ Created NPC #{npc_id}: {name}")
    
    if input("\nAdd skills now? (y/n): ").strip().lower() == 'y':
        add_skills_interactive(conn, npc_id)
    
    if input("Add weapons now? (y/n): ").strip().lower() == 'y':
        add_weapon_interactive(conn, npc_id)
    
    conn.close()

def add_skills_interactive(conn, npc_id):
    print("\nEnter skills (name die, e.g. 'Fighting 8'). Blank line to finish.")
    while True:
        line = input("  Skill: ").strip()
        if not line:
            break
        parts = line.rsplit(None, 1)
        if len(parts) != 2:
            print("  Format: SkillName DieSize (e.g. 'Fighting 8')")
            continue
        skill_name, die_val = parts[0], parse_die(parts[1])
        try:
            conn.execute(
                "INSERT INTO npc_skills (npc_id, name, die) VALUES (?, ?, ?)",
                (npc_id, skill_name, die_val)
            )
            conn.commit()
            print(f"    ✓ {skill_name} d{die_val}")
        except sqlite3.IntegrityError:
            print(f"    ! {skill_name} already exists for this NPC")

def add_weapon_interactive(conn, npc_id):
    # Look up NPC strength for damage resolution
    npc = conn.execute("SELECT strength, name FROM npcs WHERE id=?", (npc_id,)).fetchone()
    str_die = npc['strength'] if npc else 0
    
    print(f"\nAdding weapons for {npc['name']} (Str d{str_die})")
    print("Blank name to finish.\n")
    
    while True:
        wname = input("  Weapon name: ").strip()
        if not wname:
            break
        damage_str = input("  Damage (e.g. 'Str+d8', '2d6'): ").strip()
        
        # Auto-resolve Str for FG damagedice
        damagedice = damage_str
        if 'Str' in damage_str and str_die > 0:
            damagedice = damage_str.replace('Str', f'd{str_die}')
        
        print(f"    FG damagedice will be: {damagedice}")
        override = input("    Override? (blank to accept): ").strip()
        if override:
            damagedice = override
        
        trait_type = input("  Type (Melee/Ranged/Thrown) [Melee]: ").strip() or "Melee"
        ap = int(input("  AP [0]: ") or 0)
        rng = input("  Range (e.g. '15/30/60', blank for melee): ").strip() or None
        reach = int(input("  Reach [0]: ") or 0)
        notes = input("  Notes (e.g. 'Two hands, AP 2'): ").strip() or None
        
        conn.execute("""
            INSERT INTO npc_weapons (npc_id, name, damage_str, damagedice, 
                                    armor_piercing, trait_type, range, reach, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (npc_id, wname, damage_str, damagedice, ap, trait_type, rng, reach, notes))
        conn.commit()
        print(f"    ✓ {wname}")

# ============================================================
# BATCH ADD (from dict — useful for scripted imports)
# ============================================================

def add_npc_from_dict(data):
    """Add an NPC from a dictionary. Returns the new NPC id."""
    conn = get_db()
    
    skills = data.pop('skills', {})
    weapons = data.pop('weapons', [])
    armor = data.pop('armor', [])
    orgs = data.pop('organisations', [])
    appearances = data.pop('appearances', [])
    
    # Build insert from whatever fields are provided
    fields = [k for k in data.keys() if k not in ('skills', 'weapons', 'armor', 'organisations', 'appearances')]
    placeholders = ', '.join(['?'] * len(fields))
    columns = ', '.join(fields)
    values = [data[f] for f in fields]
    
    # Convert list fields to JSON
    for i, f in enumerate(fields):
        if f.endswith('_json') and isinstance(values[i], list):
            values[i] = json.dumps(values[i])
    
    cursor = conn.execute(
        f"INSERT INTO npcs ({columns}) VALUES ({placeholders})", values
    )
    npc_id = cursor.lastrowid
    
    # Add skills
    for skill_name, die_val in skills.items():
        conn.execute(
            "INSERT INTO npc_skills (npc_id, name, die) VALUES (?, ?, ?)",
            (npc_id, skill_name, parse_die(die_val))
        )
    
    # Add weapons
    for w in weapons:
        conn.execute("""
            INSERT INTO npc_weapons (npc_id, name, damage_str, damagedice,
                                    armor_piercing, trait_type, range, reach, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (npc_id, w['name'], w['damage_str'], w['damagedice'],
              w.get('ap', 0), w.get('trait_type', 'Melee'),
              w.get('range'), w.get('reach', 0), w.get('notes')))
    
    # Add armor
    for a in armor:
        conn.execute("""
            INSERT INTO npc_armor (npc_id, name, protection, area_protected, min_strength, notes)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (npc_id, a['name'], a.get('protection', 0), a.get('area_protected'),
              a.get('min_strength'), a.get('notes')))
    
    conn.commit()
    conn.close()
    return npc_id

# ============================================================
# LIST / SEARCH / SHOW
# ============================================================

def list_npcs(region=None, tier=None, org=None, incomplete=False):
    conn = get_db()
    
    query = "SELECT * FROM v_npc_overview WHERE 1=1"
    params = []
    
    if region:
        query += " AND region = ?"
        params.append(region)
    if tier:
        query += " AND tier = ?"
        params.append(tier)
    if org:
        query += " AND organisations LIKE ?"
        params.append(f"%{org}%")
    if incomplete:
        query += " AND (stat_block_complete = 0 OR narrative_complete = 0)"
    
    query += " ORDER BY region, tier, name"
    
    rows = conn.execute(query, params).fetchall()
    
    if not rows:
        print("No NPCs found.")
        return
    
    print(f"\n{'ID':>4}  {'Name':<25} {'Region':<12} {'Tier':<12} {'Arch':<10} {'Stats':>5} {'Narr':>4} {'FG':>3}  Orgs")
    print("-" * 100)
    
    for r in rows:
        stat = "✓" if r['stat_block_complete'] else "·"
        narr = "✓" if r['narrative_complete'] else "·"
        fg = "✓" if r['fg_export_ready'] else "·"
        orgs = r['organisations'] or ""
        print(f"{r['id']:>4}  {r['name']:<25} {r['region']:<12} {r['tier']:<12} {(r['archetype'] or ''):>10} {stat:>5} {narr:>4} {fg:>3}  {orgs}")
    
    print(f"\nTotal: {len(rows)} NPCs")
    conn.close()

def show_npc(identifier):
    conn = get_db()
    
    # Try by ID first, then by name
    try:
        npc_id = int(identifier)
        npc = conn.execute("SELECT * FROM npcs WHERE id=?", (npc_id,)).fetchone()
    except ValueError:
        npc = conn.execute("SELECT * FROM npcs WHERE name LIKE ?", (f"%{identifier}%",)).fetchone()
    
    if not npc:
        print(f"NPC not found: {identifier}")
        return
    
    # Header
    tier_marker = " (Wild Card)" if npc['tier'] == 'Wild Card' else ""
    print(f"\n{'='*60}")
    title_str = f" — {npc['title']}" if npc['title'] else ""
    print(f"{npc['name']}{title_str}{tier_marker}")
    print(f"{'='*60}")
    
    if npc['quote']:
        print(f'\n"{npc["quote"]}"')
    
    if npc['description']:
        print(f"\n{npc['description']}")
    
    if npc['background']:
        print(f"\n{npc['background']}")
    
    # Stat block
    if npc['agility'] > 0:
        print(f"\nAttributes: Agility {die_str(npc['agility'])}, "
              f"Smarts {die_str(npc['smarts'])}, Spirit {die_str(npc['spirit'])}, "
              f"Strength {die_str(npc['strength'])}, Vigor {die_str(npc['vigor'])}")
    
    # Skills
    skills = conn.execute(
        "SELECT name, die FROM npc_skills WHERE npc_id=? ORDER BY name", 
        (npc['id'],)
    ).fetchall()
    if skills:
        skill_str = ", ".join(f"{s['name']} {die_str(s['die'])}" for s in skills)
        print(f"Skills: {skill_str}")
    
    # Derived
    if npc['agility'] > 0:
        tough_str = str(npc['toughness'])
        if npc['toughness_armor'] > 0:
            tough_str += f" ({npc['toughness_armor']})"
        print(f"Pace: {npc['pace']}; Parry: {npc['parry']}; Toughness: {tough_str}")
    
    # Edges, Hindrances, Gear
    edges = json.loads(npc['edges_json']) if npc['edges_json'] else []
    hindrances = json.loads(npc['hindrances_json']) if npc['hindrances_json'] else []
    gear = json.loads(npc['gear_json']) if npc['gear_json'] else []
    
    if hindrances:
        print(f"Hindrances: {', '.join(hindrances)}")
    if edges:
        print(f"Edges: {', '.join(edges)}")
    if gear:
        print(f"Gear: {', '.join(gear)}")
    
    # Weapons
    weapons = conn.execute(
        "SELECT * FROM npc_weapons WHERE npc_id=?", (npc['id'],)
    ).fetchall()
    if weapons:
        print("\nWeapons:")
        for w in weapons:
            notes = f" — {w['notes']}" if w['notes'] else ""
            rng = f", Range {w['range']}" if w['range'] else ""
            print(f"  {w['name']}: {w['damage_str']}{rng}{notes}")
    
    # Powers
    if npc['power_points'] > 0:
        powers = json.loads(npc['powers_json']) if npc['powers_json'] else []
        print(f"\nPowers ({npc['power_points']} PP): {', '.join(powers)}")
    
    # Narrative
    if npc['motivation']:
        print(f"\nWhat They Want: {npc['motivation']}")
    if npc['secret']:
        print(f"Their Secret: {npc['secret']}")
    if npc['tactics']:
        print(f"Tactics: {npc['tactics']}")
    if npc['services']:
        print(f"Services: {npc['services']}")
    if npc['adventure_hook']:
        print(f"Adventure Hook: {npc['adventure_hook']}")
    
    # Organisations
    orgs = conn.execute("""
        SELECT o.name, no2.role FROM npc_organisations no2
        JOIN organisations o ON o.id = no2.org_id
        WHERE no2.npc_id = ?
    """, (npc['id'],)).fetchall()
    if orgs:
        org_str = ", ".join(f"{o['name']} ({o['role']})" if o['role'] else o['name'] for o in orgs)
        print(f"\nOrganisations: {org_str}")
    
    # Connections
    connections = conn.execute("""
        SELECT n.name, c.relationship, c.notes
        FROM npc_connections c
        JOIN npcs n ON n.id = c.npc_id_b
        WHERE c.npc_id_a = ?
        UNION
        SELECT n.name, c.relationship, c.notes
        FROM npc_connections c
        JOIN npcs n ON n.id = c.npc_id_a
        WHERE c.npc_id_b = ?
    """, (npc['id'], npc['id'])).fetchall()
    if connections:
        print("\nConnections:")
        for c in connections:
            notes = f" — {c['notes']}" if c['notes'] else ""
            print(f"  {c['name']} ({c['relationship']}){notes}")
    
    # Appearances
    appearances = conn.execute(
        "SELECT * FROM npc_appearances WHERE npc_id=?", (npc['id'],)
    ).fetchall()
    if appearances:
        print("\nAppearances:")
        for a in appearances:
            role = f" [{a['role']}]" if a['role'] else ""
            print(f"  {a['product']}{role}")
    
    # Status
    print(f"\n--- Status ---")
    print(f"Stat block: {'Complete' if npc['stat_block_complete'] else 'Incomplete'}")
    print(f"Narrative: {'Complete' if npc['narrative_complete'] else 'Incomplete'}")
    print(f"FG export: {'Ready' if npc['fg_export_ready'] else 'Not ready'}")
    if npc['source_document']:
        print(f"Source: {npc['source_document']}")
    
    conn.close()

def search_npcs(query):
    conn = get_db()
    rows = conn.execute("""
        SELECT id, name, title, region, tier, archetype
        FROM npcs 
        WHERE name LIKE ? OR title LIKE ? OR description LIKE ? 
              OR background LIKE ? OR motivation LIKE ? OR quote LIKE ?
              OR notes LIKE ?
        ORDER BY name
    """, tuple(f"%{query}%" for _ in range(7))).fetchall()
    
    if not rows:
        print(f"No NPCs matching '{query}'")
        return
    
    for r in rows:
        title = f" — {r['title']}" if r['title'] else ""
        print(f"  #{r['id']:>3}  {r['name']}{title}  [{r['region']}, {r['tier']}]")
    
    conn.close()

# ============================================================
# EDIT
# ============================================================

def edit_npc(npc_id, field, value):
    conn = get_db()
    
    # Handle JSON fields
    json_fields = ['edges_json', 'hindrances_json', 'gear_json', 'powers_json', 'special_abilities_json']
    if field in json_fields:
        # Allow comma-separated input
        if not value.startswith('['):
            value = json.dumps([v.strip() for v in value.split(',')])
    
    # Handle boolean fields
    bool_fields = ['stat_block_complete', 'narrative_complete', 'fg_export_ready']
    if field in bool_fields:
        value = 1 if value.lower() in ('1', 'true', 'yes', 'y') else 0
    
    try:
        conn.execute(f"UPDATE npcs SET {field} = ? WHERE id = ?", (value, npc_id))
        conn.commit()
        print(f"✓ Updated NPC #{npc_id}: {field} = {value}")
    except Exception as e:
        print(f"Error: {e}")
    
    conn.close()

# ============================================================
# ORGANISATION AND LINKING COMMANDS
# ============================================================

def add_organisation(name, region, org_type=None):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO organisations (name, region, type) VALUES (?, ?, ?)",
            (name, region, org_type)
        )
        conn.commit()
        print(f"✓ Added organisation: {name} ({region})")
    except sqlite3.IntegrityError:
        print(f"Organisation '{name}' already exists")
    conn.close()

def link_org(npc_id, org_name, role=None):
    conn = get_db()
    org = conn.execute("SELECT id FROM organisations WHERE name LIKE ?", (f"%{org_name}%",)).fetchone()
    if not org:
        print(f"Organisation not found: {org_name}")
        conn.close()
        return
    try:
        conn.execute(
            "INSERT INTO npc_organisations (npc_id, org_id, role) VALUES (?, ?, ?)",
            (npc_id, org['id'], role)
        )
        conn.commit()
        npc = conn.execute("SELECT name FROM npcs WHERE id=?", (npc_id,)).fetchone()
        print(f"✓ Linked {npc['name']} to {org_name}" + (f" as {role}" if role else ""))
    except sqlite3.IntegrityError:
        print("Link already exists")
    conn.close()

def link_npcs(id_a, id_b, relationship):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO npc_connections (npc_id_a, npc_id_b, relationship) VALUES (?, ?, ?)",
            (id_a, id_b, relationship)
        )
        conn.commit()
        a = conn.execute("SELECT name FROM npcs WHERE id=?", (id_a,)).fetchone()
        b = conn.execute("SELECT name FROM npcs WHERE id=?", (id_b,)).fetchone()
        print(f"✓ {a['name']} ↔ {b['name']} ({relationship})")
    except sqlite3.IntegrityError:
        print("Connection already exists")
    conn.close()

def add_appearance(npc_id, product, role=None):
    conn = get_db()
    try:
        conn.execute(
            "INSERT INTO npc_appearances (npc_id, product, role) VALUES (?, ?, ?)",
            (npc_id, product, role)
        )
        conn.commit()
        npc = conn.execute("SELECT name FROM npcs WHERE id=?", (npc_id,)).fetchone()
        print(f"✓ {npc['name']} appears in {product}" + (f" as {role}" if role else ""))
    except sqlite3.IntegrityError:
        print("Appearance already recorded")
    conn.close()

# ============================================================
# STATUS REPORT
# ============================================================

def status_report(region=None):
    conn = get_db()
    
    if region:
        rows = conn.execute(
            "SELECT * FROM v_region_status WHERE region = ?", (region,)
        ).fetchall()
    else:
        rows = conn.execute("SELECT * FROM v_region_status").fetchall()
    
    if not rows:
        print("No data.")
        return
    
    print(f"\n{'Region':<12} {'Tier':<12} {'Total':>5} {'Stats':>5} {'Narr':>5} {'FG':>5}")
    print("-" * 55)
    
    for r in rows:
        print(f"{r['region']:<12} {r['tier']:<12} {r['total']:>5} "
              f"{r['stats_done']:>5} {r['narrative_done']:>5} {r['fg_ready']:>5}")
    
    # Grand totals
    totals = conn.execute("""
        SELECT COUNT(*) as total, 
               SUM(stat_block_complete) as stats,
               SUM(narrative_complete) as narr,
               SUM(fg_export_ready) as fg
        FROM npcs
    """ + (" WHERE region = ?" if region else ""),
        (region,) if region else ()
    ).fetchone()
    
    print("-" * 55)
    print(f"{'TOTAL':<25} {totals['total']:>5} {totals['stats']:>5} "
          f"{totals['narr']:>5} {totals['fg']:>5}")
    
    conn.close()

# ============================================================
# EXPORT STAT BLOCK (formatted text)
# ============================================================

def export_statblock(identifier):
    """Export a formatted SWADE stat block for use in documents."""
    conn = get_db()
    
    try:
        npc_id = int(identifier)
        npc = conn.execute("SELECT * FROM npcs WHERE id=?", (npc_id,)).fetchone()
    except ValueError:
        npc = conn.execute("SELECT * FROM npcs WHERE name LIKE ?", (f"%{identifier}%",)).fetchone()
    
    if not npc:
        print(f"NPC not found: {identifier}")
        return
    
    # Format stat block
    lines = []
    
    wc = " (Wild Card)" if npc['tier'] == 'Wild Card' else ""
    lines.append(f"**{npc['name']}{wc}**")
    
    if npc['quote']:
        lines.append(f'*"{npc["quote"]}"*')
    
    if npc['description']:
        lines.append(f"\n{npc['description']}")
    
    lines.append("")
    
    if npc['agility'] > 0:
        lines.append(
            f"**Attributes:** Agility {die_str(npc['agility'])}, "
            f"Smarts {die_str(npc['smarts'])}, Spirit {die_str(npc['spirit'])}, "
            f"Strength {die_str(npc['strength'])}, Vigor {die_str(npc['vigor'])}"
        )
    
    skills = conn.execute(
        "SELECT name, die FROM npc_skills WHERE npc_id=? ORDER BY name",
        (npc['id'],)
    ).fetchall()
    if skills:
        skill_str = ", ".join(f"{s['name']} {die_str(s['die'])}" for s in skills)
        lines.append(f"**Skills:** {skill_str}")
    
    if npc['agility'] > 0:
        tough_str = str(npc['toughness'])
        if npc['toughness_armor'] > 0:
            tough_str += f" ({npc['toughness_armor']})"
        lines.append(f"**Pace:** {npc['pace']}; **Parry:** {npc['parry']}; **Toughness:** {tough_str}")
    
    hindrances = json.loads(npc['hindrances_json']) if npc['hindrances_json'] else []
    edges = json.loads(npc['edges_json']) if npc['edges_json'] else []
    gear = json.loads(npc['gear_json']) if npc['gear_json'] else []
    
    if hindrances:
        lines.append(f"**Hindrances:** {', '.join(hindrances)}")
    if edges:
        lines.append(f"**Edges:** {', '.join(edges)}")
    if gear:
        lines.append(f"**Gear:** {', '.join(gear)}")
    
    special = json.loads(npc['special_abilities_json']) if npc['special_abilities_json'] else []
    if special:
        lines.append("**Special Abilities:**")
        for sa in special:
            lines.append(f"  • {sa}")
    
    if npc['power_points'] > 0:
        powers = json.loads(npc['powers_json']) if npc['powers_json'] else []
        lines.append(f"**Powers ({npc['power_points']} PP):** {', '.join(powers)}")
    
    if npc['tactics']:
        lines.append(f"**Tactics:** {npc['tactics']}")
    
    print("\n".join(lines))
    conn.close()

# ============================================================
# CLI ENTRY POINT
# ============================================================

def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return
    
    cmd = sys.argv[1]
    
    if cmd == 'init':
        init_db()
    
    elif cmd == 'add':
        add_npc_interactive()
    
    elif cmd == 'list':
        region = None
        tier = None
        org = None
        incomplete = False
        i = 2
        while i < len(sys.argv):
            if sys.argv[i] == '--region' and i+1 < len(sys.argv):
                region = sys.argv[i+1]; i += 2
            elif sys.argv[i] == '--tier' and i+1 < len(sys.argv):
                tier = sys.argv[i+1]; i += 2
            elif sys.argv[i] == '--org' and i+1 < len(sys.argv):
                org = sys.argv[i+1]; i += 2
            elif sys.argv[i] == '--incomplete':
                incomplete = True; i += 1
            else:
                i += 1
        list_npcs(region, tier, org, incomplete)
    
    elif cmd == 'show':
        if len(sys.argv) < 3:
            print("Usage: show <name_or_id>")
            return
        show_npc(' '.join(sys.argv[2:]))
    
    elif cmd == 'search':
        if len(sys.argv) < 3:
            print("Usage: search <query>")
            return
        search_npcs(' '.join(sys.argv[2:]))
    
    elif cmd == 'edit':
        if len(sys.argv) < 5:
            print("Usage: edit <id> <field> <value>")
            return
        edit_npc(int(sys.argv[2]), sys.argv[3], ' '.join(sys.argv[4:]))
    
    elif cmd == 'add-skill':
        if len(sys.argv) < 5:
            print("Usage: add-skill <npc_id> <skill_name> <die>")
            return
        conn = get_db()
        npc_id = int(sys.argv[2])
        skill_name = sys.argv[3]
        die_val = parse_die(sys.argv[4])
        conn.execute(
            "INSERT OR REPLACE INTO npc_skills (npc_id, name, die) VALUES (?, ?, ?)",
            (npc_id, skill_name, die_val)
        )
        conn.commit()
        print(f"✓ {skill_name} d{die_val}")
        conn.close()
    
    elif cmd == 'add-weapon':
        if len(sys.argv) < 3:
            print("Usage: add-weapon <npc_id>")
            return
        conn = get_db()
        add_weapon_interactive(conn, int(sys.argv[2]))
        conn.close()
    
    elif cmd == 'add-org':
        if len(sys.argv) < 4:
            print("Usage: add-org <name> <region> [type]")
            return
        org_type = sys.argv[4] if len(sys.argv) > 4 else None
        add_organisation(sys.argv[2], sys.argv[3], org_type)
    
    elif cmd == 'link-org':
        if len(sys.argv) < 4:
            print("Usage: link-org <npc_id> <org_name> [role]")
            return
        role = sys.argv[4] if len(sys.argv) > 4 else None
        link_org(int(sys.argv[2]), sys.argv[3], role)
    
    elif cmd == 'link-npc':
        if len(sys.argv) < 5:
            print("Usage: link-npc <id_a> <id_b> <relationship>")
            return
        link_npcs(int(sys.argv[2]), int(sys.argv[3]), sys.argv[4])
    
    elif cmd == 'appear':
        if len(sys.argv) < 4:
            print("Usage: appear <npc_id> <product> [role]")
            return
        role = sys.argv[4] if len(sys.argv) > 4 else None
        add_appearance(int(sys.argv[2]), sys.argv[3], role)
    
    elif cmd == 'status':
        region = sys.argv[3] if len(sys.argv) > 3 and sys.argv[2] == '--region' else None
        status_report(region)
    
    elif cmd == 'export-statblock':
        if len(sys.argv) < 3:
            print("Usage: export-statblock <name_or_id>")
            return
        export_statblock(' '.join(sys.argv[2:]))
    
    else:
        print(f"Unknown command: {cmd}")
        print(__doc__)

if __name__ == '__main__':
    main()
