import os
import json

CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "XIVLauncher", "dalamudConfig.json")
BACKUP_PATH = CONFIG_PATH + ".bak"

def load_config():
    """Ensure config exists and return current beta state and password."""
    if not os.path.exists(CONFIG_PATH):
        os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
        config = {"DalamudBetaKind": "release", "DalamudBetaKey": ""}
        with open(CONFIG_PATH, "w") as f:
            json.dump(config, f, indent=4)
    with open(CONFIG_PATH, "r") as f:
        config = json.load(f)
    is_beta = config.get("DalamudBetaKind", "release") == "stg"
    password = config.get("DalamudBetaKey", "")
    return is_beta, password

def save_config(is_beta: bool, password: str):
    """Backup and write new config values."""
    if os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "r") as f:
            current = json.load(f)
        with open(BACKUP_PATH, "w") as f:
            json.dump(current, f, indent=4)
    config = {
        "DalamudBetaKind": "stg" if is_beta else "release",
        "DalamudBetaKey": password,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=4)

def revert_backup():
    """Restore config from backup if it exists."""
    if os.path.exists(BACKUP_PATH):
        with open(BACKUP_PATH, "r") as f:
            backup = json.load(f)
        with open(CONFIG_PATH, "w") as f:
            json.dump(backup, f, indent=4)
