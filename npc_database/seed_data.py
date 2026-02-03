#!/usr/bin/env python3
"""
Seed the Tribute Lands NPC database with Ammaria characters.
All stats match 201_Ammaria.docx canon exactly.
"""

VERSION = {
    "version": "2.0.0",
    "updated": "2025-02-02",
    "changes": "Canon audit — Ammaria only, all stats verified against 201_Ammaria.docx"
}

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
        ("Night's Whisper", "Ammaria", "Criminal"),
        ("The Brotherhood", "Ammaria", "Criminal"),
        ("City Watch", "Ammaria", "Government"),
        ("Ammarian Tribute Administration", "Ammaria", "Government"),
        ("Temple of the Three", "Ammaria", "Religious"),
        ("Halberd Guard", "Ammaria", "Military"),
        ("Guild of Iron", "Ammaria", "Guild"),
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
    """
    Seed Ammaria pre-generated characters and NPCs.
    All stats from 201_Ammaria.docx Appendix B (Pre-Gens) and Appendix D (Contacts).
    """
    
    # ========================================
    # PRE-GENERATED CHARACTERS (Appendix B)
    # ========================================
    
    pregens = [
        # --------------------------------------------------
        # LYSSA THORNE - Merchant Princess
        # --------------------------------------------------
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
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 4, 'Common Knowledge': 8, 'Notice': 8,
                'Persuasion': 10, 'Research': 6, 'Stealth': 4
            },
            'weapons': [],
            'armor': []
        },
        
        # --------------------------------------------------
        # CAPTAIN JORIN SALTWIND - Moonstar Veteran
        # --------------------------------------------------
        {
            'name': 'Captain Jorin Saltwind',
            'title': 'Moonstar Veteran',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'maritime',
            'rank_guideline': 'Novice',
            'quote': 'The sea rewards competence. Ammaria rewards calculation. I provide both.',
            'description': 'Twenty years commanding Consortium vessels taught Jorin that maritime profit requires seamanship and shrewd dealing.',
            'background': 'Commands the Silver Current coastal trader. Conservative in navigation, aggressive in negotiation.',
            'motivation': 'Secure his retirement through one last profitable season.',
            'secret': 'Has been smuggling small quantities of untaxed goods on every run for years.',
            'agility': 8, 'smarts': 6, 'spirit': 6, 'strength': 6, 'vigor': 6,
            'pace': 6, 'parry': 5, 'toughness': 6, 'toughness_armor': 1,
            'bennies': 3,
            'edges_json': '["Sailor\'s Edge", "Command", "Caravan Guard"]',
            'hindrances_json': '["Loyal (Major — crew and Consortium)", "Cautious (Minor)", "Obligation (Minor — Consortium duties)"]',
            'gear_json': '["Sailor\'s kit", "₡50"]',
            'tactics': 'Fights defensively, using Command to direct crew. Prefers ranged engagement from ship positions. Retreats to sea if outmatched on land.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
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
                    'notes': None
                },
                {
                    'name': 'Repeating Crossbow',
                    'damage_str': '2d6',
                    'damagedice': '2d6',
                    'ap': 3,
                    'trait_type': 'Ranged',
                    'range': '15/30/60',
                    'notes': 'AP 3'
                }
            ],
            'armor': [
                {
                    'name': 'Leather Armour',
                    'protection': 1,
                    'area_protected': 'Torso, Arms, Legs',
                    'notes': None
                }
            ]
        },
        
        # --------------------------------------------------
        # MARUS IRONHAND - Guild Armourer
        # --------------------------------------------------
        {
            'name': 'Marus Ironhand',
            'title': 'Guild Armourer',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'craftsman',
            'rank_guideline': 'Novice',
            'quote': 'Quality speaks. Ammarian quality sings. My work bellows.',
            'description': 'Master armourer from a five-generation craftsman family. Creates weapons and armour that nobles commission and warriors covet.',
            'background': 'Perfectionist who won\'t craft for evil purposes. The Ironhand name carries weight in the Ironweld Guild.',
            'motivation': 'Preserve the family legacy and train a worthy apprentice.',
            'secret': 'Has been approached by the Brotherhood to forge weapons off-guild-book. Has not yet refused.',
            'agility': 6, 'smarts': 8, 'spirit': 6, 'strength': 6, 'vigor': 6,
            'pace': 6, 'parry': 5, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Guild Journeyman", "McGyver", "Brawny"]',
            'hindrances_json': '["Code of Honor (Major — won\'t craft for evil)", "Loyal (Minor — guild)", "Stubborn (Minor)"]',
            'gear_json': '["Master tools", "₡80"]',
            'tactics': 'Fights with controlled aggression. Uses environment (forge tools, heavy objects) as improvised weapons. Protects his workshop above all.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 4, 'Common Knowledge': 6, 'Fighting': 6,
                'Intimidation': 4, 'Notice': 6, 'Persuasion': 4,
                'Repair': 10, 'Research': 6, 'Stealth': 4
            },
            'weapons': [
                {
                    'name': 'Ammarian Steel Hammer',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd6+d6',
                    'ap': 1,
                    'trait_type': 'Melee',
                    'notes': 'AP 1'
                }
            ],
            'armor': [
                {
                    'name': 'Leather Apron',
                    'protection': 1,
                    'area_protected': 'Torso',
                    'notes': 'Work protection'
                }
            ]
        },
        
        # --------------------------------------------------
        # KAEL "BOARHEART" THRACE - War Boar Keeper
        # --------------------------------------------------
        {
            'name': 'Kael "Boarheart" Thrace',
            'title': 'War Boar Keeper',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'animal handler',
            'rank_guideline': 'Novice',
            'quote': 'People fear cavalry. People flee war boars. There\'s a difference.',
            'description': 'Farm boy who discovered a talent for animal handling with family war boar stock.',
            'background': 'Now maintains breeding stock and trains mounts for guild cavalry. Protective of his charges.',
            'motivation': 'Breed the perfect war boar and earn guild recognition.',
            'secret': 'One of his boars killed a nobleman\'s son. The death was ruled an accident, but Kael knows the truth.',
            'agility': 6, 'smarts': 6, 'spirit': 8, 'strength': 8, 'vigor': 4,
            'pace': 6, 'parry': 6, 'toughness': 4, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Beast Bond", "Beast Master", "Caravan Guard"]',
            'hindrances_json': '["Loyal (Major — his animals)", "Illiterate (Minor)", "Poverty-Marked (Minor)"]',
            'gear_json': '["Handler\'s tools", "Trained war boar companion", "₡40"]',
            'tactics': 'Fights mounted when possible. Uses boar charges to break enemy lines. Protects his animals fiercely.',
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
                    'notes': None
                }
            ],
            'armor': [
                {
                    'name': 'Leather Armour',
                    'protection': 1,
                    'area_protected': 'Torso, Arms, Legs',
                    'notes': None
                }
            ]
        },
        
        # --------------------------------------------------
        # "SHADOWS" - Night's Whisper Operative
        # --------------------------------------------------
        {
            'name': '"Shadows"',
            'title': 'Night\'s Whisper Operative',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'thief',
            'rank_guideline': 'Novice',
            'quote': 'The guild doesn\'t steal. We relocate assets to more appreciative owners.',
            'description': 'Professional thief affiliated with Arr\'ath\'s premier thieves\' guild.',
            'background': 'Specialises in burglary and information theft. Strict professional standards: no unnecessary violence, no jobs attracting excessive attention, absolute loyalty to guild members.',
            'motivation': 'Rise in the guild hierarchy and eventually retire wealthy.',
            'secret': 'Shadows is not one person but a shared identity used by multiple Night\'s Whisper operatives.',
            'agility': 10, 'smarts': 6, 'spirit': 6, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 4, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Thief", "Acrobat", "Streetwise"]',
            'hindrances_json': '["Wanted (Minor — various aliases)", "Loyal (Minor — Night\'s Whisper)", "Cautious (Minor)", "Greedy (Minor)"]',
            'gear_json': '["Dark clothing", "Ammarian lockpicks (+1 Thievery)", "Grappling hook with silk rope", "Smoke bombs", "₡60"]',
            'tactics': 'Avoids combat entirely. Uses stealth, distraction, and escape routes. If cornered, throws smoke and runs.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 8, 'Common Knowledge': 4, 'Fighting': 4,
                'Notice': 6, 'Persuasion': 4, 'Stealth': 10, 'Thievery': 10
            },
            'weapons': [
                {
                    'name': 'Guild Knife',
                    'damage_str': 'Str+d4',
                    'damagedice': 'd4+d4',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'notes': None
                }
            ],
            'armor': []
        },
        
        # --------------------------------------------------
        # VIKTOR "SILVERTONGUE" CRANE - Consortium Factor
        # --------------------------------------------------
        {
            'name': 'Viktor "Silvertongue" Crane',
            'title': 'Consortium Factor',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'social',
            'rank_guideline': 'Novice',
            'quote': 'Information is currency. I traffic in both.',
            'description': 'Moonstar Consortium factor who gathers commercial intelligence.',
            'background': 'Charismatic manipulator who treats complex deals as intellectual puzzles. Secretly reports to Consortium leadership on Council activities.',
            'motivation': 'Become indispensable to the Consortium and accumulate leverage over powerful people.',
            'secret': 'His intelligence reports have led to the ruin of three merchant families. He feels no remorse.',
            'agility': 4, 'smarts': 10, 'spirit': 8, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 2, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Appraiser", "Charismatic", "Connections (Moonstar)"]',
            'hindrances_json': '["Arrogant (Major)", "Obligation (Minor — Consortium)", "Greedy (Minor)"]',
            'gear_json': '["Fine clothing", "Guild credentials", "Letters of credit", "₡200"]',
            'tactics': 'Never fights. Uses information as weapon. Will betray anyone except Consortium masters.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Athletics': 4, 'Common Knowledge': 8, 'Intimidation': 4,
                'Notice': 8, 'Persuasion': 10, 'Research': 8, 'Stealth': 4
            },
            'weapons': [],
            'armor': []
        },
        
        # --------------------------------------------------
        # RENNA ASHVEIL - Debt-Slave Gladiator
        # --------------------------------------------------
        {
            'name': 'Renna Ashveil',
            'title': 'Debt-Slave Gladiator',
            'region': 'Ammaria',
            'tier': 'Wild Card',
            'archetype': 'combat',
            'rank_guideline': 'Novice',
            'quote': 'Five years contracted. Four hundred seventeen days remain.',
            'description': "Sold herself into term slavery to discharge family debts. Assigned gladiatorial training for her master's profit.",
            'background': 'Shockingly skilled fighter who counts days toward freedom obsessively. Saves every copper toward early contract purchase.',
            'motivation': 'Survive her contract and buy her freedom early.',
            'secret': "Her master has no intention of honouring the contract's end date. She doesn't know this yet.",
            'agility': 10, 'smarts': 4, 'spirit': 6, 'strength': 8, 'vigor': 4,
            'pace': 6, 'parry': 7, 'toughness': 4, 'toughness_armor': 0,
            'bennies': 3,
            'edges_json': '["Quick", "Combat Reflexes", "First Strike"]',
            'hindrances_json': '["Obligation (Major \u2014 debt contract)", "Poverty (Minor)", "Vengeful (Minor)"]',
            'gear_json': '["Gladiatorial leathers (+1)", "Gladius (Str+d6)", "Net", "Ammarian steel dagger (Str+d4, AP 1)", "\u20a15 hidden savings"]',
            'tactics': "Explosive and aggressive. Uses Quick to act first, First Strike to punish approach, then relentless Fighting d10 attacks. Fights like someone with nothing to lose.",
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
            ],
            'armor': [
                {
                    'name': 'Gladiatorial Leathers',
                    'protection': 1,
                    'area_protected': 'Torso, Arms',
                    'notes': None
                }
            ]
        },
    ]
    
    # ========================================
    # NPC CONTACTS (Appendix D)
    # ========================================
    
    contacts = [
        # --------------------------------------------------
        # TAM "THREE-COINS" MERRIK - Professional Fixer
        # --------------------------------------------------
        {
            'name': 'Tam "Three-Coins" Merrik',
            'title': 'Professional Fixer',
            'region': 'Ammaria',
            'tier': 'Extra',
            'archetype': 'criminal',
            'rank_guideline': 'Seasoned',
            'quote': 'Everyone has a price. I help you find it.',
            'description': 'Professional bribe-facilitator and fixer who knows exactly which officials take money, how much they want, and what they\'ll do for it.',
            'background': 'Tam doesn\'t actually bribe anyone himself — he just makes introductions and suggests appropriate "donation" levels. This legal fiction keeps him out of prison.',
            'motivation': 'Maintain his network and stay useful enough that nobody wants him dead.',
            'secret': 'Works both sides — feeds information to the City Watch when it suits him.',
            'agility': 6, 'smarts': 10, 'spirit': 8, 'strength': 4, 'vigor': 6,
            'pace': 6, 'parry': 2, 'toughness': 5, 'toughness_armor': 0,
            'bennies': 0,
            'edges_json': '["Connections (bureaucrats, inspectors, minor officials)", "Calculating"]',
            'hindrances_json': '[]',
            'gear_json': '["Quality clothing", "Extensive contact book (coded)", "100-300₡"]',
            'tactics': 'Never fights if he can help it. Runs at the first sign of real violence. If cornered, offers information as currency.',
            'stat_block_complete': 1,
            'narrative_complete': 1,
            'fg_export_ready': 0,
            'source_document': '201_Ammaria',
            'skills': {
                'Common Knowledge': 12, 'Gambling': 6, 'Notice': 8, 'Persuasion': 10
            },
            'weapons': [],
            'armor': []
        },
    ]
    
    all_npcs = pregens + contacts
    
    # ========================================
    # SALTLANDS PRE-GENS (202_Saltlands)
    # ========================================
    
    saltlands_pregens = [
        # --------------------------------------------------
        # MARA "REEFBANE" SALTHEART - Corsair Captain
        # --------------------------------------------------
        {
            'name': 'Mara "Reefbane" Saltheart',
            'title': 'Corsair Captain',
            'region': 'Saltlands',
            'tier': 'Wild Card',
            'archetype': 'maritime',
            'rank_guideline': 'Novice',
            'quote': "The reef takes what the reef wants. I just make sure it wants what I'm selling.",
            'description': 'Born to the reefs and raised on deck. Captains the Gull\'s Spite, a fast cutter that runs the shallows where heavier vessels dare not follow.',
            'background': 'Rose through corsair ranks on skill rather than cruelty. Commands loyalty through competence and fair shares.',
            'motivation': 'Command her own fleet and answer to no harbour lord.',
            'secret': 'Knows the location of a pre-Shattering wreck in the deep reefs. Has told no one.',
            'agility': 8, 'smarts': 6, 'spirit': 8, 'strength': 6, 'vigor': 6,
            'pace': 6, 'parry': 6, 'toughness': 6, 'toughness_armor': 1,
            'bennies': 3,
            'edges_json': '["Sailor\'s Edge", "Command"]',
            'hindrances_json': '["Loyal (Major \u2014 crew)", "Stubborn (Minor)", "Wanted (Minor \u2014 Glasryan bounty)"]',
            'gear_json': '["Leather armour (+1)", "Cutlass (Str+d6)", "Boarding axe (Str+d6)", "Spyglass", "\u20a140"]',
            'tactics': 'Fights from the deck of her ship whenever possible. Uses terrain and crew to create advantage. Will not abandon her crew.',
            'stat_block_complete': 1,
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
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                },
                {
                    'name': 'Boarding Axe',
                    'damage_str': 'Str+d6',
                    'damagedice': 'd6+d6',
                    'ap': 0,
                    'trait_type': 'Melee',
                    'reach': 0,
                    'notes': None
                }
            ],
            'armor': [
                {
                    'name': 'Leather Armour',
                    'protection': 1,
                    'area_protected': 'Torso',
                    'notes': None
                }
            ]
        },
    ]
    
    all_npcs = all_npcs + saltlands_pregens
    
    for npc_data in all_npcs:
        npc_id = add_npc_from_dict(npc_data)
        print(f"  ✓ #{npc_id}: {npc_data['name']} ({npc_data['region']}, {npc_data['tier']})")
    
    return len(all_npcs)


def seed_org_links():
    """Link NPCs to their organisations."""
    conn = get_db()
    
    links = [
        ('Lyssa Thorne', 'Moonstar Consortium', 'Associate'),
        ('Captain Jorin Saltwind', 'Moonstar Consortium', 'Captain'),
        ('Marus Ironhand', 'Ironweld Guild', 'Master'),
        ('Kael "Boarheart" Thrace', 'Guild of Iron', 'Handler'),
        ('"Shadows"', 'Night\'s Whisper', 'Operative'),
        ('Viktor "Silvertongue" Crane', 'Moonstar Consortium', 'Factor'),
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
        ('Kael "Boarheart" Thrace', 'Ammaria Core Module', 'Pre-gen PC'),
        ('"Shadows"', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Viktor "Silvertongue" Crane', 'Ammaria Core Module', 'Pre-gen PC'),
        ('Tam "Three-Coins" Merrik', 'Ammaria Core Module', 'NPC Contact'),
        ('Renna Ashveil', 'Ammaria Core Module', 'Pre-gen PC'),
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
