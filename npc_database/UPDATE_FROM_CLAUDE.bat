@echo off
title NPC Database — Update from Claude
echo.
echo   ══════════════════════════════════════
echo   UPDATE FROM CLAUDE
echo   ══════════════════════════════════════
echo.

set "DL=%USERPROFILE%\Downloads"
set "DB=%~dp0"
set FOUND=0

:: ── Recognised app files ──
for %%F in (app.py seed_data.py npc_manager.py fg_export.py equipment_catalogue.py schema.sql canon_corrections.py) do (
    if exist "%DL%\%%F" (
        echo   [COPY] %%F
        copy /Y "%DL%\%%F" "%DB%\%%F" >nul
        del "%DL%\%%F"
        set FOUND=1
    )
)

:: ── Recognised module files (edges, hindrances, powers, equipment) ──
for %%D in (edges hindrances powers equipment) do (
    for %%F in ("%DL%\%%D\*.py" "%DL%\%%D_*.py") do (
        if exist "%%F" (
            echo   [COPY] %%~nxF
            copy /Y "%%F" "%DB%\%%D\%%~nxF" >nul
            del "%%F"
            set FOUND=1
        )
    )
)

:: ── Check for any .py or .sql files with (1), (2) etc suffixes (browser duplicates) ──
for %%F in ("%DL%\app (*.py" "%DL%\seed_data (*.py" "%DL%\npc_manager (*.py" "%DL%\fg_export (*.py" "%DL%\equipment_catalogue (*.py" "%DL%\schema (*.sql") do (
    if exist "%%F" (
        echo   [WARN] Found duplicate-named download: %%~nxF
        echo          Please rename it manually and re-run.
        set FOUND=1
    )
)

:: ── Also grab any .bat updates (except this file) ──
for %%F in (START_NPC_DATABASE.bat SYNC_TO_GITHUB.bat) do (
    if exist "%DL%\%%F" (
        echo   [COPY] %%F
        copy /Y "%DL%\%%F" "%DB%\%%F" >nul
        del "%DL%\%%F"
        set FOUND=1
    )
)

:: ── Also grab .gitignore and README ──
for %%F in (.gitignore README.md) do (
    if exist "%DL%\%%F" (
        echo   [COPY] %%F
        copy /Y "%DL%\%%F" "%DB%\%%F" >nul
        del "%DL%\%%F"
        set FOUND=1
    )
)

echo.

if %FOUND%==0 (
    echo   No new files found in Downloads.
    echo   Download files from Claude first, then run this again.
    echo.
    pause
    exit /b
)

:: ── Pull, commit, push ──
echo   Syncing to GitHub...
echo.
git pull --ff-only 2>nul
git add -A
git status --short
echo.

set /p MSG="  Describe what changed (or just press Enter): "
if "%MSG%"=="" set MSG=Update from Claude session

git commit -m "%MSG%"
git push

echo.
echo   ══════════════════════════════════════
echo   Done! Files updated and synced.
echo   ══════════════════════════════════════
echo.
pause
