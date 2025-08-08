#!/usr/bin/env bash
set -e

pyinstaller --onefile --windowed --icon=icon_V6O_icon.ico --clean dalamud_switcher/__main__.py
