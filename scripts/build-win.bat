@echo off
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

:: venv
IF NOT EXIST "..\.venv\Scripts\activate.bat" (
    call ".\mk-venv.bat"
)
call "..\.venv\Scripts\activate.bat"

:: build
pyinstaller ..\main.py -n "PyCuts" -w -i "..\PyCuts.ico" --noconfirm ^
    --add-data "..\PyCutsTrayIcon.png;." ^
    --add-data "..\PyCutsTrayIconMono.png;."

:: build config
pyinstaller ..\ui.py -n "PyCuts Config" -w -i "..\PyCuts.ico" --noconfirm ^
    --add-data "..\PyCutsTrayIcon.png;." ^
    --add-data "..\PyCutsTrayIconMono.png;."

:: create shortcuts
mklink "%APPDATA%\Microsoft\Windows\Start Menu\Programs\PyCuts.lnk" ".\dist\PyCuts\PyCuts.exe"
mklink "%APPDATA%\Microsoft\Windows\Start Menu\Programs\PyCuts Config.lnk" ".\dist\PyCuts\PyCuts Config.exe"