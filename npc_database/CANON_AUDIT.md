# AMMARIA NPC CANON AUDIT

Comparing database seed data against canonical source: **201 Ammaria.docx (Appendix B: Pre-Generated Characters)**

---

## 1. LYSSA THORNE — Merchant Princess ✓ MATCHES CANON

| Field | Canon (201) | Seed Data | Status |
|-------|-------------|-----------|--------|
| Attributes | Ag d4, Sm d8, Sp d8, St d4, Vi d6 | Same | ✓ |
| Skills | Athletics d4, CK d8, Notice d8, Persuasion d10, Research d6, Stealth d4 | Same | ✓ |
| Pace/Parry/Tough | 6 / 2 / 5 | Same | ✓ |
| Edges | Charismatic, Appraiser | Same | ✓ |
| Hindrances | Stubborn (Minor), Obligation (Minor—family), Code of Honor (Major) | Same | ✓ |
| Gear | Fine clothing, ₡150 cash | Same | ✓ |

**No corrections needed.**

---

## 2. CAPTAIN JORIN SALTWIND — Moonstar Veteran ✓ MATCHES CANON

| Field | Canon (201) | Seed Data | Status |
|-------|-------------|-----------|--------|
| Attributes | Ag d8, Sm d6, Sp d6, St d6, Vi d6 | Same | ✓ |
| Skills | Athletics d6, Boating d8, CK d6, Fighting d6, Notice d6, Persuasion d6, Shooting d6, Stealth d4 | Same | ✓ |
| Pace/Parry/Tough | 6 / 5 / 6(1) | Same | ✓ |
| Edges | Sailor's Edge, Command, Caravan Guard | Same | ✓ |
| Hindrances | Loyal (Major—crew and Consortium), Cautious (Minor), Obligation (Minor—Consortium duties) | Same | ✓ |
| Gear | Leather armour (+1), cutlass (Str+d6), repeating crossbow (2d6, AP 3, 15/30/60), sailor's kit, ₡50 | Same | ✓ |

**No corrections needed.**

---

## 3. MARUS IRONHAND — Guild Armourer ⚠ MULTIPLE ERRORS

| Field | Canon (201) | Seed Data | Status |
|-------|-------------|-----------|--------|
| **Strength** | **d6** | d8 | ⚠ WRONG |
| **Vigor** | **d6** | d8 | ⚠ WRONG |
| **Toughness** | **5** | 8 (2) | ⚠ WRONG |
| **Toughness Armor** | **0** (apron not counted in canon stat block) | 2 | ⚠ WRONG |
| **Skills: Athletics** | **d4** | d6 | ⚠ WRONG |
| **Skills: CK** | **d6** | d8 | ⚠ WRONG |
| **Skills: Intimidation** | **d4** | d6 | ⚠ WRONG |
| **Skills: Persuasion** | **d4** | MISSING | ⚠ MISSING |
| **Skills: Research** | **d6** | MISSING | ⚠ MISSING |
| **Hindrances** | Code of Honor (Major—won't craft for evil), Loyal (Minor—guild), Stubborn (Minor) | Stubborn (Minor), Loyal (Major—Guild), Obligation (Minor—family legacy) | ⚠ WRONG |
| **Gear** | Leather apron (+1), Ammarian steel hammer (Str+d6, AP 1), master tools, ₡80 | Chain shirt (+2), Warhammer (Str+d6), Ammarian steel tools, ₡75 | ⚠ WRONG |

### Corrections Required:
- Strength: 8 → **6**
- Vigor: 8 → **6**
- Toughness: 8 → **5** (canon doesn't add apron to base)
- Toughness Armor: 2 → **0**
- Athletics: 6 → **4**
- Common Knowledge: 8 → **6**
- Intimidation: 6 → **4**
- ADD Persuasion d4
- ADD Research d6
- Hindrance "Loyal" severity: Major → **Minor** (guild)
- REMOVE Obligation (Minor — family legacy)
- ADD Code of Honor (Major — won't craft for evil)
- Gear: Chain shirt (+2) → **Leather apron (+1)**
- Gear: Warhammer → **Ammarian steel hammer (Str+d6, AP 1)**
- Gear: Ammarian steel tools → **master tools**
- Gear: ₡75 → **₡80**

---

## 4. TAM "THREE-COINS" MERRIK — Professional Fixer

**Source: Skill_04 example NPC, not Ammaria Appendix B.**
Not a canonical pre-gen — created as a database example. Stats are internally consistent. No canon correction applicable.

---

## 5–8. MISSING FROM SEED DATA

The following canonical Ammaria pre-gens from 201 Appendix B were **never seeded**:

### KAEL "BOARHEART" THRACE — War Boar Keeper
- Attributes: Ag d6, Sm d6, Sp d8, St d8, Vi d4
- Skills: Athletics d6, CK d4, Fighting d8, Notice d6, Persuasion d4, Riding d8, Stealth d4, Survival d6
- Pace: 6; Parry: 6; Toughness: 4
- Edges: Beast Bond, Beast Master, Caravan Guard
- Hindrances: Loyal (Major—his animals), Illiterate (Minor), Poverty-Marked (Minor)
- Gear: Leather armour (+1), spear (Str+d6, Reach 1), short bow (2d6, Range 12/24/48), handler's tools, trained war boar companion, ₡40

### "SHADOWS" — Night's Whisper Operative
- Attributes: Ag d10, Sm d6, Sp d6, St d4, Vi d6
- Skills: Athletics d8, CK d4, Fighting d4, Notice d6, Persuasion d4, Stealth d10, Thievery d10
- Pace: 6; Parry: 4; Toughness: 5
- Edges: Thief, Acrobat, Streetwise
- Hindrances: Wanted (Minor—various aliases), Loyal (Minor—Night's Whisper), Cautious (Minor), Greedy (Minor)
- Gear: Dark clothing, Ammarian lockpicks (+1 Thievery), guild knife (Str+d4), grappling hook with silk rope, smoke bombs, ₡60

### VIKTOR "SILVERTONGUE" CRANE — Consortium Factor
- Attributes: Ag d4, Sm d10, Sp d8, St d4, Vi d6
- Skills: Athletics d4, CK d8, Intimidation d4, Notice d8, Persuasion d10, Research d8, Stealth d4
- Pace: 6; Parry: 2; Toughness: 5
- Edges: Appraiser, Charismatic, Connections (Moonstar)
- Hindrances: Arrogant (Major), Obligation (Minor—Consortium), Greedy (Minor)
- Gear: Fine clothing, guild credentials, letters of credit, ₡200

### RENNA ASHVEIL — Debt-Slave Gladiator
- Attributes: Ag d10, Sm d4, Sp d6, St d8, Vi d4
- Skills: Athletics d10, CK d4, Fighting d10, Intimidation d6, Notice d4, Persuasion d4, Stealth d4, Survival d6
- Pace: 6; Parry: 7; Toughness: 4
- Edges: Quick, Combat Reflexes, First Strike
- Hindrances: Obligation (Major—debt contract), Poverty (Minor), Vengeful (Minor)
- Gear: Gladiatorial leathers (+1), gladius (Str+d6), net, Ammarian steel dagger (Str+d4, AP 1), ₡5 hidden savings

---

## ALSO IN AMMARIA MODULE (not pre-gens, but named NPCs):

### DAVEN REDSTAR — Ashmen Enforcer
### ELARA VOSS — Guild Alchemist

These appear in the module but are supporting NPCs rather than Appendix B pre-gens.
