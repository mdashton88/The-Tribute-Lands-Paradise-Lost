@echo off
color 0A
title Tribute Lands NPC Database

echo.
echo ========================================
echo   TRIBUTE LANDS NPC DATABASE
echo ========================================
echo.

REM Step 1: Check Python
echo [1/4] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    color 0C
    echo.
    echo ERROR: Python not found!
    echo.
    echo Please install Python from: https://www.python.org/downloads/
    echo IMPORTANT: Check "Add Python to PATH" during installation!
    echo.
    pause
    exit /b 1
)
echo       Python found.

REM Step 2: Check Flask
echo [2/4] Checking Flask...
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo       Installing Flask...
    pip install flask --quiet
)
echo       Flask ready.

REM Step 3: Always rebuild database fresh
echo [3/4] Rebuilding database...
if exist tribute_lands_npcs.db (
    del tribute_lands_npcs.db >nul 2>&1
)
echo.
python seed_data.py
if errorlevel 1 (
    color 0C
    echo.
    echo ========================================
    echo   ERROR: Database build failed!
    echo   See error message above.
    echo ========================================
    echo.
    pause
    exit /b 1
)
echo.
echo       Database rebuilt with latest data.

REM Step 4: Start server
echo [4/4] Starting server...
echo.
echo ========================================
echo   SERVER RUNNING
echo   Open: http://127.0.0.1:5000
echo ========================================
echo.
echo Press Ctrl+C to stop the server.
echo.

python app.py
