# Skyrim-Profiles

Gestion de **deux usages de Skyrim SE** sur la même machine — **pas plus de deux profils** par conception (ex. Keizaal Online + solo moddé), sans mélange de configuration, sauvegardes ni fichiers SKSE.

> **Open source (MIT)** — publié sur GitHub (bientôt). Libre d'utiliser, modifier et partager. Voir [LICENSE](LICENSE) et [docs/GUIDE-INSTALLATION.md](docs/GUIDE-INSTALLATION.md).

## Première installation

1. Copier `MyConfig.example.json` → `MyConfig.json`
2. Remplir les chemins (voir le [guide d'installation](docs/GUIDE-INSTALLATION.md))
3. Créer `profiles\` pour tes deux usages
4. Lancer `Skyrim-Profiles.vbs`

## Principe

Skyrim lit ses données utilisateur depuis un dossier **unique** :

```
Documents\My Games\Skyrim Special Edition\
```

Ce projet y déploie, au moment du lancement, le contenu du **profil actif** stocké dans `profiles\`.

## Structure du dépôt

```
Skyrim-Profiles/
├── Skyrim-Profiles.vbs           # Lanceur principal (GUI, sans console)
├── Skyrim-Profiles.bat           # Lanceur alternatif (GUI)
├── MyConfig.json                 # Ta config locale (non versionnee)
├── MyConfig.example.json         # Modele a copier
├── profiles/
│   ├── Keizaal/                  # Miroir My Games — Keizaal
│   └── Solo/                     # Miroir My Games — solo moddé
├── scripts/
│   ├── Switch-SkyrimProfile.ps1  # Point d'entrée PowerShell
│   └── ProfileSwitcher.psm1      # Logique de bascule (module)
├── gui/
│   └── app.py                    # Interface tkinter
├── launchers/                    # Scripts .bat (gui, switch CLI)
├── docs/                         # Documentation / rapports
└── _Backups/                     # Backups horodatés (non versionnés)
```

## Utilisation

### Interface graphique (recommandé)

1. Fermer Skyrim.
2. Double-clic sur **`Skyrim-Profiles.vbs`** (ou `Skyrim-Profiles.bat`).
3. Choisir le profil, confirmer, lancer le jeu via le bon launcher.

### Ligne de commande (sans GUI)

```bat
launchers\Activer-Keizaal.bat
launchers\Activer-Solo.bat
```

```powershell
.\scripts\Switch-SkyrimProfile.ps1 -Profile Solo
.\scripts\Switch-SkyrimProfile.ps1 -Status
```

## Configuration

Copie **`MyConfig.example.json`** en **`MyConfig.json`** et adapte les chemins.

Guide détaillé : **[docs/GUIDE-INSTALLATION.md](docs/GUIDE-INSTALLATION.md)**

```json
{
    "profilesRoot": "E:\\...\\Skyrim-Profiles",
    "targetRoot": "C:\\Users\\<toi>\\Documents\\My Games\\Skyrim Special Edition",
    "backupRoot": "_Backups",
    "active_version": null,
    "versions": {
        "Solo": "profiles\\Solo",
        "Keizaal": "profiles\\Keizaal"
    }
}
```

| Champ | Description |
|-------|-------------|
| `profilesRoot` | Racine du dépôt |
| `targetRoot` | Dossier `My Games` lu par Skyrim |
| `active_version` | Profil actuellement déployé |
| `versions` | Nom du profil → sous-dossier dans `profiles\` |

## Flux de bascule

1. Sauvegarde de `My Games` vers le profil actuellement actif
2. Backup horodaté dans `_Backups\`
3. Déploiement miroir du profil cible → `My Games`
4. Mise à jour de `MyConfig.json`

## Prérequis

- Deux **installs de jeu séparées** (Keizaal vs Steam solo)
- PowerShell + robocopy (inclus Windows)
- Python 3 + tkinter pour la GUI (`Skyrim-Profiles.vbs`)

## Git

`MyConfig.json` et `profiles/` sont ignorés — chaque utilisateur garde sa config locale. Le dépôt fournit `MyConfig.example.json` comme modèle.

```gitignore
MyConfig.json
_Backups/
profiles/*
```

## Points d'attention

- Fermer Skyrim avant tout switch
- OneDrive sur `targetRoot` : attendre la fin de la synchro si erreur de copie
- Purger `_Backups\` manuellement si l'espace manque

Voir `gui/README.md` pour les options d'interface (tkinter, CustomTkinter, etc.).

## Licence

[MIT](LICENSE) — libre d'utiliser, modifier et redistribuer.
