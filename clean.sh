#!/usr/bin/env bash
set -euo pipefail

echo "Cleaning build artifacts..."
rm -rf venv dist build __pycache__ *.spec *.pyc