@echo off
title NPC Database — Sync to GitHub
echo.
echo   ══════════════════════════════════════
echo   SYNC TO GITHUB
echo   Pushes any changed files to the repo.
echo   ══════════════════════════════════════
echo.

:: Pull any remote changes first
echo   Pulling latest...
git pull --ff-only 2>nul
echo.

:: Stage everything, commit, push
git add -A
git status --short
echo.

set /p MSG="  Describe what changed (or just press Enter): "
if "%MSG%"=="" set MSG=Update from Claude session

git commit -m "%MSG%"
git push

echo.
echo   ══════════════════════════════════════
echo   Done! Changes are live on GitHub.
echo   ══════════════════════════════════════
echo.
pause
