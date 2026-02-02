"""
Vinlands — Regional Edges
The northern forests and mountains — forest warfare, clan bonds, and ancient magics.
"""

SOURCE = "Vinlands"

EDGES = [
    # Background Edges
    {"name": "Holtscarl", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+2 Survival and Stealth in forests; +1 damage with axes"},
    {"name": "Felsgard-Trained", "rank": "Novice", "type": "Background",
     "requirements": "Fighting d6+", "summary": "+2 Fighting in formation; +1 Toughness when adjacent to ally"},
    {"name": "Clan-Born", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+2 Persuasion with clan; +2 Common Knowledge (Vinlands politics)"},
    {"name": "Frontier-Raised", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+1 Survival or Riding; Fear checks at +1 vs natural beasts"},
    
    # Combat Edges
    {"name": "Shield Wall Veteran", "rank": "Seasoned", "type": "Combat",
     "requirements": "Fighting d8+, Shield Wall", "summary": "+2 Armor in shield wall; can use shield bash for Str+d6"},
    {"name": "Bearded Axe Master", "rank": "Seasoned", "type": "Combat",
     "requirements": "Fighting d8+", "summary": "Disarm at +2; hook shields for -2 enemy Parry"},
    {"name": "Mountain's Endurance", "rank": "Novice", "type": "Combat",
     "requirements": "Vigor d8+", "summary": "+2 Vigor vs cold/fatigue; ignore 1 level of cold penalties"},
    {"name": "Skirmisher", "rank": "Novice", "type": "Combat",
     "requirements": "Athletics d6+", "summary": "+2\" Pace in forests; withdraw without free attacks in wilderness"},
    {"name": "Dive Attack", "rank": "Seasoned", "type": "Combat",
     "requirements": "Avian, Athletics d10+", "summary": "+4 damage when diving from height; must move 6\" minimum"},
    {"name": "Sky Hunter", "rank": "Veteran", "type": "Combat",
     "requirements": "Avian, Dive Attack", "summary": "+2 Notice from altitude; can Dive Attack without movement penalty"},
    
    # Professional Edges
    {"name": "Warren-Hunter", "rank": "Seasoned", "type": "Professional",
     "requirements": "Fighting d6+, Notice d6+", "summary": "+2 Fighting vs goblins; +2 Notice in tunnels"},
    {"name": "Delver", "rank": "Novice", "type": "Professional",
     "requirements": "Notice d6+", "summary": "+2 Notice for traps/ambushes in ruins; +2 Common Knowledge (dungeon hazards)"},
    {"name": "Beast-Bonded", "rank": "Novice", "type": "Professional",
     "requirements": "Spirit d6+", "summary": "Gain animal companion; +2 to Animal Handling"},
    
    # Social Edges
    {"name": "Jarl's Voice", "rank": "Veteran", "type": "Social",
     "requirements": "Spirit d8+, Clan-Born", "summary": "Speak with authority of clan; +2 Persuasion with Vinlanders"},
    {"name": "Oathkeeper", "rank": "Novice", "type": "Social",
     "requirements": "Spirit d6+", "summary": "+2 Persuasion when oath is at stake; +2 to resist breaking oaths"},
    
    # Power Edges (Warlock/Druid Traditions)
    {"name": "Grove Initiate", "rank": "Novice", "type": "Power",
     "requirements": "AB, Spirit d6+", "summary": "+2 Faith in wilderness; sense corruption within 10\""},
    {"name": "Beast-Speaker", "rank": "Novice", "type": "Power",
     "requirements": "AB, Spirit d6+ or Beast Bond", "summary": "Communicate with natural animals; +2 Animal Handling"},
    {"name": "Oathwood Sentinel", "rank": "Seasoned", "type": "Power",
     "requirements": "Grove Initiate, Fighting d6+ or Shooting d6+", "summary": "+1 Fighting/Shooting defending natural locations"},
    {"name": "Hedge Witch", "rank": "Novice", "type": "Power",
     "requirements": "AB, Smarts d6+", "summary": "+2 Healing with folk remedies; +2 vs poison/disease"},
    {"name": "Coven Initiate", "rank": "Novice", "type": "Power",
     "requirements": "Hedge Witch, Persuasion d6+", "summary": "+1 arcane skill when 2+ coven members present"},
    {"name": "Curse-Layer", "rank": "Seasoned", "type": "Power",
     "requirements": "Hedge Witch, arcane skill d8+", "summary": "Targets suffer -2 to resist curses; double curse duration"},
]
