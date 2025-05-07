@echo off
:: to be placed in the zip release alongside mk-shortcuts.vbs
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

mkdir %LOCALAPPDATA%\\PyCuts
move ".\PyCuts.exe" "%LOCALAPPDATA%\PyCuts"
move ".\PyCuts Config.exe" "%LOCALAPPDATA%\PyCuts"
.\\mk-shortcuts.vbs