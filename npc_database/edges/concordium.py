"""
Concordium — Regional Edges
The sky-cities — altitude mastery, aerial combat, and wind magic.
"""

SOURCE = "Concordium"

EDGES = [
    # Background Edges
    {"name": "Sky-Born", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+2 Vigor vs altitude effects; no penalties from thin air"},
    {"name": "Cloud-Walker", "rank": "Novice", "type": "Background",
     "requirements": "Agility d6+", "summary": "+2 Athletics (climbing, balance); no fear of heights"},
    {"name": "Noble House", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+2 Persuasion with nobility; access to house resources"},
    
    # Combat Edges
    {"name": "Rigging Fighter", "rank": "Novice", "type": "Combat",
     "requirements": "Athletics d8+, Fighting d6+", "summary": "+2 Fighting while climbing/hanging; ignore Unstable Platform on rigging"},
    {"name": "Wind Rider", "rank": "Seasoned", "type": "Combat",
     "requirements": "Piloting d8+ or Riding d8+ (flying mount)", "summary": "+2 Piloting/Riding for flying vehicles/mounts; +1 damage on strafing runs"},
    {"name": "Altitude Fighter", "rank": "Seasoned", "type": "Combat",
     "requirements": "Fighting d8+", "summary": "+1 Parry when higher than opponent; +2 damage when striking from above"},
    {"name": "Grapple Expert", "rank": "Novice", "type": "Combat",
     "requirements": "Athletics d8+", "summary": "+2 Athletics with grappling hooks/lines; can attack while swinging"},
    
    # Professional Edges
    {"name": "Airship Pilot", "rank": "Novice", "type": "Professional",
     "requirements": "Piloting d6+", "summary": "+2 Piloting for airships; +2 Notice for weather/air currents"},
    {"name": "Pressure Technician", "rank": "Novice", "type": "Professional",
     "requirements": "Repair d6+, Smarts d6+", "summary": "+2 Repair on altitude equipment; create emergency pressure gear"},
    {"name": "Wind Reader", "rank": "Novice", "type": "Professional",
     "requirements": "Notice d6+", "summary": "+2 Notice for weather prediction; +2 Survival in aerial environments"},
    
    # Social Edges
    {"name": "Sky-Captain", "rank": "Veteran", "type": "Social",
     "requirements": "Command, Spirit d8+", "summary": "+2 Persuasion with airship crews; Command edges extend to entire ship"},
    {"name": "Cloud Court", "rank": "Seasoned", "type": "Social",
     "requirements": "Noble House, Persuasion d8+", "summary": "+2 Persuasion at court; access to exclusive functions"},
    
    # Power Edges (Sky-Binder Tradition)
    {"name": "Sky-Binder", "rank": "Novice", "type": "Power",
     "requirements": "AB, Smarts d6+", "summary": "+2 arcane skill for air/electricity/flight powers at high altitude"},
    {"name": "Rune-Smith", "rank": "Novice", "type": "Power",
     "requirements": "AB, Repair d6+", "summary": "Create temporary 24-hour enchantments without Artificer edge"},
    {"name": "Storm-Warden", "rank": "Seasoned", "type": "Power",
     "requirements": "Sky-Binder, arcane skill d8+", "summary": "+2 to powers vs weather effects; can calm or summon storms"},
    {"name": "Pressure Mage", "rank": "Seasoned", "type": "Power",
     "requirements": "AB, Smarts d8+", "summary": "Powers can affect air pressure; +2 to powers with suffocation/force effects"},
]
