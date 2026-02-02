"""
Saltlands — Regional Hindrances
The island chains — pirates, traders, and those who harvest the sea.
"""

SOURCE = "Saltlands"

HINDRANCES = [
    # Major Hindrances
    {"name": "Code Breaker", "severity": "Major",
     "summary": "Violated the Corsair Code; -4 Charisma with Code-followers, may be killed on sight"},
    {"name": "Sea Cursed", "severity": "Major",
     "summary": "-2 Boating; GM gains free Complication on sea Dramatic Tasks"},
    {"name": "Blood Feud", "severity": "Major",
     "summary": "Powerful captain with multiple ships actively hunts you"},
    {"name": "Former Slave", "severity": "Major",
     "summary": "Bear the brands; -2 Persuasion, Imperial law considers you property"},
    {"name": "Wanted by Empire", "severity": "Major",
     "summary": "Dragon Throne actively hunts you; significant bounty"},
    {"name": "Dragon-Marked", "severity": "Major",
     "summary": "Specific Glasryan pursues you with immortal patience; crews risk sharing your fate"},
    {"name": "Deep-Touched", "severity": "Major",
     "summary": "Something from depths marked you; double Fatigue recovery at sea, drawn to deep water"},
    
    # Minor Hindrances
    {"name": "Crewless", "severity": "Minor",
     "summary": "-2 Persuasion seeking shipboard work; no prize shares, no backup"},
    {"name": "Blood Feud", "severity": "Minor",
     "summary": "Single dangerous enemy captain seeks you"},
    {"name": "Wanted by Empire", "severity": "Minor",
     "summary": "Nuisance to Dragon Throne; they'll act if convenient"},
    {"name": "Debtor", "severity": "Minor",
     "summary": "Owe ~200 crowns; surplus claimed, creditor calls favours"},
    {"name": "Wyrm-Marked", "severity": "Minor",
     "summary": "Specific sea wyrm remembers you; attacks ships you're aboard, rejects your Blood Toll"},
]
