#!/usr/bin/env python3
"""
Tribute Lands FG XML Exporter
DiceForge Studios Ltd

Exports NPCs from the SQLite database to Fantasy Grounds Unity
compatible XML format. Generates the <npc> section of a db.xml file.

Usage:
    python fg_export.py --region Ammaria --output ammaria_npcs.xml
    python fg_export.py --region Ammaria --full-module --output db.xml
    python fg_export.py --npc "Lyssa Thorne" --output single_npc.xml
    python fg_export.py --all --output all_npcs.xml

The --full-module flag wraps output in a complete db.xml structure.
Without it, you get just the <npc> section for pasting into an
existing module.
"""

import sqlite3
import json
import sys
import argparse
import re
from pathlib import Path
from xml.sax.saxutils import escape

DB_PATH = Path(__file__).parent / "tribute_lands_npcs.db"

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn

def xml_escape(text):
    if not text:
        return ""
    return escape(str(text))

def make_id(name):
    """Convert NPC name to a valid XML element ID."""
    clean = re.sub(r'[^a-zA-Z0-9_]', '_', name.lower())
    clean = re.sub(r'_+', '_', clean).strip('_')
    return clean

def die_str(value):
    if value and value > 0:
        return f"d{value}"
    return ""

# ============================================================
# SINGLE NPC TO FG XML
# ============================================================

def npc_to_fg_xml(conn, npc, indent="        "):
    """Generate FG XML for a single NPC entry."""
    npc_id = make_id(npc['name'])
    lines = []
    i = indent
    i2 = indent + "    "
    i3 = indent + "        "
    i4 = indent + "            "
    
    lines.append(f'{i}<{npc_id}>')
    
    # Name
    name_open = '<name type="string">'
    name_close = '</name>'  # Using full close tag as per 506 reference
    lines.append(f'{i2}{name_open}{xml_escape(npc["name"])}{name_close}')
    
    # Wild Card flag
    if npc['tier'] == 'Wild Card':
        lines.append(f'{i2}<wildcard type="number">1</wildcard>')
        lines.append(f'{i2}<bennies type="number">{npc["bennies"] or 3}</bennies>')
    
    # Attributes
    for attr in ['agility', 'smarts', 'spirit', 'strength', 'vigor']:
        val = npc[attr]
        if val and val > 0:
            lines.append(f'{i2}<{attr} type="dice">{die_str(val)}</{attr}>')
    
    # Derived stats
    lines.append(f'{i2}<pace type="number">{npc["pace"] or 6}</pace>')
    lines.append(f'{i2}<parry type="number">{npc["parry"] or 2}</parry>')
    lines.append(f'{i2}<toughness type="number">{npc["toughness"] or 5}</toughness>')
    if npc['toughness_armor'] and npc['toughness_armor'] > 0:
        lines.append(f'{i2}<toughnessarmor type="number">{npc["toughness_armor"]}</toughnessarmor>')
    if npc['size'] and npc['size'] != 0:
        lines.append(f'{i2}<size type="number">{npc["size"]}</size>')
    
    # Skills
    skills = conn.execute(
        "SELECT name, die, modifier FROM npc_skills WHERE npc_id=? ORDER BY name",
        (npc['id'],)
    ).fetchall()
    
    if skills:
        lines.append(f'{i2}<skills>')
        for idx, s in enumerate(skills, 1):
            sid = f"id-{idx:05d}"
            lines.append(f'{i3}<{sid}>')
            lines.append(f'{i4}{name_open}{xml_escape(s["name"])}{name_close}')
            lines.append(f'{i4}<skill type="dice">{die_str(s["die"])}</skill>')
            lines.append(f'{i4}<adjustment type="number">{s["modifier"] or 0}</adjustment>')
            lines.append(f'{i4}<skillmod type="number">{s["modifier"] or 0}</skillmod>')
            lines.append(f'{i3}</{sid}>')
        lines.append(f'{i2}</skills>')
    
    # Edges
    edges = json.loads(npc['edges_json']) if npc['edges_json'] else []
    if edges:
        lines.append(f'{i2}<edges type="string">{xml_escape(", ".join(edges))}</edges>')
    
    # Hindrances
    hindrances = json.loads(npc['hindrances_json']) if npc['hindrances_json'] else []
    if hindrances:
        lines.append(f'{i2}<hindrances type="string">{xml_escape(", ".join(hindrances))}</hindrances>')
    
    # Gear
    gear = json.loads(npc['gear_json']) if npc['gear_json'] else []
    if gear:
        lines.append(f'{i2}<gear type="string">{xml_escape(", ".join(gear))}</gear>')
    
    # Weaponlist (structured for FG Combat tab)
    weapons = conn.execute(
        "SELECT * FROM npc_weapons WHERE npc_id=?", (npc['id'],)
    ).fetchall()
    
    if weapons:
        lines.append(f'{i2}<weaponlist>')
        for idx, w in enumerate(weapons, 1):
            wid = f"id-{idx:05d}"
            lines.append(f'{i3}<{wid}>')
            lines.append(f'{i4}{name_open}{xml_escape(w["name"])}{name_close}')
            lines.append(f'{i4}<damage type="string">{xml_escape(w["damage_str"])}</damage>')
            lines.append(f'{i4}<damagedice type="dice">{xml_escape(w["damagedice"])}</damagedice>')
            lines.append(f'{i4}<damagebonus type="number">{w["damage_bonus"] or 0}</damagebonus>')
            if w['armor_piercing'] and w['armor_piercing'] > 0:
                lines.append(f'{i4}<armorpiercing type="number">{w["armor_piercing"]}</armorpiercing>')
            lines.append(f'{i4}<traittype type="string">{w["trait_type"]}</traittype>')
            lines.append(f'{i4}<traitcount type="number">0</traitcount>')
            lines.append(f'{i4}<fumble type="number">1</fumble>')
            if w['range']:
                lines.append(f'{i4}<range type="string">{xml_escape(w["range"])}</range>')
            if w['reach'] and w['reach'] > 0:
                lines.append(f'{i4}<reach type="number">{w["reach"]}</reach>')
            else:
                lines.append(f'{i4}<reach type="number">0</reach>')
            if w['notes']:
                lines.append(f'{i4}<notes type="string">{xml_escape(w["notes"])}</notes>')
            lines.append(f'{i4}<bonuslist />')
            lines.append(f'{i4}<link type="windowreference"><class>weapon</class><recordname /></link>')
            lines.append(f'{i3}</{wid}>')
        lines.append(f'{i2}</weaponlist>')
    
    # Powers
    if npc['power_points'] and npc['power_points'] > 0:
        lines.append(f'{i2}<powerpoints type="number">{npc["power_points"]}</powerpoints>')
        powers = json.loads(npc['powers_json']) if npc['powers_json'] else []
        if powers:
            lines.append(f'{i2}<powers type="string">{xml_escape(", ".join(powers))}</powers>')
    
    # Special Abilities
    specials = json.loads(npc['special_abilities_json']) if npc['special_abilities_json'] else []
    if specials:
        lines.append(f'{i2}<specialabilities type="string">{xml_escape("; ".join(specials))}</specialabilities>')
    
    # Description (formatted text for FG)
    desc_parts = []
    if npc['quote']:
        desc_parts.append(f'<p><i>&quot;{xml_escape(npc["quote"])}&quot;</i></p>')
    if npc['description']:
        desc_parts.append(f'<p>{xml_escape(npc["description"])}</p>')
    if npc['background']:
        desc_parts.append(f'<p>{xml_escape(npc["background"])}</p>')
    if npc['motivation']:
        desc_parts.append(f'<p><b>What They Want:</b> {xml_escape(npc["motivation"])}</p>')
    if npc['secret']:
        desc_parts.append(f'<p><b>Their Secret:</b> {xml_escape(npc["secret"])}</p>')
    if npc['tactics']:
        desc_parts.append(f'<p><b>Tactics:</b> {xml_escape(npc["tactics"])}</p>')
    if npc['services']:
        desc_parts.append(f'<p><b>Services:</b> {xml_escape(npc["services"])}</p>')
    
    if desc_parts:
        desc_xml = ''.join(desc_parts)
        lines.append(f'{i2}<text type="formattedtext">{desc_xml}</text>')
    
    # Token reference (placeholder)
    token_name = make_id(npc['name'])
    lines.append(f'{i2}<token type="token">tokens/{token_name}.png</token>')
    
    lines.append(f'{i}</{npc_id}>')
    
    return '\n'.join(lines)

# ============================================================
# EXPORT FUNCTIONS
# ============================================================

def export_npcs(region=None, npc_name=None, full_module=False, export_all=False):
    conn = get_db()
    
    if npc_name:
        npcs = conn.execute(
            "SELECT * FROM npcs WHERE name LIKE ? AND fg_export_ready = 1",
            (f"%{npc_name}%",)
        ).fetchall()
        if not npcs:
            # Try without fg_export_ready filter
            npcs = conn.execute(
                "SELECT * FROM npcs WHERE name LIKE ?",
                (f"%{npc_name}%",)
            ).fetchall()
            if npcs:
                print(f"Note: NPC(s) found but not marked fg_export_ready. Exporting anyway.")
    elif export_all:
        npcs = conn.execute(
            "SELECT * FROM npcs WHERE stat_block_complete = 1 ORDER BY region, name"
        ).fetchall()
    elif region:
        npcs = conn.execute(
            "SELECT * FROM npcs WHERE region = ? AND stat_block_complete = 1 ORDER BY name",
            (region,)
        ).fetchall()
    else:
        print("Specify --region, --npc, or --all")
        return None
    
    if not npcs:
        print("No NPCs found matching criteria.")
        return None
    
    # Build XML
    npc_entries = []
    for npc in npcs:
        npc_entries.append(npc_to_fg_xml(conn, npc))
    
    npc_block = '\n'.join(npc_entries)
    
    if full_module:
        module_name = region or "Tribute Lands"
        module_id = make_id(module_name)
        xml = f'''<?xml version="1.0" encoding="utf-8"?>
<root version="4.8" dataversion="{__import__('datetime').date.today().strftime('%Y%m%d')}" release="5.14|CoreRPG:7">
    <library>
        <{module_id} static="true">
            <categoryname type="string">Arr'ath</categoryname>
            <name type="string">{xml_escape(module_name)}</name>
            <entries>
                <npc>
                    <librarylink type="windowreference">
                        <class>reference_list</class>
                        <recordname>npc</recordname>
                    </librarylink>
                    <name type="string">NPCs &amp; Creatures</name>
                    <recordtype type="string">npc</recordtype>
                </npc>
            </entries>
        </{module_id}>
    </library>
    <npc static="true">
{npc_block}
    </npc>
</root>'''
    else:
        xml = f'''    <npc static="true">
{npc_block}
    </npc>'''
    
    conn.close()
    print(f"Exported {len(npcs)} NPC(s)")
    return xml

# ============================================================
# CLI
# ============================================================

def main():
    parser = argparse.ArgumentParser(description="Export NPCs to Fantasy Grounds XML")
    parser.add_argument('--region', help='Export NPCs from this region')
    parser.add_argument('--npc', help='Export a specific NPC by name')
    parser.add_argument('--all', action='store_true', help='Export all NPCs with complete stat blocks')
    parser.add_argument('--full-module', action='store_true', help='Wrap in complete db.xml structure')
    parser.add_argument('--output', '-o', required=True, help='Output file path')
    
    args = parser.parse_args()
    
    xml = export_npcs(
        region=args.region,
        npc_name=args.npc,
        full_module=args.full_module,
        export_all=args.all
    )
    
    if xml:
        output_path = Path(args.output)
        output_path.write_text(xml, encoding='utf-8')
        print(f"Written to {output_path}")

if __name__ == '__main__':
    main()
