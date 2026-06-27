"""Point d'entree GUI : assistant si besoin, puis interface principale."""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gui.paths import CONFIG_PATH


def main() -> None:
    try:
        import tkinter as tk
        from tkinter import messagebox
    except ImportError:
        print("tkinter est requis. Reinstallez Python en cochant tcl/tk.", file=sys.stderr)
        sys.exit(1)

    if not CONFIG_PATH.is_file():
        from gui.wizard import run_setup_wizard

        if not run_setup_wizard():
            sys.exit(0)

    from gui.app import SkyrimProfilesApp

    if not CONFIG_PATH.is_file():
        messagebox.showerror("Configuration", "MyConfig.json introuvable apres l'assistant.")
        sys.exit(1)

    app = SkyrimProfilesApp()
    app.mainloop()


if __name__ == "__main__":
    main()
