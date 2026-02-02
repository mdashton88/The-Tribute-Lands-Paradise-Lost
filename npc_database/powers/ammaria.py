"""
Ammaria — Regional Powers
The Merchant Realms — oath-binding, appraisal, and guild magic.
Typical trappings: Ink and contracts, guild seals, alchemical reactions, merchant's scales.
"""

SOURCE = "Ammaria"

POWERS = [
    # Covenant of Letters Powers
    {"name": "Oath-Bind", "rank": "Seasoned", "pp": "3", "range": "Touch", "duration": "Permanent",
     "summary": "Magically enforce contract; oath-breaker suffers -2 to all Traits until fulfilled"},
    {"name": "Truth-Seal", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "5 rounds",
     "summary": "Target cannot knowingly lie; Spirit to resist"},
    {"name": "Assess Worth", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "Instant",
     "summary": "Know exact value of item; detect forgeries automatically"},
    {"name": "Seal Document", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "Permanent",
     "summary": "Document cannot be altered; detect tampering automatically"},
    
    # Apothecaries' Guild Powers (Alchemist Trappings)
    {"name": "Compound", "rank": "Novice", "pp": "2", "range": "Touch", "duration": "1 hour",
     "summary": "Create minor alchemical effect; smoke, flash, acid (2d4 damage)"},
    {"name": "Purify", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "Instant",
     "summary": "Remove poison, disease, or contamination from food/water"},
    {"name": "Infuse", "rank": "Seasoned", "pp": "3", "range": "Touch", "duration": "1 hour",
     "summary": "Grant potion-like effect; Boost Trait as drinkable"},
    
    # Guild Ward Magic
    {"name": "Ward Vault", "rank": "Veteran", "pp": "5", "range": "Touch", "duration": "24 hours",
     "summary": "Protect area (10\" radius) with alarm and -2 Thievery"},
    {"name": "Detect Forgery", "rank": "Novice", "pp": "1", "range": "Touch", "duration": "Instant",
     "summary": "Know if document, seal, or signature is forged"},
]
