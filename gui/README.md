# Interface graphique

## Lancement

Double-clic sur **`Skyrim-Profiles.pyw`** à la racine du projet (recommandé, sans console).

Ou en ligne de commande depuis la racine du dépôt :

```bash
python Skyrim-Profiles.pyw
# ou : python -m gui.entry
```

**Première installation :** si `MyConfig.json` est absent, un assistant tkinter guide la configuration (chemins, profil initial), puis ouvre l’interface de bascule.

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
Skyrim-Profiles.pyw
       │
       ├─ MyConfig.json absent? → gui/wizard.py (assistant)
       └─ sinon                 → gui/app.py (switch)
                                        │
                                        ▼ subprocess
                            scripts/Switch-SkyrimProfile.ps1
                                        │
                                        ▼
                            ProfileSwitcher.psm1
```

La logique métier reste en PowerShell ; Python gère l’onboarding, l’affichage et la confirmation.

## Évolutions possibles

- Indicateur visuel du profil actif (bouton désactivé / surbrillance)
- Bouton « Ouvrir My Games » / « Ouvrir dossier profil »
- Liste des backups récents avec restauration
- Thème sombre via CustomTkinter
