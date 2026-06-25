# Launchers

Scripts de lancement du projet. Tous passent par `_env.bat` qui définit `SP_ROOT` (racine du dépôt).

## À la racine du projet

| Fichier | Usage |
|---------|--------|
| **`Skyrim-Profiles.vbs`** | **Lanceur principal** — interface GUI, sans fenêtre console |
| `Skyrim-Profiles.bat` | Même chose via `.bat` (fenêtre console fugace) |

## Dans ce dossier (`launchers/`)

| Fichier | Usage |
|---------|--------|
| `gui.bat` | Interface tkinter (`gui/app.py`) |
| `Activer-Keizaal.bat` | Bascule CLI vers profil Keizaal |
| `Activer-Solo.bat` | Bascule CLI vers profil Solo |
| `_env.bat` | Chemins communs (ne pas lancer directement) |

## Raccourcis jeux (optionnel)

Place ici tes raccourcis vers Steam, MO2, Keizaal, etc. — ils ne sont pas gérés par le script de switch.
