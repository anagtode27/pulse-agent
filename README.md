Lightweight Python telemetry agent that collects system metrics and forwards them to the Pulse API.

## Project structure:

- agent.py: Handles metric collection and sends that data to the Pulse API
- build.sh: Creates a new venv, installs all dependencies, and uses PyInstaller to produce the binary.
- clean.sh: Cleans all build artifacts, called at the beginning of build.sh
- run.sh: Calls build.sh and executes the binary.

## Requirements to build the binary:

- Python or Python3

## Requirements to run the binary:

- None! PyInstaller takes care of not having Python installed.

## Usage:

- `./run.sh <optional positive integer. The amount of seconds between each log report. Defaults to 2s.>`

#### If choosing to build and run the binary:

- `git clone`
- `cd pulse-agent`
- `./run.sh`
- If running into permission error, run `chmod +x clean.sh build.sh run.sh` in the root directory of the project

#### If choosing to download and run the binary:

- Download the latest release binary, and execute it. No custom interval can be provided - defaults to 2s.

## Metrics collected:

- Stuff

#### TODO: