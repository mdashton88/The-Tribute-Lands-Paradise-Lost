# EDGE / HINDRANCE / POWER AUDIT REPORT
## NPC Validator Database vs Canonical Sources

**Date:** 2026-02-07
**Auditor:** Claude
**Sources Checked:** Ammaria PDF (canonical), 501_Edge_Strategy_Master_v2, 511_Ammaria_Mechanics_Reference_v1_4, Skill_01_Character_Build_v1_2, 202_Saltlands_v2_2, 203_Vinlands_v4_3, 204_Concordium_v2

---

## SUMMARY

| Area | Items Checked | Errors Found | Severity |
|:-----|:-------------:|:------------:|:---------|
| Validator — Core Edges | 85 | 11 | Mixed |
| Validator — Ammaria Custom | 17 | 9 | **CRITICAL** |
| Validator — Saltlands Custom | 13 | 4 | Major |
| Validator — Vinlands Custom | 12 | 2 | Minor |
| Catalogue — edges/ammaria.py | 17 | 14 | **CRITICAL** |
| Catalogue — edges/saltlands.py | 16 | 5 | Major |
| Hindrances — ammaria.py | 12 | 0 | Clean ✓ |
| **Structural** | 1 | 1 | **CRITICAL** |

**Structural Issue:** The validator has NO support for OR-style requirements (e.g. "Fighting d6+ OR Shooting d6+"). This affects Caravan Guard, Guild Journeyman, Dead Shot, Marksman, and Trademark Weapon. All OR-checks currently fail or are fudged.

---

## PART 1: VALIDATOR (edgeReqs in app.py) — CRITICAL ERRORS

These are the entries that will cause **false failure messages** on valid NPC builds.

### 1.1 Ammaria Custom Edges — WRONG Requirements

| Edge | Validator Has | Canonical Requires | Error |
|:-----|:-------------|:------------------|:------|
| **Caravan Guard** | `attrs:{vigor:6}, skills:{Fighting:6}` | Fighting d6+ **OR** Shooting d6+ | Phantom Vigor req; missing OR logic |
| **Halberd Guard** | `skills:{Fighting:6}` (name "Halberd Guard") | **Ammarian Halberd Guard**, Fighting d6+ | Wrong name — won't match NPCs using canonical name |
| **Halberd Master** | `rank:'Seasoned', edges:['Halberd Guard'], skills:{Fighting:8}` | **DOES NOT EXIST** in canonical | Phantom edge — invented, never published |
| **Canal Rat** | `attrs:{agility:6}, skills:{Athletics:6}` | **DOES NOT EXIST** in canonical Ammaria | Phantom edge |
| **Debt-Resistant** | `attrs:{spirit:6}` | **DOES NOT EXIST** in canonical Ammaria | Phantom edge |

### 1.2 Ammaria Custom Edges — MISSING from Validator

These canonical edges exist in the published Ammaria PDF but have **no entry** in edgeReqs, meaning the validator shows "no requirement data (custom edge?)" instead of actually checking them.

| Canonical Edge | Rank | Requirements |
|:--------------|:-----|:-------------|
| Photographic Memory | N | Smarts d8+ |
| Political Connections | S | Persuasion d8+ |
| Reputation (Commerce) | S | Persuasion d6+ |
| Underworld Contacts | N | Common Knowledge d6+ |
| Guild Trained | N | AB (any), Smarts d6+ |
| Commercial Caster | N | AB (any), Persuasion d6+ |
| Oath-Binder | N | AB (any), Smarts d6+ |

### 1.3 Core SWADE Edges — WRONG Requirements

| Edge | Validator Has | Should Be | Error Type |
|:-----|:-------------|:----------|:-----------|
| **Dodge** | `attrs:{agility:8}` (no rank) | **Seasoned**, Agility d8+ | Missing rank — Novice chars could pass |
| **Double Tap** | `skills:{Shooting:6}` (no rank) | **Seasoned**, Shooting d6+ | Missing rank |
| **Giant Killer** | `rank:'Seasoned'` | **Veteran** | Wrong rank — too permissive |
| **Improvisational Fighter** | `attrs:{smarts:6}` (no rank) | **Seasoned**, Smarts d6+ | Missing rank |
| **Natural Leader** | `rank:'Seasoned'` | **Novice**, Spirit d8+, Command | Wrong rank — too restrictive |
| **Ace** | `skills:{Driving:8}` | **Agility d8+** | Wrong requirement entirely |
| **Investigator** | `attrs:{smarts:8}` | Smarts d8+, **Research d8+** | Missing skill req |
| **Scholar** | `attrs:{smarts:8}` | **Research d8+** (not Smarts) | Wrong attribute, missing skill |
| **Menacing** | `attrs:{spirit:8}` | **No requirements** | Phantom Spirit req |
| **Trademark Weapon** | `skills:{Fighting:8}` | **d8+ in related skill** (Fighting, Shooting, or Athletics) | Only checks Fighting |
| **Dead Shot** | `skills:{Shooting:8}` | **Athletics OR Shooting d8+** | Missing OR logic |

### 1.4 Saltlands Custom Edges — WRONG Requirements

| Edge | Validator Has | Canonical Requires | Error |
|:-----|:-------------|:------------------|:------|
| **No Fair Fights** | `attrs:{agility:8}, skills:{Fighting:6}` | Novice, Fighting d6+ only | Phantom Agility d8+ req |
| **Board and Storm** | `attrs:{strength:6}, skills:{Fighting:6, Athletics:6}` | **DOES NOT EXIST** by this name | Canonical name is different |
| **Reef Navigator** | `skills:{Boating:8}` | **DOES NOT EXIST** by this name | Phantom edge |
| **Sea Legs** | `attrs:{agility:6}` | **DOES NOT EXIST** as edge | Phantom edge |
| **Deadeye** | `rank:'Seasoned', skills:{Shooting:8}` | **DOES NOT EXIST** in canonical Saltlands | Phantom edge |

---

## PART 2: CATALOGUE FILES (edges/ammaria.py) — CRITICAL ERRORS

The catalogue file `edges/ammaria.py` appears to have been written from an **earlier draft** rather than the canonical PDF. Almost every entry has problems.

### 2.1 Edges with WRONG Requirements

| Catalogue Entry | Has | Canonical | Error |
|:---------------|:----|:----------|:------|
| Ammarian Halberd Guard | Fighting d8+, Strength d8+ | **Fighting d6+** only | Wrong die types, phantom Strength |
| Repeater Training | Seasoned, Shooting d8+, Agility d8+ | **Novice**, Shooting d6+ (name: "Repeating Crossbow Training") | Wrong rank, wrong name, phantom Agility, wrong die |
| Appraiser | Smarts d6+ only | Smarts d6+, **Notice d6+** | Missing Notice req |
| Guild Journeyman | (no requirements listed) | Smarts d6+ or Agility d6+, trade skill d6+ | Missing all requirements |
| Guild Master | Veteran, Guild Journeyman, d10+ | **Seasoned** (name: "Guildmaster"), trade skill d8+ | Wrong rank, wrong name, wrong skill die |
| Oath-Binder | Seasoned, AB, Smarts d8+ | **Novice**, AB (any), Smarts d6+ | Wrong rank, wrong die |

### 2.2 Edges that DO NOT EXIST in Canonical Ammaria

These appear in the catalogue but have no counterpart in the published PDF:

- **Guild-Born** (Background) — invented
- **Street-Wise** (Background) — invented (different from core Streetwise)
- **Consortium Trained** (Background) — invented
- **Canal Fighter** (Combat) — invented
- **Dual-Blade** (Combat) — invented
- **Contract Broker** (Professional) — invented
- **Convincing Lie** (Social) — invented
- **Merchant Prince** (Social) — invented
- **Guildsman's Reputation** (Social) — invented
- **Compound Master** (Power) — actually canonical, keep
- **Ward-Wright** (Power) — invented

### 2.3 Canonical Edges MISSING from Catalogue

- Repeating Crossbow Mastery (S)
- War Boar Rider (S)
- Blackmarket Broker (N)
- Moneylender (S)
- Photographic Memory (N)
- Sailor's Edge (N)
- Smuggler's Eye (N)
- Patron (N)
- Political Connections (S)
- Reputation (Commerce) (S)
- Underworld Contacts (N)
- Guild Trained (N)
- Guild Alchemist (N)
- Commercial Caster (N)

### 2.4 Edges with WRONG Summaries

| Edge | Catalogue Summary | Canonical Effect |
|:-----|:-----------------|:-----------------|
| Ammarian Halberd Guard | "+1 Parry and Reach with halberds; Free Disengage" | Free attack vs enemies closing; ends action on Shake/wound |
| Caravan Guard | "+2 Notice for ambushes; +1 damage on first round" | +1 Notice (ambushes), +1 Fighting **or** Shooting first round |

---

## PART 3: HINDRANCES

### Ammaria Hindrances — CLEAN ✓

The `hindrances/ammaria.py` catalogue matches the canonical PDF accurately. All 12 entries (4 Major, 8 Minor) have correct names, severities, and summaries.

### Core Hindrances — NOT AUDITED

Core hindrances were not checked in this pass. Recommend follow-up audit.

---

## PART 4: REQUIRED FIXES

### Fix 1 — STRUCTURAL: Add OR-logic to validator (CRITICAL)

The `auditCharacter()` function needs a `skills_or` check alongside the existing `skills` (AND) check. Affects: Caravan Guard, Guild Journeyman, Dead Shot, Marksman, Trademark Weapon.

### Fix 2 — Rebuild Ammaria edgeReqs from canonical PDF (CRITICAL)

Remove phantom edges (Canal Rat, Debt-Resistant, Halberd Master). Add missing canonical edges. Fix all requirements to match published data.

### Fix 3 — Rebuild edges/ammaria.py catalogue from canonical PDF (CRITICAL)

The entire file needs replacing — it was written from an outdated draft.

### Fix 4 — Core edgeReqs corrections (MAJOR)

Fix the 11 core edge errors (missing ranks, wrong requirements, phantom attributes).

### Fix 5 — Saltlands edgeReqs cleanup (MAJOR)

Remove phantom edges, fix No Fair Fights requirements.

---

## CONFIDENCE NOTES

All Ammaria findings are **HIGH CONFIDENCE** — verified against the published PDF which is the canonical source of truth.

Core SWADE findings are **MEDIUM-HIGH CONFIDENCE** — verified against project knowledge references (Skill_01, 510, 511) which are themselves derived from the SWADE rulebook. A small number of edge requirements differ between SWADE printings; the audit follows the most recent edition as represented in project knowledge.

Saltlands and Vinlands findings are **MEDIUM CONFIDENCE** — verified against the v2_2 and v4_3 documents respectively, which are still in development. Requirements may change before publication.
