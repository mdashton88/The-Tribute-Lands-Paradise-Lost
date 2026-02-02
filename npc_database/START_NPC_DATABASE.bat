@echo off
title Tribute Lands NPC Database
color 0A
cd /d "%~dp0"

echo.
echo   =============================================
echo   TRIBUTE LANDS NPC DATABASE
echo   DiceForge Studios Ltd
echo   =============================================
echo.

:: Check for Python
echo   [1/4] Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo   ERROR: Python is not installed!
    echo.
    echo   Please download and install Python from:
    echo   https://www.python.org/downloads/
    echo.
    echo   IMPORTANT: During installation, tick the box that says
    echo   "Add Python to PATH" at the bottom of the first screen!
    echo.
    echo   After installing Python, run this file again.
    echo.
    pause
    exit /b 1
)
echo   Python found.

:: Install Flask if needed
echo   [2/4] Checking Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo   Installing Flask (one-time setup)...
    python -m pip install flask --quiet
    if errorlevel 1 (
        echo   ERROR: Failed to install Flask.
        pause
        exit /b 1
    )
)
echo   Flask ready.

:: Check database exists, create if not
echo   [3/4] Checking database...
if not exist "tribute_lands_npcs.db" (
    echo   Creating database and loading sample NPCs...
    python seed_data.py
    if errorlevel 1 (
        echo   ERROR: Failed to create database.
        pause
        exit /b 1
    )
)
echo   Database ready.

:: Start the server
echo   [4/4] Starting server...
echo.
echo   =============================================
echo   SUCCESS! Opening browser now...
echo   
echo   Keep this window open while using the app.
echo   Close this window to stop the server.
echo   =============================================
echo.

python app.py

pause
