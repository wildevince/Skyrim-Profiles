"""
Assistant de premiere installation (tkinter).

Declenche si MyConfig.json est absent. Ecrit la config, initialise les dossiers
profils et ouvre l'interface principale via gui.entry.
"""

from __future__ import annotations

import json
import webbrowser
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

import tkinter as tk

from gui.paths import (
    CONFIG_PATH,
    EXAMPLE_CONFIG_PATH,
    INIT_SCRIPT,
    PROFILE_NAMES,
    README_PATH,
    ROOT,
)
from gui.ps import run_ps_script

PADDING = {"padx": 12, "pady": 6}


def default_target_root() -> str:
    """Chemin My Games le plus probable (Documents ou OneDrive)."""
    candidates = [
        Path.home() / "OneDrive" / "Documents" / "My Games" / "Skyrim Special Edition",
        Path.home() / "Documents" / "My Games" / "Skyrim Special Edition",
    ]
    for path in candidates:
        if path.is_dir():
            return str(path)
    return str(candidates[1])


def looks_like_skyrim_my_games(path: Path) -> bool:
    if not path.is_dir():
        return False
    if (path / "Skyrim.ini").is_file() or (path / "SkyrimPrefs.ini").is_file():
        return True
    if (path / "Saves").is_dir():
        return True
    return "skyrim special edition" in path.name.lower()


def write_my_config(profiles_root: str, target_root: str, active_profile: str) -> None:
    with EXAMPLE_CONFIG_PATH.open(encoding="utf-8-sig") as f:
        cfg = json.load(f)

    cfg["profilesRoot"] = profiles_root
    cfg["targetRoot"] = target_root
    cfg["backupRoot"] = "_Backups"
    cfg["active_version"] = active_profile
    cfg["last_switch"] = None
    cfg["last_backup"] = None
    cfg["versions"] = {
        "Solo": "profiles\\Solo",
        "Keizaal": "profiles\\Keizaal",
    }

    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


class SetupWizard(tk.Tk):
    """Assistant en cinq ecrans + initialisation finale."""

    STEP_COUNT = 5

    def __init__(self) -> None:
        super().__init__()
        self.title("Skyrim Profiles — configuration")
        self.minsize(480, 360)
        self.resizable(True, True)

        self.completed = False
        self.step_index = 0
        self.profiles_root = tk.StringVar(value=str(ROOT))
        self.profiles_root_editable = tk.BooleanVar(value=False)
        self.target_root = tk.StringVar(value=default_target_root())
        self.initial_profile = tk.StringVar(value="Solo")

        self._content = ttk.Frame(self)
        self._content.pack(fill="both", expand=True)

        self._nav = ttk.Frame(self)
        self._nav.pack(fill="x", side="bottom", **PADDING)

        self._profiles_root_entry: ttk.Entry | None = None
        self._show_step(0)

    def _clear_content(self) -> None:
        for child in self._content.winfo_children():
            child.destroy()

    def _clear_nav(self) -> None:
        for child in self._nav.winfo_children():
            child.destroy()

    def _show_step(self, index: int) -> None:
        self.step_index = index
        self._clear_content()
        self._clear_nav()

        builders = (
            self._render_welcome,
            self._render_profiles_root,
            self._render_target_root,
            self._render_initial_profile,
            self._render_summary,
        )
        builders[index]()

        if index > 0:
            ttk.Button(self._nav, text="Retour", command=self._prev).pack(side="left")
        else:
            ttk.Frame(self._nav).pack(side="left")

        if index < self.STEP_COUNT - 1:
            ttk.Button(self._nav, text="Suivant", command=self._next).pack(side="right")
        else:
            ttk.Button(self._nav, text="Terminer", command=self._finish).pack(side="right")

        if index == 0:
            ttk.Button(self._nav, text="Passer l'intro", command=self._next).pack(side="right", padx=(0, 8))

    def _prev(self) -> None:
        if self.step_index > 0:
            self._show_step(self.step_index - 1)

    def _next(self) -> None:
        if not self._validate_current():
            return
        if self.step_index < self.STEP_COUNT - 1:
            self._show_step(self.step_index + 1)

    def _validate_current(self) -> bool:
        if self.step_index == 1:
            root_path = Path(self.profiles_root.get().strip())
            if not root_path.is_dir():
                messagebox.showerror("Chemin invalide", f"Dossier introuvable :\n{root_path}")
                return False
        if self.step_index == 2:
            target = Path(self.target_root.get().strip())
            if not target:
                messagebox.showerror("Chemin requis", "Selectionnez le dossier My Games de Skyrim SE.")
                return False
            if not target.is_dir():
                if not messagebox.askyesno(
                    "Dossier absent",
                    f"Le dossier n'existe pas encore :\n{target}\n\nLe creer et continuer ?",
                ):
                    return False
            elif not looks_like_skyrim_my_games(target):
                if not messagebox.askyesno(
                    "Verifier le chemin",
                    "Ce dossier ne ressemble pas a un My Games Skyrim SE habituel "
                    "(pas de Skyrim.ini ni dossier Saves).\n\nContinuer quand meme ?",
                ):
                    return False
        return True

    def _render_welcome(self) -> None:
        ttk.Label(
            self._content,
            text="Bienvenue dans Skyrim Profiles",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w", **PADDING)

        text = (
            "Cet assistant configure les deux profils (Solo modde et Keizaal) "
            "pour basculer entre eux sans melanger vos sauvegardes.\n\n"
            "Antivirus : si le ZIP GitHub est bloque, preferez git clone "
            "(voir README). Ce projet ne contient pas de malware — scripts lisibles en clair.\n\n"
            "Prerequis : Python 3 avec tkinter, PowerShell et robocopy (Windows)."
        )
        ttk.Label(self._content, text=text, wraplength=440, justify="left").pack(anchor="w", **PADDING)
        ttk.Button(self._content, text="Ouvrir le README", command=self._open_readme).pack(anchor="w", **PADDING)

    def _open_readme(self) -> None:
        if README_PATH.is_file():
            webbrowser.open(README_PATH.as_uri())
        else:
            messagebox.showinfo("README", f"Fichier introuvable :\n{README_PATH}")

    def _render_profiles_root(self) -> None:
        ttk.Label(self._content, text="Racine du projet", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", **PADDING
        )
        ttk.Label(
            self._content,
            text="Dossier ou vous avez extrait ou clone Skyrim-Profiles (profilesRoot).",
            wraplength=440,
            justify="left",
        ).pack(anchor="w", **PADDING)

        entry = ttk.Entry(self._content, textvariable=self.profiles_root, width=56)
        entry.pack(fill="x", **PADDING)
        self._profiles_root_entry = entry

        def toggle_edit() -> None:
            state = "normal" if self.profiles_root_editable.get() else "readonly"
            entry.configure(state=state)

        ttk.Checkbutton(
            self._content,
            text="Modifier (avance)",
            variable=self.profiles_root_editable,
            command=toggle_edit,
        ).pack(anchor="w", padx=12)
        toggle_edit()

    def _render_target_root(self) -> None:
        ttk.Label(self._content, text="Dossier My Games", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", **PADDING
        )
        ttk.Label(
            self._content,
            text="Chemin vers Skyrim Special Edition dans Documents (ou OneDrive).",
            wraplength=440,
            justify="left",
        ).pack(anchor="w", **PADDING)

        row = ttk.Frame(self._content)
        row.pack(fill="x", **PADDING)
        ttk.Entry(row, textvariable=self.target_root).pack(side="left", fill="x", expand=True, padx=(0, 6))
        ttk.Button(row, text="Parcourir…", command=self._browse_target).pack(side="right")

    def _browse_target(self) -> None:
        initial = self.target_root.get().strip()
        initial_dir = initial if Path(initial).is_dir() else str(Path.home() / "Documents")
        chosen = filedialog.askdirectory(
            title="Selectionner My Games\\Skyrim Special Edition",
            initialdir=initial_dir,
        )
        if chosen:
            self.target_root.set(chosen)

    def _render_initial_profile(self) -> None:
        ttk.Label(
            self._content,
            text="Contenu actuel de My Games",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", **PADDING)
        ttk.Label(
            self._content,
            text="Quel profil correspond a ce qui est dans My Games en ce moment ?\n"
            "Ce contenu sera copie dans le dossier profil choisi. L'autre profil demarre vide.",
            wraplength=440,
            justify="left",
        ).pack(anchor="w", **PADDING)

        for label, value in (("Solo modde", "Solo"), ("Keizaal", "Keizaal")):
            ttk.Radiobutton(
                self._content,
                text=label,
                value=value,
                variable=self.initial_profile,
            ).pack(anchor="w", padx=24, pady=4)

    def _render_summary(self) -> None:
        profile = self.initial_profile.get()
        label = "Solo modde" if profile == "Solo" else "Keizaal"
        text = (
            f"Racine projet : {self.profiles_root.get()}\n"
            f"My Games cible : {self.target_root.get()}\n"
            f"Profil initial : {label} ({profile})\n\n"
            "A la validation :\n"
            "  - creation de MyConfig.json\n"
            "  - creation de profiles\\Solo et profiles\\Keizaal\n"
            f"  - copie de My Games vers profiles\\{profile}\n"
            "  - ouverture de l'interface de bascule"
        )
        ttk.Label(self._content, text="Recapitulatif", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", **PADDING
        )
        ttk.Label(self._content, text=text, wraplength=440, justify="left").pack(anchor="w", **PADDING)

    def _finish(self) -> None:
        if not self._validate_current():
            return

        profile = self.initial_profile.get()
        if profile not in PROFILE_NAMES:
            messagebox.showerror("Erreur", "Profil initial invalide.")
            return

        profiles_root = self.profiles_root.get().strip()
        target_root = self.target_root.get().strip()

        target_path = Path(target_root)
        if not target_path.is_dir():
            try:
                target_path.mkdir(parents=True, exist_ok=True)
            except OSError as exc:
                messagebox.showerror("Erreur", f"Impossible de creer le dossier cible :\n{exc}")
                return

        try:
            write_my_config(profiles_root, target_root, profile)
        except OSError as exc:
            messagebox.showerror("Erreur", f"Ecriture de MyConfig.json impossible :\n{exc}")
            return

        if not INIT_SCRIPT.is_file():
            messagebox.showerror("Erreur", f"Script introuvable :\n{INIT_SCRIPT}")
            CONFIG_PATH.unlink(missing_ok=True)
            return

        busy = ttk.Label(self, text="Initialisation en cours (copie des fichiers)…")
        busy.pack(pady=8)
        self.update_idletasks()

        ok, output = run_ps_script(INIT_SCRIPT, "-InitialProfile", profile)
        busy.destroy()

        if not ok:
            messagebox.showerror(
                "Echec de l'initialisation",
                output or "La copie initiale a echoue.",
            )
            CONFIG_PATH.unlink(missing_ok=True)
            return

        self.completed = True
        self.destroy()


def run_setup_wizard() -> bool:
    """Lance l'assistant. Retourne True si la configuration a reussi."""
    wizard = SetupWizard()
    wizard.mainloop()
    return wizard.completed
