import tkinter as tk
from tkinter import messagebox

from . import config, process


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
            font=("Segoe UI", 10),
        ).pack(pady=(10, 0), anchor="w", padx=20)

        # Password field container
        self.password_frame = tk.Frame(root)
        tk.Label(
            self.password_frame,
            text="Password:",
            font=("Segoe UI", 10),
        ).pack(side="left", padx=(0, 5))

        self.password_entry = tk.Entry(
            self.password_frame,
            textvariable=self.password_var,
            width=30,
            font=("Segoe UI", 10),
        )
        self.password_entry.pack(side="left")

        # Apply button
        self.apply_btn = tk.Button(
            root,
            text="Apply",
            width=12,
            height=1,
            font=("Segoe UI", 10, "bold"),
            command=self.apply_changes,
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
        is_beta, password = config.load_config()
        self.beta_var.set(is_beta)
        self.password_var.set(password)
        self.toggle_beta()

    def apply_changes(self):
        """Validates inputs, updates config, and handles backup/revert if needed."""
        if self.beta_var.get() and not self.password_var.get().strip():
            messagebox.showwarning(
                "Validation Error", "You must enter a password to enable beta mode."
            )
            return

        if process.is_ffxiv_running():
            messagebox.showerror(
                "Error",
                "Final Fantasy XIV is currently running. Please close it before applying changes.",
            )
            return

        try:
            config.save_config(self.beta_var.get(), self.password_var.get())
            messagebox.showinfo(
                "Success",
                f"Beta mode has been {'enabled' if self.beta_var.get() else 'disabled'} and settings saved.",
            )
        except Exception as e:
            config.revert_backup()
            messagebox.showerror(
                "Error",
                f"Failed to save settings. Changes have been reverted.\nError: {e}",
            )
