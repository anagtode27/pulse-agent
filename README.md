Lightweight Python telemetry agent that collects system metrics and forwards them to the Pulse API.

Project structure:

- agent.py: handles all CLI and metric collection
- build.sh: A script that creates a venv, installs all dependencies, and uses PyInstaller to produce the binary. The build user needs to have python or python3 installed. Python is not required to run.
- run.sh: A simple script that combines build.sh and executing the binary. 


Requirements to build the binary:

- Python or Python3

Requirements to run the binary:

- None! PyInstaller takes care of not having Python installed.



How to run:

If choosing to build and run the binary:

- git clone <repo>
- cd <repo>
- ./run.sh (run chmod +x run.sh build.sh if permission denied)

If choosing to download and run the binary:

- Download the latest release binary, and execute it.

Metrics collected:

- Stuff

Usage:

- ./run.sh <optional: interval, in seconds. Defaults to 5s>




