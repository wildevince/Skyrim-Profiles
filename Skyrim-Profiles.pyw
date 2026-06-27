"""Lanceur double-clic (sans fenetre console)."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from gui.entry import main

if __name__ == "__main__":
    main()
