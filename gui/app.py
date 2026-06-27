"""
Skyrim Profiles — interface graphique minimale (tkinter).

Appelle scripts/Switch-SkyrimProfile.ps1 pour la bascule.
Lancement : double-clic sur Skyrim-Profiles.pyw a la racine du projet.
"""

from __future__ import annotations

import json
import sys
import tkinter as tk
from tkinter import messagebox, ttk

from gui.paths import CONFIG_PATH, SWITCH_SCRIPT
from gui.ps import run_ps_script


def load_config() -> dict:
    """Lit MyConfig.json (profil actif, chemins, liste des versions)."""
    with CONFIG_PATH.open(encoding="utf-8-sig") as f:
        return json.load(f)


def run_switch(profile: str) -> tuple[bool, str]:
    """Delegue la bascule au script PowerShell existant."""
    ok, output = run_ps_script(SWITCH_SCRIPT, "-Profile", profile)
    return ok, output


class SkyrimProfilesApp(tk.Tk):
    """Fenetre principale : etat, boutons de switch, journal des operations."""

    def __init__(self) -> None:
        super().__init__()
        self.title("Skyrim Profiles")
        self.minsize(420, 320)
        self._build_ui()
        self.refresh_status()

    def _build_ui(self) -> None:
        padding = {"padx": 12, "pady": 6}

        header = ttk.Label(self, text="Skyrim SE — Profile Switcher", font=("Segoe UI", 14, "bold"))
        header.pack(anchor="w", **padding)

        self.status_var = tk.StringVar(value="Chargement…")
        status_frame = ttk.LabelFrame(self, text="Etat")
        status_frame.pack(fill="x", **padding)

        ttk.Label(status_frame, textvariable=self.status_var, wraplength=380, justify="left").pack(
            anchor="w", padx=10, pady=8
        )

        actions = ttk.LabelFrame(self, text="Activer un profil")
        actions.pack(fill="x", **padding)

        btn_row = ttk.Frame(actions)
        btn_row.pack(fill="x", padx=10, pady=10)

        self.btn_solo = ttk.Button(btn_row, text="Solo modde", command=lambda: self.switch("Solo"))
        self.btn_solo.pack(side="left", expand=True, fill="x", padx=(0, 6))

        self.btn_keizaal = ttk.Button(btn_row, text="Keizaal", command=lambda: self.switch("Keizaal"))
        self.btn_keizaal.pack(side="left", expand=True, fill="x", padx=(6, 0))

        ttk.Button(self, text="Actualiser", command=self.refresh_status).pack(anchor="e", **padding)

        log_frame = ttk.LabelFrame(self, text="Journal")
        log_frame.pack(fill="both", expand=True, **padding)

        self.log = tk.Text(log_frame, height=8, wrap="word", state="disabled", font=("Consolas", 9))
        self.log.pack(fill="both", expand=True, padx=8, pady=8)

    def append_log(self, text: str) -> None:
        self.log.configure(state="normal")
        self.log.insert("end", text + "\n")
        self.log.see("end")
        self.log.configure(state="disabled")

    def refresh_status(self) -> None:
        try:
            cfg = load_config()
        except OSError as exc:
            self.status_var.set(f"Erreur lecture config : {exc}")
            return

        active = cfg.get("active_version") or "—"
        last = cfg.get("last_switch") or "jamais"
        profiles = ", ".join(cfg.get("versions", {}).keys())
        self.status_var.set(
            f"Profil actif : {active}\n"
            f"Dernier switch : {last}\n"
            f"Profils disponibles : {profiles}\n"
            f"Cible : {cfg.get('targetRoot', '—')}"
        )

    def set_busy(self, busy: bool) -> None:
        state = "disabled" if busy else "normal"
        self.btn_solo.configure(state=state)
        self.btn_keizaal.configure(state=state)

    def switch(self, profile: str) -> None:
        cfg = load_config()
        if cfg.get("active_version") == profile:
            if not messagebox.askyesno(
                "Profil deja actif",
                f"« {profile} » est deja le profil actif.\nRelancer le switch quand meme ?",
            ):
                return

        if not messagebox.askokcancel(
            "Confirmer",
            f"Activer le profil « {profile} » ?\n\nFermez Skyrim avant de continuer.",
        ):
            return

        self.set_busy(True)
        self.append_log(f"--- Switch vers {profile} ---")
        self.update_idletasks()

        ok, output = run_switch(profile)
        if output:
            self.append_log(output)

        self.set_busy(False)
        self.refresh_status()

        if ok:
            messagebox.showinfo("Termine", f"Profil « {profile} » active.")
        else:
            messagebox.showerror("Echec", output or "Le switch a echoue.")


def main() -> None:
    """Tests directs ; preferer gui.entry.main via Skyrim-Profiles.pyw."""
    if not SWITCH_SCRIPT.exists():
        messagebox.showerror("Erreur", f"Script introuvable :\n{SWITCH_SCRIPT}")
        sys.exit(1)

    app = SkyrimProfilesApp()
    app.mainloop()


if __name__ == "__main__":
    from gui.entry import main as entry_main

    entry_main()
