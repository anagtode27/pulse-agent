#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"
./build.sh
echo "Running binary..."
exec ./dist/pulse-agent "$@"