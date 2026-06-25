# Interface graphique

## Lancement

Double-clic sur **`Skyrim-Profiles.vbs`** à la racine du projet (recommandé, sans console).

Ou :

```bash
python3 gui/app.py
# ou : python gui/app.py
```

Scripts `.bat` détaillés dans `launchers/` (voir `launchers/README.md`).

## Technologie : tkinter (choix actuel)

| Option | Avantages | Inconvénients |
|--------|-----------|---------------|
| **tkinter** (actuel) | Inclus avec Python Windows, zéro dépendance, léger | Look basique |
| **CustomTkinter** | UI moderne, dark mode | `pip install customtkinter` |
| **PySide6 / PyQt** | UI riche, professionnelle | Lourd, grosse dépendance |
| **PowerShell WinForms** | Pas de Python, 100 % Windows | Moins flexible, code verbeux |

**Recommandation :** rester sur tkinter pour un outil perso à 2 boutons. Passer à CustomTkinter si tu veux un rendu plus soigné sans complexifier le déploiement.

## Architecture

```
gui/app.py  ──subprocess──▶  scripts/Switch-SkyrimProfile.ps1
                                    │
                                    ▼
                            ProfileSwitcher.psm1
```

La logique métier reste en PowerShell ; Python ne fait que l'affichage et la confirmation.

## Évolutions possibles

- Indicateur visuel du profil actif (bouton désactivé / surbrillance)
- Bouton « Ouvrir My Games » / « Ouvrir dossier profil »
- Liste des backups récents avec restauration
- Thème sombre via CustomTkinter
