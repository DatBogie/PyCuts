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
pyinstaller ../ui.py -n "PyCuts Config" --onefile --noconfirm \
--add-data "../icons/PyCutsTrayIcon.png:./" \
--add-data "../icons/PyCutsTrayIconMono.png:./"

# make .local/share folder
mkdir -p ~/.local/share/PyCuts

# copy files
cp -f "./dist/PyCuts" ~/.local/share/PyCuts/pycuts
cp -f "./dist/PyCuts Config" ~/.local/share/PyCuts/config
cp -f "../icons/PyCutsTrayIcon.png" ~/.local/share/PyCuts/icon.png
echo "Copied resources to ~/.local/share/PyCuts"

# write .dekstop main
echo """[Desktop Entry]
Type=Application
Name=PyCuts
Icon=/home/$USER/.local/share/PyCuts/icon.png
Exec=/home/$USER/.local/share/PyCuts/pycuts
Comment=Global Keyboard Shortcuts Service
Categories=Utility;
Terminal=false""" > ~/.local/share/applications/PyCuts.desktop

# write .dekstop config
echo """[Desktop Entry]
Type=Application
Name=PyCuts Config
Icon=/home/$USER/.local/share/PyCuts/icon.png
Exec=/home/$USER/.local/share/PyCuts/config
Comment=Graphical Global Keyboard Shortcuts Manager
Categories=Settings;DesktopSettings;Qt;
Terminal=false""" > ~/.local/share/applications/PyCuts\ Config.desktop

echo "Installed 'PyCuts' and 'PyCuts Config' .desktop files to ~/.local/share/applications"