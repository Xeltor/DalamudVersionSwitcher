import psutil

def is_ffxiv_running():
    """Check if the FFXIV process is currently running."""
    for proc in psutil.process_iter(["name"]):
        if proc.info["name"] == "ffxiv_dx11.exe":
            return True
    return False
