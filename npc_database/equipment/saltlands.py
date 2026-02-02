"""
Saltlands — Regional Weapons, Armour, and Gear
The island chains — pirates, traders, and those who harvest the sea.
"""

SOURCE = "Saltlands"

WEAPONS = [
    # Melee
    {"name": "Cutlass", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "200", "notes": ""},
    {"name": "Boarding Axe", "damage_str": "Str+d6", "ap": 1, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "150", "notes": "AP 1"},
    {"name": "Hook Hand", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "75", "notes": "Cannot be disarmed"},
    {"name": "Obsidian Blade", "damage_str": "Str+d6", "ap": 2, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "350", "notes": "AP 2"},
    {"name": "Belaying Pin", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "0", "notes": "Improvised"},
    # Thrown
    {"name": "Harpoon", "damage_str": "Str+d6", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 4, "cost": "100", "notes": ""},
    {"name": "Grappling Hook", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "2/4/8", "reach": 0, "weight": 3, "cost": "50", "notes": ""},
    # Ranged
    {"name": "Wheellock Pistol", "damage_str": "2d6+1", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 3, "cost": "350", "notes": "2 actions to reload"},
    {"name": "Blunderbuss", "damage_str": "1-3d6", "ap": 0, "trait_type": "Ranged",
     "range": "5/10/20", "reach": 0, "weight": 6, "cost": "400", "notes": "Cone Template"},
]

ARMOR = [
    {"name": "Hardened Leather (Saltlands)", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "d4", "weight": 8, "cost": "75", "notes": "No swim penalty"},
    {"name": "Sharkskin Vest", "protection": 2, "area_protected": "Torso",
     "min_strength": "d6", "weight": 6, "cost": "200", "notes": "No swim penalty"},
    {"name": "Shell Armour", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 10, "cost": "250", "notes": "No swim penalty"},
    {"name": "Captain's Coat", "protection": 1, "area_protected": "Torso, arms",
     "min_strength": "d4", "weight": 5, "cost": "150", "notes": "Reinforced, no swim penalty"},
]

GEAR = [
    {"name": "Navigator's Charts (Sound)", "weight": 1, "cost": "500", 
     "notes": "+1 Boating in charted waters"},
    {"name": "Spyglass (Saltlands)", "weight": 1, "cost": "200", "notes": ""},
    {"name": "Storm Glass", "weight": 1, "cost": "150", 
     "notes": "Weather prediction, +1 Survival"},
    {"name": "Diving Lung", "weight": 2, "cost": "500", 
     "notes": "30 minutes underwater"},
    {"name": "Sailor's Charm", "weight": 0, "cost": "25", 
     "notes": "Blessed, psychological comfort"},
    {"name": "Storm Pearl", "weight": 0, "cost": "100", 
     "notes": "One-use weather calming"},
    {"name": "Grappling Gear", "weight": 3, "cost": "25", 
     "notes": "Per person, for boarding"},
    {"name": "Ship Repair Kit", "weight": 10, "cost": "100", 
     "notes": "+1 Repair (ships)"},
]
