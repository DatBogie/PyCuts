#!/bin/sh
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

# venv
if [ ! -f "../.venv/bin/activate" ]; then
    "./mk-venv.sh"
fi
source "../.venv/bin/activate"

# build
pyinstaller ../main.py -n "PyCuts" --onefile --noconfirm \
--add-data "../icons/PyCutsTrayIcon.png:./" \
--add-data "../icons/PyCutsTrayIconMono.png:./"

# build config
pyinstaller ../ui.py -n "PyCuts Config" -w -i "../icons/PyCuts.icns" --noconfirm \
--add-data "../icons/PyCutsTrayIcon.png:./" \
--add-data "../icons/PyCutsTrayIconMono.png:./"

rm -rf "./dist/PyCuts Config"

cp -f "./dist/PyCuts" /usr/local/bin
cp -f "./dist/PyCuts Config.app" ~/Applications

echo "Built 'PyCuts' to PyCuts/scripts/dist/PyCuts"
echo "Built 'PyCuts Config.app' to ~/Applications/PyCuts Config.app"