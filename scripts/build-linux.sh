#!/bin/sh
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

# venv
if [ ! -f "../.venv/bin/activate" ]; then
    "../mk-venv.sh"
fi
source "../.venv/bin/activate"

# build
pyinstaller ../main.py -n "PyCuts" --onefile --noconfirm \
--add-data "../PyCutsTrayIcon.png:./" \
--add-data "../PyCutsTrayIconMono.png:./"