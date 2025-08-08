import os
import json
import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

if os.name == "nt":
    appdata = os.getenv("APPDATA")
    if not appdata:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror(
            "Environment Error",
            "The APPDATA environment variable is not set.\n"
            "Cannot locate Dalamud configuration.",
        )
        root.destroy()
        sys.exit(1)
    CONFIG_PATH = Path(appdata) / "XIVLauncher" / "dalamudConfig.json"
else:
    CONFIG_PATH = Path.home() / ".xlcore" / "dalamudConfig.json"

BACKUP_PATH = CONFIG_PATH.with_suffix(CONFIG_PATH.suffix + ".bak")

def load_config():
    """Ensure config exists and return current beta state and password."""
    if not CONFIG_PATH.exists():
        CONFIG_PATH.parent.mkdir(parents=True, exist_ok=True)
        config = {"DalamudBetaKind": "release", "DalamudBetaKey": ""}
        with CONFIG_PATH.open("w") as f:
            json.dump(config, f, indent=4)
    with CONFIG_PATH.open("r") as f:
        config = json.load(f)
    is_beta = config.get("DalamudBetaKind", "release") == "stg"
    password = config.get("DalamudBetaKey", "")
    return is_beta, password

def save_config(is_beta: bool, password: str):
    """Backup and write new config values."""
    if CONFIG_PATH.exists():
        with CONFIG_PATH.open("r") as f:
            current = json.load(f)
        with BACKUP_PATH.open("w") as f:
            json.dump(current, f, indent=4)
    config = {
        "DalamudBetaKind": "stg" if is_beta else "release",
        "DalamudBetaKey": password,
    }
    with CONFIG_PATH.open("w") as f:
        json.dump(config, f, indent=4)

def revert_backup():
    """Restore config from backup if it exists."""
    if BACKUP_PATH.exists():
        with BACKUP_PATH.open("r") as f:
            backup = json.load(f)
        with CONFIG_PATH.open("w") as f:
            json.dump(backup, f, indent=4)
