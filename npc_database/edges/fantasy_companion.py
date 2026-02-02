"""
Fantasy Companion — Edges
Source: Savage Worlds Fantasy Companion
"""

SOURCE = "Fantasy Companion"

EDGES = [
    # Combat Edges
    {"name": "Dirty Fighter", "rank": "Seasoned", "type": "Combat",
     "requirements": "", "summary": "+2 damage with The Drop or from surprise"},
    {"name": "Really Dirty Fighter", "rank": "Veteran", "type": "Combat",
     "requirements": "Dirty Fighter", "summary": "Spend Benny for automatic Shaken on enemy"},
    {"name": "Shield Wall", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d6+", "summary": "+2 Armor when adjacent to ally with shield"},
    
    # Professional Edges
    {"name": "Alchemist", "rank": "Novice", "type": "Professional",
     "requirements": "AB, Smarts d8+", "summary": "Create alchemical items; +2 arcane skill for consumables"},
    {"name": "Champion", "rank": "Novice", "type": "Professional",
     "requirements": "AB (Miracles), Spirit d8+, Fighting d6+", "summary": "+2 damage/Toughness vs supernatural evil"},
    {"name": "Holy Warrior", "rank": "Novice", "type": "Professional",
     "requirements": "AB (Miracles), Spirit d8+", "summary": "+2 damage vs supernatural evil; powers at +2 vs evil"},
    {"name": "Wizard", "rank": "Novice", "type": "Professional",
     "requirements": "AB (Magic), Smarts d8+", "summary": "Swap powers with 10 minutes and arcane skill roll"},
    {"name": "Troubadour", "rank": "Novice", "type": "Professional",
     "requirements": "Performance d8+", "summary": "+2 Performance; can earn money and information"},
    
    # Power Edges
    {"name": "Familiar", "rank": "Novice", "type": "Power",
     "requirements": "AB", "summary": "Gain magical animal companion"},
    {"name": "Ritual Caster", "rank": "Seasoned", "type": "Power",
     "requirements": "AB, Smarts d6+", "summary": "Cast rituals with extended time for +2 arcane skill"},
    
    # Social Edges
    {"name": "Gallows Humour", "rank": "Novice", "type": "Social",
     "requirements": "Spirit d8+", "summary": "Jokes grant +2 Spirit for Fear/Intimidation resistance"},
    {"name": "Reputation", "rank": "Novice", "type": "Social",
     "requirements": "", "summary": "+2 Intimidation or Persuasion (choose one) based on rep"},
    
    # Weird Edges
    {"name": "Favoured Enemy", "rank": "Novice", "type": "Weird",
     "requirements": "", "summary": "+2 damage and Notice vs chosen creature type"},
    {"name": "Giant Killer", "rank": "Veteran", "type": "Weird",
     "requirements": "", "summary": "+1d6 damage vs Size +2 or larger"},
    {"name": "Tough as Nails", "rank": "Legendary", "type": "Weird",
     "requirements": "Vigor d8+", "summary": "+1 Toughness; +1 to Wound capacity"},
]
