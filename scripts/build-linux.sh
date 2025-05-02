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
--add-data "../PyCutsTrayIcon.png:./" \
--add-data "../PyCutsTrayIconMono.png:./"

# build config
pyinstaller ../ui.py -n "PyCuts Config" --onefile --noconfirm \
--add-data "../PyCutsTrayIcon.png:./" \
--add-data "../PyCutsTrayIconMono.png:./"

# make .local/share folder
mkdir -p ~/.local/share/PyCuts

# copy files
cp "./dist/PyCuts" ~/.local/share/PyCuts/pycuts
cp "./dist/PyCuts Config" ~/.local/share/PyCuts/config
cp "../PyCutsTrayIcon.png" ~/.local/share/PyCuts/icon.png

# write .dekstop main
echo """[Desktop Entry]
Type=Application
Name=PyCuts
Icon=~/.local/share/PyCuts/icon.png
Exec=~/.local/share/PyCuts/pycuts
Comment=Global Keyboard Shortcuts Service
Categories=Utility;
Terminal=false""" > ~/.local/share/PyCuts/PyCuts.desktop

# write .dekstop config
echo """[Desktop Entry]
Type=Application
Name=PyCuts Config
Icon=~/.local/share/PyCuts/icon.png
Exec=~/.local/share/PyCuts/config
Comment=Graphical Global Keyboard Shortcuts Manager
Categories=Settings;DesktopSettings;Qt;
Terminal=false""" > ~/.local/share/PyCuts/PyCuts\ Config.desktop