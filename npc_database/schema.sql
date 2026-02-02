-- ============================================================
-- TRIBUTE LANDS NPC DATABASE
-- DiceForge Studios Ltd
-- Schema v1.0
--
-- Designed for dual purpose:
--   1. NPC tracking and cross-referencing across all modules
--   2. Direct export to Fantasy Grounds Unity XML format
--
-- Tables use a pragmatic split: structured data where FG XML
-- needs it (weapons, skills), JSON storage where flat text
-- suffices (edges, hindrances, gear).
-- ============================================================

PRAGMA journal_mode=WAL;
PRAGMA foreign_keys=ON;

-- ============================================================
-- CORE NPC TABLE
-- Maps to Skill 04 narrative format + Skill 02 mechanical base
-- ============================================================
CREATE TABLE IF NOT EXISTS npcs (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Identity
    name            TEXT NOT NULL,
    title           TEXT,                   -- "Professional Fixer", "Corsair Captain"
    region          TEXT NOT NULL CHECK(region IN (
                        'Ammaria', 'Saltlands', 'Vinlands', 
                        'Concordium', 'Glasrya', 'Global'
                    )),
    
    -- Classification
    tier            TEXT NOT NULL CHECK(tier IN (
                        'Wild Card', 'Extra', 'Walk-On'
                    )),
    archetype       TEXT,                   -- combat, social, criminal, scholarly, maritime, wilderness, spellcaster
    rank_guideline  TEXT CHECK(rank_guideline IN (
                        'Novice', 'Seasoned', 'Veteran', 'Heroic', 'Legendary', NULL
                    )),
    
    -- Narrative (Skill 04)
    quote           TEXT,                   -- Signature quote
    description     TEXT,                   -- Appearance, mannerisms (2-3 sentences)
    background      TEXT,                   -- How they got here (2-3 sentences)
    motivation      TEXT,                   -- What They Want (one sentence)
    secret          TEXT,                   -- Their Secret
    services        TEXT,                   -- What they offer PCs, with costs
    adventure_hook  TEXT,                   -- One sentence scenario seed
    tactics         TEXT,                   -- How they fight (Skill 02)
    
    -- SWADE Attributes (d4=4, d6=6, d8=8, d10=10, d12=12)
    agility         INTEGER DEFAULT 0,
    smarts          INTEGER DEFAULT 0,
    spirit          INTEGER DEFAULT 0,
    strength        INTEGER DEFAULT 0,
    vigor           INTEGER DEFAULT 0,
    
    -- Derived Stats
    pace            INTEGER DEFAULT 6,
    parry           INTEGER DEFAULT 2,
    toughness       INTEGER DEFAULT 5,
    toughness_armor INTEGER DEFAULT 0,      -- The number in parentheses
    size            INTEGER DEFAULT 0,
    
    -- Wild Card fields
    bennies         INTEGER DEFAULT 0,
    wounds_max      INTEGER DEFAULT 3,      -- 3 for standard Wild Cards
    
    -- Power Points (0 = not a caster)
    power_points    INTEGER DEFAULT 0,
    arcane_bg       TEXT,                   -- "Magic", "Miracles", etc.
    
    -- JSON storage for lists that don't need individual querying
    -- These export as flat text in FG
    edges_json      TEXT DEFAULT '[]',      -- ["Combat Reflexes", "Block"]
    hindrances_json TEXT DEFAULT '[]',      -- ["Loyal (Major)", "Cautious (Minor)"]
    gear_json       TEXT DEFAULT '[]',      -- ["Longsword (Str+d8)", "Chain mail (+2)"]
    powers_json     TEXT DEFAULT '[]',      -- ["bolt", "deflection", "armor"]
    special_abilities_json TEXT DEFAULT '[]', -- For creatures/enhanced NPCs
    
    -- Production tracking
    stat_block_complete BOOLEAN DEFAULT 0,
    narrative_complete  BOOLEAN DEFAULT 0,
    fg_export_ready     BOOLEAN DEFAULT 0,
    
    -- Metadata
    source_document TEXT,                   -- "201_Ammaria", "300_AM_Week_01"
    notes           TEXT,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- NPC SKILLS
-- Separate table because FG XML needs individual skill entries
-- with specific dice types
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_skills (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id  INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    name    TEXT NOT NULL,               -- "Fighting", "Shooting", "Notice"
    die     INTEGER NOT NULL,            -- 4, 6, 8, 10, 12
    modifier INTEGER DEFAULT 0,          -- For FG: adjustment/skillmod fields
    UNIQUE(npc_id, name)
);

-- ============================================================
-- NPC WEAPONS (maps directly to FG <weaponlist>)
-- Structured because FG XML needs specific fields
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_weapons (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id          INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,           -- "Longsword", "Crossbow"
    damage_str      TEXT NOT NULL,           -- "Str+d8" (human-readable)
    damagedice      TEXT NOT NULL,           -- "d8+d8" (FG format, Str resolved)
    damage_bonus    INTEGER DEFAULT 0,
    armor_piercing  INTEGER DEFAULT 0,
    trait_type      TEXT NOT NULL CHECK(trait_type IN (
                        'Melee', 'Ranged', 'Thrown'
                    )),
    range           TEXT,                    -- "15/30/60" for ranged
    reach           INTEGER DEFAULT 0,
    rof             INTEGER DEFAULT 0,       -- Rate of Fire
    notes           TEXT                     -- "AP 2, Reload 1", "Two hands"
);

-- ============================================================
-- NPC ARMOR (maps to FG <armors> and NPC armor value)
-- Structured for FG export and toughness calculation
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_armor (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id          INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,            -- "Chain Mail", "Leather Armor"
    protection      INTEGER NOT NULL DEFAULT 0, -- Armor bonus (+2, +3, etc.)
    area_protected  TEXT,                     -- "Torso, arms, legs"
    min_strength    TEXT,                     -- "d8" minimum Str requirement
    weight          REAL DEFAULT 0,
    cost            TEXT,                     -- "300" in regional currency
    notes           TEXT                      -- "Covers full body", "Heavy Armor"
);

-- ============================================================
-- NPC GEAR (individual items for tracking and FG export)
-- Replaces gear_json for managed items; gear_json kept for
-- backward compat and quick text entry
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_gear (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id          INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    name            TEXT NOT NULL,            -- "Rope (50')", "Lockpicks"
    quantity        INTEGER DEFAULT 1,
    weight          REAL DEFAULT 0,
    cost            TEXT,                     -- Price in regional currency
    notes           TEXT                      -- Brief description
);

-- ============================================================
-- ORGANISATIONS
-- For cross-referencing NPCs to factions
-- ============================================================
CREATE TABLE IF NOT EXISTS organisations (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL UNIQUE,
    region  TEXT NOT NULL,
    type    TEXT,                            -- "Guild", "Military", "Criminal", "Religious", "Government"
    notes   TEXT
);

-- ============================================================
-- NPC-ORGANISATION MEMBERSHIP
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_organisations (
    npc_id  INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    org_id  INTEGER NOT NULL REFERENCES organisations(id) ON DELETE CASCADE,
    role    TEXT,                            -- "Leader", "Member", "Agent", "Former"
    PRIMARY KEY (npc_id, org_id)
);

-- ============================================================
-- NPC CONNECTIONS
-- Links between NPCs (allies, enemies, contacts)
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_connections (
    npc_id_a        INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    npc_id_b        INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    relationship    TEXT NOT NULL,           -- "ally", "enemy", "employer", "contact", "rival", "family"
    notes           TEXT,
    PRIMARY KEY (npc_id_a, npc_id_b)
);

-- ============================================================
-- NPC APPEARANCES
-- Track which products/adventures feature each NPC
-- ============================================================
CREATE TABLE IF NOT EXISTS npc_appearances (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    npc_id  INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    product TEXT NOT NULL,                   -- "Ammaria", "AM_Week_01", "One-Sheet: The Counting Quarter"
    role    TEXT,                            -- "Antagonist", "Quest-giver", "Background", "Mentioned"
    notes   TEXT,
    UNIQUE(npc_id, product)
);

-- ============================================================
-- LOCATIONS (lightweight, for cross-referencing)
-- ============================================================
CREATE TABLE IF NOT EXISTS locations (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT NOT NULL,
    region  TEXT NOT NULL,
    type    TEXT,                            -- "City", "Town", "Ruin", "Tavern", "Port", "Fortress"
    notes   TEXT
);

-- NPC-Location association
CREATE TABLE IF NOT EXISTS npc_locations (
    npc_id      INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
    location_id INTEGER NOT NULL REFERENCES locations(id) ON DELETE CASCADE,
    context     TEXT,                        -- "Resides", "Operates", "Patrols", "Born"
    PRIMARY KEY (npc_id, location_id)
);

-- ============================================================
-- USEFUL INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_npcs_region ON npcs(region);
CREATE INDEX IF NOT EXISTS idx_npcs_tier ON npcs(tier);
CREATE INDEX IF NOT EXISTS idx_npcs_archetype ON npcs(archetype);
CREATE INDEX IF NOT EXISTS idx_npc_skills_npc ON npc_skills(npc_id);
CREATE INDEX IF NOT EXISTS idx_npc_weapons_npc ON npc_weapons(npc_id);
CREATE INDEX IF NOT EXISTS idx_npc_armor_npc ON npc_armor(npc_id);
CREATE INDEX IF NOT EXISTS idx_npc_gear_npc ON npc_gear(npc_id);
CREATE INDEX IF NOT EXISTS idx_npc_orgs_npc ON npc_organisations(npc_id);
CREATE INDEX IF NOT EXISTS idx_npc_appearances_npc ON npc_appearances(npc_id);

-- ============================================================
-- AUTO-UPDATE TIMESTAMP TRIGGER
-- ============================================================
CREATE TRIGGER IF NOT EXISTS update_npc_timestamp 
    AFTER UPDATE ON npcs
    FOR EACH ROW
BEGIN
    UPDATE npcs SET updated_at = CURRENT_TIMESTAMP WHERE id = OLD.id;
END;

-- ============================================================
-- USEFUL VIEWS
-- ============================================================

-- Quick overview of all NPCs with completion status
CREATE VIEW IF NOT EXISTS v_npc_overview AS
SELECT 
    n.id,
    n.name,
    n.title,
    n.region,
    n.tier,
    n.archetype,
    n.stat_block_complete,
    n.narrative_complete,
    n.fg_export_ready,
    COUNT(DISTINCT s.id) AS skill_count,
    COUNT(DISTINCT w.id) AS weapon_count,
    COUNT(DISTINCT a.id) AS appearance_count,
    GROUP_CONCAT(DISTINCT o.name) AS organisations
FROM npcs n
LEFT JOIN npc_skills s ON s.npc_id = n.id
LEFT JOIN npc_weapons w ON w.npc_id = n.id
LEFT JOIN npc_appearances a ON a.npc_id = n.id
LEFT JOIN npc_organisations no2 ON no2.npc_id = n.id
LEFT JOIN organisations o ON o.id = no2.org_id
GROUP BY n.id;

-- NPCs ready for FG export
CREATE VIEW IF NOT EXISTS v_fg_export_ready AS
SELECT * FROM npcs 
WHERE fg_export_ready = 1 
  AND stat_block_complete = 1
ORDER BY region, name;

-- Production status by region
CREATE VIEW IF NOT EXISTS v_region_status AS
SELECT 
    region,
    tier,
    COUNT(*) AS total,
    SUM(stat_block_complete) AS stats_done,
    SUM(narrative_complete) AS narrative_done,
    SUM(fg_export_ready) AS fg_ready
FROM npcs
GROUP BY region, tier
ORDER BY region, tier;
