# Skyrim-Profiles

Gestion de **deux usages de Skyrim SE** sur la même machine — **pas plus de deux profils** par conception (ex. Keizaal Online + solo moddé), sans mélange de configuration, sauvegardes ni fichiers SKSE.

> **Open source (MIT)** — publié sur GitHub (bientôt). Libre d'utiliser, modifier et partager. Voir [LICENSE](LICENSE) et [docs/GUIDE-INSTALLATION.md](docs/GUIDE-INSTALLATION.md).

> **Antivirus / faux positifs** — Windows Defender et d'autres AV bloquent parfois le **ZIP GitHub** à tort (scripts non signés). **Ce n'est pas un malware** : tout le code est lisible en clair. Voir le [guide antivirus](docs/GUIDE-INSTALLATION.md#antivirus-et-téléchargement-github) pour débloquer ou installer autrement.

## Première installation

### Récupérer le projet (recommandé : `git clone`)

Le clone évite souvent le blocage du ZIP par l'antivirus :

```bat
git clone https://github.com/TON_USER/Skyrim-Profiles.git
cd Skyrim-Profiles
```

Alternative : télécharger le ZIP depuis une [release taguée](docs/GUIDE-INSTALLATION.md#releases-taguées-et-checksums-sha-256) (`v1.0.0`, etc.) et vérifier le checksum SHA-256 publié dans les notes.

### Configurer et lancer

1. Installer **Python 3** depuis [python.org](https://python.org) — cocher **« Add python.exe to PATH »** et **tcl/tk** (tkinter).
2. Double-clic sur **`Skyrim-Profiles.pyw`** à la racine du projet.
3. Suivre l'**assistant de première installation** (chemins, profil actuel dans My Games).
4. Utiliser l'interface pour basculer entre profils avant de lancer le jeu.

## Principe

Skyrim lit ses données utilisateur depuis un dossier **unique** :

```
Documents\My Games\Skyrim Special Edition\
```

Ce projet y déploie, au moment du lancement, le contenu du **profil actif** stocké dans `profiles\`.

## Structure du dépôt

```
Skyrim-Profiles/
├── Skyrim-Profiles.pyw           # Lanceur principal (GUI, sans console)
├── MyConfig.json                 # Ta config locale (creee par l'assistant)
├── MyConfig.example.json         # Modele de reference
├── profiles/
│   ├── Keizaal/                  # Miroir My Games — Keizaal
│   └── Solo/                     # Miroir My Games — solo moddé
├── scripts/
│   ├── Switch-SkyrimProfile.ps1  # Point d'entrée PowerShell
│   ├── Initialize-SkyrimProfiles.ps1
│   └── ProfileSwitcher.psm1      # Logique de bascule (module)
├── gui/
│   ├── entry.py                  # Entree GUI (assistant ou switch)
│   ├── wizard.py                 # Assistant premiere installation
│   └── app.py                    # Interface de bascule
├── launchers/                    # Raccourcis jeux optionnels
├── docs/                         # Documentation / rapports
└── _Backups/                     # Backups horodatés (non versionnés)
```

## Utilisation

### Interface graphique (recommandé)

1. Fermer Skyrim.
2. Double-clic sur **`Skyrim-Profiles.pyw`**.
3. Choisir le profil, confirmer, lancer le jeu via le bon launcher.

### Ligne de commande (sans GUI)

```powershell
.\scripts\Switch-SkyrimProfile.ps1 -Profile Solo
.\scripts\Switch-SkyrimProfile.ps1 -Profile Keizaal
.\scripts\Switch-SkyrimProfile.ps1 -Status
```

Les noms de profil correspondent aux clés de `versions` dans `MyConfig.json`.

## Configuration

`MyConfig.json` est créé par l'assistant au premier lancement. Pour reconfigurer, supprime ce fichier et relance `Skyrim-Profiles.pyw`.

Guide détaillé : **[docs/GUIDE-INSTALLATION.md](docs/GUIDE-INSTALLATION.md)**

```json
{
    "profilesRoot": "E:\\...\\Skyrim-Profiles",
    "targetRoot": "C:\\Users\\<toi>\\Documents\\My Games\\Skyrim Special Edition",
    "backupRoot": "_Backups",
    "active_version": "Solo",
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
- Python 3 + tkinter pour la GUI (`Skyrim-Profiles.pyw`)

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
- Ne bascule vers l'autre profil qu'après avoir préparé cette installation (profil vide au départ)

## Antivirus et téléchargement

| Situation | Piste |
|-----------|--------|
| ZIP bloqué ou mis en quarantaine | Préférer [`git clone`](#récupérer-le-projet-recommandé--git-clone) |
| Besoin du ZIP (pas de Git) | Release taguée `v*` + [vérification SHA-256](docs/GUIDE-INSTALLATION.md#releases-taguées-et-checksums-sha-256) |
| GUI ne démarre pas | Vérifier Python + tkinter ; lancer `python Skyrim-Profiles.pyw` pour voir l'erreur |
| Switch sans GUI | `.\scripts\Switch-SkyrimProfile.ps1 -Profile <nom>` (pas de Python) |

Détails, exceptions Defender et dépannage : **[guide antivirus](docs/GUIDE-INSTALLATION.md#antivirus-et-téléchargement-github)**.

Voir `gui/README.md` pour l'architecture de l'interface.

## Licence

[MIT](LICENSE) — libre d'utiliser, modifier et redistribuer.
