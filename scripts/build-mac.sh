#!/bin/sh
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

# venv
if [ ! -f "../.venv/bin/activate" ]; then
    "./mk-venv.sh"
fi
source "../.venv/bin/activate"

# build
pyinstaller ../main.py -n "pycuts" --onefile --noconfirm \
--add-data "../icons/PyCutsTrayIcon.png:./" \
--add-data "../icons/PyCutsTrayIconMono.png:./"

# build config
pyinstaller ../ui.py -n "PyCuts Config" -w -i "../icons/PyCuts.icns" --noconfirm \
--add-data "../icons/PyCutsTrayIcon.png:./" \
--add-data "../icons/PyCutsTrayIconMono.png:./"

rm -rf "./dist/PyCuts Config"

cp -f "./dist/pycuts" /usr/local/bin
cp -rf "./dist/PyCuts Config.app" ~/Applications

echo "Built 'PyCuts' to /usr/local/bin/pycuts"
echo "Built 'PyCuts Config.app' to ~/Applications/PyCuts Config.app"