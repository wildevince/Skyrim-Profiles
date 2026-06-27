"""Invocation des scripts PowerShell du projet."""

from __future__ import annotations

import subprocess
from pathlib import Path

from gui.paths import ROOT


def run_ps_script(script: Path, *args: str) -> tuple[bool, str]:
    cmd = [
        "powershell",
        "-NoProfile",
        "-ExecutionPolicy",
        "Bypass",
        "-File",
        str(script),
        *args,
    ]
    result = subprocess.run(
        cmd,
        cwd=ROOT,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = (result.stdout or "") + (result.stderr or "")
    return result.returncode == 0, output.strip()
