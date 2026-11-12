#!/usr/bin/env bash
# Build a standalone executable with PyInstaller.
# Output: dist/BankApp (one-folder) or dist/BankApp.app on macOS.
set -e

pip install -r requirements.txt

pyinstaller \
  --name BankApp \
  --onefile \
  --windowed \
  --clean \
  --noconfirm \
  bank_app.py

echo "Build complete. See the dist/ folder."