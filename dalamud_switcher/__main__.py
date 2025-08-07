import os
import tkinter as tk

from .ui import DalamudVersionSwitcher


def main():
    root = tk.Tk()

    # Set application icon if available
    icon_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "icon_V6O_icon.ico"))
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)

    app = DalamudVersionSwitcher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
