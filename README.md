# Dalamud Version Switcher

## Project Overview
Dalamud Version Switcher is a small Tkinter-based utility for Final Fantasy XIV that toggles Dalamud's beta mode by updating its configuration file. It offers a simple GUI for enabling or disabling beta mode and handles backups of the existing configuration.

## Prerequisites
- Python 3.9 or later
- `pip` for installing dependencies
- Access to the Dalamud configuration path used by XIVLauncher

## Installation
Install the required packages:

```bash
pip install -r requirements.txt
```

## Usage
### Launch the GUI
Run the module entry point to open the switcher window:

```bash
python -m dalamud_switcher
```

### Beta-mode behavior
- Checking **Enable Dalamud Beta** sets `DalamudBetaKind` to `stg` in `dalamudConfig.json` and requires a beta password.
- Unchecking it restores the `release` channel.
- The application must not be running Final Fantasy XIV when changes are applied.
- Configuration changes are backed up and automatically reverted on failure.

## Building / Packaging
Create a standalone executable with PyInstaller:

```bash
pyinstaller --onefile --windowed --icon=icon_V6O_icon.ico --clean dalamud_switcher/__main__.py
```

On Windows, the included batch script runs the same command inside a virtual environment:

```bat
build.bat
```

## Linux Build & Install

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the build script:

```bash
./build.sh
```

3. Install the binary:

Copy the executable from `dist/` to a directory on your PATH, for example:

```bash
cp dist/__main__ ~/.local/bin/dalamud-switcher
```

Ensure `~/.local/bin` is in your `PATH`.

> **Note**: Tkinter on Linux expects `.png` icons set via `iconphoto`. If the `.ico` icon does not display, convert it to `.png`.

