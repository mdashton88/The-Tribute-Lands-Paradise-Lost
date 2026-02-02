#!/usr/bin/env python3
"""
Tribute Lands NPC Database — Web Interface
DiceForge Studios Ltd

Double-click this file (or run 'python app.py') to launch the
visual NPC manager in your browser.

Requires: pip install flask
"""

import sqlite3
import json
import os
import sys
import webbrowser
import threading
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, send_file, redirect, url_for

# Equipment catalogue — weapons, armor, gear from all sources
from equipment_catalogue import WEAPONS as CAT_WEAPONS, ARMOR as CAT_ARMOR, GEAR as CAT_GEAR, SOURCES as CAT_SOURCES

# ============================================================
# CONFIGURATION
# ============================================================

APP_DIR = Path(__file__).parent
DB_PATH = APP_DIR / "tribute_lands_npcs.db"
SCHEMA_PATH = APP_DIR / "schema.sql"

app = Flask(__name__)

# ============================================================
# DATABASE HELPERS
# ============================================================

def get_db():
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys=ON")
    return conn

def init_db_if_needed():
    if not DB_PATH.exists():
        conn = get_db()
        with open(SCHEMA_PATH, 'r') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print(f"Database created at {DB_PATH}")
    else:
        # Auto-migrate: add new tables if they don't exist
        conn = get_db()
        tables = [r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()]
        if 'npc_armor' not in tables:
            conn.execute("""CREATE TABLE IF NOT EXISTS npc_armor (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npc_id INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                protection INTEGER NOT NULL DEFAULT 0,
                area_protected TEXT,
                min_strength TEXT,
                weight REAL DEFAULT 0,
                cost TEXT,
                notes TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_npc_armor_npc ON npc_armor(npc_id)")
            print("  Migrated: npc_armor table added")
        if 'npc_gear' not in tables:
            conn.execute("""CREATE TABLE IF NOT EXISTS npc_gear (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npc_id INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                quantity INTEGER DEFAULT 1,
                weight REAL DEFAULT 0,
                cost TEXT,
                notes TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_npc_gear_npc ON npc_gear(npc_id)")
            print("  Migrated: npc_gear table added")
        conn.commit()
        conn.close()

def die_str(value):
    if value and value > 0:
        return f"d{value}"
    return "—"

def row_to_dict(row):
    if row is None:
        return None
    return dict(row)

def rows_to_list(rows):
    return [dict(r) for r in rows]

# ============================================================
# HTML TEMPLATE
# ============================================================

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tribute Lands — NPC Database</title>
    <style>
        :root {
            --bg-dark: #1a1a1a;
            --bg-card: #242424;
            --bg-input: #2e2e2e;
            --bg-hover: #333;
            --border: #444;
            --text: #d4d0c8;
            --text-dim: #888;
            --text-bright: #f0ece0;
            --accent: #c49a4a;
            --accent-dim: #8a6d33;
            --red: #a44;
            --green: #5a5;
            --blue: #4a7a9a;
            --tag-wc: #c49a4a;
            --tag-extra: #5a8a5a;
            --tag-walkon: #666;
        }

        * { box-sizing: border-box; margin: 0; padding: 0; }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, sans-serif;
            background: var(--bg-dark);
            color: var(--text);
            line-height: 1.5;
        }

        /* --- HEADER --- */
        header {
            background: linear-gradient(135deg, #1a1a1a 0%, #2a2218 100%);
            border-bottom: 2px solid var(--accent-dim);
            padding: 12px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }
        header h1 {
            font-size: 18px;
            color: var(--accent);
            font-weight: 600;
            letter-spacing: 1px;
        }
        header .subtitle {
            font-size: 11px;
            color: var(--text-dim);
            letter-spacing: 2px;
            text-transform: uppercase;
        }
        .header-stats {
            display: flex;
            gap: 16px;
            font-size: 12px;
            color: var(--text-dim);
        }
        .header-stats .stat-num {
            color: var(--accent);
            font-weight: 600;
        }

        /* --- LAYOUT --- */
        .container {
            display: flex;
            height: calc(100vh - 52px);
        }

        /* --- SIDEBAR --- */
        .sidebar {
            width: 340px;
            min-width: 340px;
            background: var(--bg-card);
            border-right: 1px solid var(--border);
            display: flex;
            flex-direction: column;
        }
        .sidebar-controls {
            padding: 10px;
            border-bottom: 1px solid var(--border);
            display: flex;
            flex-direction: column;
            gap: 6px;
        }
        .filter-row {
            display: flex;
            gap: 6px;
        }
        .sidebar-controls input,
        .sidebar-controls select {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 5px 8px;
            border-radius: 3px;
            font-size: 12px;
        }
        .sidebar-controls input { flex: 1; }
        .sidebar-controls select { min-width: 100px; }

        .npc-list {
            flex: 1;
            overflow-y: auto;
            padding: 4px;
        }
        .npc-item {
            padding: 8px 10px;
            border-radius: 4px;
            cursor: pointer;
            border: 1px solid transparent;
            margin-bottom: 2px;
        }
        .npc-item:hover { background: var(--bg-hover); }
        .npc-item.active {
            background: var(--bg-hover);
            border-color: var(--accent-dim);
        }
        .npc-item .npc-name {
            font-size: 13px;
            font-weight: 600;
            color: var(--text-bright);
        }
        .npc-item .npc-meta {
            font-size: 11px;
            color: var(--text-dim);
            margin-top: 1px;
        }
        .tier-tag {
            display: inline-block;
            padding: 0 5px;
            border-radius: 2px;
            font-size: 10px;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .tier-tag.wc { background: var(--tag-wc); color: #1a1a1a; }
        .tier-tag.extra { background: var(--tag-extra); color: #fff; }
        .tier-tag.walkon { background: var(--tag-walkon); color: #ccc; }

        .status-dots { display: inline-flex; gap: 3px; margin-left: 6px; }
        .status-dot {
            width: 8px; height: 8px; border-radius: 50%;
            display: inline-block;
        }
        .status-dot.on { background: var(--green); }
        .status-dot.off { background: var(--border); }

        .sidebar-footer {
            padding: 8px 10px;
            border-top: 1px solid var(--border);
            display: flex;
            gap: 6px;
        }

        /* --- MAIN CONTENT --- */
        .main {
            flex: 1;
            overflow-y: auto;
            padding: 20px 28px;
        }
        .main.empty-state {
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--text-dim);
            font-size: 14px;
        }

        /* --- NPC DETAIL VIEW --- */
        .npc-header {
            margin-bottom: 16px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border);
        }
        .npc-header h2 {
            font-size: 22px;
            color: var(--text-bright);
            font-weight: 600;
        }
        .npc-header .npc-title-line {
            font-size: 14px;
            color: var(--accent);
            margin-top: 2px;
        }
        .npc-quote {
            font-style: italic;
            color: var(--accent);
            margin: 12px 0;
            padding-left: 12px;
            border-left: 2px solid var(--accent-dim);
            font-size: 14px;
        }
        .npc-description, .npc-background {
            margin-bottom: 10px;
            font-size: 13px;
            line-height: 1.6;
        }

        /* --- STAT BLOCK --- */
        .stat-block {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 14px 16px;
            margin: 14px 0;
            font-size: 13px;
        }
        .stat-block .stat-line {
            margin-bottom: 4px;
        }
        .stat-block .stat-label {
            font-weight: 600;
            color: var(--text-bright);
        }
        .stat-block .derived-line {
            display: flex;
            gap: 16px;
            margin: 6px 0;
        }

        /* --- SECTIONS --- */
        .section {
            margin: 16px 0;
        }
        .section h3 {
            font-size: 13px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
            margin-bottom: 6px;
            padding-bottom: 3px;
            border-bottom: 1px solid var(--border);
        }
        .section-content {
            font-size: 13px;
            line-height: 1.6;
        }
        .section-content p { margin-bottom: 4px; }

        /* --- TABLES --- */
        table.data-table {
            width: 100%;
            border-collapse: collapse;
            font-size: 12px;
            margin-top: 4px;
        }
        table.data-table th {
            text-align: left;
            color: var(--text-dim);
            font-weight: 600;
            padding: 4px 8px;
            border-bottom: 1px solid var(--border);
        }
        table.data-table td {
            padding: 4px 8px;
            border-bottom: 1px solid #2a2a2a;
        }

        /* --- TAGS --- */
        .tag-list { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
        .tag {
            background: var(--bg-input);
            border: 1px solid var(--border);
            padding: 2px 8px;
            border-radius: 3px;
            font-size: 11px;
            color: var(--text);
        }

        /* --- TWO-COLUMN DETAIL LAYOUT --- */
        .detail-columns {
            display: flex;
            gap: 20px;
            margin-top: 14px;
        }
        .col-stats {
            width: 420px;
            min-width: 420px;
            flex-shrink: 0;
        }
        .col-narrative {
            flex: 1;
            min-width: 0;
        }
        .stat-block-panel {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 14px 16px;
            font-size: 13px;
        }
        .stat-block-panel h3 {
            font-size: 12px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 10px;
            padding-bottom: 5px;
            border-bottom: 1px solid var(--accent-dim);
        }
        .stat-block-panel .stat-section {
            margin-bottom: 8px;
        }
        .stat-block-panel .stat-section-label {
            font-size: 10px;
            color: var(--text-dim);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 2px;
        }
        .stat-block-panel .stat-val {
            color: var(--text-bright);
        }
        .stat-block-panel .derived-row {
            display: flex;
            gap: 12px;
            padding: 6px 0;
            border-top: 1px solid #2a2a2a;
            border-bottom: 1px solid #2a2a2a;
            margin: 6px 0;
        }
        .stat-block-panel .derived-item {
            text-align: center;
        }
        .stat-block-panel .derived-item .derived-num {
            font-size: 18px;
            font-weight: 700;
            color: var(--accent);
        }
        .stat-block-panel .derived-item .derived-label {
            font-size: 10px;
            color: var(--text-dim);
            text-transform: uppercase;
        }
        .weapons-panel {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 14px 16px;
            margin-top: 10px;
            font-size: 13px;
        }
        .weapons-panel h3 {
            font-size: 12px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 8px;
        }
        .weapon-entry {
            padding: 4px 0;
            border-bottom: 1px solid #2a2a2a;
            font-size: 12px;
        }
        .weapon-entry:last-child { border-bottom: none; }
        .weapon-entry .wep-name { font-weight: 600; color: var(--text-bright); }
        .actions-bar {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 10px 16px;
            margin-top: 10px;
            display: flex;
            gap: 6px;
            flex-wrap: wrap;
        }

        /* --- BUTTONS --- */
        .btn {
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 5px 12px;
            border-radius: 3px;
            cursor: pointer;
            font-size: 12px;
            text-decoration: none;
            display: inline-block;
        }
        .btn:hover { background: var(--bg-hover); border-color: var(--accent-dim); }
        .btn.primary { background: var(--accent-dim); color: var(--text-bright); border-color: var(--accent); }
        .btn.primary:hover { background: var(--accent); color: #1a1a1a; }
        .btn.danger { border-color: var(--red); }
        .btn.danger:hover { background: var(--red); color: #fff; }
        .btn.sm { padding: 3px 8px; font-size: 11px; }

        /* --- FORMS / MODAL --- */
        .modal-overlay {
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.7);
            z-index: 100;
            align-items: center;
            justify-content: center;
        }
        .modal-overlay.active { display: flex; }
        .modal {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 6px;
            padding: 20px;
            width: 600px;
            max-height: 85vh;
            overflow-y: auto;
        }
        .modal h3 {
            color: var(--accent);
            margin-bottom: 14px;
            font-size: 16px;
        }
        .form-group {
            margin-bottom: 10px;
        }
        .form-group label {
            display: block;
            font-size: 11px;
            color: var(--text-dim);
            margin-bottom: 3px;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }
        .form-group input,
        .form-group select,
        .form-group textarea {
            width: 100%;
            background: var(--bg-input);
            border: 1px solid var(--border);
            color: var(--text);
            padding: 6px 8px;
            border-radius: 3px;
            font-size: 13px;
            font-family: inherit;
        }
        .form-group textarea { resize: vertical; min-height: 60px; }
        .form-row { display: flex; gap: 10px; }
        .form-row .form-group { flex: 1; }
        .form-actions {
            margin-top: 14px;
            display: flex;
            gap: 8px;
            justify-content: flex-end;
        }

        /* --- EXPORT PANEL --- */
        .export-panel {
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 12px 16px;
            margin-top: 14px;
        }
        .export-panel pre {
            background: var(--bg-dark);
            padding: 10px;
            border-radius: 3px;
            font-size: 12px;
            overflow-x: auto;
            max-height: 300px;
            overflow-y: auto;
            white-space: pre-wrap;
            color: var(--text);
            margin-top: 8px;
        }

        /* --- TABS --- */
        .tab-bar {
            display: flex;
            gap: 2px;
            margin-bottom: 14px;
        }
        .tab-btn {
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-bottom: none;
            color: var(--text-dim);
            padding: 6px 14px;
            border-radius: 4px 4px 0 0;
            cursor: pointer;
            font-size: 12px;
        }
        .tab-btn.active {
            background: var(--bg-card);
            color: var(--accent);
            border-color: var(--accent-dim);
        }
        .tab-panel { display: none; }
        .tab-panel.active { display: block; }

        /* Scrollbar styling */
        ::-webkit-scrollbar { width: 8px; }
        ::-webkit-scrollbar-track { background: var(--bg-dark); }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #555; }
    </style>
</head>
<body>

<header>
    <div>
        <h1>TRIBUTE LANDS — NPC DATABASE</h1>
        <div class="subtitle">DiceForge Studios Ltd</div>
    </div>
    <div class="header-stats" id="headerStats"></div>
</header>

<div class="container">
    <!-- SIDEBAR -->
    <div class="sidebar">
        <div class="sidebar-controls">
            <input type="text" id="searchInput" placeholder="Search NPCs..." oninput="filterNPCs()">
            <div class="filter-row">
                <select id="regionFilter" onchange="filterNPCs()">
                    <option value="">All Regions</option>
                    <option>Ammaria</option>
                    <option>Saltlands</option>
                    <option>Vinlands</option>
                    <option>Concordium</option>
                    <option>Glasrya</option>
                    <option>Global</option>
                </select>
                <select id="tierFilter" onchange="filterNPCs()">
                    <option value="">All Tiers</option>
                    <option>Wild Card</option>
                    <option>Extra</option>
                    <option>Walk-On</option>
                </select>
            </div>
        </div>
        <div class="npc-list" id="npcList"></div>
        <div class="sidebar-footer">
            <button class="btn primary" onclick="openAddModal()" style="flex:1">+ New NPC</button>
            <button class="btn" onclick="showStatusView()">Status</button>
        </div>
    </div>

    <!-- MAIN CONTENT -->
    <div class="main empty-state" id="mainContent">
        Select an NPC or create a new one
    </div>
</div>

<!-- ADD/EDIT MODAL -->
<div class="modal-overlay" id="npcModal">
    <div class="modal">
        <h3 id="modalTitle">New NPC</h3>
        <input type="hidden" id="editId">

        <div class="form-row">
            <div class="form-group">
                <label>Name *</label>
                <input id="f_name" required>
            </div>
            <div class="form-group">
                <label>Title / Role</label>
                <input id="f_title" placeholder="e.g. Professional Fixer">
            </div>
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Region *</label>
                <select id="f_region">
                    <option>Ammaria</option>
                    <option>Saltlands</option>
                    <option>Vinlands</option>
                    <option>Concordium</option>
                    <option>Glasrya</option>
                    <option>Global</option>
                </select>
            </div>
            <div class="form-group">
                <label>Tier *</label>
                <select id="f_tier">
                    <option>Wild Card</option>
                    <option>Extra</option>
                    <option>Walk-On</option>
                </select>
            </div>
            <div class="form-group">
                <label>Archetype</label>
                <select id="f_archetype">
                    <option value="">—</option>
                    <option>combat</option>
                    <option>social</option>
                    <option>criminal</option>
                    <option>scholarly</option>
                    <option>maritime</option>
                    <option>wilderness</option>
                    <option>spellcaster</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label>Signature Quote</label>
            <input id="f_quote" placeholder="Reveals personality, not just information">
        </div>

        <div class="form-group">
            <label>Description (appearance, mannerisms)</label>
            <textarea id="f_description" rows="2"></textarea>
        </div>

        <div class="form-group">
            <label>Background</label>
            <textarea id="f_background" rows="2"></textarea>
        </div>

        <div class="form-row">
            <div class="form-group"><label>Agility</label><select id="f_agility" class="die-select"><option value="0">—</option><option value="4">d4</option><option value="6">d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option></select></div>
            <div class="form-group"><label>Smarts</label><select id="f_smarts" class="die-select"><option value="0">—</option><option value="4">d4</option><option value="6">d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option></select></div>
            <div class="form-group"><label>Spirit</label><select id="f_spirit" class="die-select"><option value="0">—</option><option value="4">d4</option><option value="6">d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option></select></div>
            <div class="form-group"><label>Strength</label><select id="f_strength" class="die-select"><option value="0">—</option><option value="4">d4</option><option value="6">d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option></select></div>
            <div class="form-group"><label>Vigor</label><select id="f_vigor" class="die-select"><option value="0">—</option><option value="4">d4</option><option value="6">d6</option><option value="8">d8</option><option value="10">d10</option><option value="12">d12</option></select></div>
        </div>

        <div class="form-row">
            <div class="form-group"><label>Pace</label><input id="f_pace" type="number" value="6"></div>
            <div class="form-group"><label>Parry</label><input id="f_parry" type="number" value="2"></div>
            <div class="form-group"><label>Toughness</label><input id="f_toughness" type="number" value="5"></div>
            <div class="form-group"><label>Tough (Armor)</label><input id="f_toughness_armor" type="number" value="0"></div>
            <div class="form-group"><label>Bennies</label><input id="f_bennies" type="number" value="0"></div>
        </div>

        <div class="form-group">
            <label>Edges (comma-separated)</label>
            <input id="f_edges" placeholder="Charismatic, Block, Combat Reflexes">
        </div>
        <div class="form-group">
            <label>Hindrances (comma-separated)</label>
            <input id="f_hindrances" placeholder="Loyal (Major), Cautious (Minor)">
        </div>
        <div class="form-group">
            <label>Gear (comma-separated)</label>
            <input id="f_gear" placeholder="Longsword (Str+d8), Chain mail (+2), 50 coins">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Power Points</label>
                <input id="f_power_points" type="number" value="0">
            </div>
            <div class="form-group">
                <label>Arcane Background</label>
                <input id="f_arcane_bg" placeholder="Magic, Miracles, etc.">
            </div>
        </div>
        <div class="form-group">
            <label>Powers (comma-separated)</label>
            <input id="f_powers" placeholder="bolt, deflection, armor">
        </div>

        <div class="form-group">
            <label>What They Want (motivation)</label>
            <input id="f_motivation">
        </div>
        <div class="form-group">
            <label>Their Secret</label>
            <textarea id="f_secret" rows="2"></textarea>
        </div>
        <div class="form-group">
            <label>Tactics</label>
            <textarea id="f_tactics" rows="2"></textarea>
        </div>
        <div class="form-group">
            <label>Services</label>
            <input id="f_services">
        </div>
        <div class="form-group">
            <label>Adventure Hook</label>
            <input id="f_adventure_hook">
        </div>

        <div class="form-row">
            <div class="form-group">
                <label>Source Document</label>
                <input id="f_source_document" placeholder="e.g. 201_Ammaria">
            </div>
            <div class="form-group">
                <label>Rank Guideline</label>
                <select id="f_rank_guideline">
                    <option value="">—</option>
                    <option>Novice</option>
                    <option>Seasoned</option>
                    <option>Veteran</option>
                    <option>Heroic</option>
                    <option>Legendary</option>
                </select>
            </div>
        </div>

        <div class="form-group">
            <label>Notes</label>
            <textarea id="f_notes" rows="2"></textarea>
        </div>

        <div class="form-actions">
            <button class="btn" onclick="closeModal()">Cancel</button>
            <button class="btn primary" onclick="saveNPC()">Save NPC</button>
        </div>
    </div>
</div>

<!-- SKILLS MODAL -->
<div class="modal-overlay" id="skillsModal">
    <div class="modal" style="width:450px">
        <h3>Manage Skills — <span id="skillsNpcName"></span></h3>
        <div id="skillsList"></div>
        <div class="form-row" style="margin-top:10px">
            <div class="form-group"><label>Skill Name</label><input id="newSkillName" placeholder="Fighting"></div>
            <div class="form-group" style="max-width:100px"><label>Die</label>
                <select id="newSkillDie"><option value="4">d4</option><option value="6">d6</option><option value="8" selected>d8</option><option value="10">d10</option><option value="12">d12</option></select>
            </div>
            <div class="form-group" style="max-width:80px;align-self:flex-end">
                <button class="btn primary" onclick="addSkill()">Add</button>
            </div>
        </div>
        <div class="form-actions"><button class="btn" onclick="closeSkillsModal()">Done</button></div>
    </div>
</div>

<!-- WEAPONS MODAL -->
<div class="modal-overlay" id="weaponsModal">
    <div class="modal" style="width:580px">
        <h3>Manage Weapons — <span id="weaponsNpcName"></span></h3>
        <div id="weaponsList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD WEAPON</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1">
                <label>Pick from Catalogue</label>
                <select id="catWeaponPick" onchange="fillWeaponFromCat()" style="font-size:12px">
                    <option value="">— Custom / Manual —</option>
                </select>
            </div>
            <div class="form-group" style="max-width:140px">
                <label>Source</label>
                <select id="catWeaponSource" onchange="loadWeaponCatalogue()" style="font-size:12px">
                    <option value="All">All Sources</option>
                </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>Name</label><input id="newWepName" placeholder="Longsword"></div>
            <div class="form-group"><label>Damage</label><input id="newWepDamage" placeholder="Str+d8"></div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>FG Damagedice</label><input id="newWepDice" placeholder="d8+d8"></div>
            <div class="form-group" style="max-width:80px"><label>AP</label><input id="newWepAP" type="number" value="0"></div>
            <div class="form-group" style="max-width:100px"><label>Type</label>
                <select id="newWepType"><option>Melee</option><option>Ranged</option><option>Thrown</option></select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>Range</label><input id="newWepRange" placeholder="15/30/60"></div>
            <div class="form-group" style="max-width:80px"><label>Reach</label><input id="newWepReach" type="number" value="0"></div>
            <div class="form-group"><label>Notes</label><input id="newWepNotes" placeholder="Two hands, Reload 1"></div>
        </div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addWeapon()">Add Weapon</button></div>
        <div class="form-actions"><button class="btn" onclick="closeWeaponsModal()">Done</button></div>
    </div>
</div>

<!-- ARMOUR MODAL -->
<div class="modal-overlay" id="armorModal">
    <div class="modal" style="width:530px">
        <h3>Manage Armour — <span id="armorNpcName"></span></h3>
        <div id="armorList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD ARMOUR</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1">
                <label>Pick from Catalogue</label>
                <select id="catArmorPick" onchange="fillArmorFromCat()" style="font-size:12px">
                    <option value="">— Custom / Manual —</option>
                </select>
            </div>
            <div class="form-group" style="max-width:140px">
                <label>Source</label>
                <select id="catArmorSource" onchange="loadArmorCatalogue()" style="font-size:12px">
                    <option value="All">All Sources</option>
                </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>Name</label><input id="newArmorName" placeholder="Chain Mail"></div>
            <div class="form-group" style="max-width:100px"><label>Protection</label><input id="newArmorProt" type="number" value="2"></div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>Areas Protected</label><input id="newArmorArea" placeholder="Torso, arms, legs"></div>
            <div class="form-group" style="max-width:100px"><label>Min Str</label><input id="newArmorStr" placeholder="d8"></div>
        </div>
        <div class="form-row">
            <div class="form-group" style="max-width:100px"><label>Weight</label><input id="newArmorWeight" type="number" value="0" step="0.5"></div>
            <div class="form-group" style="max-width:100px"><label>Cost</label><input id="newArmorCost" placeholder="300"></div>
            <div class="form-group"><label>Notes</label><input id="newArmorNotes" placeholder="Heavy Armor"></div>
        </div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addArmor()">Add Armour</button></div>
        <div class="form-actions"><button class="btn" onclick="closeArmorModal()">Done</button></div>
    </div>
</div>

<!-- GEAR MODAL -->
<div class="modal-overlay" id="gearModal">
    <div class="modal" style="width:510px">
        <h3>Manage Gear — <span id="gearNpcName"></span></h3>
        <div id="gearList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD ITEM</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1">
                <label>Pick from Catalogue</label>
                <select id="catGearPick" onchange="fillGearFromCat()" style="font-size:12px">
                    <option value="">— Custom / Manual —</option>
                </select>
            </div>
            <div class="form-group" style="max-width:140px">
                <label>Source</label>
                <select id="catGearSource" onchange="loadGearCatalogue()" style="font-size:12px">
                    <option value="All">All Sources</option>
                </select>
            </div>
        </div>
        <div class="form-row">
            <div class="form-group"><label>Item Name</label><input id="newGearName" placeholder="Rope (50')"></div>
            <div class="form-group" style="max-width:70px"><label>Qty</label><input id="newGearQty" type="number" value="1" min="1"></div>
        </div>
        <div class="form-row">
            <div class="form-group" style="max-width:100px"><label>Weight</label><input id="newGearWeight" type="number" value="0" step="0.5"></div>
            <div class="form-group" style="max-width:100px"><label>Cost</label><input id="newGearCost" placeholder="10"></div>
            <div class="form-group"><label>Notes</label><input id="newGearNotes" placeholder=""></div>
        </div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addGear()">Add Item</button></div>
        <div class="form-actions"><button class="btn" onclick="closeGearModal()">Done</button></div>
    </div>
</div>

<script>
// ============================================================
// STATE
// ============================================================
let allNPCs = [];
let currentNPC = null;
let currentSkillsNpcId = null;
let currentWeaponsNpcId = null;
let currentArmorNpcId = null;
let currentGearNpcId = null;

// ============================================================
// API CALLS
// ============================================================
async function api(url, method='GET', body=null) {
    const opts = { method, headers: {'Content-Type': 'application/json'} };
    if (body) opts.body = JSON.stringify(body);
    const r = await fetch(url, opts);
    return r.json();
}

// ============================================================
// LOAD & FILTER
// ============================================================
async function loadNPCs() {
    allNPCs = await api('/api/npcs');
    filterNPCs();
    updateHeaderStats();
}

function filterNPCs() {
    const search = document.getElementById('searchInput').value.toLowerCase();
    const region = document.getElementById('regionFilter').value;
    const tier = document.getElementById('tierFilter').value;

    let filtered = allNPCs.filter(n => {
        if (region && n.region !== region) return false;
        if (tier && n.tier !== tier) return false;
        if (search && !n.name.toLowerCase().includes(search)
            && !(n.title||'').toLowerCase().includes(search)
            && !(n.organisations||'').toLowerCase().includes(search))
            return false;
        return true;
    });

    renderNPCList(filtered);
}

function renderNPCList(npcs) {
    const el = document.getElementById('npcList');
    if (!npcs.length) {
        el.innerHTML = '<div style="padding:20px;text-align:center;color:var(--text-dim)">No NPCs found</div>';
        return;
    }

    el.innerHTML = npcs.map(n => {
        const tierClass = n.tier === 'Wild Card' ? 'wc' : n.tier === 'Extra' ? 'extra' : 'walkon';
        const active = currentNPC && currentNPC.id === n.id ? 'active' : '';
        const title = n.title ? ` — ${n.title}` : '';
        const orgs = n.organisations ? ` · ${n.organisations}` : '';
        return `
            <div class="npc-item ${active}" onclick="selectNPC(${n.id})">
                <div class="npc-name">
                    ${n.name}
                    <span class="tier-tag ${tierClass}">${n.tier === 'Wild Card' ? 'WC' : n.tier === 'Walk-On' ? 'W-O' : 'EXT'}</span>
                    <span class="status-dots" title="Stats / Narrative / FG">
                        <span class="status-dot ${n.stat_block_complete ? 'on' : 'off'}"></span>
                        <span class="status-dot ${n.narrative_complete ? 'on' : 'off'}"></span>
                        <span class="status-dot ${n.fg_export_ready ? 'on' : 'off'}"></span>
                    </span>
                </div>
                <div class="npc-meta">${n.region}${title}${orgs}</div>
            </div>`;
    }).join('');
}

function updateHeaderStats() {
    const total = allNPCs.length;
    const complete = allNPCs.filter(n => n.stat_block_complete && n.narrative_complete).length;
    const fgReady = allNPCs.filter(n => n.fg_export_ready).length;
    document.getElementById('headerStats').innerHTML = `
        <span><span class="stat-num">${total}</span> NPCs</span>
        <span><span class="stat-num">${complete}</span> Complete</span>
        <span><span class="stat-num">${fgReady}</span> FG Ready</span>`;
}

// ============================================================
// NPC DETAIL VIEW
// ============================================================
async function selectNPC(id) {
    const data = await api(`/api/npcs/${id}`);
    currentNPC = data;
    renderNPCDetail(data);
    filterNPCs(); // refresh active state
}

function dieStr(v) { return v > 0 ? 'd'+v : '—'; }

function renderNPCDetail(n) {
    const el = document.getElementById('mainContent');
    el.classList.remove('empty-state');

    const wcLabel = n.tier === 'Wild Card' ? ' ★' : '';
    const tierText = n.tier === 'Wild Card' ? 'Wild Card' : n.tier;
    const titleLine = n.title ? `<div class="npc-title-line">${n.title}</div>` : '';
    const quote = n.quote ? `<div class="npc-quote">"${n.quote}"</div>` : '';

    // ── LEFT COLUMN: STAT BLOCK ──
    let statsPanel = '';
    if (n.agility > 0) {
        const tough = n.toughness_armor > 0 ? `${n.toughness} (${n.toughness_armor})` : `${n.toughness}`;

        // Derived stat validation (SWADE rules)
        const fightingSkill = (n.skills||[]).find(s => s.name === 'Fighting');
        const fightingDie = fightingSkill ? fightingSkill.die : 0;
        const expectedPace = 6;
        const expectedParry = fightingDie > 0 ? 2 + Math.floor(fightingDie / 2) : 2;
        const expectedToughBase = 2 + Math.floor(n.vigor / 2);
        const expectedToughness = expectedToughBase + (n.toughness_armor || 0);

        const paceOk = n.pace === expectedPace;
        const parryOk = n.parry === expectedParry;
        const toughOk = n.toughness === expectedToughness;

        const paceColour = paceOk ? 'var(--success, #4a4)' : 'var(--danger, #c44)';
        const parryColour = parryOk ? 'var(--success, #4a4)' : 'var(--danger, #c44)';
        const toughColour = toughOk ? 'var(--success, #4a4)' : 'var(--danger, #c44)';

        const paceTip = paceOk ? 'Base 6 ✓' : `Expected ${expectedPace} (base 6) — edge/hindrance?`;
        const parryTip = parryOk ? `2 + Fighting ${dieStr(fightingDie)}/2 = ${expectedParry} ✓` : `Expected ${expectedParry} (2 + ${fightingDie > 0 ? dieStr(fightingDie)+'/2' : 'no Fighting'})`;
        const toughTip = toughOk ? `2 + Vigor ${dieStr(n.vigor)}/2${n.toughness_armor ? ' + '+n.toughness_armor+' armour' : ''} = ${expectedToughness} ✓` : `Expected ${expectedToughness} (2 + ${dieStr(n.vigor)}/2${n.toughness_armor ? ' + '+n.toughness_armor+' armour' : ''})`;

        const skills = (n.skills||[]).map(s => `${s.name} ${dieStr(s.die)}`).join(', ');
        const hindrances = (n.hindrances||[]).length ? `<div class="stat-section"><span class="stat-section-label">Hindrances</span><div class="stat-val">${n.hindrances.join(', ')}</div></div>` : '';
        const edges = (n.edges||[]).length ? `<div class="stat-section"><span class="stat-section-label">Edges</span><div class="stat-val">${n.edges.join(', ')}</div></div>` : '';
        const powers = n.power_points > 0 ? `<div class="stat-section"><span class="stat-section-label">Powers (${n.power_points} PP)${n.arcane_bg ? ' — '+n.arcane_bg : ''}</span><div class="stat-val">${(n.powers||[]).join(', ')}</div></div>` : '';
        const specials = (n.special_abilities||[]).length ? `<div class="stat-section"><span class="stat-section-label">Special Abilities</span><div class="stat-val">${n.special_abilities.join(', ')}</div></div>` : '';
        const bennies = n.tier === 'Wild Card' ? `<div class="derived-item"><div class="derived-num">${n.bennies}</div><div class="derived-label">Bennies</div></div>` : '';

        statsPanel = `
            <div class="stat-block-panel">
                <h3>${n.name}${wcLabel} — ${tierText}</h3>
                <div class="stat-section">
                    <span class="stat-section-label">Attributes</span>
                    <div class="stat-val">Agility ${dieStr(n.agility)}, Smarts ${dieStr(n.smarts)}, Spirit ${dieStr(n.spirit)}, Strength ${dieStr(n.strength)}, Vigor ${dieStr(n.vigor)}</div>
                </div>
                <div class="stat-section">
                    <span class="stat-section-label">Skills</span>
                    <div class="stat-val">${skills || '<span style="color:var(--text-dim)">None</span>'} <button class="btn sm" onclick="openSkillsModal(${n.id},'${n.name.replace(/'/g,"\\\\'")}')">Edit</button></div>
                </div>
                <div class="derived-row">
                    <div class="derived-item" title="${paceTip}"><div class="derived-num" style="color:${paceColour}">${n.pace}</div><div class="derived-label">Pace</div></div>
                    <div class="derived-item" title="${parryTip}"><div class="derived-num" style="color:${parryColour}">${n.parry}</div><div class="derived-label">Parry</div></div>
                    <div class="derived-item" title="${toughTip}"><div class="derived-num" style="color:${toughColour}">${tough}</div><div class="derived-label">Toughness</div></div>
                    ${bennies}
                </div>
                ${hindrances}${edges}${powers}${specials}
            </div>`;
    } else {
        statsPanel = `<div class="stat-block-panel"><h3>${n.name} — ${tierText}</h3><div style="color:var(--text-dim);font-size:12px">No attributes set. <button class="btn sm" onclick="openEditModal(${n.id})">Edit NPC</button></div></div>`;
    }

    // Weapons panel
    let weaponsPanel = '';
    const safeName = n.name.replace(/'/g,"\\\\'");
    if (n.weapons && n.weapons.length) {
        const rows = n.weapons.map(w => {
            const ap = w.armor_piercing ? `, AP ${w.armor_piercing}` : '';
            const rng = w.range ? `, Range ${w.range}` : '';
            const notes = w.notes ? `, ${w.notes}` : '';
            return `<div class="weapon-entry"><span class="wep-name">${w.name}</span> (${w.damage_str}${ap}${rng}${notes}) <button class="btn sm danger" onclick="deleteWeapon(${w.id})" style="float:right">×</button></div>`;
        }).join('');
        weaponsPanel = `<div class="weapons-panel"><h3>Weapons <button class="btn sm" onclick="openWeaponsModal(${n.id},'${safeName}')">+ Add</button></h3>${rows}</div>`;
    } else {
        weaponsPanel = `<div class="weapons-panel"><h3>Weapons <button class="btn sm" onclick="openWeaponsModal(${n.id},'${safeName}')">+ Add</button></h3><div style="color:var(--text-dim);font-size:12px">No weapons defined</div></div>`;
    }

    // Armour panel
    let armorPanel = '';
    if (n.armor && n.armor.length) {
        const rows = n.armor.map(a => {
            const area = a.area_protected ? ` — ${a.area_protected}` : '';
            const minStr = a.min_strength ? `, Min Str ${a.min_strength}` : '';
            const notes = a.notes ? `, ${a.notes}` : '';
            return `<div class="weapon-entry"><span class="wep-name">${a.name}</span> (+${a.protection}${area}${minStr}${notes}) <button class="btn sm danger" onclick="deleteArmor(${a.id})" style="float:right">×</button></div>`;
        }).join('');
        armorPanel = `<div class="weapons-panel"><h3>Armour <button class="btn sm" onclick="openArmorModal(${n.id},'${safeName}')">+ Add</button></h3>${rows}</div>`;
    } else {
        armorPanel = `<div class="weapons-panel"><h3>Armour <button class="btn sm" onclick="openArmorModal(${n.id},'${safeName}')">+ Add</button></h3><div style="color:var(--text-dim);font-size:12px">No armour defined</div></div>`;
    }

    // Gear panel
    let gearPanel = '';
    if (n.gear_items && n.gear_items.length) {
        const rows = n.gear_items.map(g => {
            const qty = g.quantity > 1 ? ` ×${g.quantity}` : '';
            const notes = g.notes ? ` (${g.notes})` : '';
            return `<div class="weapon-entry"><span class="wep-name">${g.name}</span>${qty}${notes} <button class="btn sm danger" onclick="deleteGear(${g.id})" style="float:right">×</button></div>`;
        }).join('');
        gearPanel = `<div class="weapons-panel"><h3>Gear <button class="btn sm" onclick="openGearModal(${n.id},'${safeName}')">+ Add</button></h3>${rows}</div>`;
    } else {
        // Fall back to legacy gear_json if no managed items
        const legacyGear = (n.gear||[]);
        if (legacyGear.length) {
            const rows = legacyGear.map((g, idx) => `<div class="weapon-entry"><span>${g}</span> <button class="btn sm danger" onclick="deleteLegacyGear(${n.id},${idx})" style="float:right">×</button></div>`).join('');
            gearPanel = `<div class="weapons-panel"><h3>Gear <button class="btn sm" onclick="openGearModal(${n.id},'${safeName}')">+ Add</button></h3>${rows}<div style="font-size:10px;color:var(--text-dim);margin-top:4px">Legacy data — add items via + Add to convert</div></div>`;
        } else {
            gearPanel = `<div class="weapons-panel"><h3>Gear <button class="btn sm" onclick="openGearModal(${n.id},'${safeName}')">+ Add</button></h3><div style="color:var(--text-dim);font-size:12px">No gear defined</div></div>`;
        }
    }

    // Tactics (goes under stats — it's mechanical)
    let tacticsHtml = '';
    if (n.tactics) {
        tacticsHtml = `<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:4px;padding:10px 16px;margin-top:10px;font-size:12px"><span style="color:var(--accent);font-weight:600;text-transform:uppercase;letter-spacing:1px;font-size:11px">Tactics</span><div style="margin-top:4px;color:var(--text)">${n.tactics}</div></div>`;
    }

    // Action buttons + production status (bottom of left column)
    const statusHtml = `
        <div class="actions-bar">
            <div style="width:100%;display:flex;gap:12px;margin-bottom:4px">
                <label style="font-size:11px;cursor:pointer"><input type="checkbox" ${n.stat_block_complete?'checked':''} onchange="toggleStatus(${n.id},'stat_block_complete',this.checked)"> Stats</label>
                <label style="font-size:11px;cursor:pointer"><input type="checkbox" ${n.narrative_complete?'checked':''} onchange="toggleStatus(${n.id},'narrative_complete',this.checked)"> Narrative</label>
                <label style="font-size:11px;cursor:pointer"><input type="checkbox" ${n.fg_export_ready?'checked':''} onchange="toggleStatus(${n.id},'fg_export_ready',this.checked)"> FG Ready</label>
            </div>
            <button class="btn sm" onclick="openEditModal(${n.id})">Edit</button>
            <button class="btn sm" onclick="exportStatblock(${n.id})">Stat Block</button>
            <button class="btn sm" onclick="exportFGXml(${n.id})">FG XML</button>
            <button class="btn sm danger" onclick="deleteNPC(${n.id})" style="margin-left:auto">Delete</button>
        </div>`;

    // ── RIGHT COLUMN: NARRATIVE ──
    const desc = n.description ? `<div class="section"><h3>Description</h3><div class="section-content">${n.description}</div></div>` : '';
    const bg = n.background ? `<div class="section"><h3>Background</h3><div class="section-content">${n.background}</div></div>` : '';

    let narrative = '';
    const narParts = [];
    if (n.motivation) narParts.push(`<p><strong>What They Want:</strong> ${n.motivation}</p>`);
    if (n.secret) narParts.push(`<p><strong>Their Secret:</strong> ${n.secret}</p>`);
    if (n.services) narParts.push(`<p><strong>Services:</strong> ${n.services}</p>`);
    if (n.adventure_hook) narParts.push(`<p><strong>Adventure Hook:</strong> ${n.adventure_hook}</p>`);
    if (narParts.length) {
        narrative = `<div class="section"><h3>Story</h3><div class="section-content">${narParts.join('')}</div></div>`;
    }

    // Organisations
    let orgsHtml = '';
    if (n.organisations_detail && n.organisations_detail.length) {
        const tags = n.organisations_detail.map(o => `<span class="tag">${o.name}${o.role ? ' ('+o.role+')' : ''}</span>`).join('');
        orgsHtml = `<div class="section"><h3>Organisations</h3><div class="tag-list">${tags}</div></div>`;
    }

    // Connections
    let connsHtml = '';
    if (n.connections && n.connections.length) {
        const tags = n.connections.map(c => `<span class="tag">${c.name} — ${c.relationship}</span>`).join('');
        connsHtml = `<div class="section"><h3>Connections</h3><div class="tag-list">${tags}</div></div>`;
    }

    // Appearances
    let appsHtml = '';
    if (n.appearances && n.appearances.length) {
        const tags = n.appearances.map(a => `<span class="tag">${a.product}${a.role ? ' ['+a.role+']' : ''}</span>`).join('');
        appsHtml = `<div class="section"><h3>Appearances</h3><div class="tag-list">${tags}</div></div>`;
    }

    // Notes
    let notesHtml = '';
    if (n.notes) {
        notesHtml = `<div class="section"><h3>Notes</h3><div class="section-content" style="font-size:12px;color:var(--text-dim)">${n.notes}</div></div>`;
    }
    const source = n.source_document ? `<div style="font-size:11px;color:var(--text-dim);margin-top:8px">Source: ${n.source_document}${n.rank_guideline ? ' · '+n.rank_guideline+' rank' : ''}</div>` : '';

    el.innerHTML = `
        <div class="npc-header">
            <h2>${n.name}</h2>
            ${titleLine}
        </div>
        ${quote}
        <div class="detail-columns">
            <div class="col-stats">
                ${statsPanel}
                ${weaponsPanel}
                ${armorPanel}
                ${gearPanel}
                ${tacticsHtml}
                ${statusHtml}
                <div id="exportOutput"></div>
            </div>
            <div class="col-narrative">
                ${desc}${bg}${narrative}${orgsHtml}${connsHtml}${appsHtml}${notesHtml}${source}
            </div>
        </div>`;
}

// ============================================================
// ADD / EDIT NPC
// ============================================================
function openAddModal() {
    document.getElementById('modalTitle').textContent = 'New NPC';
    document.getElementById('editId').value = '';
    // Clear all fields
    ['name','title','quote','description','background','motivation','secret','tactics','services','adventure_hook','source_document','notes','edges','hindrances','gear','powers','arcane_bg'].forEach(f => {
        document.getElementById('f_'+f).value = '';
    });
    ['agility','smarts','spirit','strength','vigor'].forEach(f => { document.getElementById('f_'+f).value = '0'; });
    document.getElementById('f_pace').value = 6;
    document.getElementById('f_parry').value = 2;
    document.getElementById('f_toughness').value = 5;
    document.getElementById('f_toughness_armor').value = 0;
    document.getElementById('f_bennies').value = 0;
    document.getElementById('f_power_points').value = 0;
    document.getElementById('f_region').value = 'Ammaria';
    document.getElementById('f_tier').value = 'Wild Card';
    document.getElementById('f_archetype').value = '';
    document.getElementById('f_rank_guideline').value = '';
    document.getElementById('npcModal').classList.add('active');
}

async function openEditModal(id) {
    const n = await api(`/api/npcs/${id}`);
    document.getElementById('modalTitle').textContent = 'Edit — ' + n.name;
    document.getElementById('editId').value = id;

    document.getElementById('f_name').value = n.name || '';
    document.getElementById('f_title').value = n.title || '';
    document.getElementById('f_region').value = n.region || 'Ammaria';
    document.getElementById('f_tier').value = n.tier || 'Wild Card';
    document.getElementById('f_archetype').value = n.archetype || '';
    document.getElementById('f_quote').value = n.quote || '';
    document.getElementById('f_description').value = n.description || '';
    document.getElementById('f_background').value = n.background || '';
    document.getElementById('f_agility').value = n.agility || 0;
    document.getElementById('f_smarts').value = n.smarts || 0;
    document.getElementById('f_spirit').value = n.spirit || 0;
    document.getElementById('f_strength').value = n.strength || 0;
    document.getElementById('f_vigor').value = n.vigor || 0;
    document.getElementById('f_pace').value = n.pace || 6;
    document.getElementById('f_parry').value = n.parry || 2;
    document.getElementById('f_toughness').value = n.toughness || 5;
    document.getElementById('f_toughness_armor').value = n.toughness_armor || 0;
    document.getElementById('f_bennies').value = n.bennies || 0;
    document.getElementById('f_edges').value = (n.edges||[]).join(', ');
    document.getElementById('f_hindrances').value = (n.hindrances||[]).join(', ');
    document.getElementById('f_gear').value = (n.gear||[]).join(', ');
    document.getElementById('f_power_points').value = n.power_points || 0;
    document.getElementById('f_arcane_bg').value = n.arcane_bg || '';
    document.getElementById('f_powers').value = (n.powers||[]).join(', ');
    document.getElementById('f_motivation').value = n.motivation || '';
    document.getElementById('f_secret').value = n.secret || '';
    document.getElementById('f_tactics').value = n.tactics || '';
    document.getElementById('f_services').value = n.services || '';
    document.getElementById('f_adventure_hook').value = n.adventure_hook || '';
    document.getElementById('f_source_document').value = n.source_document || '';
    document.getElementById('f_rank_guideline').value = n.rank_guideline || '';
    document.getElementById('f_notes').value = n.notes || '';

    document.getElementById('npcModal').classList.add('active');
}

function closeModal() { document.getElementById('npcModal').classList.remove('active'); }

function csvToList(s) { return s ? s.split(',').map(x=>x.trim()).filter(x=>x) : []; }

async function saveNPC() {
    const editId = document.getElementById('editId').value;
    const data = {
        name: document.getElementById('f_name').value,
        title: document.getElementById('f_title').value || null,
        region: document.getElementById('f_region').value,
        tier: document.getElementById('f_tier').value,
        archetype: document.getElementById('f_archetype').value || null,
        quote: document.getElementById('f_quote').value || null,
        description: document.getElementById('f_description').value || null,
        background: document.getElementById('f_background').value || null,
        agility: parseInt(document.getElementById('f_agility').value) || 0,
        smarts: parseInt(document.getElementById('f_smarts').value) || 0,
        spirit: parseInt(document.getElementById('f_spirit').value) || 0,
        strength: parseInt(document.getElementById('f_strength').value) || 0,
        vigor: parseInt(document.getElementById('f_vigor').value) || 0,
        pace: parseInt(document.getElementById('f_pace').value) || 6,
        parry: parseInt(document.getElementById('f_parry').value) || 2,
        toughness: parseInt(document.getElementById('f_toughness').value) || 5,
        toughness_armor: parseInt(document.getElementById('f_toughness_armor').value) || 0,
        bennies: parseInt(document.getElementById('f_bennies').value) || 0,
        edges_json: JSON.stringify(csvToList(document.getElementById('f_edges').value)),
        hindrances_json: JSON.stringify(csvToList(document.getElementById('f_hindrances').value)),
        gear_json: JSON.stringify(csvToList(document.getElementById('f_gear').value)),
        power_points: parseInt(document.getElementById('f_power_points').value) || 0,
        arcane_bg: document.getElementById('f_arcane_bg').value || null,
        powers_json: JSON.stringify(csvToList(document.getElementById('f_powers').value)),
        motivation: document.getElementById('f_motivation').value || null,
        secret: document.getElementById('f_secret').value || null,
        tactics: document.getElementById('f_tactics').value || null,
        services: document.getElementById('f_services').value || null,
        adventure_hook: document.getElementById('f_adventure_hook').value || null,
        source_document: document.getElementById('f_source_document').value || null,
        rank_guideline: document.getElementById('f_rank_guideline').value || null,
        notes: document.getElementById('f_notes').value || null,
    };

    if (!data.name) { alert('Name is required'); return; }

    let result;
    if (editId) {
        result = await api(`/api/npcs/${editId}`, 'PUT', data);
    } else {
        result = await api('/api/npcs', 'POST', data);
    }

    closeModal();
    await loadNPCs();
    if (result.id) selectNPC(result.id);
}

// ============================================================
// SKILLS
// ============================================================
function openSkillsModal(npcId, name) {
    currentSkillsNpcId = npcId;
    document.getElementById('skillsNpcName').textContent = name;
    document.getElementById('skillsModal').classList.add('active');
    loadSkills();
}
function closeSkillsModal() {
    document.getElementById('skillsModal').classList.remove('active');
    if (currentNPC) selectNPC(currentNPC.id);
}
async function loadSkills() {
    const skills = await api(`/api/npcs/${currentSkillsNpcId}/skills`);
    const el = document.getElementById('skillsList');
    if (!skills.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No skills yet</div>'; return; }
    el.innerHTML = `<table class="data-table">${skills.map(s => `
        <tr><td>${s.name}</td><td>d${s.die}</td><td><button class="btn sm danger" onclick="deleteSkill(${s.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addSkill() {
    const name = document.getElementById('newSkillName').value.trim();
    const die = document.getElementById('newSkillDie').value;
    if (!name) return;
    await api(`/api/npcs/${currentSkillsNpcId}/skills`, 'POST', {name, die: parseInt(die)});
    document.getElementById('newSkillName').value = '';
    loadSkills();
}
async function deleteSkill(skillId) {
    await api(`/api/skills/${skillId}`, 'DELETE');
    loadSkills();
}

// ============================================================
// WEAPONS
// ============================================================
function openWeaponsModal(npcId, name) {
    currentWeaponsNpcId = npcId;
    document.getElementById('weaponsNpcName').textContent = name;
    document.getElementById('weaponsModal').classList.add('active');
    loadWeapons();
    loadCatalogueSources().then(() => loadWeaponCatalogue());
}
function closeWeaponsModal() {
    document.getElementById('weaponsModal').classList.remove('active');
    if (currentNPC) selectNPC(currentNPC.id);
}
async function loadWeapons() {
    const weapons = await api(`/api/npcs/${currentWeaponsNpcId}/weapons`);
    const el = document.getElementById('weaponsList');
    if (!weapons.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No weapons yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Name</th><th>Dmg</th><th>FG Dice</th><th>Type</th><th>AP</th><th></th></tr>${weapons.map(w => `
        <tr><td>${w.name}</td><td>${w.damage_str}</td><td>${w.damagedice}</td><td>${w.trait_type}</td><td>${w.armor_piercing||'—'}</td><td><button class="btn sm danger" onclick="deleteWeapon(${w.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addWeapon() {
    const data = {
        name: document.getElementById('newWepName').value.trim(),
        damage_str: document.getElementById('newWepDamage').value.trim(),
        damagedice: document.getElementById('newWepDice').value.trim(),
        armor_piercing: parseInt(document.getElementById('newWepAP').value) || 0,
        trait_type: document.getElementById('newWepType').value,
        range: document.getElementById('newWepRange').value.trim() || null,
        reach: parseInt(document.getElementById('newWepReach').value) || 0,
        notes: document.getElementById('newWepNotes').value.trim() || null,
    };
    if (!data.name || !data.damage_str) { alert('Name and damage required'); return; }
    await api(`/api/npcs/${currentWeaponsNpcId}/weapons`, 'POST', data);
    ['newWepName','newWepDamage','newWepDice','newWepRange','newWepNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('newWepAP').value = 0;
    document.getElementById('newWepReach').value = 0;
    document.getElementById('catWeaponPick').value = '';
    loadWeapons();
}
async function deleteWeapon(weaponId) {
    await api(`/api/weapons/${weaponId}`, 'DELETE');
    if (document.getElementById('weaponsModal').classList.contains('active')) loadWeapons();
    else if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// ARMOUR
// ============================================================
function openArmorModal(npcId, name) {
    currentArmorNpcId = npcId;
    document.getElementById('armorNpcName').textContent = name;
    document.getElementById('armorModal').classList.add('active');
    loadArmor();
    loadCatalogueSources().then(() => loadArmorCatalogue());
}
function closeArmorModal() {
    document.getElementById('armorModal').classList.remove('active');
    if (currentNPC) selectNPC(currentNPC.id);
}
async function loadArmor() {
    const armor = await api(`/api/npcs/${currentArmorNpcId}/armor`);
    const el = document.getElementById('armorList');
    if (!armor.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No armour yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Name</th><th>Prot</th><th>Area</th><th>Min Str</th><th>Notes</th><th></th></tr>${armor.map(a => `
        <tr><td>${a.name}</td><td>+${a.protection}</td><td>${a.area_protected||'—'}</td><td>${a.min_strength||'—'}</td><td>${a.notes||''}</td><td><button class="btn sm danger" onclick="deleteArmor(${a.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addArmor() {
    const data = {
        name: document.getElementById('newArmorName').value.trim(),
        protection: parseInt(document.getElementById('newArmorProt').value) || 0,
        area_protected: document.getElementById('newArmorArea').value.trim() || null,
        min_strength: document.getElementById('newArmorStr').value.trim() || null,
        weight: parseFloat(document.getElementById('newArmorWeight').value) || 0,
        cost: document.getElementById('newArmorCost').value.trim() || null,
        notes: document.getElementById('newArmorNotes').value.trim() || null,
    };
    if (!data.name) { alert('Armour name required'); return; }
    await api(`/api/npcs/${currentArmorNpcId}/armor`, 'POST', data);
    ['newArmorName','newArmorArea','newArmorStr','newArmorCost','newArmorNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('newArmorProt').value = 2;
    document.getElementById('newArmorWeight').value = 0;
    document.getElementById('catArmorPick').value = '';
    loadArmor();
}
async function deleteArmor(armorId) {
    await api(`/api/armor/${armorId}`, 'DELETE');
    if (document.getElementById('armorModal').classList.contains('active')) loadArmor();
    else if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// GEAR
// ============================================================
function openGearModal(npcId, name) {
    currentGearNpcId = npcId;
    document.getElementById('gearNpcName').textContent = name;
    document.getElementById('gearModal').classList.add('active');
    loadGear();
    loadCatalogueSources().then(() => loadGearCatalogue());
}
function closeGearModal() {
    document.getElementById('gearModal').classList.remove('active');
    if (currentNPC) selectNPC(currentNPC.id);
}
async function loadGear() {
    const gear = await api(`/api/npcs/${currentGearNpcId}/gear`);
    const el = document.getElementById('gearList');
    if (!gear.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No gear yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Item</th><th>Qty</th><th>Wt</th><th>Cost</th><th>Notes</th><th></th></tr>${gear.map(g => `
        <tr><td>${g.name}</td><td>${g.quantity}</td><td>${g.weight||'—'}</td><td>${g.cost||'—'}</td><td>${g.notes||''}</td><td><button class="btn sm danger" onclick="deleteGear(${g.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addGear() {
    const data = {
        name: document.getElementById('newGearName').value.trim(),
        quantity: parseInt(document.getElementById('newGearQty').value) || 1,
        weight: parseFloat(document.getElementById('newGearWeight').value) || 0,
        cost: document.getElementById('newGearCost').value.trim() || null,
        notes: document.getElementById('newGearNotes').value.trim() || null,
    };
    if (!data.name) { alert('Item name required'); return; }
    await api(`/api/npcs/${currentGearNpcId}/gear`, 'POST', data);
    ['newGearName','newGearCost','newGearNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('newGearQty').value = 1;
    document.getElementById('newGearWeight').value = 0;
    document.getElementById('catGearPick').value = '';
    loadGear();
}
async function deleteGear(gearId) {
    await api(`/api/gear/${gearId}`, 'DELETE');
    if (document.getElementById('gearModal').classList.contains('active')) loadGear();
    else if (currentNPC) selectNPC(currentNPC.id);
}

async function deleteLegacyGear(npcId, index) {
    await api(`/api/npcs/${npcId}/legacy_gear/${index}`, 'DELETE');
    if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// EQUIPMENT CATALOGUE — Dropdown auto-fill
// ============================================================
let catWeaponsCache = [];
let catArmorCache = [];
let catGearCache = [];
let catSourcesLoaded = false;

async function loadCatalogueSources() {
    if (catSourcesLoaded) return;
    const sources = await api('/api/catalogue/sources');
    ['catWeaponSource','catArmorSource','catGearSource'].forEach(id => {
        const sel = document.getElementById(id);
        if (!sel) return;
        sources.forEach(s => {
            const opt = document.createElement('option');
            opt.value = s; opt.textContent = s;
            sel.appendChild(opt);
        });
    });
    catSourcesLoaded = true;
}

async function loadWeaponCatalogue() {
    const source = document.getElementById('catWeaponSource').value;
    catWeaponsCache = await api(`/api/catalogue/weapons?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catWeaponPick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catWeaponsCache.forEach((w, i) => {
        if (w.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = w.source;
            sel.appendChild(grp);
            lastSource = w.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        const tag = w.trait_type === 'Ranged' ? w.damage_str : w.damage_str;
        opt.textContent = `${w.name} (${w.damage_str}${w.ap ? ', AP '+w.ap : ''})`;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}

function fillWeaponFromCat() {
    const idx = document.getElementById('catWeaponPick').value;
    if (idx === '') return;
    const w = catWeaponsCache[parseInt(idx)];
    document.getElementById('newWepName').value = w.name;
    document.getElementById('newWepDamage').value = w.damage_str;
    document.getElementById('newWepDice').value = '';
    document.getElementById('newWepAP').value = w.ap || 0;
    document.getElementById('newWepType').value = w.trait_type;
    document.getElementById('newWepRange').value = w.range || '';
    document.getElementById('newWepReach').value = w.reach || 0;
    document.getElementById('newWepNotes').value = w.notes || '';
}

async function loadArmorCatalogue() {
    const source = document.getElementById('catArmorSource').value;
    catArmorCache = await api(`/api/catalogue/armor?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catArmorPick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catArmorCache.forEach((a, i) => {
        if (a.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = a.source;
            sel.appendChild(grp);
            lastSource = a.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = `${a.name} (+${a.protection})`;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}

function fillArmorFromCat() {
    const idx = document.getElementById('catArmorPick').value;
    if (idx === '') return;
    const a = catArmorCache[parseInt(idx)];
    document.getElementById('newArmorName').value = a.name;
    document.getElementById('newArmorProt').value = a.protection;
    document.getElementById('newArmorArea').value = a.area_protected || '';
    document.getElementById('newArmorStr').value = a.min_strength || '';
    document.getElementById('newArmorWeight').value = a.weight || 0;
    document.getElementById('newArmorCost').value = a.cost || '';
    document.getElementById('newArmorNotes').value = a.notes || '';
}

async function loadGearCatalogue() {
    const source = document.getElementById('catGearSource').value;
    catGearCache = await api(`/api/catalogue/gear?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catGearPick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catGearCache.forEach((g, i) => {
        if (g.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = g.source;
            sel.appendChild(grp);
            lastSource = g.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = g.name;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}

function fillGearFromCat() {
    const idx = document.getElementById('catGearPick').value;
    if (idx === '') return;
    const g = catGearCache[parseInt(idx)];
    document.getElementById('newGearName').value = g.name;
    document.getElementById('newGearQty').value = 1;
    document.getElementById('newGearWeight').value = g.weight || 0;
    document.getElementById('newGearCost').value = g.cost || '';
    document.getElementById('newGearNotes').value = g.notes || '';
}

// ============================================================
// STATUS TOGGLES
// ============================================================
async function toggleStatus(npcId, field, value) {
    await api(`/api/npcs/${npcId}`, 'PUT', {[field]: value ? 1 : 0});
    await loadNPCs();
}

// ============================================================
// EXPORTS
// ============================================================
async function exportStatblock(npcId) {
    const data = await api(`/api/npcs/${npcId}/statblock`);
    document.getElementById('exportOutput').innerHTML = `
        <div class="export-panel">
            <h3 style="font-size:13px;color:var(--accent)">STAT BLOCK (Markdown)</h3>
            <pre>${data.statblock}</pre>
            <button class="btn sm" onclick="copyToClipboard(this)" style="margin-top:6px">Copy</button>
        </div>`;
}

async function exportFGXml(npcId) {
    const data = await api(`/api/npcs/${npcId}/fgxml`);
    document.getElementById('exportOutput').innerHTML = `
        <div class="export-panel">
            <h3 style="font-size:13px;color:var(--accent)">FANTASY GROUNDS XML</h3>
            <pre>${escapeHtml(data.xml)}</pre>
            <button class="btn sm" onclick="copyToClipboard(this)" style="margin-top:6px">Copy</button>
        </div>`;
}

function escapeHtml(s) { return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }

function copyToClipboard(btn) {
    const pre = btn.parentElement.querySelector('pre');
    navigator.clipboard.writeText(pre.textContent);
    btn.textContent = 'Copied!';
    setTimeout(() => btn.textContent = 'Copy', 1500);
}

// ============================================================
// DELETE
// ============================================================
async function deleteNPC(id) {
    if (!confirm('Delete this NPC permanently?')) return;
    await api(`/api/npcs/${id}`, 'DELETE');
    currentNPC = null;
    document.getElementById('mainContent').innerHTML = 'Select an NPC or create a new one';
    document.getElementById('mainContent').classList.add('empty-state');
    await loadNPCs();
}

// ============================================================
// STATUS VIEW
// ============================================================
async function showStatusView() {
    const data = await api('/api/status');
    const el = document.getElementById('mainContent');
    el.classList.remove('empty-state');
    currentNPC = null;
    filterNPCs();

    const rows = data.map(r => `
        <tr><td>${r.region}</td><td>${r.tier}</td><td>${r.total}</td><td>${r.stats_done}</td><td>${r.narrative_done}</td><td>${r.fg_ready}</td></tr>`).join('');

    el.innerHTML = `
        <div class="npc-header"><h2>Production Status</h2></div>
        <table class="data-table">
            <tr><th>Region</th><th>Tier</th><th>Total</th><th>Stats Done</th><th>Narrative Done</th><th>FG Ready</th></tr>
            ${rows}
        </table>
        <div style="margin-top:20px">
            <button class="btn primary" onclick="exportRegionFG()">Export All FG-Ready NPCs</button>
        </div>
        <div id="exportOutput"></div>`;
}

async function exportRegionFG() {
    const data = await api('/api/export/all');
    document.getElementById('exportOutput').innerHTML = `
        <div class="export-panel">
            <h3 style="font-size:13px;color:var(--accent)">FULL FG MODULE XML (${data.count} NPCs)</h3>
            <pre>${escapeHtml(data.xml)}</pre>
            <button class="btn sm" onclick="copyToClipboard(this)" style="margin-top:6px">Copy</button>
        </div>`;
}

// ============================================================
// INIT
// ============================================================
loadNPCs();
</script>
</body>
</html>
'''

# ============================================================
# API ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/npcs', methods=['GET'])
def api_list_npcs():
    conn = get_db()
    rows = conn.execute("SELECT * FROM v_npc_overview ORDER BY region, tier, name").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/npcs/<int:npc_id>', methods=['GET'])
def api_get_npc(npc_id):
    conn = get_db()
    npc = row_to_dict(conn.execute("SELECT * FROM npcs WHERE id=?", (npc_id,)).fetchone())
    if not npc:
        return jsonify({'error': 'Not found'}), 404

    # Parse JSON fields
    npc['edges'] = json.loads(npc.get('edges_json') or '[]')
    npc['hindrances'] = json.loads(npc.get('hindrances_json') or '[]')
    npc['gear'] = json.loads(npc.get('gear_json') or '[]')
    npc['powers'] = json.loads(npc.get('powers_json') or '[]')
    npc['special_abilities'] = json.loads(npc.get('special_abilities_json') or '[]')

    # Related data
    npc['skills'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_skills WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall())
    npc['weapons'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_weapons WHERE npc_id=?", (npc_id,)).fetchall())
    npc['armor'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_armor WHERE npc_id=?", (npc_id,)).fetchall())
    npc['gear_items'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_gear WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall())
    npc['organisations_detail'] = rows_to_list(conn.execute("""
        SELECT o.name, no2.role FROM npc_organisations no2
        JOIN organisations o ON o.id = no2.org_id WHERE no2.npc_id = ?
    """, (npc_id,)).fetchall())
    npc['connections'] = rows_to_list(conn.execute("""
        SELECT n.name, c.relationship FROM npc_connections c
        JOIN npcs n ON n.id = c.npc_id_b WHERE c.npc_id_a = ?
        UNION
        SELECT n.name, c.relationship FROM npc_connections c
        JOIN npcs n ON n.id = c.npc_id_a WHERE c.npc_id_b = ?
    """, (npc_id, npc_id)).fetchall())
    npc['appearances'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_appearances WHERE npc_id=?", (npc_id,)).fetchall())

    conn.close()
    return jsonify(npc)

@app.route('/api/npcs', methods=['POST'])
def api_create_npc():
    data = request.json
    conn = get_db()

    fields = ['name','title','region','tier','archetype','rank_guideline','quote',
              'description','background','motivation','secret','services','adventure_hook',
              'tactics','agility','smarts','spirit','strength','vigor','pace','parry',
              'toughness','toughness_armor','bennies','power_points','arcane_bg',
              'edges_json','hindrances_json','gear_json','powers_json',
              'stat_block_complete','narrative_complete','fg_export_ready',
              'source_document','notes']

    present = {k: data[k] for k in fields if k in data}
    cols = ', '.join(present.keys())
    placeholders = ', '.join(['?'] * len(present))
    values = list(present.values())

    cursor = conn.execute(f"INSERT INTO npcs ({cols}) VALUES ({placeholders})", values)
    npc_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return jsonify({'id': npc_id})

@app.route('/api/npcs/<int:npc_id>', methods=['PUT'])
def api_update_npc(npc_id):
    data = request.json
    conn = get_db()

    sets = []
    values = []
    for k, v in data.items():
        sets.append(f"{k} = ?")
        values.append(v)
    values.append(npc_id)

    conn.execute(f"UPDATE npcs SET {', '.join(sets)} WHERE id = ?", values)
    conn.commit()
    conn.close()
    return jsonify({'id': npc_id})

@app.route('/api/npcs/<int:npc_id>', methods=['DELETE'])
def api_delete_npc(npc_id):
    conn = get_db()
    conn.execute("DELETE FROM npcs WHERE id=?", (npc_id,))
    conn.commit()
    conn.close()
    return jsonify({'deleted': npc_id})

# --- SKILLS ---
@app.route('/api/npcs/<int:npc_id>/skills', methods=['GET'])
def api_get_skills(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_skills WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/npcs/<int:npc_id>/skills', methods=['POST'])
def api_add_skill(npc_id):
    data = request.json
    conn = get_db()
    conn.execute("INSERT OR REPLACE INTO npc_skills (npc_id, name, die) VALUES (?,?,?)",
                 (npc_id, data['name'], data['die']))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/skills/<int:skill_id>', methods=['DELETE'])
def api_delete_skill(skill_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_skills WHERE id=?", (skill_id,))
    conn.commit()
    conn.close()
    return jsonify({'deleted': skill_id})

# --- WEAPONS ---
@app.route('/api/npcs/<int:npc_id>/weapons', methods=['GET'])
def api_get_weapons(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_weapons WHERE npc_id=?", (npc_id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/npcs/<int:npc_id>/weapons', methods=['POST'])
def api_add_weapon(npc_id):
    d = request.json
    conn = get_db()
    conn.execute("""INSERT INTO npc_weapons (npc_id, name, damage_str, damagedice,
                    armor_piercing, trait_type, range, reach, notes)
                    VALUES (?,?,?,?,?,?,?,?,?)""",
                 (npc_id, d['name'], d['damage_str'], d['damagedice'],
                  d.get('armor_piercing',0), d.get('trait_type','Melee'),
                  d.get('range'), d.get('reach',0), d.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/weapons/<int:weapon_id>', methods=['DELETE'])
def api_delete_weapon(weapon_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_weapons WHERE id=?", (weapon_id,))
    conn.commit()
    conn.close()
    return jsonify({'deleted': weapon_id})

# --- ARMOUR ---
@app.route('/api/npcs/<int:npc_id>/armor', methods=['GET'])
def api_get_armor(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_armor WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/npcs/<int:npc_id>/armor', methods=['POST'])
def api_add_armor(npc_id):
    d = request.json
    conn = get_db()
    conn.execute("""INSERT INTO npc_armor (npc_id, name, protection, area_protected,
                    min_strength, weight, cost, notes)
                    VALUES (?,?,?,?,?,?,?,?)""",
                 (npc_id, d['name'], d.get('protection', 0),
                  d.get('area_protected'), d.get('min_strength'),
                  d.get('weight', 0), d.get('cost'), d.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/armor/<int:armor_id>', methods=['DELETE'])
def api_delete_armor(armor_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_armor WHERE id=?", (armor_id,))
    conn.commit()
    conn.close()
    return jsonify({'deleted': armor_id})

# --- GEAR ---
@app.route('/api/npcs/<int:npc_id>/gear', methods=['GET'])
def api_get_gear(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_gear WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

@app.route('/api/npcs/<int:npc_id>/gear', methods=['POST'])
def api_add_gear(npc_id):
    d = request.json
    conn = get_db()
    conn.execute("""INSERT INTO npc_gear (npc_id, name, quantity, weight, cost, notes)
                    VALUES (?,?,?,?,?,?)""",
                 (npc_id, d['name'], d.get('quantity', 1),
                  d.get('weight', 0), d.get('cost'), d.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({'ok': True})

@app.route('/api/gear/<int:gear_id>', methods=['DELETE'])
def api_delete_gear(gear_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_gear WHERE id=?", (gear_id,))
    conn.commit()
    conn.close()
    return jsonify({'deleted': gear_id})

@app.route('/api/npcs/<int:npc_id>/legacy_gear/<int:index>', methods=['DELETE'])
def api_delete_legacy_gear(npc_id, index):
    """Remove a single item from the gear_json array by index."""
    conn = get_db()
    row = conn.execute("SELECT gear_json FROM npcs WHERE id=?", (npc_id,)).fetchone()
    if not row or not row['gear_json']:
        conn.close()
        return jsonify({'error': 'Not found'}), 404
    items = json.loads(row['gear_json'])
    if index < 0 or index >= len(items):
        conn.close()
        return jsonify({'error': 'Index out of range'}), 400
    removed = items.pop(index)
    conn.execute("UPDATE npcs SET gear_json=? WHERE id=?", (json.dumps(items), npc_id))
    conn.commit()
    conn.close()
    return jsonify({'removed': removed, 'remaining': len(items)})

# --- EXPORTS ---
@app.route('/api/npcs/<int:npc_id>/statblock', methods=['GET'])
def api_statblock(npc_id):
    conn = get_db()
    npc = conn.execute("SELECT * FROM npcs WHERE id=?", (npc_id,)).fetchone()
    if not npc:
        return jsonify({'error': 'Not found'}), 404

    lines = []
    wc = " (Wild Card)" if npc['tier'] == 'Wild Card' else ""
    lines.append(f"**{npc['name']}{wc}**")
    if npc['quote']:
        lines.append(f'*"{npc["quote"]}"*')
    if npc['description']:
        lines.append(f"\n{npc['description']}")
    lines.append("")
    if npc['agility'] > 0:
        lines.append(f"**Attributes:** Agility {die_str(npc['agility'])}, Smarts {die_str(npc['smarts'])}, Spirit {die_str(npc['spirit'])}, Strength {die_str(npc['strength'])}, Vigor {die_str(npc['vigor'])}")
    skills = conn.execute("SELECT name, die FROM npc_skills WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    if skills:
        skill_str = ', '.join('{} {}'.format(s['name'], die_str(s['die'])) for s in skills)
        lines.append(f"**Skills:** {skill_str}")
    if npc['agility'] > 0:
        t = f"{npc['toughness']} ({npc['toughness_armor']})" if npc['toughness_armor'] else str(npc['toughness'])
        lines.append(f"**Pace:** {npc['pace']}; **Parry:** {npc['parry']}; **Toughness:** {t}")
    for label, field in [('Hindrances','hindrances_json'),('Edges','edges_json')]:
        items = json.loads(npc[field]) if npc[field] else []
        if items: lines.append(f"**{label}:** {', '.join(items)}")
    # Gear — prefer managed gear items, fall back to legacy JSON
    gear_items = conn.execute("SELECT name, quantity, notes FROM npc_gear WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    if gear_items:
        gear_parts = []
        for g in gear_items:
            part = g['name']
            if g['quantity'] and g['quantity'] > 1:
                part = '{} ×{}'.format(g['name'], g['quantity'])
            if g['notes']:
                part += ' ({})'.format(g['notes'])
            gear_parts.append(part)
        lines.append(f"**Gear:** {', '.join(gear_parts)}")
    else:
        legacy = json.loads(npc['gear_json']) if npc['gear_json'] else []
        if legacy: lines.append(f"**Gear:** {', '.join(legacy)}")
    # Armour
    armor_items = conn.execute("SELECT name, protection, area_protected, notes FROM npc_armor WHERE npc_id=?", (npc_id,)).fetchall()
    if armor_items:
        armor_parts = []
        for a in armor_items:
            part = '{} (+{})'.format(a['name'], a['protection'])
            if a['area_protected']:
                part += ' — {}'.format(a['area_protected'])
            armor_parts.append(part)
        lines.append(f"**Armour:** {', '.join(armor_parts)}")
    if npc['power_points'] and npc['power_points'] > 0:
        powers = json.loads(npc['powers_json']) if npc['powers_json'] else []
        lines.append(f"**Powers ({npc['power_points']} PP):** {', '.join(powers)}")
    if npc['tactics']:
        lines.append(f"**Tactics:** {npc['tactics']}")
    conn.close()
    return jsonify({'statblock': '\n'.join(lines)})

@app.route('/api/npcs/<int:npc_id>/fgxml', methods=['GET'])
def api_fg_xml(npc_id):
    # Import the export module
    sys.path.insert(0, str(APP_DIR))
    from fg_export import npc_to_fg_xml, get_db as fg_get_db
    conn = fg_get_db()
    npc = conn.execute("SELECT * FROM npcs WHERE id=?", (npc_id,)).fetchone()
    if not npc:
        return jsonify({'error': 'Not found'}), 404
    xml = npc_to_fg_xml(conn, npc, indent="    ")
    conn.close()
    return jsonify({'xml': xml})

@app.route('/api/export/all', methods=['GET'])
def api_export_all():
    sys.path.insert(0, str(APP_DIR))
    from fg_export import npc_to_fg_xml, get_db as fg_get_db
    conn = fg_get_db()
    npcs = conn.execute("SELECT * FROM npcs WHERE stat_block_complete=1 ORDER BY region, name").fetchall()
    entries = [npc_to_fg_xml(conn, n) for n in npcs]
    xml = '<npc static="true">\n' + '\n'.join(entries) + '\n</npc>'
    conn.close()
    return jsonify({'xml': xml, 'count': len(npcs)})

@app.route('/api/status', methods=['GET'])
def api_status():
    conn = get_db()
    rows = conn.execute("SELECT * FROM v_region_status").fetchall()
    conn.close()
    return jsonify(rows_to_list(rows))

# ============================================================
# EQUIPMENT CATALOGUE API
# ============================================================

@app.route('/api/catalogue/weapons', methods=['GET'])
def api_catalogue_weapons():
    source = request.args.get('source', 'All')
    if source == 'All':
        return jsonify(CAT_WEAPONS)
    return jsonify([w for w in CAT_WEAPONS if w['source'] == source])

@app.route('/api/catalogue/armor', methods=['GET'])
def api_catalogue_armor():
    source = request.args.get('source', 'All')
    if source == 'All':
        return jsonify(CAT_ARMOR)
    return jsonify([a for a in CAT_ARMOR if a['source'] == source])

@app.route('/api/catalogue/gear', methods=['GET'])
def api_catalogue_gear():
    source = request.args.get('source', 'All')
    if source == 'All':
        return jsonify(CAT_GEAR)
    return jsonify([g for g in CAT_GEAR if g['source'] == source])

@app.route('/api/catalogue/sources', methods=['GET'])
def api_catalogue_sources():
    return jsonify(CAT_SOURCES)

# ============================================================
# LAUNCH
# ============================================================

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    init_db_if_needed()
    print("\n  ╔══════════════════════════════════════════════╗")
    print("  ║  TRIBUTE LANDS NPC DATABASE                  ║")
    print("  ║  DiceForge Studios Ltd                       ║")
    print("  ║                                              ║")
    print("  ║  Open http://127.0.0.1:5000 in your browser  ║")
    print("  ║  Press Ctrl+C to stop                        ║")
    print("  ╚══════════════════════════════════════════════╝\n")

    # Auto-open browser after a short delay
    threading.Timer(1.0, open_browser).start()

    app.run(debug=False, port=5000)
