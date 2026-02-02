"""
Saltlands — Regional Edges
The island chains — sea legs, storm magic, and corsair codes.
"""

SOURCE = "Saltlands"

EDGES = [
    # Background Edges
    {"name": "Reefborn", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "Hold breath 2× normal; +2 Athletics (swimming); low-light vision underwater"},
    {"name": "Salt-Weathered", "rank": "Novice", "type": "Background",
     "requirements": "Vigor d6+", "summary": "+2 Vigor vs sea hazards (drowning, exposure, storms)"},
    {"name": "Saltborn Navigator", "rank": "Novice", "type": "Background",
     "requirements": "Smarts d6+", "summary": "+2 Boating; can navigate by stars; sense weather changes"},
    
    # Combat Edges
    {"name": "Brace of Pistols", "rank": "Novice", "type": "Combat",
     "requirements": "Shooting d6+", "summary": "Draw and fire up to 3 pistols as single action"},
    {"name": "Cutlass & Pistol", "rank": "Seasoned", "type": "Combat",
     "requirements": "Fighting d6+, Shooting d6+", "summary": "Two-Fisted with sword/pistol combo; +1 Parry"},
    {"name": "Brawler's Tempo", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d6+", "summary": "Ignore 2 points of Gang Up bonus; +1 unarmed damage"},
    {"name": "Boarding Action", "rank": "Seasoned", "type": "Combat",
     "requirements": "Athletics d8+, Fighting d6+", "summary": "+2 Fighting on first round after boarding; ignore Unstable Platform"},
    {"name": "Storm Fighter", "rank": "Seasoned", "type": "Combat",
     "requirements": "Agility d8+", "summary": "Ignore weather penalties in combat; +1 Parry in rain/storm"},
    
    # Professional Edges
    {"name": "Prize Master", "rank": "Seasoned", "type": "Professional",
     "requirements": "Smarts d8+, Boating d6+", "summary": "+2 to assess prize value; +2 Persuasion dividing plunder"},
    {"name": "Ship's Surgeon", "rank": "Novice", "type": "Professional",
     "requirements": "Healing d8+", "summary": "+2 Healing at sea; ignore -2 battlefield conditions"},
    {"name": "Reef-Diver", "rank": "Novice", "type": "Professional",
     "requirements": "Athletics d8+", "summary": "+2 Notice underwater; ignore pressure penalties to 100 feet"},
    
    # Social Edges
    {"name": "Code-Keeper", "rank": "Seasoned", "type": "Social",
     "requirements": "Spirit d8+", "summary": "+2 Persuasion with corsairs; can invoke Code for arbitration"},
    {"name": "Captain's Authority", "rank": "Veteran", "type": "Social",
     "requirements": "Command, Spirit d8+", "summary": "Command edges extend to entire crew; +2 Intimidation aboard ship"},
    
    # Power Edges
    {"name": "Storm Caller", "rank": "Novice", "type": "Power",
     "requirements": "AB, Spirit d6+", "summary": "+2 arcane skill for weather/water/lightning powers; +2 Boating in storms"},
    {"name": "Sea Witch", "rank": "Novice", "type": "Power",
     "requirements": "AB, Smarts d6+", "summary": "+2 arcane skill for curses/hexes; +2 Healing for sea conditions"},
    {"name": "Thalassa's Voice", "rank": "Novice", "type": "Power",
     "requirements": "AB, Spirit d6+", "summary": "+2 arcane skill within sight of sea; +2 Intimidation vs sailors"},
    {"name": "Soul Warden", "rank": "Seasoned", "type": "Power",
     "requirements": "AB (Miracles), Spirit d8+", "summary": "+2 to powers affecting spirits/undead; sense nearby death"},
]
