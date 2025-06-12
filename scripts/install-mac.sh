#!/bin/sh
# To be placed in the .zip release.
SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
cd "$SCRIPT_DIR"

if [ -f ~/Applications/PyCuts\ Config.app ]; then
    rm -rf ~/Applications/PyCuts\ Config.app
fi
mv -f "./PyCuts Config.app" ~/Applications/PyCuts\ Config.app
echo "Moved 'PyCuts Config.app' to ~/Applications/PyCuts Config.app"

mv -f ./PyCuts /usr/local/bin
