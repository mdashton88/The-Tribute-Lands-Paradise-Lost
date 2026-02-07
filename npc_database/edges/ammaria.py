"""
Ammaria — Regional Edges
Rebuilt from canonical Ammaria PDF — audited 2026-02-07
Source: 201_Ammaria.pdf (published version)
"""

SOURCE = "Ammaria"

EDGES = [
    # ── Combat Edges ──
    {"name": "Ammarian Halberd Guard", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d6+",
     "summary": "Free attack vs enemies closing to melee; ends their action on Shake/wound. One per round."},
    {"name": "Caravan Guard", "rank": "Novice", "type": "Combat",
     "requirements": "Fighting d6+ or Shooting d6+",
     "summary": "+1 Notice (ambushes); +1 Fighting or Shooting (choose one) first round of ambush combat"},
    {"name": "Repeating Crossbow Training", "rank": "Novice", "type": "Combat",
     "requirements": "Shooting d6+",
     "summary": "May fire repeating crossbow at ROF 2; +2 Repair to clear jams"},
    {"name": "Repeating Crossbow Mastery", "rank": "Seasoned", "type": "Combat",
     "requirements": "Repeating Crossbow Training, Shooting d8+",
     "summary": "Ignore Recoil penalty when firing repeating crossbow at ROF 2"},
    {"name": "War Boar Rider", "rank": "Seasoned", "type": "Combat",
     "requirements": "Riding d8+",
     "summary": "+2 Riding (war boars); berserk control difficulty reduced by 2"},

    # ── Professional Edges ──
    {"name": "Appraiser", "rank": "Novice", "type": "Professional",
     "requirements": "Smarts d6+, Notice d6+",
     "summary": "+2 Notice/Common Knowledge to assess value and spot forgeries"},
    {"name": "Blackmarket Broker", "rank": "Novice", "type": "Professional",
     "requirements": "Common Knowledge d6+, Persuasion d6+",
     "summary": "+2 Common Knowledge for contraband, fences, and black markets"},
    {"name": "Guild Journeyman", "rank": "Novice", "type": "Professional",
     "requirements": "Smarts d6+ or Agility d6+, trade skill d6+",
     "summary": "+1 trade skill in guild structures; +1 Common Knowledge (guild matters); guild facilities"},
    {"name": "Guildmaster", "rank": "Seasoned", "type": "Professional",
     "requirements": "Guild Journeyman, trade skill d8+",
     "summary": "+2 Persuasion (guild authority); guild resources 1/session"},
    {"name": "Moneylender", "rank": "Seasoned", "type": "Professional",
     "requirements": "Smarts d8+, Persuasion d6+",
     "summary": "+2 Persuasion with debtors; Notice to spot financial distress"},
    {"name": "Photographic Memory", "rank": "Novice", "type": "Professional",
     "requirements": "Smarts d8+",
     "summary": "+2 Smarts to recall previously encountered information"},
    {"name": "Sailor's Edge", "rank": "Novice", "type": "Professional",
     "requirements": "Boating d6+, Athletics d4+",
     "summary": "Ignore 1 pt platform penalty; +1 Fighting aboard ships; +1 Persuasion with seafarers"},
    {"name": "Smuggler's Eye", "rank": "Novice", "type": "Professional",
     "requirements": "Notice d6+",
     "summary": "+2 Notice to detect hidden cargo, compartments, contraband"},

    # ── Social Edges ──
    {"name": "Patron", "rank": "Novice", "type": "Social",
     "requirements": "",
     "summary": "Monthly stipend; social access; patron obligations"},
    {"name": "Political Connections", "rank": "Seasoned", "type": "Social",
     "requirements": "Persuasion d8+",
     "summary": "+2 Persuasion with officials; advance notice of policy changes 1/session"},
    {"name": "Reputation (Commerce)", "rank": "Seasoned", "type": "Social",
     "requirements": "Persuasion d6+",
     "summary": "+2 Persuasion with merchants and guild members"},
    {"name": "Underworld Contacts", "rank": "Novice", "type": "Social",
     "requirements": "Common Knowledge d6+",
     "summary": "+2 Streetwise; locate criminal contacts with Common Knowledge roll"},

    # ── Magic Edges ──
    {"name": "Guild Alchemist", "rank": "Novice", "type": "Power",
     "requirements": "AB (Alchemist), Smarts d6+",
     "summary": "+2 Alchemy in proper workspace; jury-rig workspace with Smarts roll"},
    {"name": "Guild Trained", "rank": "Novice", "type": "Power",
     "requirements": "AB (any), Smarts d6+",
     "summary": "+2 arcane skill in proper workspace; jury-rig with Smarts roll"},
    {"name": "Commercial Caster", "rank": "Novice", "type": "Power",
     "requirements": "AB (any), Persuasion d6+",
     "summary": "+1 arcane skill for paying clients; +2 Persuasion for fees"},
    {"name": "Oath-Binder", "rank": "Novice", "type": "Power",
     "requirements": "AB (any), Smarts d6+",
     "summary": "+2 arcane skill for binding/compelling powers; reputation effect"},
]
