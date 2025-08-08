from pathlib import Path
import tkinter as tk

from .ui import DalamudVersionSwitcher


def main():
    root = tk.Tk()

    # Set application icon if available
    icon_path = Path(__file__).resolve().parent.parent / "icon_V6O_icon.ico"
    if icon_path.exists():
        root.iconbitmap(str(icon_path))

    app = DalamudVersionSwitcher(root)
    root.mainloop()


if __name__ == "__main__":
    main()
