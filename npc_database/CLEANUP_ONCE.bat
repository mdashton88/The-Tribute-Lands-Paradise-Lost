@echo off
title NPC Database — One-Time Cleanup
echo.
echo   ══════════════════════════════════════
echo   ONE-TIME REPO CLEANUP
echo   Run this once, then delete this file.
echo   ══════════════════════════════════════
echo.

git rm -r --cached __pycache__ 2>nul
git rm --cached tribute_lands_npcs.db 2>nul
git rm --cached "START_NPC_DATABASE.bat - Shortcut.lnk" 2>nul
git add -A
git commit -m "Add .gitignore, remove cached files"
git push

echo.
echo   Done! You can delete this file now.
echo.
pause
