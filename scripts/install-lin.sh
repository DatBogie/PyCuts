#!/bin/sh
# To be placed in the .zip release.
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

mkdir -p ~/.local/share/PyCuts

mv -f ./PyCuts ~/.local/share/PyCuts/pycuts
mv -f "./PyCuts Config" ~/.local/share/PyCuts/config
mv -f "./PyCutsTrayIcon.png" ~/.local/share/PyCuts/icon.png
echo "Moved files"

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
