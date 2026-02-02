"""
Vinlands — Regional Powers
The northern forests — druid magic, warlock hexes, and the voices of the wild.
Typical trappings: Leaves and bark, animal spirits, blood runes, moonlight, root and vine.
"""

SOURCE = "Vinlands"

POWERS = [
    # Druid/Grove Powers
    {"name": "Speak with Plants", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "10 min",
     "summary": "Communicate with plants; learn what they've witnessed"},
    {"name": "Forest Walk", "rank": "Novice", "pp": "2", "range": "Self", "duration": "1 hour",
     "summary": "Pass through vegetation without trace; ignore Difficult Ground"},
    {"name": "Nature's Wrath", "rank": "Seasoned", "pp": "3", "range": "Smarts", "duration": "Instant",
     "summary": "Plants attack; 2d6 damage and Entangled in LBT"},
    {"name": "Grove Ward", "rank": "Veteran", "pp": "5", "range": "Touch", "duration": "24 hours",
     "summary": "Protect natural area; +4 to detect intruders, plants resist them"},
    {"name": "Call the Hunt", "rank": "Seasoned", "pp": "3", "range": "1 mile", "duration": "1 hour",
     "summary": "Summon local predators to aid; arrive in 2d6 minutes"},
    
    # Warlock/Witch Powers (Hexes)
    {"name": "Hex", "rank": "Novice", "pp": "2", "range": "Smarts", "duration": "Until sunset/sunrise",
     "summary": "-1 to all Trait rolls; -2 on Raise; Spirit to resist"},
    {"name": "Evil Eye", "rank": "Seasoned", "pp": "3", "range": "Sight", "duration": "1 week",
     "summary": "Target suffers bad luck; GM gains 2 Complications per session"},
    {"name": "Wasting Curse", "rank": "Veteran", "pp": "4", "range": "Touch", "duration": "Permanent",
     "summary": "Target loses 1 Vigor die; ritual to remove; Spirit resists"},
    {"name": "Witch-Sight", "rank": "Novice", "pp": "1", "range": "Self", "duration": "5 rounds",
     "summary": "See through illusions; detect supernatural creatures"},
    {"name": "Crone's Blessing", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "1 day",
     "summary": "+2 to one skill; typically Survival, Healing, or Notice"},
    
    # Blood Magic (Dangerous)
    {"name": "Blood Bond", "rank": "Seasoned", "pp": "3 + wound", "range": "Touch", "duration": "Permanent",
     "summary": "Link two creatures; sense location and condition; share 1 Wound"},
    {"name": "Sacrifice", "rank": "Veteran", "pp": "Special", "range": "Touch", "duration": "Instant",
     "summary": "Convert wounds to PP (1 Wound = 5 PP); dangerous"},
]
