"""
Vinlands — Regional Weapons, Armour, and Gear
The northern forests and mountains — hardy folk, ancient ruins, and cold steel.
"""

SOURCE = "Vinlands"

WEAPONS = [
    # Melee
    {"name": "Bearded Axe", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "100", 
     "notes": "See Bearded Axe special rules"},
    {"name": "Northern Battle Axe", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 8, "cost": "150", 
     "notes": "Two hands, AP 1 vs rigid armour"},
    {"name": "Seax", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "25", 
     "notes": "+1 Survival as tool"},
    {"name": "War-Pick", "damage_str": "Str+d6", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 4, "cost": "100", "notes": "AP 2"},
    {"name": "Mammoth Lance", "damage_str": "Str+d8", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 2, "weight": 10, "cost": "150", 
     "notes": "Reach 2, +4 damage on charge, requires Large+ mount"},
    {"name": "Thornhook", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "30", 
     "notes": "+1 Athletics (climbing) and Survival (foraging)"},
    # Thrown
    {"name": "Throwing Axe (Vinlander)", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 2, "cost": "25", "notes": ""},
    # Ranged
    {"name": "Valdmork Longbow", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "12/24/48", "reach": 0, "weight": 3, "cost": "200", 
     "notes": "AP 1, Min Str d6"},
    {"name": "Felsgard Crossbow", "damage_str": "2d6", "ap": 2, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "300", 
     "notes": "AP 2, 2 actions to reload"},
]

ARMOR = [
    {"name": "Furs", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "", "weight": 8, "cost": "30", 
     "notes": "+4 vs Cold environmental effects"},
    {"name": "Fur Armour", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 12, "cost": "50", 
     "notes": "+4 vs Cold environmental effects"},
    {"name": "Greenbark", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 10, "cost": "100", 
     "notes": "+2 Stealth in forests"},
    {"name": "Holtscarl Leathers", "protection": 2, "area_protected": "Torso, arms, legs",
     "min_strength": "d6", "weight": 10, "cost": "75", 
     "notes": "+2 Stealth in forests, no climbing penalty"},
    {"name": "Warden's Coat", "protection": 3, "area_protected": "Torso, arms",
     "min_strength": "d8", "weight": 18, "cost": "175", 
     "notes": "Reinforced leather with iron rings"},
    {"name": "Felsgard Chain", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 25, "cost": "200", 
     "notes": "+2 vs Cold environmental effects"},
    {"name": "Delver's Mail", "protection": 3, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 20, "cost": "250", 
     "notes": "Blackened, no snag penalty in tunnels"},
    {"name": "Felsgard Half-Plate", "protection": 3, "area_protected": "Torso",
     "min_strength": "d8", "weight": 25, "cost": "300", 
     "notes": "Torso and shoulders only"},
    {"name": "Felsgard Plate", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d10", "weight": 40, "cost": "500", 
     "notes": "+2 vs Cold environmental effects"},
    {"name": "Mammoth-Scale", "protection": 4, "area_protected": "Torso, arms, legs",
     "min_strength": "d8", "weight": 30, "cost": "600", 
     "notes": "Rare, status symbol"},
    {"name": "Vinlander Round Shield (Medium)", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 8, "cost": "50", 
     "notes": "Parry +2, +2 Armour vs ranged"},
    {"name": "Vinlander Round Shield (Large)", "protection": 2, "area_protected": "Shield",
     "min_strength": "", "weight": 12, "cost": "75", 
     "notes": "Parry +3, +2 Armour vs ranged, -1 to attack"},
]

GEAR = [
    {"name": "Thornhook (tool)", "weight": 2, "cost": "30", 
     "notes": "+1 Athletics (climbing), +1 Survival (foraging)"},
    {"name": "Canopy Harness", "weight": 5, "cost": "50", 
     "notes": "Negates fall damage under 30' when anchored"},
    {"name": "Waldl Cloak", "weight": 4, "cost": "75", 
     "notes": "+2 Stealth in forests, +2 vs Cold/wet"},
    {"name": "Goblin-Smoke Pots (3)", "weight": 3, "cost": "25", 
     "notes": "MBT for 3 rds, goblinoids Vigor or flee"},
    {"name": "Tree-Spikes", "weight": 2, "cost": "15", 
     "notes": "+2 Athletics (climbing trees)"},
]
