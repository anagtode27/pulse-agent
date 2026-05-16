#!/usr/bin/env bash
set -euo pipefail

# Check for invalid number of arguments
if [ "$#" -gt 1  ]; then
    echo "Error: Too many arguments. Script allows a maximum of 1 argument." >&2
    exit 1
fi

# If there's an argument, check that it's a positive integer
if [ "$#" -eq 1 ] && { [[ ! "$1" =~ ^[0-9]+$ ]] || [ "$1" -le 0 ]; }; then
    echo "Error: interval must be a positive integer, got '$1'" >&2
    exit 1
fi

cd "$(dirname "$0")"
./build.sh
echo "Executing binary..."
exec ./dist/pulse-agent "$@"