"""
Fantasy Companion — Weapons, Armour, and Gear
Source: Savage Worlds Fantasy Companion
"""

SOURCE = "Fantasy Companion"

WEAPONS = [
    # Melee Weapons
    {"name": "Bastard Sword", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "350", "notes": "Two hands for Str+d10"},
    {"name": "Scimitar", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "300", "notes": ""},
    {"name": "Morningstar", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "200", "notes": ""},
    {"name": "War Flail", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 5, "cost": "300", "notes": "Ignores Shield bonus, Two hands"},
    {"name": "Trident", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "3/6/12", "reach": 1, "weight": 4, "cost": "150", "notes": "Reach 1, can be thrown"},
    {"name": "Whip", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 1, "cost": "50", "notes": "Reach 2, can Entangle"},
    {"name": "Cestus", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "50", "notes": "Fist weapon"},
    # Ranged Weapons
    {"name": "Short Bow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 2, "cost": "200", "notes": ""},
    {"name": "Composite Bow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 3, "cost": "400", "notes": "AP 1"},
    {"name": "Hand Crossbow", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 1, "cost": "200", "notes": "One hand"},
    {"name": "Heavy Crossbow", "damage_str": "2d8", "ap": 2, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "400", "notes": "AP 2, Reload 2"},
    {"name": "Javelin", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 2, "cost": "50", "notes": ""},
    {"name": "Throwing Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 0.5, "cost": "25", "notes": ""},
]

ARMOR = [
    {"name": "Hide Armour", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 12, "cost": "30", "notes": ""},
    {"name": "Ring Mail", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 15, "cost": "100", "notes": ""},
    {"name": "Scale Mail", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 20, "cost": "200", "notes": ""},
    {"name": "Breastplate", "protection": 3, "area_protected": "Torso",
     "min_strength": "d8", "weight": 15, "cost": "200", "notes": "Torso only"},
    {"name": "Half Plate", "protection": 3, "area_protected": "Torso, arms",
     "min_strength": "d8", "weight": 22, "cost": "350", "notes": ""},
    {"name": "Full Plate", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 40, "cost": "750", "notes": "Heavy Armour"},
    {"name": "Chain Coif", "protection": 3, "area_protected": "Head",
     "min_strength": "", "weight": 3, "cost": "100", "notes": ""},
]

GEAR = [
    {"name": "Holy Symbol", "weight": 0.5, "cost": "25", "notes": "Required for Miracles (Faith)"},
    {"name": "Arcane Fetish", "weight": 0.5, "cost": "50", "notes": "Arcane focus"},
    {"name": "Spell Components Pouch", "weight": 1, "cost": "50", "notes": ""},
    {"name": "Thieves' Tools", "weight": 1, "cost": "250", "notes": "+1 Thievery for locks/traps"},
    {"name": "Climber's Kit", "weight": 3, "cost": "100", "notes": "+1 Athletics (climbing)"},
    {"name": "Disguise Kit", "weight": 2, "cost": "100", "notes": "+1 Performance (disguise)"},
    {"name": "Potion of Healing", "weight": 0.5, "cost": "150", "notes": "Heal one Wound"},
]
