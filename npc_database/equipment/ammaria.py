"""
Ammaria — Regional Weapons, Armour, and Gear
The Merchant Realms — guilds, trade routes, and pragmatic commerce.
"""

SOURCE = "Ammaria"

WEAPONS = [
    # Ranged
    {"name": "Repeating Crossbow", "damage_str": "2d6", "ap": 3, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 12, "cost": "600", 
     "notes": "AP 3, Magazine 6, ROF 2 w/Training edge, Jam on crit fail"},
    {"name": "Hand Crossbow (Ammarian)", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 2, "cost": "150", 
     "notes": "Concealable (-2 to spot)"},
    {"name": "Dock Bow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 4, "cost": "60", 
     "notes": "AP 1, Marine standard"},
    # Melee
    {"name": "Guild Halberd", "damage_str": "Str+d8", "ap": 1, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 12, "cost": "100", 
     "notes": "AP 1, Reach 1, Two hands"},
    {"name": "Guild Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "25", 
     "notes": "+1 Stealth to conceal"},
    {"name": "Slaver's Club", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "15", 
     "notes": "Non-lethal"},
    {"name": "Sap", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "10", 
     "notes": "Non-lethal, +2 Stealth to conceal"},
    {"name": "Boat Hook", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 4, "cost": "20", 
     "notes": "Reach 1"},
]

ARMOR = [
    {"name": "Padded Jacket", "protection": 1, "area_protected": "Torso",
     "min_strength": "", "weight": 4, "cost": "25", 
     "notes": "Worn under clothing"},
    {"name": "Guild Leathers", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 8, "cost": "100", 
     "notes": "Standard militia issue"},
    {"name": "Sailor's Coat", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "", "weight": 5, "cost": "75", 
     "notes": "Water-resistant, -1 swim penalty"},
    {"name": "Ammarian Breastplate", "protection": 4, "area_protected": "Torso",
     "min_strength": "d8", "weight": 15, "cost": "900", 
     "notes": "-1 run penalty, +1 Intimidation"},
    {"name": "Guild Champion Plate", "protection": 5, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 25, "cost": "2500", 
     "notes": "Full plate, guild elite only"},
]

GEAR = [
    {"name": "Ammarian Steel Tools", "weight": 3, "cost": "100", 
     "notes": "+1 Repair"},
    {"name": "Merchant's Ledger", "weight": 1, "cost": "25", 
     "notes": "+1 Common Knowledge (trade)"},
    {"name": "Guild Credentials", "weight": 0, "cost": "Varies", 
     "notes": "Required for guild privileges"},
    {"name": "Tribute Documents (Forged)", "weight": 0, "cost": "500+", 
     "notes": "Criminal offence if caught"},
    {"name": "Bribery Purse", "weight": 1, "cost": "100+", 
     "notes": "Pre-counted denominations for quick bribes"},
]
