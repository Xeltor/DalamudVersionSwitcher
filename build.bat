@echo off
setlocal

REM Define virtual environment folder
set VENV_DIR=.venv

REM Check if venv exists
if not exist %VENV_DIR%\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv %VENV_DIR%
)

REM Activate virtual environment
call %VENV_DIR%\Scripts\activate.bat

REM Install requirements if needed
echo Installing/updating requirements...
pip install --upgrade pip >nul
pip install -r requirements.txt

REM Run PyInstaller
echo Building with PyInstaller...
pyinstaller --onefile --windowed --icon=icon_V6O_icon.ico --clean DalamudVersionSwitcher.py

REM Done
echo Build complete!
pause
endlocal
