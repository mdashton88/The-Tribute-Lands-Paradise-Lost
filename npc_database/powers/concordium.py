"""
Concordium — Regional Powers
The sky-cities — wind magic, pressure manipulation, and runic artifice.
Typical trappings: Wind and cloud, lightning, runes and clockwork, crystallised air.
"""

SOURCE = "Concordium"

POWERS = [
    # Sky-Binder Powers
    {"name": "Wind Lift", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "5 rounds",
     "summary": "Slow falls and grants +4 to jumping; can glide horizontally"},
    {"name": "Air Bubble", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "1 hour",
     "summary": "Create breathable air in Small Burst; works at any altitude"},
    {"name": "Pressure Wave", "rank": "Seasoned", "pp": "3", "range": "Smarts", "duration": "Instant",
     "summary": "Cone Template; Str roll or knocked back 2d6\"; 2d6 damage on collision"},
    {"name": "Cloud Walk", "rank": "Veteran", "pp": "3", "range": "Self", "duration": "5 rounds",
     "summary": "Walk on clouds and mist as solid ground; Pace 6"},
    {"name": "Eye of the Storm", "rank": "Seasoned", "pp": "3", "range": "Self (MBT)", "duration": "5 rounds",
     "summary": "Create calm area in storm; ignore all weather penalties inside"},
    
    # Runic Artificer Powers
    {"name": "Inscribe Rune", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "24 hours",
     "summary": "Create temporary enchantment on object; one power stored"},
    {"name": "Activate Mechanism", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "1 hour",
     "summary": "Power clockwork device without fuel; +2 Repair"},
    {"name": "Runic Shield", "rank": "Seasoned", "pp": "3", "range": "Touch", "duration": "5 rounds",
     "summary": "+4 Armor vs magic; +2 to resist powers; runes glow when active"},
    
    # Pressure Magic
    {"name": "Altitude Sickness", "rank": "Seasoned", "pp": "2", "range": "Smarts", "duration": "Instant",
     "summary": "Target suffers altitude effects; Vigor or 1 Fatigue"},
    {"name": "Void Pocket", "rank": "Veteran", "pp": "4", "range": "Touch", "duration": "5 rounds",
     "summary": "Remove air from SBT; 2d6 damage per round, Vigor for half; no sound"},
    {"name": "Pressure Seal", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "1 hour",
     "summary": "Seal container/room against pressure changes; airtight"},
]
