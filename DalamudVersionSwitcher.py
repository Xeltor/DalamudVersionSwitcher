import os
import json
import psutil
import tkinter as tk
from tkinter import messagebox

# Paths to config and backup
CONFIG_PATH = os.path.join(os.getenv("APPDATA"), "XIVLauncher", "dalamudConfig.json")
BACKUP_PATH = CONFIG_PATH + ".bak"


class DalamudVersionSwitcher:
    def __init__(self, root):
        self.root = root
        self.root.title("Dalamud Version Switcher")
        self.root.geometry("330x120")  # Fixed window size
        self.root.resizable(False, False)

        # UI variables
        self.beta_var = tk.BooleanVar()
        self.password_var = tk.StringVar()

        # Beta mode toggle checkbox
        tk.Checkbutton(
            root,
            text="Enable Dalamud Beta",
            variable=self.beta_var,
            command=self.toggle_beta,
            font=("Segoe UI", 10)
        ).pack(pady=(10, 0), anchor="w", padx=20)

        # Password field container
        self.password_frame = tk.Frame(root)
        tk.Label(
            self.password_frame,
            text="Password:",
            font=("Segoe UI", 10)
        ).pack(side="left", padx=(0, 5))

        self.password_entry = tk.Entry(
            self.password_frame,
            textvariable=self.password_var,
            width=30,
            font=("Segoe UI", 10)
        )
        self.password_entry.pack(side="left")

        # Apply button
        self.apply_btn = tk.Button(
            root,
            text="Apply",
            width=12,
            height=1,
            font=("Segoe UI", 10, "bold"),
            command=self.apply_changes
        )

        # Hide password field initially
        self.password_frame.pack_forget()
        self.apply_btn.pack(pady=(20, 0))

        # Load initial configuration state
        self.load_config()

    def toggle_beta(self):
        """Toggles the visibility of the password field based on beta mode."""
        if self.beta_var.get():
            self.password_frame.pack(pady=(10, 0), padx=20, anchor="w")
            self.apply_btn.pack_forget()
            self.apply_btn.pack(pady=(10, 0))
        else:
            self.password_frame.pack_forget()
            self.apply_btn.pack_forget()
            self.apply_btn.pack(pady=(20, 0))

    def load_config(self):
        """Reads existing config or creates a default one if missing."""
        if not os.path.exists(CONFIG_PATH):
            os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
            config = {
                "DalamudBetaKind": "release",
                "DalamudBetaKey": ""
            }
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)

        with open(CONFIG_PATH, "r") as f:
            config = json.load(f)

        # Update UI state based on config
        is_beta = config.get("DalamudBetaKind", "release") == "stg"
        password = config.get("DalamudBetaKey", "")

        self.beta_var.set(is_beta)
        self.password_var.set(password)
        self.toggle_beta()

    def apply_changes(self):
        """Validates inputs, updates config, and handles backup/revert if needed."""
        if self.beta_var.get() and not self.password_var.get().strip():
            messagebox.showwarning("Validation Error", "You must enter a password to enable beta mode.")
            return

        if self.is_ffxiv_running():
            messagebox.showerror("Error", "Final Fantasy XIV is currently running. Please close it before applying changes.")
            return

        try:
            # Backup current config
            if os.path.exists(CONFIG_PATH):
                with open(CONFIG_PATH, "r") as f:
                    config = json.load(f)
                with open(BACKUP_PATH, "w") as f:
                    json.dump(config, f, indent=4)
            else:
                config = {}

            # Update values
            config["DalamudBetaKind"] = "stg" if self.beta_var.get() else "release"
            config["DalamudBetaKey"] = self.password_var.get()

            # Save new config
            with open(CONFIG_PATH, "w") as f:
                json.dump(config, f, indent=4)

            messagebox.showinfo("Success", f"Beta mode has been {'enabled' if self.beta_var.get() else 'disabled'} and settings saved.")

        except Exception as e:
            # Revert to backup if something fails
            if os.path.exists(BACKUP_PATH):
                with open(BACKUP_PATH, "r") as f:
                    backup = json.load(f)
                with open(CONFIG_PATH, "w") as f:
                    json.dump(backup, f, indent=4)

            messagebox.showerror("Error", f"Failed to save settings. Changes have been reverted.\nError: {e}")

    def is_ffxiv_running(self):
        """Checks if the FFXIV process is currently running."""
        for proc in psutil.process_iter(["name"]):
            if proc.info["name"] == "ffxiv_dx11.exe":
                return True
        return False


if __name__ == "__main__":
    root = tk.Tk()

    # Set application icon if available
    icon_path = os.path.join(os.path.dirname(__file__), "icon_V6O_icon.ico")
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    app = DalamudVersionSwitcher(root)
    root.mainloop()
