@echo off
SET SCRIPT_DIR=%~dp0
cd /d %SCRIPT_DIR%

python -m venv "..\\.venv"
call "..\\.venv\\Scripts\\activate.bat"
pip install -r "..\\requirements.txt"