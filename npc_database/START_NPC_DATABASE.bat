@echo off
title Tribute Lands NPC Database
echo.
echo   Tribute Lands NPC Database
echo   DiceForge Studios Ltd
echo.
echo   Checking requirements...

python -m pip install flask >nul 2>&1
if errorlevel 1 (
    echo   Installing Flask...
    python -m pip install flask
)

echo   Starting server...
echo   Your browser will open automatically.
echo   Close this window to stop the server.
echo.

python app.py

pause
