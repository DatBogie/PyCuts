@echo off
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%
SET SCRIPT_DIR_UP=%SCRIPT_DIR%\\..

:: venv
IF NOT EXIST ..\\.venv\\Scripts\\activate.bat (
    call .\\mk-venv.bat
)
call ..\\.venv\\Scripts\\activate.bat

:: build
pyinstaller %SCRIPT_DIR_UP%\\main.py -n "PyCuts" -w --onefile -i %SCRIPT_DIR_UP%\\icons\\PyCuts.ico --noconfirm ^
    --add-data ..\\icons\\PyCutsTrayIcon.png;. ^
    --add-data ..\\icons\\PyCutsTrayIconMono.png;.

:: build config
pyinstaller %SCRIPT_DIR_UP%\\ui.py -n "PyCuts Config" -w --onefile -i %SCRIPT_DIR_UP%\\icons\\PyCuts.ico --noconfirm ^
    --add-data %SCRIPT_DIR_UP%\\icons\\PyCutsTrayIcon.png;. ^
    --add-data %SCRIPT_DIR_UP%\\icons\\PyCutsTrayIconMono.png;.

:: install / create shortcuts
mkdir %LOCALAPPDATA%\\PyCuts
xcopy ".\\dist\\PyCuts.exe" "%LOCALAPPDATA%\\PyCuts"
xcopy ".\\dist\\PyCuts Config.exe" "%LOCALAPPDATA%\\PyCuts"
.\\mk-shortcuts.vbs
