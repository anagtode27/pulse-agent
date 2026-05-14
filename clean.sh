#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")"

echo "Cleaning build artifacts..."
rm -rf venv dist build __pycache__ *.spec *.pyc