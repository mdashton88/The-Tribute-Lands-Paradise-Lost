"""
Ammaria — Regional Edges
The Merchant Realms — guild mastery, merchant cunning, and urban survival.
"""

SOURCE = "Ammaria"

EDGES = [
    # Background Edges
    {"name": "Guild-Born", "rank": "Novice", "type": "Background",
     "requirements": "", "summary": "+2 Common Knowledge (guild politics); +1 Persuasion with guild members"},
    {"name": "Street-Wise", "rank": "Novice", "type": "Background",
     "requirements": "Smarts d6+", "summary": "+2 Notice and Streetwise in urban environments"},
    {"name": "Consortium Trained", "rank": "Novice", "type": "Background",
     "requirements": "Smarts d8+", "summary": "+2 Research; access to Consortium networks"},
    
    # Combat Edges
    {"name": "Ammarian Halberd Guard", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d8+, Strength d8+", "summary": "+1 Parry and Reach with halberds; Free Disengage"},
    {"name": "Canal Fighter", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d6+", "summary": "Ignore Unstable Platform on boats; +1 Fighting in confined spaces"},
    {"name": "Repeater Training", "rank": "Seasoned", "type": "Combat",
     "requirements": "Shooting d8+, Agility d8+", "summary": "ROF 2 with repeating crossbows; ignore Reload penalty"},
    {"name": "Dual-Blade", "rank": "Seasoned", "type": "Combat",
     "requirements": "Fighting d8+, Two-Fisted", "summary": "Extra attack with off-hand at no penalty"},
    
    # Professional Edges
    {"name": "Appraiser", "rank": "Novice", "type": "Professional",
     "requirements": "Smarts d6+", "summary": "+2 Notice to assess value; detect forgeries"},
    {"name": "Guild Journeyman", "rank": "Novice", "type": "Professional",
     "requirements": "", "summary": "+2 to guild-related skill; access to guild resources"},
    {"name": "Guild Master", "rank": "Veteran", "type": "Professional",
     "requirements": "Guild Journeyman, d10+ in guild skill", "summary": "+2 Persuasion with guild; command guild resources"},
    {"name": "Contract Broker", "rank": "Seasoned", "type": "Professional",
     "requirements": "Persuasion d8+, Smarts d8+", "summary": "+2 Persuasion for negotiations; +2 Notice for contract loopholes"},
    {"name": "Caravan Guard", "rank": "Novice", "type": "Professional",
     "requirements": "Fighting d6+ or Shooting d6+", "summary": "+2 Notice for ambushes; +1 damage on first round of combat"},
    
    # Social Edges
    {"name": "Convincing Lie", "rank": "Novice", "type": "Social",
     "requirements": "Persuasion d6+", "summary": "+2 Persuasion when lying; +2 to detect lies told to you"},
    {"name": "Merchant Prince", "rank": "Veteran", "type": "Social",
     "requirements": "Persuasion d10+, Rich", "summary": "+2 Persuasion (commerce); double starting funds"},
    {"name": "Guildsman's Reputation", "rank": "Seasoned", "type": "Social",
     "requirements": "Guild Journeyman", "summary": "+2 Intimidation with those who know your guild standing"},
    
    # Power Edges (Covenant of Letters)
    {"name": "Oath-Binder", "rank": "Seasoned", "type": "Power",
     "requirements": "AB, Smarts d8+", "summary": "+2 arcane skill for binding powers; oaths magically enforced"},
    {"name": "Compound Master", "rank": "Seasoned", "type": "Power",
     "requirements": "AB, Alchemist", "summary": "+2 arcane skill for consumables; +1 to shelf life"},
    {"name": "Ward-Wright", "rank": "Veteran", "type": "Power",
     "requirements": "AB (Magic), arcane skill d10+", "summary": "Create lasting protective wards; +2 protection powers"},
]
