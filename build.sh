#!/usr/bin/env bash

# Safety flags in case the script errors out
set -euo pipefail

# Clean all prev. build artifacts
./clean.sh
echo "Done."

# Check for either python3 or python in the PATH
if command -v python3 >/dev/null 2>&1; then
  PYTHON=python3
elif command -v python >/dev/null 2>&1; then
  PYTHON=python
else
  echo "Python 3 not found. Install Python first." >&2
  exit 1
fi

# Create a fresh virtual environment if python exists
echo "Creating virtual environment..."
rm -rf venv
$PYTHON -m venv venv
source venv/bin/activate
echo "Done."

# Install dependencies into the venv
echo "Installing dependencies..."
pip install -r requirements.txt
echo "Done."

# Build the executable
echo "Building pulse-agent..."
$PYTHON -m PyInstaller --onefile agent.py --name pulse-agent