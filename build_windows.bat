@echo off
setlocal
chcp 65001 >nul

REM ============================================================
REM  MIB2 Converter v2.0 - build script (Windows)
REM  Result: dist\MIB2_Converter_v2.exe
REM ============================================================

cd /d "%~dp0"

echo [1/4] Installing dependencies...
python -m pip install --upgrade pip
python -m pip install PySide6 pyinstaller
if errorlevel 1 (
    echo ERROR: pip install failed
    pause
    exit /b 1
)

echo [2/4] Cleaning old build artifacts...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist
if exist MIB2_Converter_v2.spec del /q MIB2_Converter_v2.spec

echo [3/4] Building exe...
python -m PyInstaller ^
    --onefile ^
    --windowed ^
    --icon=icon.ico ^
    --name "MIB2_Converter_v2" ^
    --add-data "icon.ico;." ^
    --add-data "free-icon-russia-555451.png;." ^
    --add-data "free-icon-united-states-206626.png;." ^
    mibcongui_v2.py
if errorlevel 1 (
    echo ERROR: build failed
    pause
    exit /b 1
)

echo [4/4] Done.
echo Artifact: %cd%\dist\MIB2_Converter_v2.exe
echo.
echo Smoke-test before release:
echo   1. Run dist\MIB2_Converter_v2.exe
echo   2. Convert: variant 17214 + ZR metainfo + HWID 36
echo   3. Special - Links replacement only
echo   4. Special - HMI ZR-PQ patches - Future date patch
echo.
pause
