#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Canon correction script for Ammaria NPCs.
Fixes Marus Ironhand to match 201 Ammaria.docx and adds missing pre-gens.

Run from the npc_database directory:
  python3 canon_corrections.py
"""

import sys, os
sys.path.insert(0, os.path.dirname(__file__))

from npc_manager import get_db, add_npc_from_dict

COIN = "₡"

def fix_marus_ironhand():
    """Correct Marus Ironhand to match canonical 201 Ammaria.docx."""
    conn = get_db()
    
    marus = conn.execute("SELECT id FROM npcs WHERE name='Marus Ironhand'").fetchone()
    if not marus:
        print("  X Marus Ironhand not found in database")
        return
    npc_id = marus['id']
    print(f"  Found Marus Ironhand (ID: {npc_id})")
    
    # Fix attributes and derived stats
    conn.execute("""UPDATE npcs SET
        strength = 6,
        vigor = 6,
        toughness = 5,
        toughness_armor = 0,
        gear_json = ?
        WHERE id = ?""", (f'["Leather apron (+1)", "Ammarian steel hammer (Str+d6, AP 1)", "Master tools", "{COIN}80"]', npc_id))
    print("  OK Fixed attributes: Str d8->d6, Vi d8->d6")
    print("  OK Fixed Toughness: 8(2)->5(0)")
    print("  OK Fixed gear to canon")
    
    # Fix skills
    skill_corrections = {
        'Athletics': 4,
        'Common Knowledge': 6,
        'Fighting': 6,
        'Intimidation': 4,
        'Notice': 6,
        'Repair': 10,
        'Stealth': 4,
    }
    skill_additions = {
        'Persuasion': 4,
        'Research': 6,
    }
    
    for skill, die in skill_corrections.items():
        conn.execute("UPDATE npc_skills SET die_type=? WHERE npc_id=? AND name=?",
                     (die, npc_id, skill))
    for skill, die in skill_additions.items():
        existing = conn.execute("SELECT id FROM npc_skills WHERE npc_id=? AND name=?",
                               (npc_id, skill)).fetchone()
        if not existing:
            conn.execute("INSERT INTO npc_skills (npc_id, name, die_type) VALUES (?,?,?)",
                         (npc_id, skill, die))
            print(f"  OK Added missing skill: {skill} d{die}")
        else:
            conn.execute("UPDATE npc_skills SET die_type=? WHERE npc_id=? AND name=?",
                         (die, npc_id, skill))
    print("  OK Fixed skills: Athletics d4, CK d6, Intimidation d4, +Persuasion d4, +Research d6")
    
    # Fix hindrances (managed table)
    conn.execute("DELETE FROM npc_hindrances WHERE npc_id=?", (npc_id,))
    canon_hindrances = [
        ('Code of Honor', 'Major', "won't craft for evil"),
        ('Loyal', 'Minor', 'guild'),
        ('Stubborn', 'Minor', None),
    ]
    for name, severity, notes in canon_hindrances:
        conn.execute("""INSERT INTO npc_hindrances (npc_id, name, severity, notes, source)
                        VALUES (?, ?, ?, ?, 'SWADE Core')""",
                     (npc_id, name, severity, notes))
    conn.execute("UPDATE npcs SET hindrances_json='[]' WHERE id=?", (npc_id,))
    print("  OK Fixed hindrances: Code of Honor (Major), Loyal (Minor-guild), Stubborn (Minor)")
    
    # Fix weapons
    conn.execute("DELETE FROM npc_weapons WHERE npc_id=?", (npc_id,))
    conn.execute("""INSERT INTO npc_weapons (npc_id, name, damage_str, damagedice, ap, trait_type, reach, notes)
                    VALUES (?, 'Ammarian steel hammer', 'Str+d6', 'd6+d6', 1, 'Melee', 0, 'AP 1')""",
                 (npc_id,))
    print("  OK Fixed weapon: Ammarian steel hammer (Str+d6, AP 1)")
    
    # Fix armor
    conn.execute("DELETE FROM npc_armor WHERE npc_id=?", (npc_id,))
    conn.execute("""INSERT INTO npc_armor (npc_id, name, armor_bonus, covers, notes)
                    VALUES (?, 'Leather apron', 1, 'Torso', NULL)""",
                 (npc_id,))
    print("  OK Fixed armor: Leather apron (+1)")
    
    conn.commit()
    conn.close()
    print("  OK Marus Ironhand corrected to canon\n")


def add_missing_pregens():
    """Add the 4 missing Ammaria pre-gens from 201 Appendix B."""
    
    missing_npcs = [
        {
            'name': 'Kael "Boarheart" Thrace',
            'title': 'War Boar Keeper',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'combat',
            'rank_guideline': 'Novice',
            'quote': "People fear cavalry. People flee war boars. There's a difference.",
            'description': 'Farm boy who discovered a talent for animal handling with family war boar stock. Now maintains breeding stock and trains mounts for guild cavalry.',
            'background': 'Protective of his charges. The war boars trust him instinctively, which experienced handlers find unsettling.',
            'motivation': 'Protect his animals and prove their worth to the guilds.',
            'secret': 'His favourite boar, Tusker, is smarter than most people he works with.',
            'agility': 6, 'smarts': 6, 'spirit': 8, 'strength': 8, 'vigor': 4,
            'pace': 6, 'parry': 6, 'toughness': 4, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Beast Bond", "Beast Master", "Caravan Guard"]',
            'hindrances_json': '["Loyal (Major \u2014 his animals)", "Illiterate (Minor)", "Poverty-Marked (Minor)"]',
            'gear_json': '["Leather armour (+1)", "Spear (Str+d6, Reach 1)", "Short bow (2d6, Range 12/24/48)", "Handler\u2019s tools", "Trained war boar companion", "{COIN}40"]',
            'tactics': "Fights mounted when possible. Dismounted, uses spear reach. Always protects his animals first.",
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 6, 'Common Knowledge': 4, 'Fighting': 8,
                'Notice': 6, 'Persuasion': 4, 'Riding': 8,
                'Stealth': 4, 'Survival': 6
            },
            'weapons': [
                {
                    'name': 'Spear',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd8+d6',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 1,
                    'notes': 'Reach 1'
                },
                {
                    'name': 'Short Bow',
                    'damage_str': '2d6',
                    'damagedice': '2d6',
                    'ap': 0,
                    'trait_type': 'Ranged',
                    'range': '12/24/48',
                    'reach': 0,
                    'notes': None
                }
            ]
        },
        {
            'name': '"Shadows"',
            'title': "Night's Whisper Operative",
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'criminal',
            'rank_guideline': 'Novice',
            'quote': "The guild doesn't steal. We relocate assets to more appreciative owners.",
            'description': "Professional thief affiliated with Arr'ath's premier thieves' guild. Specialises in burglary and information theft.",
            'background': "Strict professional standards: no unnecessary violence, no jobs attracting excessive attention, absolute loyalty to guild members.",
            'motivation': "Rise within the Night's Whisper hierarchy and eventually run a crew.",
            'secret': 'Keeping a personal ledger of every job — insurance against betrayal, but devastating if found.',
            'agility': 10, 'smarts': 6, 'spirit': 6, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 4, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Thief", "Acrobat", "Streetwise"]',
            'hindrances_json': '["Wanted (Minor \u2014 various aliases)", "Loyal (Minor \u2014 Night\u2019s Whisper)", "Cautious (Minor)", "Greedy (Minor)"]',
            'gear_json': '["Dark clothing", "Ammarian lockpicks (+1 Thievery)", "Guild knife (Str+d4)", "Grappling hook with silk rope", "Smoke bombs", "{COIN}60"]',
            'tactics': "Never fights fair. Uses smoke bombs to escape, grappling hook for elevation. Surrenders rather than risk death.",
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 8, 'Common Knowledge': 4, 'Fighting': 4,
                'Notice': 6, 'Persuasion': 4, 'Stealth': 10,
                'Thievery': 10
            },
            'weapons': [
                {
                    'name': 'Guild Knife',
                    'damage_str': 'Str+d4',
                    'damagedice': 'd4+d4',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                }
            ]
        },
        {
            'name': 'Viktor "Silvertongue" Crane',
            'title': 'Consortium Factor',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'social',
            'rank_guideline': 'Novice',
            'quote': 'Information is currency. I traffic in both.',
            'description': 'Moonstar Consortium factor who gathers commercial intelligence. Charismatic manipulator who treats complex deals as intellectual puzzles.',
            'background': 'Secretly reports to Consortium leadership on Council activities.',
            'motivation': 'Accumulate enough influence to become indispensable to the Consortium.',
            'secret': 'Has been selling selective information to multiple factions, playing all sides.',
            'agility': 4, 'smarts': 10, 'spirit': 8, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 2, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Appraiser", "Charismatic", "Connections (Moonstar)"]',
            'hindrances_json': '["Arrogant (Major)", "Obligation (Minor \u2014 Consortium)", "Greedy (Minor)"]',
            'gear_json': '["Fine clothing", "Guild credentials", "Letters of credit", "{COIN}200"]',
            'tactics': "Avoids all physical confrontation. Uses social leverage and Consortium connections. Runs if violence erupts.",
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 4, 'Common Knowledge': 8, 'Intimidation': 4,
                'Notice': 8, 'Persuasion': 10, 'Research': 8,
                'Stealth': 4
            },
            'weapons': []
        },
        {
            'name': 'Renna Ashveil',
            'title': 'Debt-Slave Gladiator',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'combat',
            'rank_guideline': 'Novice',
            'quote': 'Five years contracted. Four hundred seventeen days remain.',
            'description': "Sold herself into term slavery to discharge family debts. Assigned gladiatorial training for master's profit.",
            'background': 'Shockingly skilled fighter who counts days toward freedom obsessively. Saves every copper toward early contract purchase.',
            'motivation': 'Survive her contract and buy her freedom early.',
            'secret': "Her master has no intention of honouring the contract's end date.",
            'agility': 10, 'smarts': 4, 'spirit': 6, 'strength': 8, 'vigor': 4,
            'pace': 6, 'parry': 7, 'toughness': 4, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Quick", "Combat Reflexes", "First Strike"]',
            'hindrances_json': '["Obligation (Major \u2014 debt contract)", "Poverty (Minor)", "Vengeful (Minor)"]',
            'gear_json': '["Gladiatorial leathers (+1)", "Gladius (Str+d6)", "Net", "Ammarian steel dagger (Str+d4, AP 1)", "{COIN}5 hidden savings"]',
            'tactics': "Explosive and aggressive. Uses Quick to act first, First Strike to punish approach, then relentless attacks.",
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 10, 'Common Knowledge': 4, 'Fighting': 10,
                'Intimidation': 6, 'Notice': 4, 'Persuasion': 4,
                'Stealth': 4, 'Survival': 6
            },
            'weapons': [
                {
                    'name': 'Gladius',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd8+d6',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                },
                {
                    'name': 'Ammarian Steel Dagger',
                    'damage_str': 'Str+d4',
                    'damagedice': 'd8+d4',
                    'ap': 1,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': 'AP 1'
                }
            ]
        },
    ]
    
    for npc_data in missing_npcs:
        conn = get_db()
        existing = conn.execute("SELECT id FROM npcs WHERE name=?", (npc_data['name'],)).fetchone()
        conn.close()
        
        if existing:
            print(f"  Already exists: {npc_data['name']} (ID: {existing['id']}) -- skipping")
            continue
        
        npc_id = add_npc_from_dict(npc_data)
        print(f"  OK Added {npc_data['name']} (ID: {npc_id})")
    
    print()


def add_missing_org_links():
    """Link new NPCs to organisations."""
    conn = get_db()
    
    new_links = [
        ('Kael', 'Ironweld Guild', 'Supplier'),
        ('Shadows', 'The Brotherhood', 'Rival'),
        ('Viktor', 'Moonstar Consortium', 'Factor'),
    ]
    
    for npc_name, org_name, role in new_links:
        npc = conn.execute("SELECT id FROM npcs WHERE name LIKE ?", (f"%{npc_name}%",)).fetchone()
        org = conn.execute("SELECT id FROM organisations WHERE name LIKE ?", (f"%{org_name}%",)).fetchone()
        if npc and org:
            existing = conn.execute(
                "SELECT id FROM npc_organisations WHERE npc_id=? AND org_id=?",
                (npc['id'], org['id'])
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO npc_organisations (npc_id, org_id, role) VALUES (?, ?, ?)",
                    (npc['id'], org['id'], role)
                )
                print(f"  OK Linked {npc_name} -> {org_name} ({role})")
    
    conn.commit()
    conn.close()


def add_missing_appearances():
    """Record product appearances for new NPCs."""
    conn = get_db()
    
    new_appearances = [
        ('Kael', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Shadows', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Viktor', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Renna', 'Ammaria Core Module', 'Pre-gen PC'),
    ]
    
    for npc_name, product, role in new_appearances:
        npc = conn.execute("SELECT id FROM npcs WHERE name LIKE ?", (f"%{npc_name}%",)).fetchone()
        if npc:
            existing = conn.execute(
                "SELECT id FROM npc_appearances WHERE npc_id=? AND product=?",
                (npc['id'], product)
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO npc_appearances (npc_id, product, role) VALUES (?, ?, ?)",
                    (npc['id'], product, role)
                )
    
    conn.commit()
    conn.close()
    print("  OK Product appearances recorded\n")


def main():
    print("\n=== AMMARIA CANON CORRECTIONS ===\n")
    
    print("--- Fixing Marus Ironhand ---")
    fix_marus_ironhand()
    
    print("--- Adding Missing Pre-Gens ---")
    add_missing_pregens()
    
    print("--- Organisation Links ---")
    add_missing_org_links()
    
    print("--- Product Appearances ---")
    add_missing_appearances()
    
    print("=== CORRECTIONS COMPLETE ===")
    print("  Marus Ironhand: Restored to 201 Ammaria canon")
    print("  Added: Kael Boarheart, Shadows, Viktor Crane, Renna Ashveil")
    print("  Total Ammaria pre-gens should now be: 7 (+ Tam as example NPC)\n")


if __name__ == '__main__':
    main()
