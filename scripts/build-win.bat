@echo off
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

:: venv
IF NOT EXIST ..\\.venv\\Scripts\\activate.bat (
    call .\\mk-venv.bat
)
call ..\\.venv\\Scripts\\activate.bat

:: build
pyinstaller ..\\main.py -n "PyCuts" -w --onefile -i ..\\icons\\PyCuts.ico --noconfirm ^
    --add-data ..\\icons\\PyCutsTrayIcon.png;. ^
    --add-data ..\\icons\\PyCutsTrayIconMono.png;.

:: build config
pyinstaller ..\\ui.py -n "PyCuts Config" -w --onefile -i ..\\PyCuts.ico --noconfirm ^
    --add-data ..\\icons\\PyCutsTrayIcon.png;. ^
    --add-data ..\\icons\\PyCutsTrayIconMono.png;.

:: install / create shortcuts
mkdir %LOCALAPPDATA%\\PyCuts
xcopy ".\\dist\\PyCuts.exe" "%LOCALAPPDATA%\\PyCuts"
xcopy ".\\dist\\PyCuts Config.exe" "%LOCALAPPDATA%\\PyCuts"
.\\mk-shortcuts.vbs
