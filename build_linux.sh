#!/usr/bin/env bash
# ============================================================
#  MIB2 Converter v2.0 - build script (Linux)
#  Result: dist/MIB2_Converter_v2
#  Note: Linux build has no --windowed console suppression
#        difference; the app itself is GUI (PySide6).
# ============================================================
set -e
cd "$(dirname "$0")"

echo "[1/3] Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install PySide6 pyinstaller

echo "[2/3] Cleaning old build artifacts..."
rm -rf build dist MIB2_Converter_v2.spec

echo "[3/3] Building binary..."
python3 -m PyInstaller \
    --onefile \
    --windowed \
    --icon=icon.ico \
    --name "MIB2_Converter_v2" \
    --add-data "icon.ico:." \
    --add-data "free-icon-russia-555451.png:." \
    --add-data "free-icon-united-states-206626.png:." \
    mibcongui_v2.py

echo "Done. Artifact: $(pwd)/dist/MIB2_Converter_v2"
