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