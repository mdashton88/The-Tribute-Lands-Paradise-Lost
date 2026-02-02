"""
Ammaria — Regional Hindrances
The Merchant Realms — guilds, debts, and the price of survival under tribute.
"""

SOURCE = "Ammaria"

HINDRANCES = [
    # Major Hindrances
    {"name": "Former Slave (Escaped)", "severity": "Major",
     "summary": "-2 Persuasion (respectable citizens); Slavers' Guild actively hunts you"},
    {"name": "Gang Debt", "severity": "Major",
     "summary": "Owe criminals; -2 vs their Intimidation, Spirit roll to refuse requests"},
    {"name": "Guild Blacklisted", "severity": "Major",
     "summary": "Expelled from guild system; cannot conduct legal trade"},
    {"name": "Tribute-Touched", "severity": "Major",
     "summary": "-2 Persuasion vs Glasryans; Spirit roll to resist acting against them"},
    
    # Minor Hindrances
    {"name": "Collaborator's Blood", "severity": "Minor",
     "summary": "Family tainted by suspected Glasryan service; -1 Persuasion with those who know"},
    {"name": "Country-Born", "severity": "Minor",
     "summary": "-2 Common Knowledge (guild politics, urban customs, city navigation)"},
    {"name": "Dark Reputation", "severity": "Minor",
     "summary": "-1 Persuasion; known for something unsavoury"},
    {"name": "Former Slave (Manumitted)", "severity": "Minor",
     "summary": "-2 Persuasion (respectable Ammarians); legal restrictions still apply"},
    {"name": "Guild Obligations", "severity": "Minor",
     "summary": "Exceptional dues, duties, and demands from your guild"},
    {"name": "Poverty-Marked", "severity": "Minor",
     "summary": "-1 Persuasion with social betters; obvious signs of poverty"},
    {"name": "Soft Heart", "severity": "Minor",
     "summary": "Spirit roll to ignore suffering or act purely for profit"},
    {"name": "Unguilded", "severity": "Minor",
     "summary": "-2 Persuasion (commerce); cannot conduct legal regulated trade"},
]
