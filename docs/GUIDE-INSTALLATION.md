# Guide d'installation et de configuration

Ce projet est conçu pour **gérer exactement deux installations** de Skyrim SE sur la **même machine Windows** — pas plus.

Exemple typique :

| Profil | Usage |
|--------|--------|
| **Profil A** | Keizaal Online, ou une install moddée dédiée |
| **Profil B** | Solo moddé (Steam / MO2 / Vortex) |

Chaque profil est un miroir du dossier `My Games\Skyrim Special Edition`. Avant de jouer, tu actives le profil voulu ; le script déploie ses fichiers (`.ini`, sauvegardes, SKSE, etc.) vers `My Games`.

> **Limite volontaire :** le code et la config ciblent **deux profils**. Ajouter un troisième usage demande de modifier le projet toi-même (voir section [Personnalisation](#personnalisation)).

---

## Licence

Ce projet est sous licence **[MIT](../LICENSE)** : utilisation, modification, distribution et usage commercial autorisés, sans garantie. Tu peux remplacer « Skyrim-Profiles contributors » par ton nom dans `LICENSE` si tu le souhaites.

## Open source

Le code sera publié sur **GitHub** (bientôt). Contributions, retours et forks sont les bienvenus.

---

## Prérequis

1. **Windows** avec PowerShell et `robocopy` (inclus par défaut).
2. **Deux installs de jeu séparées** sur le disque (ex. dossier Keizaal + install Steam solo) — ce projet ne gère **pas** les exécutables ni les mods dans `Data\`, seulement `My Games`.
3. **Python 3** + tkinter (pour l'interface graphique) — optionnel si tu utilises les `.bat` en ligne de commande.

---

## Installation rapide

### 1. Récupérer le projet

Clone ou télécharge le dépôt, par exemple :

```
E:\Games\Skyrim-Profiles\
```

### 2. Créer ta configuration locale

Le fichier `MyConfig.json` est **spécifique à ta machine** et n'est pas versionné.

```bat
copy MyConfig.example.json MyConfig.json
```

Ouvre `MyConfig.json` et adapte les valeurs (voir tableau ci-dessous).

### 3. Créer les dossiers de profils

Crée deux dossiers correspondant aux clés de `versions` :

```
profiles\ProfilA\
profiles\ProfilB\
```

Tu peux renommer `ProfilA` / `ProfilB` (ex. `Keizaal`, `Solo`) — garde la **cohérence** entre les noms dans `versions` et les noms de dossiers.

### 4. Premier remplissage (optionnel)

Si tu as déjà joué avec l'un des deux setups, lance le jeu une dernière fois avec ce setup actif, puis :

1. Ferme Skyrim.
2. Active l'autre profil via la GUI ou les launchers.
3. Le script **sauvegarde automatiquement** l'état courant de `My Games` dans le profil précédent avant de basculer.

Au premier switch depuis un profil, son dossier est rempli avec le contenu actuel de `My Games`.

### 5. Lancer l'outil

- **Interface graphique :** double-clic sur `Skyrim-Profiles.vbs`
- **Ligne de commande :** `launchers\Activer-Keizaal.bat` / `Activer-Solo.bat` (à renommer si tu as changé les noms de profils)

---

## Remplir `MyConfig.json`

Template de référence : **`MyConfig.example.json`**

| Champ | Obligatoire | Description | Exemple |
|-------|-------------|-------------|---------|
| `profilesRoot` | Oui | Chemin **absolu** vers la racine de ce dépôt | `E:\Games\Skyrim-Profiles` |
| `targetRoot` | Oui | Dossier `My Games\Skyrim Special Edition` lu par Skyrim | `C:\Users\Alice\Documents\My Games\Skyrim Special Edition` |
| `backupRoot` | Oui | Sous-dossier des backups (relatif à `profilesRoot`) | `_Backups` |
| `active_version` | Non | Profil actuellement déployé ; `null` au premier lancement | `"Solo"` ou `null` |
| `last_switch` | Non | Horodatage du dernier switch (rempli par le script) | `null` |
| `last_backup` | Non | Chemin du dernier backup (rempli par le script) | `null` |
| `versions` | Oui | **Exactement deux entrées** : nom du profil → sous-dossier | voir ci-dessous |

### Exemple rempli (deux profils : Keizaal + Solo)

```json
{
    "profilesRoot": "E:\\Games\\Skyrim-Profiles",
    "targetRoot": "C:\\Users\\Alice\\Documents\\My Games\\Skyrim Special Edition",
    "backupRoot": "_Backups",
    "active_version": null,
    "last_switch": null,
    "last_backup": null,
    "versions": {
        "Solo": "profiles\\Solo",
        "Keizaal": "profiles\\Keizaal"
    }
}
```

### Points importants

- **Échappement Windows :** dans le JSON, les backslashes sont doublés (`\\`).
- **OneDrive :** si `Documents` est synchronisé, le chemin peut être `C:\Users\...\OneDrive\Documents\My Games\...`. Ferme Skyrim et attends la fin de la synchro en cas d'erreur de copie.
- **Deux profils seulement :** les clés de `versions` définissent tes deux usages. Les boutons GUI et launchers par défaut utilisent `Solo` et `Keizaal` — renomme-les dans la config **et** dans `gui/app.py` / `launchers/` si tu choisis d'autres noms.

---

## Utilisation quotidienne

```
1. Fermer Skyrim
2. Double-clic Skyrim-Profiles.vbs
3. Choisir le profil → confirmer
4. Lancer le jeu via le launcher adapté (Keizaal, Steam, MO2…)
```

---

## Personnalisation

Le projet est open source : tu peux :

- renommer les profils dans `MyConfig.json` et les dossiers `profiles\` ;
- adapter les `.bat` dans `launchers\` ;
- modifier `gui/app.py` pour d'autres libellés ou un 3ᵉ bouton ;
- étendre `ProfileSwitcher.psm1` pour plus de deux profils.

Pour **plus de deux installations**, il faudra adapter le code (GUI, launchers, validation) — ce n'est pas le cas d'usage prévu par défaut.

---

## Dépannage

| Problème | Piste |
|----------|--------|
| `Profil inconnu` | Le nom passé au script doit correspondre à une clé de `versions` |
| Erreur robocopy | Skyrim encore ouvert, ou fichier verrouillé par OneDrive |
| Python introuvable | Installer Python 3, cocher « Add to PATH », ou utiliser les `.bat` CLI |
| GUI : erreur JSON | Vérifier la syntaxe de `MyConfig.json` ; pas de virgule en trop |

---

## Fichiers à ne pas versionner (Git)

- `MyConfig.json` — config locale
- `profiles/` — données de jeu (saves, logs…)
- `_Backups/` — snapshots automatiques

Le template **`MyConfig.example.json`** reste dans le dépôt comme modèle pour les nouveaux utilisateurs.

---

## Voir aussi

- [README.md](../README.md) — vue d'ensemble du projet
- [gui/README.md](../gui/README.md) — interface graphique
