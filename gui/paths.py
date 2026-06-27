"""Chemins stables du depot (independants du CWD)."""

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CONFIG_PATH = ROOT / "MyConfig.json"
EXAMPLE_CONFIG_PATH = ROOT / "MyConfig.example.json"
README_PATH = ROOT / "README.md"
SWITCH_SCRIPT = ROOT / "scripts" / "Switch-SkyrimProfile.ps1"
INIT_SCRIPT = ROOT / "scripts" / "Initialize-SkyrimProfiles.ps1"

PROFILE_NAMES = ("Solo", "Keizaal")
