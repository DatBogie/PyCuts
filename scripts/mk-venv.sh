#!/bin/sh
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

python3 -m venv ../.venv
source ../.venv/bin/activate
pip3 install -r "../requirements.txt"
