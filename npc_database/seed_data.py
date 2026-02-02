#!/usr/bin/env python3
"""
Seed the Tribute Lands NPC database with existing Ammaria characters.
Run after init to populate with known NPCs from the module content.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from npc_manager import init_db, add_npc_from_dict, get_db

def seed_organisations():
    """Add key Ammaria organisations."""
    conn = get_db()
    orgs = [
        ("Moonstar Consortium", "Ammaria", "Guild"),
        ("Ironweld Guild", "Ammaria", "Guild"),
        ("Dyers' Guild", "Ammaria", "Guild"),
        ("The Brotherhood", "Ammaria", "Criminal"),
        ("City Watch", "Ammaria", "Government"),
        ("Ammarian Tribute Administration", "Ammaria", "Government"),
        ("Temple of the Three", "Ammaria", "Religious"),
        ("Halberd Guard", "Ammaria", "Military"),
        ("Glasryan Garrison", "Ammaria", "Military"),
        ("Crimson Fleet", "Saltlands", "Criminal"),
        ("Broken Chain", "Saltlands", "Criminal"),
        ("Harbour Lords", "Saltlands", "Government"),
        ("Temple of Three Tides", "Saltlands", "Religious"),
        ("Tidesworn", "Saltlands", "Religious"),
        ("Fencing Circle", "Saltlands", "Criminal"),
        ("Holtscarl Wardens", "Vinlands", "Military"),
        ("Felsgard Clans", "Vinlands", "Military"),
        ("Glasryan Slaving Legion", "Global", "Military"),
    ]
    for name, region, org_type in orgs:
        try:
            conn.execute(
                "INSERT INTO organisations (name, region, type) VALUES (?, ?, ?)",
                (name, region, org_type)
            )
        except:
            pass
    conn.commit()
    conn.close()
    print(f"✓ Seeded {len(orgs)} organisations")

def seed_ammaria_npcs():
    """Seed pre-generated characters from Ammaria module."""
    
    npcs = [
        {
            'name': 'Lyssa Thorne',
            'title': 'Merchant Princess',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'social',
            'rank_guideline': 'Novice',
            'quote': 'Everything negotiable has a price. Everything else? Also negotiable.',
            'description': 'Born into the Thorne merchant dynasty, Lyssa broke her arranged betrothal and now builds her own commercial network.',
            'background': 'She refuses the slave trade and honours her word even when costly — principled stubbornness hidden behind a polished Ammarian facade.',
            'motivation': 'Build an independent trading network free from family control.',
            'secret': 'Her former betrothed now works for the Brotherhood, and their paths will cross.',
            'agility': 4, 'smarts': 8, 'spirit': 8, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 2, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Charismatic", "Appraiser"]',
            'hindrances_json': '["Stubborn (Minor)", "Obligation (Minor — family)", "Code of Honor (Major)"]',
            'gear_json': '["Fine clothing", "₡150 cash"]',
            'tactics': 'Avoids direct combat. Uses social leverage, bribery, and hired muscle to resolve conflicts.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 1,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 4, 'Common Knowledge': 8, 'Notice': 8,
                'Persuasion': 10, 'Research': 6, 'Stealth': 4
            },
            'weapons': []
        },
        {
            'name': 'Captain Jorin Saltwind',
            'title': 'Moonstar Veteran',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'maritime',
            'rank_guideline': 'Novice',
            'quote': 'The sea rewards competence. Ammaria rewards calculation. I provide both.',
            'description': 'Twenty years commanding Consortium vessels taught Jorin that maritime profit requires seamanship and shrewd dealing. Commands the Silver Current coastal trader.',
            'background': 'Conservative in navigation, aggressive in negotiation. The Moonstar Consortium trusts him with sensitive cargo runs.',
            'motivation': 'Secure his retirement through one last profitable season.',
            'secret': 'Has been smuggling small quantities of untaxed goods on every run for years.',
            'agility': 8, 'smarts': 6, 'spirit': 6, 'strength': 6, 'vigor': 6,
            'pace': 6, 'parry': 5, 'toughness': 7, 'toughness_armor': 2,
            'bennies': 3,
            'edges_json': '["Sailor\'s Edge", "Command", "Caravan Guard"]',
            'hindrances_json': '["Loyal (Major — crew and Consortium)", "Cautious (Minor)", "Obligation (Minor — Consortium duties)"]',
            'gear_json': '["Sailor\'s kit", "₡50"]',
            'tactics': 'Fights defensively, using Command to direct crew. Prefers ranged engagement from ship positions. Retreats to sea if outmatched on land.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 1,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 6, 'Boating': 8, 'Common Knowledge': 6,
                'Fighting': 6, 'Notice': 6, 'Persuasion': 6,
                'Shooting': 6, 'Stealth': 4
            },
            'weapons': [
                {
                    'name': 'Cutlass',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd6+d6',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                },
                {
                    'name': 'Repeating Crossbow',
                    'damage_str': '2d6',
                    'damagedice': '2d6',
                    'ap': 3,
                    'trait_type': 'Ranged',
                    'range': '15/30/60',
                    'reach': 0,
                    'notes': 'AP 3'
                }
            ]
        },
        {
            'name': 'Marus Ironhand',
            'title': 'Guild Armourer',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'combat',
            'rank_guideline': 'Novice',
            'quote': 'Quality speaks. Ammarian quality sings. My work bellows.',
            'description': 'Master armourer from a five-generation craftsman family. Broad-shouldered, permanently scarred hands from decades at the forge.',
            'background': 'The Ironhand name carries weight in the Ironweld Guild. Marus maintains the family reputation with obsessive attention to craft.',
            'motivation': 'Preserve the family legacy and train a worthy apprentice.',
            'secret': 'Has been approached by the Brotherhood to forge weapons off-guild-book. Has not yet refused.',
            'agility': 6, 'smarts': 8, 'spirit': 6, 'strength': 8, 'vigor': 8,
            'pace': 6, 'parry': 5, 'toughness': 8, 'toughness_armor': 2,
            'bennies': 3,
            'edges_json': '["Guild Journeyman", "Brawny", "McGyver"]',
            'hindrances_json': '["Stubborn (Minor)", "Loyal (Major — Guild)", "Obligation (Minor — family legacy)"]',
            'gear_json': '["Ammarian steel tools", "₡75"]',
            'tactics': 'Fights with controlled aggression. Uses environment (forge tools, heavy objects) as improvised weapons. Protects his workshop above all.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 1,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 6, 'Common Knowledge': 8, 'Fighting': 6,
                'Intimidation': 6, 'Notice': 6, 'Repair': 10,
                'Stealth': 4
            },
            'weapons': [
                {
                    'name': 'Warhammer',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd8+d6',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                }
            ]
        },
        {
            'name': 'Tam "Three-Coins" Merrik',
            'title': 'Professional Fixer',
            'region': 'Ammaria',
            'tier': 'Extra',
            'archetype': 'criminal',
            'rank_guideline': 'Seasoned',
            'quote': 'Everyone has a price. I just help people discover theirs.',
            'description': 'Thirty-four, neat clothes, ledger always under arm. He explains terms clearly, offers payment plans, and apologises when violence becomes necessary.',
            'background': 'Tam doesn\'t actually bribe anyone himself — he just makes introductions and suggests appropriate "donation" levels. This legal fiction keeps him out of prison.',
            'motivation': 'Maintain his network and stay useful enough that nobody wants him dead.',
            'secret': 'Works both sides — feeds information to the City Watch when it suits him.',
            'agility': 6, 'smarts': 8, 'spirit': 8, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 4, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 0,
            'edges_json': '["Connections", "Streetwise"]',
            'hindrances_json': '["Greedy (Minor)", "Cautious (Minor)"]',
            'gear_json': '["Fine clothes", "Ledger", "₡200 in various currencies"]',
            'tactics': 'Never fights if he can help it. Runs at the first sign of real violence. If cornered, offers information as currency.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 1,
            'source_document': 'Skill_04',
            'skills': {
                'Common Knowledge': 8, 'Fighting': 4, 'Gambling': 6,
                'Notice': 8, 'Persuasion': 10, 'Stealth': 6,
                'Streetwise': 8, 'Thievery': 6
            },
            'weapons': [
                {
                    'name': 'Dagger',
                    'damage_str': 'Str+d4',
                    'damagedice': 'd4+d4',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                }
            ]
        },
    ]
    
    # Saltlands pre-gens
    saltlands_npcs = [
        {
            'name': 'Mara "Reefbane" Saltheart',
            'title': 'Corsair Captain',
            'region': 'Saltlands',
            'tier': 'Wild Card',
            'archetype': 'maritime',
            'rank_guideline': 'Novice',
            'quote': 'The reef takes what the reef wants. I just make sure it wants what I\'m selling.',
            'motivation': 'Command her own fleet and answer to no harbour lord.',
            'agility': 8, 'smarts': 6, 'spirit': 8, 'strength': 6, 'vigor': 6,
            'pace': 6, 'parry': 6, 'toughness': 6, 'toughness_armor': 1,
            'bennies': 3,
            'edges_json': '["Sailor\'s Edge", "Command"]',
            'gear_json': '[]',
            'stat_block_complete': 0,
            'narrative_complete': 0,
            'fg_export_ready': 0,
            'source_document': '202_Saltlands',
            'skills': {
                'Athletics': 6, 'Boating': 8, 'Fighting': 8,
                'Intimidation': 6, 'Notice': 6, 'Shooting': 6, 'Stealth': 4
            },
            'weapons': [
                {
                    'name': 'Cutlass',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd6+d6',
                    'trait_type': 'Melee',
                },
                {
                    'name': 'Boarding Axe',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd6+d6',
                    'trait_type': 'Melee',
                }
            ]
        },
    ]
    
    all_npcs = npcs + saltlands_npcs
    
    for npc_data in all_npcs:
        npc_id = add_npc_from_dict(npc_data)
        print(f"  ✓ #{npc_id}: {npc_data['name']} ({npc_data['region']}, {npc_data['tier']})")
    
    return len(all_npcs)

def seed_org_links():
    """Link NPCs to their organisations."""
    conn = get_db()
    
    links = [
        ('Lyssa Thorne', 'Moonstar Consortium', 'Member'),
        ('Captain Jorin Saltwind', 'Moonstar Consortium', 'Captain'),
        ('Marus Ironhand', 'Ironweld Guild', 'Master'),
        ('Tam "Three-Coins" Merrik', 'The Brotherhood', 'Associate'),
        ('Tam "Three-Coins" Merrik', 'City Watch', 'Informant'),
        ('Mara "Reefbane" Saltheart', 'Crimson Fleet', 'Captain'),
    ]
    
    for npc_name, org_name, role in links:
        npc = conn.execute("SELECT id FROM npcs WHERE name LIKE ?", (f"%{npc_name}%",)).fetchone()
        org = conn.execute("SELECT id FROM organisations WHERE name LIKE ?", (f"%{org_name}%",)).fetchone()
        if npc and org:
            try:
                conn.execute(
                    "INSERT INTO npc_organisations (npc_id, org_id, role) VALUES (?, ?, ?)",
                    (npc['id'], org['id'], role)
                )
            except:
                pass
    
    conn.commit()
    conn.close()
    print("✓ Organisation links established")

def seed_appearances():
    """Record product appearances."""
    conn = get_db()
    
    appearances = [
        ('Lyssa Thorne', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Captain Jorin Saltwind', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Marus Ironhand', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Tam "Three-Coins" Merrik', 'Ammaria Core Module', 'Example NPC'),
        ('Mara "Reefbane" Saltheart', 'Saltlands Core Module', 'Pre-gen PC'),
    ]
    
    for npc_name, product, role in appearances:
        npc = conn.execute("SELECT id FROM npcs WHERE name LIKE ?", (f"%{npc_name}%",)).fetchone()
        if npc:
            try:
                conn.execute(
                    "INSERT INTO npc_appearances (npc_id, product, role) VALUES (?, ?, ?)",
                    (npc['id'], product, role)
                )
            except:
                pass
    
    conn.commit()
    conn.close()
    print("✓ Product appearances recorded")

def main():
    print("\n=== SEEDING TRIBUTE LANDS NPC DATABASE ===\n")
    
    # Initialise
    init_db()
    
    # Seed
    seed_organisations()
    count = seed_ammaria_npcs()
    seed_org_links()
    seed_appearances()
    
    print(f"\n✓ Database seeded with {count} NPCs")
    print("  Run 'python npc_manager.py list' to see them")
    print("  Run 'python npc_manager.py show 1' to view details")
    print("  Run 'python fg_export.py --region Ammaria --output test.xml' to test FG export\n")

if __name__ == '__main__':
    main()
