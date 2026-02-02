"""
Equipment Catalogue for the Tribute Lands NPC Database.
Covers Savage Worlds core, Fantasy Companion, and all regional sources.
Each entry tagged with source for filtering.
"""

# =============================================================
# WEAPONS CATALOGUE
# =============================================================
# Fields: name, damage_str, ap, trait_type, range, reach, weight, cost, notes, source
# damage_str uses the display string (Str+d8); damagedice is calculated at assignment time
# based on NPC Strength.

WEAPONS = [
    # ---------------------------------------------------------
    # SAVAGE WORLDS CORE — Melee
    # ---------------------------------------------------------
    {"name": "Unarmed", "damage_str": "Str", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 0, "cost": "0", "notes": "", "source": "Core"},
    {"name": "Dagger/Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "3/6/12", "reach": 0, "weight": 1, "cost": "25", "notes": "Can be thrown", "source": "Core"},
    {"name": "Short Sword", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "100", "notes": "", "source": "Core"},
    {"name": "Long Sword", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "300", "notes": "", "source": "Core"},
    {"name": "Great Sword", "damage_str": "Str+d10", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 6, "cost": "400", "notes": "Two hands", "source": "Core"},
    {"name": "Rapier", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "150", "notes": "Parry +1", "source": "Core"},
    {"name": "Axe", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "3/6/12", "reach": 0, "weight": 2, "cost": "100", "notes": "Can be thrown", "source": "Core"},
    {"name": "Battle Axe", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "300", "notes": "", "source": "Core"},
    {"name": "Great Axe", "damage_str": "Str+d10", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 7, "cost": "400", "notes": "AP 1, Two hands", "source": "Core"},
    {"name": "Mace", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "100", "notes": "", "source": "Core"},
    {"name": "Maul", "damage_str": "Str+d10", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 10, "cost": "400", "notes": "AP 2, Two hands", "source": "Core"},
    {"name": "Flail", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "200", "notes": "Ignores Shield bonus", "source": "Core"},
    {"name": "Warhammer", "damage_str": "Str+d6", "ap": 1, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "200", "notes": "AP 1", "source": "Core"},
    {"name": "Spear", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "3/6/12", "reach": 1, "weight": 3, "cost": "100", "notes": "Reach 1, Parry +1 (two hands), can be thrown", "source": "Core"},
    {"name": "Pike", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 8, "cost": "200", "notes": "Reach 2, Two hands", "source": "Core"},
    {"name": "Halberd", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 6, "cost": "250", "notes": "Reach 1, Two hands", "source": "Core"},
    {"name": "Staff", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 4, "cost": "10", "notes": "Reach 1, Parry +1, Two hands", "source": "Core"},
    {"name": "Lance", "damage_str": "Str+d8", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 6, "cost": "300", "notes": "AP 2, Reach 2, requires mount", "source": "Core"},
    {"name": "Club", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "5", "notes": "", "source": "Core"},

    # SAVAGE WORLDS CORE — Ranged
    {"name": "Bow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "12/24/48", "reach": 0, "weight": 2, "cost": "250", "notes": "", "source": "Core"},
    {"name": "Longbow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 3, "cost": "300", "notes": "AP 1", "source": "Core"},
    {"name": "Crossbow", "damage_str": "2d6", "ap": 2, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 5, "cost": "250", "notes": "AP 2, Reload 1", "source": "Core"},
    {"name": "Sling", "damage_str": "Str+d4", "ap": 0, "trait_type": "Ranged",
     "range": "4/8/16", "reach": 0, "weight": 0.5, "cost": "10", "notes": "", "source": "Core"},
    {"name": "Net (Weighted)", "damage_str": "-", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 4, "cost": "50", "notes": "Entangle, -2 Pace, Bound on Raise", "source": "Core"},

    # ---------------------------------------------------------
    # FANTASY COMPANION — Melee
    # ---------------------------------------------------------
    {"name": "Bastard Sword", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "350", "notes": "Two hands for Str+d10", "source": "Fantasy Companion"},
    {"name": "Scimitar", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "300", "notes": "", "source": "Fantasy Companion"},
    {"name": "Morningstar", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "200", "notes": "", "source": "Fantasy Companion"},
    {"name": "War Flail", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 5, "cost": "300", "notes": "Ignores Shield bonus, Two hands", "source": "Fantasy Companion"},
    {"name": "Trident", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "3/6/12", "reach": 1, "weight": 4, "cost": "150", "notes": "Reach 1, can be thrown", "source": "Fantasy Companion"},
    {"name": "Whip", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 1, "cost": "50", "notes": "Reach 2, can Entangle", "source": "Fantasy Companion"},
    {"name": "Cestus", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "50", "notes": "Fist weapon", "source": "Fantasy Companion"},

    # FANTASY COMPANION — Ranged
    {"name": "Short Bow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 2, "cost": "200", "notes": "", "source": "Fantasy Companion"},
    {"name": "Composite Bow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 3, "cost": "400", "notes": "AP 1", "source": "Fantasy Companion"},
    {"name": "Hand Crossbow", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 1, "cost": "200", "notes": "One hand", "source": "Fantasy Companion"},
    {"name": "Heavy Crossbow", "damage_str": "2d8", "ap": 2, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "400", "notes": "AP 2, Reload 2", "source": "Fantasy Companion"},
    {"name": "Javelin", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 2, "cost": "50", "notes": "", "source": "Fantasy Companion"},
    {"name": "Throwing Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 0.5, "cost": "25", "notes": "", "source": "Fantasy Companion"},

    # ---------------------------------------------------------
    # TRIBUTE LANDS: AMMARIA
    # ---------------------------------------------------------
    {"name": "Repeating Crossbow", "damage_str": "2d6", "ap": 3, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 12, "cost": "600", "notes": "AP 3, Magazine 6, ROF 2 w/Training edge, Jam on crit fail", "source": "Ammaria"},
    {"name": "Hand Crossbow (Ammarian)", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 2, "cost": "150", "notes": "Concealable (-2 to spot)", "source": "Ammaria"},
    {"name": "Dock Bow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 4, "cost": "60", "notes": "AP 1, Marine standard", "source": "Ammaria"},
    {"name": "Guild Halberd", "damage_str": "Str+d8", "ap": 1, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 12, "cost": "100", "notes": "AP 1, Reach 1, Two hands", "source": "Ammaria"},
    {"name": "Guild Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "25", "notes": "+1 Stealth to conceal", "source": "Ammaria"},
    {"name": "Slaver's Club", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "15", "notes": "Non-lethal", "source": "Ammaria"},
    {"name": "Sap", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "10", "notes": "Non-lethal, +2 Stealth to conceal", "source": "Ammaria"},
    {"name": "Boat Hook", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 4, "cost": "20", "notes": "Reach 1", "source": "Ammaria"},

    # ---------------------------------------------------------
    # TRIBUTE LANDS: SALTLANDS
    # ---------------------------------------------------------
    {"name": "Cutlass", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "200", "notes": "", "source": "Saltlands"},
    {"name": "Boarding Axe", "damage_str": "Str+d6", "ap": 1, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "150", "notes": "AP 1", "source": "Saltlands"},
    {"name": "Hook Hand", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "75", "notes": "Cannot be disarmed", "source": "Saltlands"},
    {"name": "Obsidian Blade", "damage_str": "Str+d6", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "350", "notes": "AP 2", "source": "Saltlands"},
    {"name": "Harpoon", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 4, "cost": "100", "notes": "", "source": "Saltlands"},
    {"name": "Belaying Pin", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "0", "notes": "Improvised", "source": "Saltlands"},
    {"name": "Grappling Hook", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "2/4/8", "reach": 0, "weight": 3, "cost": "50", "notes": "", "source": "Saltlands"},
    {"name": "Wheellock Pistol", "damage_str": "2d6+1", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 3, "cost": "350", "notes": "2 actions to reload", "source": "Saltlands"},
    {"name": "Blunderbuss", "damage_str": "1-3d6", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 6, "cost": "400", "notes": "Cone Template", "source": "Saltlands"},

    # ---------------------------------------------------------
    # TRIBUTE LANDS: VINLANDS
    # ---------------------------------------------------------
    {"name": "Bearded Axe", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "100", "notes": "See Bearded Axe special rules", "source": "Vinlands"},
    {"name": "Northern Battle Axe", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 8, "cost": "150", "notes": "Two hands, AP 1 vs rigid armour", "source": "Vinlands"},
    {"name": "Throwing Axe (Vinlander)", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 2, "cost": "25", "notes": "", "source": "Vinlands"},
    {"name": "Seax", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "25", "notes": "+1 Survival as tool", "source": "Vinlands"},
    {"name": "Valdmork Longbow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "12/24/48", "reach": 0, "weight": 3, "cost": "200", "notes": "AP 1, Min Str d6", "source": "Vinlands"},
    {"name": "Felsgard Crossbow", "damage_str": "2d6", "ap": 2, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "300", "notes": "AP 2, 2 actions to reload", "source": "Vinlands"},
    {"name": "War-Pick", "damage_str": "Str+d6", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "100", "notes": "AP 2", "source": "Vinlands"},
    {"name": "Mammoth Lance", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 10, "cost": "150", "notes": "Reach 2, +4 damage on charge, requires Large+ mount", "source": "Vinlands"},
    {"name": "Thornhook", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "30", "notes": "+1 Athletics (climbing) and Survival (foraging)", "source": "Vinlands"},

    # ---------------------------------------------------------
    # TRIBUTE LANDS: CONCORDIUM
    # ---------------------------------------------------------
    {"name": "Boarding Pike", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 5, "cost": "75", "notes": "Reach 1, +1 to resist Disarm", "source": "Concordium"},
    {"name": "Sky-Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 0.5, "cost": "25", "notes": "Balanced for throwing", "source": "Concordium"},
    {"name": "Rigging Axe", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "40", "notes": "Sever ropes as free action on Raise", "source": "Concordium"},
    {"name": "Grapple-Sword", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "100", "notes": "+2 Athletics when swinging on lines", "source": "Concordium"},
    {"name": "Cloudsilk Garrote", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 0, "cost": "50", "notes": "+2 Stealth to conceal", "source": "Concordium"},
    {"name": "Weighted Line", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "20", "notes": "Can entangle", "source": "Concordium"},
    {"name": "Boarding Crossbow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 4, "cost": "150", "notes": "Compact, one-handed, -1 Shooting", "source": "Concordium"},
    {"name": "Hunting Bow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "12/24/48", "reach": 0, "weight": 2, "cost": "200", "notes": "Light draw, mount-back use", "source": "Concordium"},
    {"name": "Grapple Bow", "damage_str": "-", "ap": 0, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 5, "cost": "250", "notes": "Fires grappling hooks, 50' line", "source": "Concordium"},
    {"name": "Wind Rifle", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "500", "notes": "AP 1, air-compressed, no gunpowder", "source": "Concordium"},
    {"name": "Repeating Crossbow (Concordium)", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 6, "cost": "400", "notes": "6-bolt magazine, ROF 2", "source": "Concordium"},
]


# =============================================================
# ARMOUR CATALOGUE
# =============================================================
# Fields: name, protection, area_protected, min_strength, weight, cost, notes, source

ARMOR = [
    # SAVAGE WORLDS CORE
    {"name": "Leather", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 10, "cost": "50", "notes": "", "source": "Core"},
    {"name": "Chain Mail", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 25, "cost": "300", "notes": "", "source": "Core"},
    {"name": "Plate Mail", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 35, "cost": "500", "notes": "", "source": "Core"},
    {"name": "Pot Helm", "protection": 3, "area_protected": "Head",
     "min_strength": "", "weight": 3, "cost": "75", "notes": "50% vs head shot", "source": "Core"},
    {"name": "Full Helm", "protection": 3, "area_protected": "Head",
     "min_strength": "", "weight": 4, "cost": "150", "notes": "", "source": "Core"},
    {"name": "Small Shield", "protection": 0, "area_protected": "Shield",
     "min_strength": "", "weight": 4, "cost": "25", "notes": "Parry +1", "source": "Core"},
    {"name": "Medium Shield", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 8, "cost": "50", "notes": "Parry +2, +2 Armor vs ranged", "source": "Core"},
    {"name": "Large Shield", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 12, "cost": "75", "notes": "Parry +3, +2 Armor vs ranged, -1 to attack", "source": "Core"},

    # FANTASY COMPANION
    {"name": "Hide Armour", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 12, "cost": "30", "notes": "", "source": "Fantasy Companion"},
    {"name": "Ring Mail", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 15, "cost": "100", "notes": "", "source": "Fantasy Companion"},
    {"name": "Scale Mail", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 20, "cost": "200", "notes": "", "source": "Fantasy Companion"},
    {"name": "Breastplate", "protection": 3, "area_protected": "Torso",
     "min_strength": "d8", "weight": 15, "cost": "200", "notes": "Torso only", "source": "Fantasy Companion"},
    {"name": "Half Plate", "protection": 3, "area_protected": "Torso, arms",
     "min_strength": "d8", "weight": 22, "cost": "350", "notes": "", "source": "Fantasy Companion"},
    {"name": "Full Plate", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 40, "cost": "750", "notes": "Heavy Armour", "source": "Fantasy Companion"},
    {"name": "Chain Coif", "protection": 3, "area_protected": "Head",
     "min_strength": "", "weight": 3, "cost": "100", "notes": "", "source": "Fantasy Companion"},

    # TRIBUTE LANDS: AMMARIA
    {"name": "Padded Jacket", "protection": 1, "area_protected": "Torso",
     "min_strength": "", "weight": 4, "cost": "25", "notes": "Worn under clothing", "source": "Ammaria"},
    {"name": "Guild Leathers", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 8, "cost": "100", "notes": "Standard militia issue", "source": "Ammaria"},
    {"name": "Sailor's Coat", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "", "weight": 5, "cost": "75", "notes": "Water-resistant, -1 swim penalty", "source": "Ammaria"},
    {"name": "Ammarian Breastplate", "protection": 4, "area_protected": "Torso",
     "min_strength": "d8", "weight": 15, "cost": "900", "notes": "-1 run penalty, +1 Intimidation", "source": "Ammaria"},
    {"name": "Guild Champion Plate", "protection": 5, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 25, "cost": "2500", "notes": "Full plate, guild elite only", "source": "Ammaria"},

    # TRIBUTE LANDS: SALTLANDS
    {"name": "Hardened Leather (Saltlands)", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "d4", "weight": 8, "cost": "75", "notes": "No swim penalty", "source": "Saltlands"},
    {"name": "Sharkskin Vest", "protection": 2, "area_protected": "Torso",
     "min_strength": "d6", "weight": 6, "cost": "200", "notes": "No swim penalty", "source": "Saltlands"},
    {"name": "Shell Armour", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 10, "cost": "250", "notes": "No swim penalty", "source": "Saltlands"},
    {"name": "Captain's Coat", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "d4", "weight": 5, "cost": "150", "notes": "Reinforced, no swim penalty", "source": "Saltlands"},

    # TRIBUTE LANDS: VINLANDS
    {"name": "Furs", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "", "weight": 8, "cost": "30", "notes": "+4 vs Cold environmental effects", "source": "Vinlands"},
    {"name": "Fur Armour", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 12, "cost": "50", "notes": "+4 vs Cold environmental effects", "source": "Vinlands"},
    {"name": "Greenbark", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 10, "cost": "100", "notes": "+2 Stealth in forests", "source": "Vinlands"},
    {"name": "Holtscarl Leathers", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 10, "cost": "75", "notes": "+2 Stealth in forests, no climbing penalty", "source": "Vinlands"},
    {"name": "Warden's Coat", "protection": 3, "area_protected": "Torso, arms",
     "min_strength": "d8", "weight": 18, "cost": "175", "notes": "Reinforced leather with iron rings", "source": "Vinlands"},
    {"name": "Felsgard Chain", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 25, "cost": "200", "notes": "+2 vs Cold environmental effects", "source": "Vinlands"},
    {"name": "Delver's Mail", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 20, "cost": "250", "notes": "Blackened, no snag penalty in tunnels", "source": "Vinlands"},
    {"name": "Felsgard Half-Plate", "protection": 3, "area_protected": "Torso",
     "min_strength": "d8", "weight": 25, "cost": "300", "notes": "Torso and shoulders only", "source": "Vinlands"},
    {"name": "Felsgard Plate", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 40, "cost": "500", "notes": "+2 vs Cold environmental effects", "source": "Vinlands"},
    {"name": "Mammoth-Scale", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 30, "cost": "600", "notes": "Rare, status symbol", "source": "Vinlands"},
    {"name": "Vinlander Round Shield (Medium)", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 8, "cost": "50", "notes": "Parry +2, +2 Armour vs ranged", "source": "Vinlands"},
    {"name": "Vinlander Round Shield (Large)", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 12, "cost": "75", "notes": "Parry +3, +2 Armour vs ranged, -1 to attack", "source": "Vinlands"},

    # TRIBUTE LANDS: CONCORDIUM
    {"name": "Flight Leathers", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "", "weight": 8, "cost": "100", "notes": "No swim/climbing penalty", "source": "Concordium"},
    {"name": "Cloudsilk Vest", "protection": 1, "area_protected": "Torso",
     "min_strength": "", "weight": 2, "cost": "300", "notes": "Near-weightless, concealed under clothing", "source": "Concordium"},
    {"name": "Boarding Coat", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 12, "cost": "200", "notes": "-1 Athletics for climbing", "source": "Concordium"},
]


# =============================================================
# GEAR CATALOGUE
# =============================================================
# Fields: name, weight, cost, notes, source

GEAR = [
    # SAVAGE WORLDS CORE — Adventuring Gear
    {"name": "Backpack", "weight": 2, "cost": "50", "notes": "", "source": "Core"},
    {"name": "Bedroll", "weight": 4, "cost": "25", "notes": "", "source": "Core"},
    {"name": "Candle (10)", "weight": 1, "cost": "5", "notes": "", "source": "Core"},
    {"name": "Crowbar", "weight": 2, "cost": "10", "notes": "", "source": "Core"},
    {"name": "Flint & Steel", "weight": 0.5, "cost": "3", "notes": "", "source": "Core"},
    {"name": "Grappling Hook", "weight": 2, "cost": "100", "notes": "", "source": "Core"},
    {"name": "Hammer", "weight": 1, "cost": "10", "notes": "", "source": "Core"},
    {"name": "Lantern", "weight": 2, "cost": "25", "notes": "", "source": "Core"},
    {"name": "Lockpicks", "weight": 0.5, "cost": "200", "notes": "", "source": "Core"},
    {"name": "Manacles", "weight": 1, "cost": "15", "notes": "", "source": "Core"},
    {"name": "Oil (1 pint)", "weight": 1, "cost": "2", "notes": "", "source": "Core"},
    {"name": "Quiver (20 arrows)", "weight": 2, "cost": "25", "notes": "", "source": "Core"},
    {"name": "Rope (50')", "weight": 7, "cost": "10", "notes": "", "source": "Core"},
    {"name": "Shovel", "weight": 3, "cost": "5", "notes": "", "source": "Core"},
    {"name": "Spyglass", "weight": 1, "cost": "500", "notes": "", "source": "Core"},
    {"name": "Torch (6)", "weight": 3, "cost": "5", "notes": "", "source": "Core"},
    {"name": "Waterskin", "weight": 1, "cost": "5", "notes": "", "source": "Core"},
    {"name": "Whetstone", "weight": 0.5, "cost": "5", "notes": "", "source": "Core"},
    {"name": "Fine Clothing", "weight": 2, "cost": "200", "notes": "", "source": "Core"},
    {"name": "Normal Clothing", "weight": 2, "cost": "20", "notes": "", "source": "Core"},
    {"name": "Winter Clothing", "weight": 4, "cost": "50", "notes": "", "source": "Core"},
    {"name": "Rations (1 week)", "weight": 5, "cost": "10", "notes": "", "source": "Core"},
    {"name": "Healers Kit", "weight": 2, "cost": "25", "notes": "+1 Healing, 5 uses", "source": "Core"},

    # FANTASY COMPANION
    {"name": "Holy Symbol", "weight": 0.5, "cost": "25", "notes": "Required for Miracles (Faith)", "source": "Fantasy Companion"},
    {"name": "Arcane Fetish", "weight": 0.5, "cost": "50", "notes": "Arcane focus", "source": "Fantasy Companion"},
    {"name": "Spell Components Pouch", "weight": 1, "cost": "50", "notes": "", "source": "Fantasy Companion"},
    {"name": "Thieves' Tools", "weight": 1, "cost": "250", "notes": "+1 Thievery for locks/traps", "source": "Fantasy Companion"},
    {"name": "Climber's Kit", "weight": 3, "cost": "100", "notes": "+1 Athletics (climbing)", "source": "Fantasy Companion"},
    {"name": "Disguise Kit", "weight": 2, "cost": "100", "notes": "+1 Performance (disguise)", "source": "Fantasy Companion"},
    {"name": "Potion of Healing", "weight": 0.5, "cost": "150", "notes": "Heal one Wound", "source": "Fantasy Companion"},

    # TRIBUTE LANDS: AMMARIA
    {"name": "Ammarian Steel Tools", "weight": 3, "cost": "100", "notes": "+1 Repair", "source": "Ammaria"},
    {"name": "Merchant's Ledger", "weight": 1, "cost": "25", "notes": "+1 Common Knowledge (trade)", "source": "Ammaria"},
    {"name": "Guild Credentials", "weight": 0, "cost": "Varies", "notes": "Required for guild privileges", "source": "Ammaria"},
    {"name": "Tribute Documents (Forged)", "weight": 0, "cost": "500+", "notes": "Criminal offence if caught", "source": "Ammaria"},
    {"name": "Bribery Purse", "weight": 1, "cost": "100+", "notes": "Pre-counted denominations for quick bribes", "source": "Ammaria"},

    # TRIBUTE LANDS: SALTLANDS
    {"name": "Navigator's Charts (Sound)", "weight": 1, "cost": "500", "notes": "+1 Boating in charted waters", "source": "Saltlands"},
    {"name": "Spyglass (Saltlands)", "weight": 1, "cost": "200", "notes": "", "source": "Saltlands"},
    {"name": "Storm Glass", "weight": 1, "cost": "150", "notes": "Weather prediction, +1 Survival", "source": "Saltlands"},
    {"name": "Diving Lung", "weight": 2, "cost": "500", "notes": "30 minutes underwater", "source": "Saltlands"},
    {"name": "Sailor's Charm", "weight": 0, "cost": "25", "notes": "Blessed, psychological comfort", "source": "Saltlands"},
    {"name": "Storm Pearl", "weight": 0, "cost": "100", "notes": "One-use weather calming", "source": "Saltlands"},
    {"name": "Grappling Gear", "weight": 3, "cost": "25", "notes": "Per person, for boarding", "source": "Saltlands"},
    {"name": "Ship Repair Kit", "weight": 10, "cost": "100", "notes": "+1 Repair (ships)", "source": "Saltlands"},

    # TRIBUTE LANDS: VINLANDS
    {"name": "Thornhook (tool)", "weight": 2, "cost": "30", "notes": "+1 Athletics (climbing), +1 Survival (foraging)", "source": "Vinlands"},
    {"name": "Canopy Harness", "weight": 5, "cost": "50", "notes": "Negates fall damage under 30' when anchored", "source": "Vinlands"},
    {"name": "Waldl Cloak", "weight": 4, "cost": "75", "notes": "+2 Stealth in forests, +2 vs Cold/wet", "source": "Vinlands"},
    {"name": "Goblin-Smoke Pots (3)", "weight": 3, "cost": "25", "notes": "MBT for 3 rds, goblinoids Vigor or flee", "source": "Vinlands"},
    {"name": "Tree-Spikes", "weight": 2, "cost": "15", "notes": "+2 Athletics (climbing trees)", "source": "Vinlands"},

    # TRIBUTE LANDS: CONCORDIUM
    {"name": "Barometric Charm", "weight": 0, "cost": "100", "notes": "Glows on sudden altitude drop", "source": "Concordium"},
    {"name": "Wind-Reader Ribbons", "weight": 0, "cost": "25", "notes": "Show air current direction/speed", "source": "Concordium"},
    {"name": "Pressure Flask", "weight": 2, "cost": "75", "notes": "Sealed, maintains surface pressure", "source": "Concordium"},
    {"name": "Signal Mirror", "weight": 0, "cost": "15", "notes": "Long-distance visual comms", "source": "Concordium"},
    {"name": "Rescue Whistle", "weight": 0, "cost": "30", "notes": "Audible 1 mile", "source": "Concordium"},
    {"name": "Night-Eye Drops", "weight": 0, "cost": "50", "notes": "Low-light vision 4 hrs, light-sensitive after", "source": "Concordium"},
    {"name": "Emergency Parachute", "weight": 5, "cost": "200", "notes": "Single use, deploy as free action", "source": "Concordium"},
]


# All unique sources for filter dropdowns
SOURCES = ["Core", "Fantasy Companion", "Ammaria", "Saltlands", "Vinlands", "Concordium"]


def get_weapons(source=None):
    if source and source != "All":
        return [w for w in WEAPONS if w["source"] == source]
    return WEAPONS

def get_armor(source=None):
    if source and source != "All":
        return [a for a in ARMOR if a["source"] == source]
    return ARMOR

def get_gear(source=None):
    if source and source != "All":
        return [g for g in GEAR if g["source"] == source]
    return GEAR
