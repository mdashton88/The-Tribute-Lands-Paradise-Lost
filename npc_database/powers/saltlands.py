"""
Saltlands — Regional Powers
The island chains — storm magic, sea curses, and the voices of the deep.
Typical trappings: Seawater, lightning, fog, coral, whale-song, salt spray.
"""

SOURCE = "Saltlands"

POWERS = [
    # Storm Caller Powers
    {"name": "Call Storm", "rank": "Seasoned", "pp": "4", "range": "Self (1 mile)", "duration": "1 hour",
     "summary": "Summon or intensify storm; -2 to all Boating rolls in area"},
    {"name": "Calm Seas", "rank": "Novice", "pp": "2", "range": "Self (ship)", "duration": "1 hour",
     "summary": "Reduce sea state by one level; ignore storm penalties"},
    {"name": "Lightning Strike", "rank": "Seasoned", "pp": "3", "range": "Smarts×2", "duration": "Instant",
     "summary": "3d6 damage, AP 2; +1d6 if target wearing metal"},
    {"name": "Wind Wall", "rank": "Novice", "pp": "2", "range": "Smarts", "duration": "5 rounds",
     "summary": "Barrier of wind; -4 to ranged attacks through"},
    {"name": "Favourable Winds", "rank": "Novice", "pp": "2", "range": "Self (ship)", "duration": "4 hours",
     "summary": "+2 to Boating; increase ship speed by 25%"},
    
    # Sea Witch Powers (Curses)
    {"name": "Sea Curse", "rank": "Seasoned", "pp": "3", "range": "Touch", "duration": "Permanent",
     "summary": "-2 to Boating and swimming; Spirit to resist; requires ritual to remove"},
    {"name": "Drowning Touch", "rank": "Veteran", "pp": "4", "range": "Touch", "duration": "Instant",
     "summary": "Target's lungs fill with water; Vigor or Stunned, 2d6 on Raise"},
    {"name": "Blood Toll", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "Instant",
     "summary": "Sacrifice blood (1 Wound) for +2 to next roll or appease sea creatures"},
    
    # Temple of Thalassa Powers
    {"name": "Breathe Water", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "1 hour",
     "summary": "Breathe underwater; speak normally; resist pressure to 100 fathoms"},
    {"name": "Speak with Fish", "rank": "Novice", "pp": "1", "range": "Smarts", "duration": "10 min",
     "summary": "Communicate with sea creatures; limited by intelligence"},
    {"name": "Sea's Blessing", "rank": "Seasoned", "pp": "3", "range": "Touch (ship)", "duration": "1 week",
     "summary": "Ship gains +2 to all Boating; crew +2 vs sea hazards"},
]
