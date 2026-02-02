"""
Concordium — Regional Weapons, Armour, and Gear
The sky-cities — airship crews, altitude specialists, and those who live above the clouds.
"""

SOURCE = "Concordium"

WEAPONS = [
    # Melee
    {"name": "Boarding Pike", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 1, "weight": 5, "cost": "75", 
     "notes": "Reach 1, +1 to resist Disarm"},
    {"name": "Rigging Axe", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 2, "cost": "40", 
     "notes": "Sever ropes as free action on Raise"},
    {"name": "Grapple-Sword", "damage_str": "Str+d6", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 3, "cost": "100", 
     "notes": "+2 Athletics when swinging on lines"},
    {"name": "Cloudsilk Garrote", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 0, "cost": "50", 
     "notes": "+2 Stealth to conceal"},
    {"name": "Weighted Line", "damage_str": "Str+d4", "ap": 0, "trait_type": "Melee",
     "range": "", "reach": 0, "weight": 1, "cost": "20", 
     "notes": "Can entangle"},
    # Thrown
    {"name": "Sky-Knife", "damage_str": "Str+d4", "ap": 0, "trait_type": "Thrown",
     "range": "3/6/12", "reach": 0, "weight": 0.5, "cost": "25", 
     "notes": "Balanced for throwing"},
    # Ranged
    {"name": "Boarding Crossbow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 4, "cost": "150", 
     "notes": "Compact, one-handed, -1 Shooting"},
    {"name": "Hunting Bow", "damage_str": "2d6", "ap": 0, "trait_type": "Ranged",
     "range": "12/24/48", "reach": 0, "weight": 2, "cost": "200", 
     "notes": "Light draw, mount-back use"},
    {"name": "Grapple Bow", "damage_str": "-", "ap": 0, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 5, "cost": "250", 
     "notes": "Fires grappling hooks, 50' line"},
    {"name": "Wind Rifle", "damage_str": "2d6", "ap": 1, "trait_type": "Ranged",
     "range": "15/30/60", "reach": 0, "weight": 8, "cost": "500", 
     "notes": "AP 1, air-compressed, no gunpowder"},
    {"name": "Repeating Crossbow (Concordium)", "damage_str": "2d4", "ap": 0, "trait_type": "Ranged",
     "range": "10/20/40", "reach": 0, "weight": 6, "cost": "400", 
     "notes": "6-bolt magazine, ROF 2"},
]

ARMOR = [
    {"name": "Flight Leathers", "protection": 1, "area_protected": "Torso, arms, legs",
     "min_strength": "", "weight": 8, "cost": "100", 
     "notes": "No swim/climbing penalty"},
    {"name": "Cloudsilk Vest", "protection": 1, "area_protected": "Torso",
     "min_strength": "", "weight": 2, "cost": "300", 
     "notes": "Near-weightless, concealed under clothing"},
    {"name": "Boarding Coat", "protection": 2, "area_protected": "Torso, arms",
     "min_strength": "d6", "weight": 12, "cost": "200", 
     "notes": "-1 Athletics for climbing"},
]

GEAR = [
    {"name": "Barometric Charm", "weight": 0, "cost": "100", 
     "notes": "Glows on sudden altitude drop"},
    {"name": "Wind-Reader Ribbons", "weight": 0, "cost": "25", 
     "notes": "Show air current direction/speed"},
    {"name": "Pressure Flask", "weight": 2, "cost": "75", 
     "notes": "Sealed, maintains surface pressure"},
    {"name": "Signal Mirror", "weight": 0, "cost": "15", 
     "notes": "Long-distance visual comms"},
    {"name": "Rescue Whistle", "weight": 0, "cost": "30", 
     "notes": "Audible 1 mile"},
    {"name": "Night-Eye Drops", "weight": 0, "cost": "50", 
     "notes": "Low-light vision 4 hrs, light-sensitive after"},
    {"name": "Emergency Parachute", "weight": 5, "cost": "200", 
     "notes": "Single use, deploy as free action"},
]
