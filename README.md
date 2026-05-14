# Lightweight Python telemetry agent that collects system metrics and forwards them to the Pulse API.

## Project structure:

- agent.py: Handles all CLI and metric collection
- build.sh: A script that creates a new venv, installs all dependencies, and uses PyInstaller to produce the binary. The build user needs to have python or python3 installed. End users do not need python to run
- clean.sh: A simple script to clean all build artifacts. Called at the start of build.sh.
- run.sh: A simple script that combines build.sh and executing the binary. 

##Requirements to build the binary:

- Python or Python3

## Requirements to run the binary:

- None! PyInstaller takes care of not having Python installed.

## Usage:

- ./run.sh <optional: positive integer, interval. The amount of seconds between each log report. Defaults to 2s.>

### If choosing to build and run the binary:

- git clone <repo>
- cd <repo>
- ./run.sh (run chmod +x run.sh build.sh if permission denied)
- See "Usage" section below

### If choosing to download and run the binary:

- Download the latest release binary, and execute it. No custom interval can be provided - defaults to 2s.

## Metrics collected:

- Stuff






