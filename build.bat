@echo off
chcp 65001 >nul
title Building Skill Manager...
echo.
echo  ============================================
echo   Skill Manager - Building executable...
echo  ============================================
echo.

REM Check PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo  Installing PyInstaller...
    pip install pyinstaller -q
)

echo  Building with PyInstaller...
pyinstaller --noconfirm --onefile --windowed ^
    --name "SkillManager" ^
    --hidden-import yaml ^
    --hidden-import requests ^
    --hidden-import customtkinter ^
    --collect-submodules customtkinter ^
    --clean ^
    main.py

if errorlevel 1 (
    echo.
    echo  [ERROR] Build failed!
    pause
    exit /b 1
)

echo.
echo  ============================================
echo   Build complete!
echo   Output: dist\SkillManager.exe
echo  ============================================
echo.
pause
