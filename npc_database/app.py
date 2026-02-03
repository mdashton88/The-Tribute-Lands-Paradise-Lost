#!/usr/bin/env python3
"""
Tribute Lands NPC Database — Web Interface
DiceForge Studios Ltd

Double-click this file (or run 'python app.py') to launch the
visual NPC manager in your browser.

Requires: pip install flask
"""

VERSION = {
    "version": "2.1.0",
    "updated": "2025-02-02",
    "changes": "Resizable columns with drag handles + px width gauges"
}

import sqlite3
import json
import os
import sys
import webbrowser
import threading
import subprocess
from pathlib import Path
from flask import Flask, render_template_string, request, jsonify, send_file, redirect, url_for, send_from_directory
from werkzeug.utils import secure_filename

# Equipment catalogue — weapons, armor, gear from all sources
from equipment import WEAPONS as CAT_WEAPONS, ARMOR as CAT_ARMOR, GEAR as CAT_GEAR, SOURCES as CAT_SOURCES
from equipment import VERSION as EQUIPMENT_VERSION

# Character options catalogues
from hindrances import HINDRANCES as CAT_HINDRANCES, SOURCES as HINDRANCE_SOURCES
from hindrances import VERSION as HINDRANCES_VERSION
from edges import EDGES as CAT_EDGES, SOURCES as EDGE_SOURCES
from edges import VERSION as EDGES_VERSION
from powers import POWERS as CAT_POWERS, SOURCES as POWER_SOURCES
from powers import VERSION as POWERS_VERSION

# Try to import seed_data VERSION
try:
    from seed_data import VERSION as SEED_VERSION
except ImportError:
    SEED_VERSION = {"version": "?", "updated": "?", "changes": "Could not load"}

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

def auto_seed_if_empty():
    """Automatically run seed_data.py if the database has no NPCs."""
    conn = get_db()
    count = conn.execute("SELECT COUNT(*) FROM npcs").fetchone()[0]
    conn.close()
    if count == 0:
        print("  Database empty — auto-seeding...")
        seed_path = APP_DIR / "seed_data.py"
        if seed_path.exists():
            import subprocess
            subprocess.run([sys.executable, str(seed_path)], cwd=str(APP_DIR))
        else:
            print("  Warning: seed_data.py not found, skipping auto-seed")

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
        if 'npc_hindrances' not in tables:
            conn.execute("""CREATE TABLE IF NOT EXISTS npc_hindrances (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npc_id INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                severity TEXT NOT NULL DEFAULT 'Minor',
                source TEXT,
                notes TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_npc_hindrances_npc ON npc_hindrances(npc_id)")
            print("  Migrated: npc_hindrances table added")
        if 'npc_edges' not in tables:
            conn.execute("""CREATE TABLE IF NOT EXISTS npc_edges (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npc_id INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                source TEXT,
                notes TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_npc_edges_npc ON npc_edges(npc_id)")
            print("  Migrated: npc_edges table added")
        if 'npc_powers' not in tables:
            conn.execute("""CREATE TABLE IF NOT EXISTS npc_powers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                npc_id INTEGER NOT NULL REFERENCES npcs(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                power_points INTEGER DEFAULT 0,
                range TEXT,
                duration TEXT,
                trapping TEXT,
                source TEXT,
                notes TEXT
            )""")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_npc_powers_npc ON npc_powers(npc_id)")
            print("  Migrated: npc_powers table added")
        conn.commit()
        conn.close()

    # Portrait column migration
    conn = get_db()
    cols = [r[1] for r in conn.execute("PRAGMA table_info(npcs)").fetchall()]
    if 'portrait_path' not in cols:
        conn.execute("ALTER TABLE npcs ADD COLUMN portrait_path TEXT")
        conn.commit()
        print("  Migrated: portrait_path column added")
    conn.close()

    # Ensure portraits directory exists
    portraits_dir = APP_DIR / 'portraits'
    portraits_dir.mkdir(exist_ok=True)

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
            --success: #5a5;
            --warning: #c90;
            --danger: #c44;
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
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 50;
            height: 52px;
            box-sizing: border-box;
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
            margin-top: 52px;
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
            margin-bottom: 0;
            padding: 12px 0;
            border-bottom: 1px solid var(--border);
            position: sticky;
            top: 0;
            background: var(--bg-main);
            z-index: 8;
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
            margin: 0;
            padding: 8px 0 8px 12px;
            border-left: 2px solid var(--accent-dim);
            font-size: 14px;
            position: sticky;
            top: 60px;
            background: var(--bg-main);
            z-index: 7;
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

        /* --- THREE-COLUMN DETAIL LAYOUT --- */
        .detail-columns {
            display: flex;
            gap: 0;
            margin-top: 10px;
            height: calc(100vh - 220px);
        }
        .col-stats {
            width: 400px;
            min-width: 200px;
            flex-shrink: 0;
            overflow-y: auto;
            position: relative;
        }
        .col-workspace {
            flex: 1;
            min-width: 200px;
            overflow-y: auto;
            background: var(--bg-card);
            border: 1px solid var(--border);
            border-radius: 4px;
            padding: 14px 16px;
            position: relative;
        }
        .col-narrative {
            width: 400px;
            min-width: 200px;
            flex-shrink: 0;
            overflow-y: auto;
            position: relative;
        }
        /* --- RESIZE HANDLES --- */
        .col-resizer {
            width: 6px;
            cursor: col-resize;
            background: transparent;
            flex-shrink: 0;
            position: relative;
            z-index: 10;
            transition: background 0.15s;
        }
        .col-resizer:hover, .col-resizer.dragging {
            background: var(--accent-dim);
        }
        .col-resizer::after {
            content: '';
            position: absolute;
            top: 50%;
            left: 1px;
            width: 4px;
            height: 32px;
            transform: translateY(-50%);
            border-left: 1px solid var(--border);
            border-right: 1px solid var(--border);
        }
        /* --- WIDTH GAUGE --- */
        .col-gauge {
            position: absolute;
            top: 4px;
            right: 8px;
            font-size: 11px;
            color: var(--accent);
            opacity: 0.85;
            pointer-events: none;
            font-family: monospace;
            font-weight: 600;
            z-index: 5;
        }
        .col-workspace .col-gauge { right: 22px; }
        .workspace-empty {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            color: var(--text-dim);
            font-size: 13px;
            text-align: center;
        }
        .workspace-empty .ws-hint { font-size: 11px; margin-top: 6px; color: var(--border); }
        .workspace-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
            padding-bottom: 8px;
            border-bottom: 1px solid var(--border);
        }
        .workspace-header h3 {
            font-size: 14px;
            color: var(--accent);
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        .panel-clickable h3 { cursor: pointer; }
        .panel-clickable h3:hover { color: var(--text-bright); }

        /* --- PORTRAIT --- */
        .portrait-area {
            text-align: center;
            margin-bottom: 14px;
        }
        .portrait-frame {
            width: 100%;
            max-width: 260px;
            aspect-ratio: 3/4;
            margin: 0 auto 8px;
            background: var(--bg-input);
            border: 1px solid var(--border);
            border-radius: 4px;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
            position: relative;
        }
        .portrait-frame img {
            width: 100%;
            height: 100%;
            object-fit: cover;
        }
        .portrait-frame .portrait-placeholder {
            color: var(--text-dim);
            font-size: 11px;
        }
        .portrait-upload-btn {
            font-size: 11px;
            cursor: pointer;
            color: var(--accent-dim);
        }
        .portrait-upload-btn:hover { color: var(--accent); }
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
            <button class="btn" onclick="openSettingsModal()" title="Settings">⚙️</button>
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

<!-- SETTINGS MODAL -->
<div class="modal-overlay" id="settingsModal">
    <div class="modal" style="width:550px;max-height:80vh">
        <h3>⚙️ Settings</h3>
        <div style="display:flex;gap:8px;margin-bottom:12px;border-bottom:1px solid var(--border)">
            <button class="btn sm" id="tabVersions" onclick="showSettingsTab('versions')" style="border-radius:4px 4px 0 0">Versions</button>
            <button class="btn sm" id="tabMigration" onclick="showSettingsTab('migration')" style="border-radius:4px 4px 0 0">Migration</button>
            <button class="btn sm" id="tabAbout" onclick="showSettingsTab('about')" style="border-radius:4px 4px 0 0">About</button>
        </div>
        <div id="settingsContent" style="overflow-y:auto;max-height:55vh"></div>
        <div class="form-actions"><button class="btn" onclick="closeSettingsModal()">Close</button></div>
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
let currentHindrancesNpcId = null;
let currentEdgesNpcId = null;
let currentPowersNpcId = null;

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
    const safeName = n.name.replace(/'/g,"\\\\'").replace(/"/g,"&quot;");

    // ── COLUMN 2: STAT BLOCK ──
    let statsPanel = '';
    if (n.agility > 0) {
        const tough = n.toughness_armor > 0 ? `${n.toughness} (${n.toughness_armor})` : `${n.toughness}`;
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
        const hindrances = (n.hindrance_items||[]).length ?
            `<div class="stat-section"><span class="stat-section-label">Hindrances</span><div class="stat-val">${n.hindrance_items.map(h => h.severity === 'Major' ? `<strong>${h.name}</strong> (Major${h.notes ? ', '+h.notes : ''})` : `${h.name}${h.notes ? ' ('+h.notes+')' : ''}`).join(', ')}</div></div>` :
            ((n.hindrances||[]).length ? `<div class="stat-section"><span class="stat-section-label">Hindrances</span><div class="stat-val">${n.hindrances.join(', ')} <span style="font-size:10px;color:var(--text-dim)">(legacy)</span></div></div>` : '');
        const edges = (n.edge_items||[]).length ?
            `<div class="stat-section"><span class="stat-section-label">Edges</span><div class="stat-val">${n.edge_items.map(e => e.notes ? `${e.name} (${e.notes})` : e.name).join(', ')}</div></div>` :
            ((n.edges||[]).length ? `<div class="stat-section"><span class="stat-section-label">Edges</span><div class="stat-val">${n.edges.join(', ')} <span style="font-size:10px;color:var(--text-dim)">(legacy)</span></div></div>` : '');
        const powers = (n.power_items||[]).length ?
            `<div class="stat-section"><span class="stat-section-label">Powers (${n.power_points} PP)${n.arcane_bg ? ' — '+n.arcane_bg : ''}</span><div class="stat-val">${n.power_items.map(p => {
                let txt = p.name;
                if (p.trapping) txt += ` [${p.trapping}]`;
                return txt;
            }).join(', ')}</div></div>` :
            (n.power_points > 0 ? `<div class="stat-section"><span class="stat-section-label">Powers (${n.power_points} PP)${n.arcane_bg ? ' — '+n.arcane_bg : ''}</span><div class="stat-val">${(n.powers||[]).join(', ')} <span style="font-size:10px;color:var(--text-dim)">(legacy)</span></div></div>` : '');
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
                    <div class="stat-val">${skills || '<span style="color:var(--text-dim)">None</span>'} <button class="btn sm" onclick="openSkillsModal(${n.id},'${safeName}')">Edit</button></div>
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

    // Summary panels — compact, click header to open workspace
    const wepSummary = (n.weapons && n.weapons.length) ?
        n.weapons.map(w => `<div class="weapon-entry"><span class="wep-name">${w.name}</span> (${w.damage_str}${w.armor_piercing ? ', AP '+w.armor_piercing : ''}${w.range ? ', Range '+w.range : ''})</div>`).join('') :
        '<div style="color:var(--text-dim);font-size:12px">None</div>';
    const weaponsPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('weapons',${n.id},'${safeName}')">Weapons ✎</h3>${wepSummary}</div>`;

    const armSummary = (n.armor && n.armor.length) ?
        n.armor.map(a => `<div class="weapon-entry"><span class="wep-name">${a.name}</span> (+${a.protection}${a.area_protected ? ' — '+a.area_protected : ''})</div>`).join('') :
        '<div style="color:var(--text-dim);font-size:12px">None</div>';
    const armorPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('armor',${n.id},'${safeName}')">Armour ✎</h3>${armSummary}</div>`;

    let gearSummary = '';
    if (n.gear_items && n.gear_items.length) {
        gearSummary = n.gear_items.map(g => `<div class="weapon-entry">${g.name}${g.quantity > 1 ? ' ×'+g.quantity : ''}</div>`).join('');
    } else if ((n.gear||[]).length) {
        gearSummary = n.gear.map(g => `<div class="weapon-entry">${g}</div>`).join('') + '<div style="font-size:10px;color:var(--text-dim)">Legacy</div>';
    } else {
        gearSummary = '<div style="color:var(--text-dim);font-size:12px">None</div>';
    }
    const gearPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('gear',${n.id},'${safeName}')">Gear ✎</h3>${gearSummary}</div>`;

    const hindSummary = (n.hindrance_items && n.hindrance_items.length) ?
        n.hindrance_items.map(h => `<div class="weapon-entry">${h.name} (${h.severity})</div>`).join('') :
        ((n.hindrances||[]).length ? n.hindrances.map(h => `<div class="weapon-entry">${h}</div>`).join('') + '<div style="font-size:10px;color:var(--text-dim)">Legacy</div>' : '<div style="color:var(--text-dim);font-size:12px">None</div>');
    const hindrancesPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('hindrances',${n.id},'${safeName}')">Hindrances ✎</h3>${hindSummary}</div>`;

    const edgSummary = (n.edge_items && n.edge_items.length) ?
        n.edge_items.map(e => `<div class="weapon-entry">${e.name}</div>`).join('') :
        ((n.edges||[]).length ? n.edges.map(e => `<div class="weapon-entry">${e}</div>`).join('') + '<div style="font-size:10px;color:var(--text-dim)">Legacy</div>' : '<div style="color:var(--text-dim);font-size:12px">None</div>');
    const edgesPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('edges',${n.id},'${safeName}')">Edges ✎</h3>${edgSummary}</div>`;

    const powSummary = (n.power_items && n.power_items.length) ?
        n.power_items.map(p => `<div class="weapon-entry">${p.name}${p.trapping ? ' ['+p.trapping+']' : ''}</div>`).join('') :
        '<div style="color:var(--text-dim);font-size:12px">None</div>';
    const powersPanel = `<div class="weapons-panel panel-clickable"><h3 onclick="openWorkspace('powers',${n.id},'${safeName}')">Powers ✎</h3>${powSummary}</div>`;

    // Tactics
    let tacticsHtml = '';
    if (n.tactics) {
        tacticsHtml = `<div style="background:var(--bg-card);border:1px solid var(--border);border-radius:4px;padding:10px 16px;margin-top:10px;font-size:12px"><span style="color:var(--accent);font-weight:600;text-transform:uppercase;letter-spacing:1px;font-size:11px">Tactics</span><div style="margin-top:4px;color:var(--text)">${n.tactics}</div></div>`;
    }

    // Action buttons + production status
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

    // ── COLUMN 4: NARRATIVE + PORTRAIT ──
    const portraitSrc = n.portrait_path ? `/portraits/${n.portrait_path}?t=${Date.now()}` : '';
    const portraitHtml = `
        <div class="portrait-area">
            <div class="portrait-frame">
                ${portraitSrc ? `<img src="${portraitSrc}" alt="${n.name}">` : '<span class="portrait-placeholder">No portrait</span>'}
            </div>
            <label class="portrait-upload-btn">
                Upload Portrait <input type="file" accept="image/*" style="display:none" onchange="uploadPortrait(${n.id}, this)">
            </label>
            ${portraitSrc ? ` · <span class="portrait-upload-btn" onclick="deletePortrait(${n.id})">Remove</span>` : ''}
        </div>`;

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

    let orgsHtml = '';
    if (n.organisations_detail && n.organisations_detail.length) {
        const tags = n.organisations_detail.map(o => `<span class="tag">${o.name}${o.role ? ' ('+o.role+')' : ''}</span>`).join('');
        orgsHtml = `<div class="section"><h3>Organisations</h3><div class="tag-list">${tags}</div></div>`;
    }
    let connsHtml = '';
    if (n.connections && n.connections.length) {
        const tags = n.connections.map(c => `<span class="tag">${c.name} — ${c.relationship}</span>`).join('');
        connsHtml = `<div class="section"><h3>Connections</h3><div class="tag-list">${tags}</div></div>`;
    }
    let appsHtml = '';
    if (n.appearances && n.appearances.length) {
        const tags = n.appearances.map(a => `<span class="tag">${a.product}${a.role ? ' ['+a.role+']' : ''}</span>`).join('');
        appsHtml = `<div class="section"><h3>Appearances</h3><div class="tag-list">${tags}</div></div>`;
    }
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
        <div class="detail-columns" id="detailColumns">
            <div class="col-stats" id="colStats">
                <div class="col-gauge" id="gaugeStats"></div>
                ${statsPanel}
                ${weaponsPanel}
                ${armorPanel}
                ${gearPanel}
                ${hindrancesPanel}
                ${edgesPanel}
                ${powersPanel}
                ${tacticsHtml}
                ${statusHtml}
                <div id="exportOutput"></div>
            </div>
            <div class="col-resizer" id="resizer1"></div>
            <div class="col-workspace" id="workspacePanel">
                <div class="col-gauge" id="gaugeWorkspace"></div>
                <div class="workspace-empty">
                    <div>Click any panel heading to edit</div>
                    <div class="ws-hint">Weapons ✎ · Armour ✎ · Gear ✎ · Hindrances ✎ · Edges ✎ · Powers ✎</div>
                </div>
            </div>
            <div class="col-resizer" id="resizer2"></div>
            <div class="col-narrative" id="colNarrative">
                <div class="col-gauge" id="gaugeNarrative"></div>
                ${portraitHtml}
                ${desc}${bg}${narrative}${orgsHtml}${connsHtml}${appsHtml}${notesHtml}${source}
            </div>
        </div>`;
    initResizers();
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
// WORKSPACE PANEL — Dynamic editing in Column 3
// ============================================================
let activeWorkspace = null;

function openWorkspace(type, npcId, name) {
    activeWorkspace = type;
    // Reset source-loaded flags since workspace creates fresh elements
    catSourcesLoaded = false;
    hindSourcesLoaded = false;
    edgeSourcesLoaded = false;
    powerSourcesLoaded = false;
    const ws = document.getElementById('workspacePanel');
    const renderers = { weapons: renderWeaponsWS, armor: renderArmorWS, gear: renderGearWS, hindrances: renderHindrancesWS, edges: renderEdgesWS, powers: renderPowersWS };
    if (renderers[type]) {
        ws.innerHTML = renderers[type](npcId, name);
        // Trigger load
        const loaders = {
            weapons:    () => { currentWeaponsNpcId = npcId; loadWeapons(); loadCatalogueSources().then(() => loadWeaponCatalogue()); },
            armor:      () => { currentArmorNpcId = npcId; loadArmor(); loadCatalogueSources().then(() => loadArmorCatalogue()); },
            gear:       () => { currentGearNpcId = npcId; loadGear(); loadCatalogueSources().then(() => loadGearCatalogue()); },
            hindrances: () => { currentHindrancesNpcId = npcId; loadHindrances(); loadHindranceSources().then(() => loadHindranceCatalogue()); },
            edges:      () => { currentEdgesNpcId = npcId; loadEdges(); loadEdgeSources().then(() => loadEdgeCatalogue()); },
            powers:     () => { currentPowersNpcId = npcId; loadPowers(); loadPowerSources().then(() => loadPowerCatalogue()); },
        };
        loaders[type]();
    }
}
function closeWorkspace() {
    activeWorkspace = null;
    const ws = document.getElementById('workspacePanel');
    if (ws) ws.innerHTML = '<div class="workspace-empty"><div>Click any panel heading to edit</div><div class="ws-hint">Weapons ✎ · Armour ✎ · Gear ✎ · Hindrances ✎ · Edges ✎ · Powers ✎</div></div>';
    if (currentNPC) selectNPC(currentNPC.id);
}

function renderWeaponsWS(npcId, name) {
    return `<div class="workspace-header"><h3>Weapons — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="weaponsList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD WEAPON</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catWeaponSearch" placeholder="Search weapons..." oninput="filterCatalogue('weapon')" style="font-size:12px;margin-bottom:4px">
                <select id="catWeaponPick" onchange="fillWeaponFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catWeaponSource" onchange="loadWeaponCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-row"><div class="form-group"><label>Name</label><input id="newWepName" placeholder="Longsword"></div><div class="form-group"><label>Damage</label><input id="newWepDamage" placeholder="Str+d8"></div></div>
        <div class="form-row"><div class="form-group"><label>FG Damagedice</label><input id="newWepDice" placeholder="d8+d8"></div><div class="form-group" style="max-width:80px"><label>AP</label><input id="newWepAP" type="number" value="0"></div><div class="form-group" style="max-width:100px"><label>Type</label><select id="newWepType"><option>Melee</option><option>Ranged</option><option>Thrown</option></select></div></div>
        <div class="form-row"><div class="form-group"><label>Range</label><input id="newWepRange" placeholder="15/30/60"></div><div class="form-group" style="max-width:80px"><label>Reach</label><input id="newWepReach" type="number" value="0"></div><div class="form-group"><label>Notes</label><input id="newWepNotes" placeholder="Two hands, Reload 1"></div></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addWeapon()">Add Weapon</button></div>`;
}
function renderArmorWS(npcId, name) {
    return `<div class="workspace-header"><h3>Armour — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="armorList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD ARMOUR</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catArmorSearch" placeholder="Search armour..." oninput="filterCatalogue('armor')" style="font-size:12px;margin-bottom:4px">
                <select id="catArmorPick" onchange="fillArmorFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catArmorSource" onchange="loadArmorCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-row"><div class="form-group"><label>Name</label><input id="newArmorName" placeholder="Chain Hauberk"></div><div class="form-group" style="max-width:80px"><label>Prot</label><input id="newArmorProt" type="number" value="2"></div></div>
        <div class="form-row"><div class="form-group"><label>Area</label><input id="newArmorArea" placeholder="Torso, Arms, Legs"></div><div class="form-group"><label>Min Str</label><input id="newArmorStr" placeholder="d8"></div></div>
        <div class="form-row"><div class="form-group" style="max-width:80px"><label>Weight</label><input id="newArmorWeight" type="number" value="0" step="0.5"></div><div class="form-group"><label>Cost</label><input id="newArmorCost" placeholder="300₡"></div><div class="form-group"><label>Notes</label><input id="newArmorNotes"></div></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addArmor()">Add Armour</button></div>`;
}
function renderGearWS(npcId, name) {
    return `<div class="workspace-header"><h3>Gear — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="gearList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD ITEM</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catGearSearch" placeholder="Search gear..." oninput="filterCatalogue('gear')" style="font-size:12px;margin-bottom:4px">
                <select id="catGearPick" onchange="fillGearFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catGearSource" onchange="loadGearCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-row"><div class="form-group"><label>Name</label><input id="newGearName" placeholder="Rope (50 feet)"></div><div class="form-group" style="max-width:60px"><label>Qty</label><input id="newGearQty" type="number" value="1"></div></div>
        <div class="form-row"><div class="form-group" style="max-width:80px"><label>Weight</label><input id="newGearWeight" type="number" value="0" step="0.5"></div><div class="form-group"><label>Cost</label><input id="newGearCost" placeholder="10₡"></div><div class="form-group"><label>Notes</label><input id="newGearNotes"></div></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addGear()">Add Item</button></div>`;
}
function renderHindrancesWS(npcId, name) {
    return `<div class="workspace-header"><h3>Hindrances — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="hindrancesList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD HINDRANCE</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catHindranceSearch" placeholder="Search hindrances..." oninput="filterCatalogue('hindrance')" style="font-size:12px;margin-bottom:4px">
                <select id="catHindrancePick" onchange="fillHindranceFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catHindranceSource" onchange="loadHindranceCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-row"><div class="form-group"><label>Name</label><input id="newHindName" placeholder="Loyal"></div><div class="form-group" style="max-width:120px"><label>Severity</label><select id="newHindSeverity"><option>Minor</option><option>Major</option></select></div></div>
        <div class="form-group"><label>Notes</label><input id="newHindNotes" placeholder="Optional details"></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addHindrance()">Add Hindrance</button></div>`;
}
function renderEdgesWS(npcId, name) {
    return `<div class="workspace-header"><h3>Edges — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="edgesList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD EDGE</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catEdgeSearch" placeholder="Search edges..." oninput="filterCatalogue('edge')" style="font-size:12px;margin-bottom:4px">
                <select id="catEdgePick" onchange="fillEdgeFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catEdgeSource" onchange="loadEdgeCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-group"><label>Name</label><input id="newEdgeName" placeholder="Command"></div>
        <div class="form-group"><label>Notes</label><input id="newEdgeNotes" placeholder="Requirements, details"></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addEdge()">Add Edge</button></div>`;
}
function renderPowersWS(npcId, name) {
    return `<div class="workspace-header"><h3>Powers — ${name}</h3><button class="btn sm" onclick="closeWorkspace()">✕ Done</button></div>
        <div id="powersList"></div>
        <h4 style="margin-top:12px;color:var(--text-dim);font-size:12px">ADD POWER</h4>
        <div class="form-row" style="margin-bottom:6px;align-items:flex-end">
            <div class="form-group" style="flex:1"><label>Pick from Catalogue</label>
                <input id="catPowerSearch" placeholder="Search powers..." oninput="filterCatalogue('power')" style="font-size:12px;margin-bottom:4px">
                <select id="catPowerPick" onchange="fillPowerFromCat()" style="font-size:12px" size="6"><option value="">— Custom / Manual —</option></select>
            </div>
            <div class="form-group" style="max-width:140px"><label>Source</label>
                <select id="catPowerSource" onchange="loadPowerCatalogue()" style="font-size:12px"><option value="All">All Sources</option></select>
            </div>
        </div>
        <div class="form-row"><div class="form-group"><label>Name</label><input id="newPowerName" placeholder="Bolt"></div><div class="form-group" style="max-width:80px"><label>PP</label><input id="newPowerPP" type="number" value="0"></div></div>
        <div class="form-row"><div class="form-group"><label>Range</label><input id="newPowerRange" placeholder="Smarts x2"></div><div class="form-group"><label>Duration</label><input id="newPowerDuration" placeholder="Instant"></div></div>
        <div class="form-row"><div class="form-group"><label>Trapping</label><input id="newPowerTrapping" placeholder="Fire, Shadow, etc."></div><div class="form-group"><label>Notes</label><input id="newPowerNotes"></div></div>
        <div style="margin-top:8px"><button class="btn primary" onclick="addPower()">Add Power</button></div>`;
}

// ============================================================
// COLUMN RESIZER + WIDTH GAUGE
// ============================================================
function updateGauges() {
    const stats = document.getElementById('colStats');
    const ws = document.getElementById('workspacePanel');
    const nar = document.getElementById('colNarrative');
    const g1 = document.getElementById('gaugeStats');
    const g2 = document.getElementById('gaugeWorkspace');
    const g3 = document.getElementById('gaugeNarrative');
    if (stats && g1) g1.textContent = Math.round(stats.offsetWidth) + 'px';
    if (ws && g2) g2.textContent = Math.round(ws.offsetWidth) + 'px';
    if (nar && g3) g3.textContent = Math.round(nar.offsetWidth) + 'px';
}

function initResizers() {
    updateGauges();
    const container = document.getElementById('detailColumns');
    if (!container) return;

    setupResizer('resizer1', 'colStats', 'workspacePanel', 'left');
    setupResizer('resizer2', 'workspacePanel', 'colNarrative', 'right');
}

function setupResizer(resizerId, leftId, rightId, mode) {
    const resizer = document.getElementById(resizerId);
    const leftCol = document.getElementById(leftId);
    const rightCol = document.getElementById(rightId);
    if (!resizer || !leftCol || !rightCol) return;

    let startX, startLeftW, startRightW;

    resizer.addEventListener('mousedown', function(e) {
        e.preventDefault();
        startX = e.clientX;
        startLeftW = leftCol.offsetWidth;
        startRightW = rightCol.offsetWidth;
        resizer.classList.add('dragging');
        document.body.style.cursor = 'col-resize';
        document.body.style.userSelect = 'none';

        function onMove(e) {
            const dx = e.clientX - startX;
            const newLeft = Math.max(200, startLeftW + dx);
            const newRight = Math.max(200, startRightW - dx);
            // Only apply if both above minimums
            if (newLeft >= 200 && newRight >= 200) {
                leftCol.style.width = newLeft + 'px';
                leftCol.style.minWidth = newLeft + 'px';
                leftCol.style.flex = 'none';
                if (rightId !== 'workspacePanel') {
                    rightCol.style.width = newRight + 'px';
                    rightCol.style.minWidth = newRight + 'px';
                    rightCol.style.flex = 'none';
                }
            }
            updateGauges();
        }
        function onUp() {
            resizer.classList.remove('dragging');
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
            document.removeEventListener('mousemove', onMove);
            document.removeEventListener('mouseup', onUp);
            updateGauges();
        }
        document.addEventListener('mousemove', onMove);
        document.addEventListener('mouseup', onUp);
    });
}

// ============================================================
// PORTRAIT
// ============================================================
async function uploadPortrait(npcId, input) {
    if (!input.files || !input.files[0]) return;
    const formData = new FormData();
    formData.append('file', input.files[0]);
    const resp = await fetch(`/api/npcs/${npcId}/portrait`, { method: 'POST', body: formData });
    const data = await resp.json();
    if (data.success && currentNPC) selectNPC(currentNPC.id);
}
async function deletePortrait(npcId) {
    await api(`/api/npcs/${npcId}/portrait`, 'DELETE');
    if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// WEAPONS
// ============================================================
function openWeaponsModal(npcId, name) { openWorkspace('weapons', npcId, name); }
function closeWeaponsModal() { closeWorkspace(); }
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
    if (activeWorkspace === 'weapons') loadWeapons();
    else if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// ARMOUR
// ============================================================
function openArmorModal(npcId, name) { openWorkspace('armor', npcId, name); }
function closeArmorModal() { closeWorkspace(); }
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
    if (activeWorkspace === 'armor') loadArmor();
    else if (currentNPC) selectNPC(currentNPC.id);
}

// ============================================================
// GEAR
// ============================================================
function openGearModal(npcId, name) { openWorkspace('gear', npcId, name); }
function closeGearModal() { closeWorkspace(); }
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
    if (activeWorkspace === 'gear') loadGear();
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
let catHindrancesCache = [];
let catEdgesCache = [];
let catPowersCache = [];
let hindSourcesLoaded = false;
let edgeSourcesLoaded = false;
let powerSourcesLoaded = false;
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
// HINDRANCES
// ============================================================
function openHindrancesModal(npcId, name) { openWorkspace('hindrances', npcId, name); }
function closeHindrancesModal() { closeWorkspace(); }
async function loadHindrances() {
    const items = await api(`/api/npcs/${currentHindrancesNpcId}/hindrances`);
    const el = document.getElementById('hindrancesList');
    if (!items.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No hindrances yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Name</th><th>Severity</th><th>Notes</th><th></th></tr>${items.map(h => `
        <tr><td>${h.name}</td><td style="color:${h.severity==='Major'?'var(--red)':'var(--text-dim)'}">${h.severity}</td><td>${h.notes||'—'}</td><td><button class="btn sm danger" onclick="deleteHindrance(${h.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addHindrance() {
    const data = {
        name: document.getElementById('newHindName').value.trim(),
        severity: document.getElementById('newHindSeverity').value,
        notes: document.getElementById('newHindNotes').value.trim() || null,
    };
    if (!data.name) { alert('Hindrance name required'); return; }
    await api(`/api/npcs/${currentHindrancesNpcId}/hindrances`, 'POST', data);
    ['newHindName','newHindNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('newHindSeverity').value = 'Minor';
    document.getElementById('catHindrancePick').value = '';
    loadHindrances();
}
async function deleteHindrance(hindId) {
    const npcId = currentHindrancesNpcId || currentNPC.id;
    await api(`/api/npcs/${npcId}/hindrances/${hindId}`, 'DELETE');
    if (activeWorkspace === 'hindrances') loadHindrances();
    else if (currentNPC) selectNPC(currentNPC.id);
}
async function loadHindranceSources() {
    if (hindSourcesLoaded) return;
    const sources = await api('/api/catalogue/hindrances/sources');
    const sel = document.getElementById('catHindranceSource');
    sources.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = s;
        sel.appendChild(opt);
    });
    hindSourcesLoaded = true;
}
async function loadHindranceCatalogue() {
    const source = document.getElementById('catHindranceSource').value;
    catHindrancesCache = await api(`/api/catalogue/hindrances?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catHindrancePick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catHindrancesCache.forEach((h, i) => {
        if (h.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = h.source;
            sel.appendChild(grp);
            lastSource = h.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = `${h.name} (${h.severity})`;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}
function fillHindranceFromCat() {
    const idx = document.getElementById('catHindrancePick').value;
    if (idx === '') return;
    const h = catHindrancesCache[parseInt(idx)];
    document.getElementById('newHindName').value = h.name;
    document.getElementById('newHindSeverity').value = h.severity;
    document.getElementById('newHindNotes').value = '';
}

// ============================================================
// EDGES
// ============================================================
function openEdgesModal(npcId, name) { openWorkspace('edges', npcId, name); }
function closeEdgesModal() { closeWorkspace(); }
async function loadEdges() {
    const items = await api(`/api/npcs/${currentEdgesNpcId}/edges`);
    const el = document.getElementById('edgesList');
    if (!items.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No edges yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Name</th><th>Notes</th><th></th></tr>${items.map(e => `
        <tr><td>${e.name}</td><td>${e.notes||'—'}</td><td><button class="btn sm danger" onclick="deleteEdge(${e.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addEdge() {
    const data = {
        name: document.getElementById('newEdgeName').value.trim(),
        notes: document.getElementById('newEdgeNotes').value.trim() || null,
    };
    if (!data.name) { alert('Edge name required'); return; }
    await api(`/api/npcs/${currentEdgesNpcId}/edges`, 'POST', data);
    ['newEdgeName','newEdgeNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('catEdgePick').value = '';
    loadEdges();
}
async function deleteEdge(edgeId) {
    const npcId = currentEdgesNpcId || currentNPC.id;
    await api(`/api/npcs/${npcId}/edges/${edgeId}`, 'DELETE');
    if (activeWorkspace === 'edges') loadEdges();
    else if (currentNPC) selectNPC(currentNPC.id);
}
async function loadEdgeSources() {
    if (edgeSourcesLoaded) return;
    const sources = await api('/api/catalogue/edges/sources');
    const sel = document.getElementById('catEdgeSource');
    sources.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = s;
        sel.appendChild(opt);
    });
    edgeSourcesLoaded = true;
}
async function loadEdgeCatalogue() {
    const source = document.getElementById('catEdgeSource').value;
    catEdgesCache = await api(`/api/catalogue/edges?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catEdgePick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catEdgesCache.forEach((e, i) => {
        if (e.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = e.source;
            sel.appendChild(grp);
            lastSource = e.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = `${e.name} (${e.rank}, ${e.type})`;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}
function fillEdgeFromCat() {
    const idx = document.getElementById('catEdgePick').value;
    if (idx === '') return;
    const e = catEdgesCache[parseInt(idx)];
    document.getElementById('newEdgeName').value = e.name;
    document.getElementById('newEdgeNotes').value = e.requirements || '';
}

// ============================================================
// POWERS
// ============================================================
function openPowersModal(npcId, name) { openWorkspace('powers', npcId, name); }
function closePowersModal() { closeWorkspace(); }
async function loadPowers() {
    const items = await api(`/api/npcs/${currentPowersNpcId}/powers`);
    const el = document.getElementById('powersList');
    if (!items.length) { el.innerHTML = '<div style="color:var(--text-dim);font-size:12px">No powers yet</div>'; return; }
    el.innerHTML = `<table class="data-table"><tr><th>Name</th><th>PP</th><th>Range</th><th>Duration</th><th>Trapping</th><th></th></tr>${items.map(p => `
        <tr><td>${p.name}</td><td>${p.power_points||'—'}</td><td>${p.range||'—'}</td><td>${p.duration||'—'}</td><td>${p.trapping||'—'}</td><td><button class="btn sm danger" onclick="deletePower(${p.id})">×</button></td></tr>`).join('')}</table>`;
}
async function addPower() {
    const data = {
        name: document.getElementById('newPowerName').value.trim(),
        power_points: parseInt(document.getElementById('newPowerPP').value) || 0,
        range: document.getElementById('newPowerRange').value.trim() || null,
        duration: document.getElementById('newPowerDuration').value.trim() || null,
        trapping: document.getElementById('newPowerTrapping').value.trim() || null,
        notes: document.getElementById('newPowerNotes').value.trim() || null,
    };
    if (!data.name) { alert('Power name required'); return; }
    await api(`/api/npcs/${currentPowersNpcId}/powers`, 'POST', data);
    ['newPowerName','newPowerRange','newPowerDuration','newPowerTrapping','newPowerNotes'].forEach(id => document.getElementById(id).value = '');
    document.getElementById('newPowerPP').value = 0;
    document.getElementById('catPowerPick').value = '';
    loadPowers();
}
async function deletePower(powerId) {
    const npcId = currentPowersNpcId || currentNPC.id;
    await api(`/api/npcs/${npcId}/powers/${powerId}`, 'DELETE');
    if (activeWorkspace === 'powers') loadPowers();
    else if (currentNPC) selectNPC(currentNPC.id);
}
async function loadPowerSources() {
    if (powerSourcesLoaded) return;
    const sources = await api('/api/catalogue/powers/sources');
    const sel = document.getElementById('catPowerSource');
    sources.forEach(s => {
        const opt = document.createElement('option');
        opt.value = s; opt.textContent = s;
        sel.appendChild(opt);
    });
    powerSourcesLoaded = true;
}
async function loadPowerCatalogue() {
    const source = document.getElementById('catPowerSource').value;
    catPowersCache = await api(`/api/catalogue/powers?source=${encodeURIComponent(source)}`);
    const sel = document.getElementById('catPowerPick');
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    let lastSource = '';
    catPowersCache.forEach((p, i) => {
        if (p.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = p.source;
            sel.appendChild(grp);
            lastSource = p.source;
        }
        const opt = document.createElement('option');
        opt.value = i;
        opt.textContent = `${p.name} (${p.pp} PP, ${p.rank})`;
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
}
function fillPowerFromCat() {
    const idx = document.getElementById('catPowerPick').value;
    if (idx === '') return;
    const p = catPowersCache[parseInt(idx)];
    document.getElementById('newPowerName').value = p.name;
    document.getElementById('newPowerPP').value = parseInt(p.pp) || 0;
    document.getElementById('newPowerRange').value = p.range || '';
    document.getElementById('newPowerDuration').value = p.duration || '';
    document.getElementById('newPowerTrapping').value = '';
    document.getElementById('newPowerNotes').value = p.summary || '';
}

// ============================================================
// CATALOGUE SEARCH FILTER (universal for all 6 catalogues)
// ============================================================
function filterCatalogue(type) {
    const config = {
        weapon:    { cache: catWeaponsCache,    pickId: 'catWeaponPick',    searchId: 'catWeaponSearch',    label: w => `${w.name} (${w.damage_str}${w.ap ? ', AP '+w.ap : ''})` },
        armor:     { cache: catArmorCache,      pickId: 'catArmorPick',     searchId: 'catArmorSearch',     label: a => `${a.name} (+${a.protection})` },
        gear:      { cache: catGearCache,       pickId: 'catGearPick',      searchId: 'catGearSearch',      label: g => g.name },
        hindrance: { cache: catHindrancesCache, pickId: 'catHindrancePick', searchId: 'catHindranceSearch', label: h => `${h.name} (${h.severity})` },
        edge:      { cache: catEdgesCache,      pickId: 'catEdgePick',      searchId: 'catEdgeSearch',      label: e => `${e.name} (${e.rank}, ${e.type})` },
        power:     { cache: catPowersCache,     pickId: 'catPowerPick',     searchId: 'catPowerSearch',     label: p => `${p.name} (${p.pp} PP, ${p.rank})` },
    };
    const c = config[type];
    if (!c) return;
    const query = document.getElementById(c.searchId).value.toLowerCase().trim();
    const sel = document.getElementById(c.pickId);
    sel.innerHTML = '<option value="">— Custom / Manual —</option>';
    
    const filtered = query ? c.cache.filter((item, i) => {
        const text = c.label(item).toLowerCase();
        return text.includes(query);
    }) : c.cache;
    
    let lastSource = '';
    filtered.forEach(item => {
        const origIdx = c.cache.indexOf(item);
        if (item.source !== lastSource) {
            const grp = document.createElement('optgroup');
            grp.label = item.source;
            sel.appendChild(grp);
            lastSource = item.source;
        }
        const opt = document.createElement('option');
        opt.value = origIdx;
        opt.textContent = c.label(item);
        const grps = sel.querySelectorAll('optgroup');
        grps[grps.length-1].appendChild(opt);
    });
    
    if (query && filtered.length === 0) {
        const opt = document.createElement('option');
        opt.value = ''; opt.textContent = '— No matches —'; opt.disabled = true;
        sel.appendChild(opt);
    }
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
// SETTINGS
// ============================================================
let settingsVersions = null;

async function openSettingsModal() {
    document.getElementById('settingsModal').classList.add('active');
    showSettingsTab('versions');
}

function closeSettingsModal() {
    document.getElementById('settingsModal').classList.remove('active');
}

async function showSettingsTab(tab) {
    // Update tab buttons
    document.querySelectorAll('#settingsModal .btn.sm').forEach(b => b.style.background = 'var(--bg-dark)');
    document.getElementById('tab' + tab.charAt(0).toUpperCase() + tab.slice(1)).style.background = 'var(--primary)';
    
    const content = document.getElementById('settingsContent');
    
    if (tab === 'versions') {
        // Fetch versions if not cached
        if (!settingsVersions) {
            content.innerHTML = '<div style="color:var(--text-dim)">Loading...</div>';
            settingsVersions = await api('/api/versions');
        }
        
        const v = settingsVersions;
        content.innerHTML = `
            <table style="width:100%;font-size:13px;border-collapse:collapse">
                <tr style="border-bottom:1px solid var(--border)">
                    <th style="text-align:left;padding:8px 4px;color:var(--text-dim)">Component</th>
                    <th style="text-align:left;padding:8px 4px;color:var(--text-dim)">Version</th>
                    <th style="text-align:left;padding:8px 4px;color:var(--text-dim)">Updated</th>
                    <th style="text-align:left;padding:8px 4px;color:var(--text-dim)">Changes</th>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:8px 4px;font-weight:600">app.py</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.app.version}</td>
                    <td style="padding:8px 4px">${v.app.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.app.changes}</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:8px 4px;font-weight:600">seed_data.py</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.seed_data.version}</td>
                    <td style="padding:8px 4px">${v.seed_data.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.seed_data.changes}</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:8px 4px;font-weight:600">equipment/</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.equipment.version}</td>
                    <td style="padding:8px 4px">${v.equipment.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.equipment.changes}</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:8px 4px;font-weight:600">hindrances/</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.hindrances.version}</td>
                    <td style="padding:8px 4px">${v.hindrances.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.hindrances.changes}</td>
                </tr>
                <tr style="border-bottom:1px solid var(--border)">
                    <td style="padding:8px 4px;font-weight:600">edges/</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.edges.version}</td>
                    <td style="padding:8px 4px">${v.edges.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.edges.changes}</td>
                </tr>
                <tr>
                    <td style="padding:8px 4px;font-weight:600">powers/</td>
                    <td style="padding:8px 4px;color:var(--primary)">${v.powers.version}</td>
                    <td style="padding:8px 4px">${v.powers.updated}</td>
                    <td style="padding:8px 4px;font-size:11px;color:var(--text-dim)">${v.powers.changes}</td>
                </tr>
            </table>
            <div id="updateSection" style="margin-top:16px;padding:12px;background:var(--bg-dark);border-radius:4px">
                <div style="display:flex;align-items:center;justify-content:space-between">
                    <span style="font-size:12px;color:var(--text-dim)">Check for updates from GitHub</span>
                    <div>
                        <button class="btn" onclick="openGitHub()" style="font-size:12px;margin-right:8px">
                            📂 View Repo
                        </button>
                        <button class="btn primary" onclick="runUpdate()" id="updateBtn" style="font-size:12px">
                            🔄 Check for Updates
                        </button>
                    </div>
                </div>
                <div id="updateStatus" style="margin-top:8px;display:none"></div>
            </div>
        `;
    } else if (tab === 'migration') {
        content.innerHTML = '<div style="color:var(--text-dim)">Scanning legacy data...</div>';
        const preview = await api('/api/migration/preview');
        if (!preview.npcs || !preview.npcs.length) {
            content.innerHTML = `<div style="text-align:center;padding:20px">
                <div style="color:var(--success);font-size:14px;font-weight:600;margin-bottom:8px">✓ All Clean</div>
                <div style="font-size:12px;color:var(--text-dim)">No legacy JSON data found. All hindrances, edges and powers are managed through catalogues.</div>
            </div>`;
        } else {
            let rows = '';
            for (const npc of preview.npcs) {
                const items = [];
                for (const h of (npc.hindrances||[])) {
                    const icon = h.matched ? '✓' : '⚠';
                    const cls = h.matched ? 'color:var(--success)' : 'color:var(--warning, #e6a817)';
                    items.push(`<div style="font-size:11px;margin:2px 0"><span style="${cls}">${icon}</span> <strong>H:</strong> ${h.original} → ${h.name} (${h.severity})${h.notes ? ' ['+h.notes+']' : ''}${!h.matched ? ' <em style="color:var(--warning, #e6a817)">not in catalogue</em>' : ''}</div>`);
                }
                for (const e of (npc.edges||[])) {
                    const icon = e.matched ? '✓' : '⚠';
                    const cls = e.matched ? 'color:var(--success)' : 'color:var(--warning, #e6a817)';
                    items.push(`<div style="font-size:11px;margin:2px 0"><span style="${cls}">${icon}</span> <strong>E:</strong> ${e.original} → ${e.name}${e.notes ? ' ['+e.notes+']' : ''}${!e.matched ? ' <em style="color:var(--warning, #e6a817)">not in catalogue</em>' : ''}</div>`);
                }
                for (const p of (npc.powers||[])) {
                    const icon = p.matched ? '✓' : '⚠';
                    const cls = p.matched ? 'color:var(--success)' : 'color:var(--warning, #e6a817)';
                    items.push(`<div style="font-size:11px;margin:2px 0"><span style="${cls}">${icon}</span> <strong>P:</strong> ${p.original} → ${p.name}${!p.matched ? ' <em style="color:var(--warning, #e6a817)">not in catalogue</em>' : ''}</div>`);
                }
                rows += `<div style="margin-bottom:12px;padding:10px;background:var(--bg-dark);border-radius:4px">
                    <div style="font-weight:600;margin-bottom:4px">${npc.name} <span style="font-size:11px;color:var(--text-dim)">(ID ${npc.id})</span></div>
                    ${items.join('')}
                </div>`;
            }
            content.innerHTML = `
                <div style="margin-bottom:12px">
                    <div style="font-size:13px;font-weight:600;margin-bottom:4px">Legacy Data Migration</div>
                    <div style="font-size:11px;color:var(--text-dim);margin-bottom:8px">
                        Found ${preview.total_items} legacy items across ${preview.npcs.length} NPCs.
                        <span style="color:var(--success)">✓</span> = catalogue match,
                        <span style="color:var(--warning, #e6a817)">⚠</span> = will be added as custom entry.
                        Legacy JSON fields will be cleared after migration.
                    </div>
                </div>
                <div style="max-height:35vh;overflow-y:auto;margin-bottom:12px">${rows}</div>
                <div style="display:flex;gap:8px;align-items:center">
                    <button class="btn primary" id="migrateBtn" onclick="executeMigration()" style="font-size:12px">
                        🔄 Migrate All Legacy Data
                    </button>
                    <div id="migrateStatus" style="font-size:11px"></div>
                </div>`;
        }
    } else if (tab === 'about') {
        content.innerHTML = `
            <div style="text-align:center;padding:20px">
                <div style="font-size:24px;font-weight:700;color:var(--primary);margin-bottom:8px">TRIBUTE LANDS</div>
                <div style="font-size:14px;margin-bottom:16px">NPC Database</div>
                <div style="font-size:12px;color:var(--text-dim);margin-bottom:20px">DiceForge Studios Ltd</div>
                <div style="font-size:11px;color:var(--text-dim);line-height:1.6">
                    A production database for managing NPCs across<br>
                    The Tribute Lands: Paradise Lost setting.<br><br>
                    Built for Savage Worlds Adventure Edition.
                </div>
            </div>
        `;
    }
}

function openGitHub() {
    window.open('https://github.com/mdashton88/The-Tribute-Lands-Paradise-Lost', '_blank');
}

async function executeMigration() {
    const btn = document.getElementById('migrateBtn');
    const status = document.getElementById('migrateStatus');
    btn.disabled = true;
    btn.innerHTML = '⏳ Migrating...';
    status.innerHTML = '';
    try {
        const result = await api('/api/migration/execute', 'POST');
        if (result.success) {
            status.innerHTML = `<span style="color:var(--success)">✓ Migrated ${result.migrated_items} items across ${result.migrated_npcs} NPCs. Legacy fields cleared.</span>`;
            btn.innerHTML = '✓ Done';
            if (result.warnings && result.warnings.length) {
                status.innerHTML += '<br>' + result.warnings.map(w => `<span style="color:var(--warning, #e6a817);font-size:10px">⚠ ${w}</span>`).join('<br>');
            }
        } else {
            status.innerHTML = `<span style="color:var(--danger)">✗ ${result.error || 'Migration failed'}</span>`;
            btn.disabled = false;
            btn.innerHTML = '🔄 Retry Migration';
        }
    } catch(e) {
        status.innerHTML = `<span style="color:var(--danger)">✗ ${e.message}</span>`;
        btn.disabled = false;
        btn.innerHTML = '🔄 Retry Migration';
    }
}

async function runUpdate() {
    const btn = document.getElementById('updateBtn');
    const status = document.getElementById('updateStatus');
    
    btn.disabled = true;
    btn.innerHTML = '⏳ Checking...';
    status.style.display = 'block';
    status.innerHTML = '<span style="color:var(--text-dim)">Connecting to GitHub...</span>';
    
    try {
        const resp = await fetch('/api/update', {method: 'POST'});
        const data = await resp.json();
        
        if (data.success) {
            if (data.needs_restart) {
                status.innerHTML = '<span style="color:var(--success)">✓ ' + data.message + '</span>' +
                    '<br><span style="font-size:11px;color:var(--text-dim);margin-top:4px;display:block">' + 
                    (data.details || '') + '</span>' +
                    '<br><button class="btn primary" onclick="location.reload()" style="margin-top:8px;font-size:12px">🔄 Restart Now</button>';
            } else {
                status.innerHTML = '<span style="color:var(--success)">✓ ' + data.message + '</span>';
            }
        } else if (data.use_desktop) {
            // Git CLI not found — offer to open GitHub Desktop
            status.innerHTML = '<span style="color:var(--warning)">Git CLI not installed.</span>' +
                '<br><span style="font-size:11px;color:var(--text-dim);margin-top:4px;display:block">' +
                'Click below to open GitHub Desktop, then pull and restart.</span>' +
                '<br><button class="btn primary" onclick="openGitHubDesktop()" style="margin-top:8px;font-size:12px">📂 Open GitHub Desktop</button>';
        } else {
            status.innerHTML = '<span style="color:var(--danger)">✗ ' + data.message + '</span>';
        }
    } catch (err) {
        status.innerHTML = '<span style="color:var(--danger)">✗ Connection error: ' + err.message + '</span>';
    }
    
    btn.disabled = false;
    btn.innerHTML = '🔄 Check for Updates';
}

async function openGitHubDesktop() {
    const status = document.getElementById('updateStatus');
    try {
        const resp = await fetch('/api/open-github-desktop', {method: 'POST'});
        const data = await resp.json();
        if (data.success) {
            status.innerHTML = '<span style="color:var(--success)">✓ ' + data.message + '</span>' +
                '<br><span style="font-size:11px;color:var(--text-dim);margin-top:4px;display:block">' +
                'Pull changes in GitHub Desktop, then restart the app.</span>';
        } else {
            status.innerHTML = '<span style="color:var(--danger)">✗ ' + data.message + '</span>';
        }
    } catch (err) {
        status.innerHTML = '<span style="color:var(--danger)">✗ ' + err.message + '</span>';
    }
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
    npc['hindrance_items'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_hindrances WHERE npc_id=? ORDER BY severity DESC, name", (npc_id,)).fetchall())
    npc['edge_items'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_edges WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall())
    npc['power_items'] = rows_to_list(conn.execute(
        "SELECT * FROM npc_powers WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall())
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
    # Prefer managed hindrances over legacy JSON
    managed_hindrances = conn.execute("SELECT name, severity, notes FROM npc_hindrances WHERE npc_id=? ORDER BY severity DESC, name", (npc_id,)).fetchall()
    if managed_hindrances:
        hind_parts = []
        for h in managed_hindrances:
            part = h['name']
            if h['severity'] == 'Major':
                part += ' (Major)'
            if h['notes']:
                part += ' — {}'.format(h['notes'])
            hind_parts.append(part)
        # Override legacy line
        lines = [l for l in lines if not l.startswith('**Hindrances:**')]
        lines.append(f"**Hindrances:** {', '.join(hind_parts)}")
    # Prefer managed edges over legacy JSON
    managed_edges = conn.execute("SELECT name, notes FROM npc_edges WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
    if managed_edges:
        edge_parts = ['{}{}'.format(e['name'], ' ({})'.format(e['notes']) if e['notes'] else '') for e in managed_edges]
        lines = [l for l in lines if not l.startswith('**Edges:**')]
        lines.append(f"**Edges:** {', '.join(edge_parts)}")
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
        managed_powers = conn.execute("SELECT name, power_points, range, duration, trapping FROM npc_powers WHERE npc_id=? ORDER BY name", (npc_id,)).fetchall()
        if managed_powers:
            power_parts = []
            for p in managed_powers:
                part = p['name']
                if p['trapping']:
                    part += ' [{}]'.format(p['trapping'])
                power_parts.append(part)
            lines.append(f"**Powers ({npc['power_points']} PP):** {', '.join(power_parts)}")
        else:
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
# HINDRANCES CATALOGUE & MANAGEMENT
# ============================================================

@app.route('/api/catalogue/hindrances', methods=['GET'])
def api_catalogue_hindrances():
    source = request.args.get('source', 'All')
    severity = request.args.get('severity', 'All')
    results = CAT_HINDRANCES
    if source != 'All':
        results = [h for h in results if h['source'] == source]
    if severity != 'All':
        results = [h for h in results if h['severity'] == severity]
    return jsonify(results)

@app.route('/api/catalogue/hindrances/sources', methods=['GET'])
def api_hindrance_sources():
    return jsonify(HINDRANCE_SOURCES)

@app.route('/api/npcs/<int:npc_id>/hindrances', methods=['GET'])
def api_get_npc_hindrances(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_hindrances WHERE npc_id = ?", (npc_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/npcs/<int:npc_id>/hindrances', methods=['POST'])
def api_add_npc_hindrance(npc_id):
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO npc_hindrances (npc_id, name, severity, source, notes)
        VALUES (?, ?, ?, ?, ?)
    """, (npc_id, data['name'], data['severity'], data.get('source'), data.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/npcs/<int:npc_id>/hindrances/<int:hind_id>', methods=['DELETE'])
def api_delete_npc_hindrance(npc_id, hind_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_hindrances WHERE id = ? AND npc_id = ?", (hind_id, npc_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ============================================================
# EDGES CATALOGUE & MANAGEMENT
# ============================================================

@app.route('/api/catalogue/edges', methods=['GET'])
def api_catalogue_edges():
    source = request.args.get('source', 'All')
    results = CAT_EDGES
    if source != 'All':
        results = [e for e in results if e['source'] == source]
    return jsonify(results)

@app.route('/api/catalogue/edges/sources', methods=['GET'])
def api_edge_sources():
    return jsonify(EDGE_SOURCES)

@app.route('/api/npcs/<int:npc_id>/edges', methods=['GET'])
def api_get_npc_edges(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_edges WHERE npc_id = ?", (npc_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/npcs/<int:npc_id>/edges', methods=['POST'])
def api_add_npc_edge(npc_id):
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO npc_edges (npc_id, name, source, notes)
        VALUES (?, ?, ?, ?)
    """, (npc_id, data['name'], data.get('source'), data.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/npcs/<int:npc_id>/edges/<int:edge_id>', methods=['DELETE'])
def api_delete_npc_edge(npc_id, edge_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_edges WHERE id = ? AND npc_id = ?", (edge_id, npc_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ============================================================
# POWERS CATALOGUE & MANAGEMENT
# ============================================================

@app.route('/api/catalogue/powers', methods=['GET'])
def api_catalogue_powers():
    source = request.args.get('source', 'All')
    results = CAT_POWERS
    if source != 'All':
        results = [p for p in results if p['source'] == source]
    return jsonify(results)

@app.route('/api/catalogue/powers/sources', methods=['GET'])
def api_power_sources():
    return jsonify(POWER_SOURCES)

@app.route('/api/npcs/<int:npc_id>/powers', methods=['GET'])
def api_get_npc_powers(npc_id):
    conn = get_db()
    rows = conn.execute("SELECT * FROM npc_powers WHERE npc_id = ?", (npc_id,)).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/npcs/<int:npc_id>/powers', methods=['POST'])
def api_add_npc_power(npc_id):
    data = request.json
    conn = get_db()
    conn.execute("""
        INSERT INTO npc_powers (npc_id, name, power_points, range, duration, trapping, source, notes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (npc_id, data['name'], data.get('power_points', 0), data.get('range'),
          data.get('duration'), data.get('trapping'), data.get('source'), data.get('notes')))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/npcs/<int:npc_id>/powers/<int:power_id>', methods=['DELETE'])
def api_delete_npc_power(npc_id, power_id):
    conn = get_db()
    conn.execute("DELETE FROM npc_powers WHERE id = ? AND npc_id = ?", (power_id, npc_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

@app.route('/api/versions', methods=['GET'])
def api_versions():
    """Return version info for all system components."""
    return jsonify({
        "app": VERSION,
        "seed_data": SEED_VERSION,
        "equipment": EQUIPMENT_VERSION,
        "hindrances": HINDRANCES_VERSION,
        "edges": EDGES_VERSION,
        "powers": POWERS_VERSION
    })

@app.route('/api/update', methods=['POST'])
def api_update():
    """Run git pull to update from GitHub."""
    try:
        # Run git pull from the app directory
        result = subprocess.run(
            ['git', 'pull'],
            cwd=APP_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        output = result.stdout.strip()
        if result.returncode == 0:
            if 'Already up to date' in output:
                return jsonify({"success": True, "message": "Already up to date!", "needs_restart": False})
            else:
                return jsonify({"success": True, "message": "Updates pulled! Restart to apply.", "needs_restart": True, "details": output})
        else:
            return jsonify({"success": False, "message": f"Git error: {result.stderr.strip()}"})
    except subprocess.TimeoutExpired:
        return jsonify({"success": False, "message": "Update timed out. Check your connection."})
    except FileNotFoundError:
        # Git CLI not found — try to open GitHub Desktop instead
        return jsonify({"success": False, "message": "git_not_found", "use_desktop": True})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})

@app.route('/api/open-github-desktop', methods=['POST'])
def api_open_github_desktop():
    """Open GitHub Desktop to the repository."""
    try:
        # Get the repo root (parent of npc_database)
        repo_dir = APP_DIR.parent
        
        if sys.platform == 'win32':
            # Try to open GitHub Desktop on Windows
            # Method 1: Use the github: URI scheme
            os.startfile(f'github-windows://openRepo/{repo_dir}')
            return jsonify({"success": True, "message": "Opening GitHub Desktop..."})
        elif sys.platform == 'darwin':
            # macOS
            subprocess.run(['open', '-a', 'GitHub Desktop', str(repo_dir)])
            return jsonify({"success": True, "message": "Opening GitHub Desktop..."})
        else:
            # Linux - unlikely but handle it
            return jsonify({"success": False, "message": "Please open GitHub Desktop manually."})
    except Exception as e:
        return jsonify({"success": False, "message": f"Could not open GitHub Desktop: {str(e)}"})

# ============================================================
# LEGACY DATA MIGRATION
# ============================================================

import re as _re

def _parse_hindrance(raw):
    """Parse 'Loyal (Major — crew)' → {name, severity, notes, original}"""
    raw = raw.strip()
    result = {'original': raw, 'name': raw, 'severity': 'Minor', 'notes': ''}
    # Match pattern like "Name (Major — notes)" or "Name (Minor)"
    m = _re.match(r'^(.+?)\s*\((Major|Minor)(?:\s*[—–-]\s*(.+?))?\)\s*$', raw)
    if m:
        result['name'] = m.group(1).strip()
        result['severity'] = m.group(2)
        result['notes'] = (m.group(3) or '').strip()
    return result

def _parse_edge(raw):
    """Parse 'Connections (bureaucrats, inspectors)' → {name, notes, original}"""
    raw = raw.strip()
    result = {'original': raw, 'name': raw, 'notes': ''}
    # Check if parenthetical is NOT a severity indicator — it's edge notes
    m = _re.match(r'^(.+?)\s*\((.+?)\)\s*$', raw)
    if m:
        result['name'] = m.group(1).strip()
        result['notes'] = m.group(2).strip()
    return result

def _match_hindrance(parsed, catalogue):
    """Try to match parsed hindrance against catalogue. Returns source if matched."""
    name_lower = parsed['name'].lower()
    for item in catalogue:
        if item['name'].lower() == name_lower:
            return item.get('source', 'Core')
    return None

def _match_edge(parsed, catalogue):
    """Try to match parsed edge against catalogue. Returns source if matched."""
    name_lower = parsed['name'].lower()
    for item in catalogue:
        if item['name'].lower() == name_lower:
            return item.get('source', 'Core')
    return None

def _match_power(name, catalogue):
    """Try to match power name against catalogue."""
    name_lower = name.lower().strip()
    for item in catalogue:
        if item['name'].lower() == name_lower:
            return item
    return None

@app.route('/api/migration/preview', methods=['GET'])
def api_migration_preview():
    from powers import POWERS as CAT_POWERS
    conn = get_db()
    npcs = rows_to_list(conn.execute(
        "SELECT id, name, hindrances_json, edges_json, powers_json FROM npcs"
    ).fetchall())

    result_npcs = []
    total_items = 0

    for npc in npcs:
        hindrances_raw = json.loads(npc.get('hindrances_json') or '[]')
        edges_raw = json.loads(npc.get('edges_json') or '[]')
        powers_raw = json.loads(npc.get('powers_json') or '[]')

        if not hindrances_raw and not edges_raw and not powers_raw:
            continue

        # Check if already migrated (managed items exist)
        existing_h = conn.execute("SELECT COUNT(*) FROM npc_hindrances WHERE npc_id=?", (npc['id'],)).fetchone()[0]
        existing_e = conn.execute("SELECT COUNT(*) FROM npc_edges WHERE npc_id=?", (npc['id'],)).fetchone()[0]
        existing_p = conn.execute("SELECT COUNT(*) FROM npc_powers WHERE npc_id=?", (npc['id'],)).fetchone()[0]

        npc_result = {'id': npc['id'], 'name': npc['name'], 'hindrances': [], 'edges': [], 'powers': []}

        for h_raw in hindrances_raw:
            parsed = _parse_hindrance(h_raw)
            source = _match_hindrance(parsed, CAT_HINDRANCES)
            parsed['matched'] = source is not None
            parsed['source'] = source or 'Custom'
            npc_result['hindrances'].append(parsed)
            total_items += 1

        for e_raw in edges_raw:
            parsed = _parse_edge(e_raw)
            source = _match_edge(parsed, CAT_EDGES)
            parsed['matched'] = source is not None
            parsed['source'] = source or 'Custom'
            npc_result['edges'].append(parsed)
            total_items += 1

        for p_raw in powers_raw:
            p_name = p_raw.strip()
            match = _match_power(p_name, CAT_POWERS)
            npc_result['powers'].append({
                'original': p_raw,
                'name': p_name,
                'matched': match is not None,
                'source': match.get('source', 'Core') if match else 'Custom'
            })
            total_items += 1

        if npc_result['hindrances'] or npc_result['edges'] or npc_result['powers']:
            npc_result['already_has_managed'] = {
                'hindrances': existing_h, 'edges': existing_e, 'powers': existing_p
            }
            result_npcs.append(npc_result)

    return jsonify({'npcs': result_npcs, 'total_items': total_items})

@app.route('/api/migration/execute', methods=['POST'])
def api_migration_execute():
    from powers import POWERS as CAT_POWERS
    conn = get_db()
    npcs = rows_to_list(conn.execute(
        "SELECT id, name, hindrances_json, edges_json, powers_json, power_points, arcane_bg FROM npcs"
    ).fetchall())

    migrated_npcs = 0
    migrated_items = 0
    warnings = []

    for npc in npcs:
        hindrances_raw = json.loads(npc.get('hindrances_json') or '[]')
        edges_raw = json.loads(npc.get('edges_json') or '[]')
        powers_raw = json.loads(npc.get('powers_json') or '[]')

        if not hindrances_raw and not edges_raw and not powers_raw:
            continue

        npc_touched = False

        # Migrate hindrances
        for h_raw in hindrances_raw:
            parsed = _parse_hindrance(h_raw)
            source = _match_hindrance(parsed, CAT_HINDRANCES) or 'Custom'
            # Check for duplicate
            existing = conn.execute(
                "SELECT id FROM npc_hindrances WHERE npc_id=? AND name=?",
                (npc['id'], parsed['name'])
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO npc_hindrances (npc_id, name, severity, source, notes) VALUES (?,?,?,?,?)",
                    (npc['id'], parsed['name'], parsed['severity'], source, parsed['notes'])
                )
                migrated_items += 1
                npc_touched = True
            else:
                warnings.append(f"{npc['name']}: hindrance '{parsed['name']}' already exists, skipped")

        # Migrate edges
        for e_raw in edges_raw:
            parsed = _parse_edge(e_raw)
            source = _match_edge(parsed, CAT_EDGES) or 'Custom'
            existing = conn.execute(
                "SELECT id FROM npc_edges WHERE npc_id=? AND name=?",
                (npc['id'], parsed['name'])
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO npc_edges (npc_id, name, source, notes) VALUES (?,?,?,?)",
                    (npc['id'], parsed['name'], source, parsed['notes'])
                )
                migrated_items += 1
                npc_touched = True
            else:
                warnings.append(f"{npc['name']}: edge '{parsed['name']}' already exists, skipped")

        # Migrate powers
        for p_raw in powers_raw:
            p_name = p_raw.strip()
            match = _match_power(p_name, CAT_POWERS)
            source = match.get('source', 'Core') if match else 'Custom'
            pp_cost = match.get('pp', 0) if match else 0
            existing = conn.execute(
                "SELECT id FROM npc_powers WHERE npc_id=? AND name=?",
                (npc['id'], p_name)
            ).fetchone()
            if not existing:
                conn.execute(
                    "INSERT INTO npc_powers (npc_id, name, power_points, source, notes) VALUES (?,?,?,?,?)",
                    (npc['id'], p_name, pp_cost, source, '')
                )
                migrated_items += 1
                npc_touched = True
            else:
                warnings.append(f"{npc['name']}: power '{p_name}' already exists, skipped")

        # Clear legacy JSON fields
        if npc_touched:
            conn.execute(
                "UPDATE npcs SET hindrances_json='[]', edges_json='[]', powers_json='[]' WHERE id=?",
                (npc['id'],)
            )
            migrated_npcs += 1

    conn.commit()
    return jsonify({
        'success': True,
        'migrated_npcs': migrated_npcs,
        'migrated_items': migrated_items,
        'warnings': warnings
    })

# ============================================================
# PORTRAIT MANAGEMENT
# ============================================================

@app.route('/portraits/<path:filename>')
def serve_portrait(filename):
    return send_from_directory(APP_DIR / 'portraits', filename)

@app.route('/api/npcs/<int:npc_id>/portrait', methods=['POST'])
def api_upload_portrait(npc_id):
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    f = request.files['file']
    if not f.filename:
        return jsonify({"error": "Empty filename"}), 400
    ext = Path(f.filename).suffix.lower()
    if ext not in ('.png', '.jpg', '.jpeg', '.webp', '.gif'):
        return jsonify({"error": "Unsupported image format"}), 400
    safe_name = f"npc_{npc_id}{ext}"
    portraits_dir = APP_DIR / 'portraits'
    portraits_dir.mkdir(exist_ok=True)
    # Remove old portrait if different extension
    for old in portraits_dir.glob(f"npc_{npc_id}.*"):
        old.unlink()
    f.save(portraits_dir / safe_name)
    conn = get_db()
    conn.execute("UPDATE npcs SET portrait_path = ? WHERE id = ?", (safe_name, npc_id))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "path": f"/portraits/{safe_name}"})

@app.route('/api/npcs/<int:npc_id>/portrait', methods=['DELETE'])
def api_delete_portrait(npc_id):
    conn = get_db()
    row = conn.execute("SELECT portrait_path FROM npcs WHERE id = ?", (npc_id,)).fetchone()
    if row and row['portrait_path']:
        p = APP_DIR / 'portraits' / row['portrait_path']
        if p.exists():
            p.unlink()
    conn.execute("UPDATE npcs SET portrait_path = NULL WHERE id = ?", (npc_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True})

# ============================================================
# LAUNCH
# ============================================================

def open_browser():
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    init_db_if_needed()
    auto_seed_if_empty()
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
