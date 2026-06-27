# Guide d'installation et de configuration

Ce projet gère **exactement deux usages** de Skyrim SE sur la **même machine Windows** — pas plus.

Exemple typique :

| Profil | Usage |
|--------|--------|
| **Keizaal** | Keizaal Online, ou une install moddée dédiée |
| **Solo** | Solo moddé (Steam / MO2 / Vortex) |

Skyrim ne lit qu’**un seul** dossier `My Games\Skyrim Special Edition` à la fois. Ce projet y déploie le contenu du **profil actif** (fichiers `.ini`, sauvegardes, SKSE, etc.) stocké dans `profiles\`. Tu changes de profil **avant** de lancer le jeu, via l’interface ou PowerShell.

> **Limite volontaire :** le code et la config ciblent **deux profils**. Un troisième usage demande de modifier le projet toi-même (voir [Personnalisation](#personnalisation)).

---

## Licence

Ce projet est sous licence **[MIT](../LICENSE)** : utilisation, modification, distribution et usage commercial autorisés, sans garantie.

## Open source

Code publié sur **GitHub** : [github.com/wildevince/Skyrim-Profiles](https://github.com/wildevince/Skyrim-Profiles). Contributions et retours sont les bienvenus.

---

## Prérequis

1. **Windows** avec PowerShell et `robocopy` (inclus par défaut).
2. **Deux façons de lancer le jeu** sur le disque (ex. install Keizaal + Steam/MO2 solo) — ce projet ne gère **pas** les exécutables ni les mods dans `Data\`, seulement le dossier `My Games`.
3. **Python 3** + tkinter (interface graphique et assistant d’installation). La GUI appelle PowerShell en arrière-plan pour les copies de fichiers.

---

## Installation rapide

### 1. Récupérer le projet

**Recommandé — `git clone`** (souvent moins bloqué par l’antivirus que le ZIP) :

```bat
git clone https://github.com/wildevince/Skyrim-Profiles.git
cd Skyrim-Profiles
```

Alternative : ZIP depuis une **release taguée** (`v1.0.0`, etc.) — voir [Releases taguées et checksums SHA-256](#releases-taguées-et-checksums-sha-256).

### 2. Installer Python

Télécharge Python 3 depuis [python.org](https://python.org). À l’installation :

- coche **« Add python.exe to PATH »** ;
- assure-toi que **tcl/tk** (tkinter) est inclus.

### 3. Premier lancement

Double-clic sur **`Skyrim-Profiles.pyw`** à la racine du projet.

Si `MyConfig.json` est **absent**, l’**assistant de première installation** s’ouvre automatiquement (détail dans la section suivante). Sinon, l’interface de bascule s’affiche directement.

### 4. Usage quotidien

- **Interface graphique :** double-clic sur `Skyrim-Profiles.pyw`
- **Ligne de commande :** `.\scripts\Switch-SkyrimProfile.ps1 -Profile Solo` (ou `Keizaal`)

---

## Assistant de première installation (wizard)

L’assistant (`gui/wizard.py`) évite l’édition manuelle de `MyConfig.json` au premier lancement. Il est implémenté en **tkinter** et s’appuie sur **`scripts/Initialize-SkyrimProfiles.ps1`** pour la copie initiale des fichiers.

### Quand s’affiche-t-il ?

| Condition | Comportement |
|-----------|--------------|
| `MyConfig.json` **absent** | Assistant → puis interface de bascule |
| `MyConfig.json` **présent** | Interface de bascule uniquement |
| Assistant **annulé** ou **échoué** | Fermeture sans ouvrir la GUI ; pas de config partielle conservée en cas d’échec de copie |

Pour **tout recommencer** : supprime `MyConfig.json` (et éventuellement les dossiers `profiles\` vides) puis relance `Skyrim-Profiles.pyw`.

### Déroulé en cinq écrans

```text
Skyrim-Profiles.pyw
        │
        ▼
  MyConfig.json absent ?
        │
   oui  │  non → GUI de bascule
        ▼
 ┌──────────────────────────────────────────────────────────┐
 │ 1. Bienvenue                                              │
 │ 2. Racine du projet (profilesRoot)                        │
 │ 3. Dossier My Games (targetRoot)                          │
 │ 4. Profil actuel dans My Games                            │
 │ 5. Récapitulatif → Terminer                               │
 └──────────────────────────────────────────────────────────┘
        │
        ▼
  Écriture MyConfig.json
  + Initialize-SkyrimProfiles.ps1
        │
        ▼
  Interface de bascule (même processus)
```

#### Écran 1 — Bienvenue

- Présentation du projet (deux profils : Solo moddé et Keizaal).
- Rappel **antivirus** : préférer `git clone` si le ZIP est bloqué ; lien vers le README.
- Prérequis rappelés : Python + tkinter, PowerShell, robocopy.
- **« Passer l’intro »** ou **« Suivant »** pour continuer.

#### Écran 2 — Racine du projet (`profilesRoot`)

- Champ **prérempli** avec le dossier où se trouve le dépôt (emplacement de `Skyrim-Profiles.pyw`).
- En lecture seule par défaut ; case **« Modifier (avancé) »** pour corriger si le dépôt a été déplacé.
- Validation : le dossier doit exister.

#### Écran 3 — Dossier My Games (`targetRoot`)

- Chemin vers `...\My Games\Skyrim Special Edition` (Documents ou **OneDrive\Documents**).
- Préremplissage automatique si un dossier Skyrim SE standard est détecté.
- Bouton **« Parcourir… »** pour sélectionner le dossier.
- Validations :
  - chemin obligatoire ;
  - si le dossier n’existe pas : proposition de le créer ;
  - si le dossier ne ressemble pas à un My Games Skyrim SE (`Skyrim.ini`, `Saves`, etc.) : avertissement avec possibilité de continuer quand même.

#### Écran 4 — Contenu actuel de My Games

Question : **quel profil correspond à ce qui est dans My Games en ce moment ?**

| Choix affiché | Clé enregistrée |
|---------------|-----------------|
| Solo moddé | `Solo` |
| Keizaal | `Keizaal` |

> **Important :** le contenu actuel de `My Games` sera **copié** dans `profiles\<profil choisi>`. L’**autre** profil démarre **vide**. Ne bascule vers l’autre profil qu’après avoir préparé cette installation — sinon un dossier vide serait déployé dans `My Games`.

#### Écran 5 — Récapitulatif

Affiche les chemins et le profil initial. **« Terminer »** lance l’initialisation.

### Actions à la validation (« Terminer »)

1. **Écriture de `MyConfig.json`** à partir du modèle `MyConfig.example.json` (le modèle reste dans le dépôt).
2. **Appel PowerShell** : `scripts/Initialize-SkyrimProfiles.ps1 -InitialProfile <Solo|Keizaal>`, qui :
   - crée `profiles\Solo`, `profiles\Keizaal` et `_Backups\` si besoin ;
   - effectue une copie miroir (`robocopy /MIR`) de `targetRoot` vers `profiles\<profil choisi>` ;
   - enregistre `active_version` et `last_switch` dans `MyConfig.json`.
3. **Ouverture automatique** de l’interface de bascule (`gui/app.py`) dans le même processus.

En cas d’**échec** de la copie (Skyrim ouvert, fichier verrouillé, OneDrive, etc.), `MyConfig.json` est supprimé pour éviter une config à moitié valide — relance l’assistant après avoir corrigé la cause.

### Ce que l’assistant ne fait pas

- Il n’installe pas Python (à faire avant le double-clic sur `.pyw`).
- Il ne configure pas les exécutables du jeu (Steam, Keizaal, MO2) — place tes raccourcis où tu veux (ex. dossier `dev/` en local).
- Il ne remplit pas le second profil : c’est le premier **switch** ultérieur qui sauvegardera le profil actif puis déploiera l’autre.

---

## Remplir `MyConfig.json` (manuel, optionnel)

Si tu préfères ne pas utiliser l’assistant, copie le template et adapte-le :

```bat
copy MyConfig.example.json MyConfig.json
```

Puis lance une initialisation manuelle :

```powershell
.\scripts\Initialize-SkyrimProfiles.ps1 -InitialProfile Solo
```

(ou `Keizaal`, après avoir rempli les chemins dans le JSON)

### Champs de configuration

Template de référence : **`MyConfig.example.json`**

| Champ | Obligatoire | Description | Exemple |
|-------|-------------|-------------|---------|
| `profilesRoot` | Oui | Chemin **absolu** vers la racine de ce dépôt | `E:\Games\Skyrim-Profiles` |
| `targetRoot` | Oui | Dossier `My Games\Skyrim Special Edition` lu par Skyrim | `C:\Users\Alice\Documents\My Games\Skyrim Special Edition` |
| `backupRoot` | Oui | Sous-dossier des backups (relatif à `profilesRoot`) | `_Backups` |
| `active_version` | Non | Profil actuellement déployé ; fixé par l’assistant ou l’init | `"Solo"` |
| `last_switch` | Non | Horodatage du dernier switch (rempli par le script) | `null` |
| `last_backup` | Non | Chemin du dernier backup (rempli par le script) | `null` |
| `versions` | Oui | **Exactement deux entrées** : nom du profil → sous-dossier | voir ci-dessous |

### Exemple rempli (Keizaal + Solo)

```json
{
    "profilesRoot": "E:\\Games\\Skyrim-Profiles",
    "targetRoot": "C:\\Users\\Alice\\Documents\\My Games\\Skyrim Special Edition",
    "backupRoot": "_Backups",
    "active_version": "Keizaal",
    "last_switch": "2026-06-27 10:00:00",
    "last_backup": null,
    "versions": {
        "Solo": "profiles\\Solo",
        "Keizaal": "profiles\\Keizaal"
    }
}
```

### Points importants

- **Échappement Windows :** dans le JSON, les backslashes sont doublés (`\\`).
- **OneDrive :** si `Documents` est synchronisé, le chemin peut être `C:\Users\...\OneDrive\Documents\My Games\...`. Ferme Skyrim et attends la fin de la synchro en cas d’erreur de copie.
- **Deux profils seulement :** les clés de `versions` définissent tes deux usages. Les boutons GUI utilisent `Solo` et `Keizaal` par défaut — pour d’autres noms, adapte aussi `gui/app.py`.

---

## Utilisation quotidienne

```
1. Fermer Skyrim
2. Double-clic Skyrim-Profiles.pyw
3. Choisir le profil → confirmer
4. Lancer le jeu via le launcher adapté (Keizaal, Steam, MO2…)
```

À chaque bascule, le script :

1. sauvegarde `My Games` vers le profil actuellement actif ;
2. crée un backup horodaté dans `_Backups\` ;
3. déploie le profil cible vers `My Games` ;
4. met à jour `MyConfig.json`.

---

## Personnalisation

Le projet est open source : tu peux :

- renommer les profils dans `MyConfig.json` et les dossiers `profiles\` ;
- modifier `gui/app.py` pour d’autres libellés ou un 3ᵉ bouton ;
- étendre `ProfileSwitcher.psm1` pour plus de deux profils.

Pour **plus de deux usages**, il faudra adapter le code (GUI, assistant, validation) — ce n’est pas le cas d’usage prévu par défaut.

---

## Antivirus et téléchargement GitHub

**Ce n’est pas un virus.** Les antivirus bloquent souvent les archives GitHub qui contiennent des **scripts non signés** — surtout avant qu’elles soient « connues » (peu de téléchargements, pas de signature éditeur).

### Fichiers souvent signalés à tort

| Fichier | Pourquoi l’AV réagit |
|---------|----------------------|
| **Scripts PowerShell** (`.ps1`, `.psm1`) | `-ExecutionPolicy Bypass` et copie miroir (`robocopy /MIR`) |
| **`ProfileSwitcher.psm1`** | Copie de fichiers en masse — heuristique « comportement suspect » |
| **Le ZIP entier** | Bundle de scripts non signés depuis un dépôt inconnu |

Le **ZIP entier** reste le point de friction principal à l’import. Le lanceur `.pyw` est en général moins signalé que les anciens lanceurs `.vbs` / `.bat`.

### Solutions (par ordre de simplicité)

**1. `git clone` au lieu du ZIP** (méthode recommandée) :

```bat
git clone https://github.com/wildevince/Skyrim-Profiles.git
cd Skyrim-Profiles
```

**2. Release taguée + checksum SHA-256** — si tu dois utiliser le ZIP, préfère une release `v*` (ex. `v1.0.0`) et vérifie l’intégrité du fichier téléchargé (voir section ci-dessous). Le hash ne supprime pas l’alerte AV, mais confirme que l’archive n’a pas été altérée après déblocage.

**3. Autoriser après coup** — si le ZIP est mis en quarantaine :
- Ouvrir l’antivirus → Historique / Quarantaine
- Restaurer le dossier `Skyrim-Profiles` et ajouter une **exception** sur ce dossier

**4. Lancer la GUI autrement** :
- `python Skyrim-Profiles.pyw` depuis la racine du projet (affiche les erreurs Python dans une console)
- Sans GUI : `.\scripts\Switch-SkyrimProfile.ps1 -Profile <nom>`

**5. Télécharger fichier par fichier** sur GitHub (bouton *Raw*) — fastidieux, dernier recours.

**6. Vérifier le code** — tout est lisible en clair (`.ps1`, `.py`, `.pyw`). Aucun binaire obligatoire dans le dépôt.

### Releases taguées et checksums SHA-256

Chaque release GitHub portant un tag sémantique (`v1.0.0`, `v1.1.0`, …) publie :

- l’archive ZIP du dépôt ;
- le **SHA-256** du ZIP dans les notes de release (et fichier `SHA256SUMS.txt` joint si applicable).

**Vérifier après téléchargement** (PowerShell) :

```powershell
Get-FileHash -Path ".\Skyrim-Profiles-v1.0.0.zip" -Algorithm SHA256
```

Compare la sortie `Hash` avec la valeur indiquée sur la page de la release.

**Mainteneur** — générer le hash avant publication :

```powershell
.\dev\New-ReleaseChecksums.ps1 -ZipPath ".\Skyrim-Profiles-v1.0.0.zip"
```

### Ce que le projet ne fait pas

- Pas d’accès réseau, pas d’envoi de données
- Pas d’installation système cachée
- Modifie uniquement `My Games\Skyrim Special Edition` et les dossiers `profiles\` / `_Backups\` configurés

---

## Dépannage

| Problème | Piste |
|----------|--------|
| L’assistant ne s’ouvre pas | `MyConfig.json` existe déjà — supprime-le pour relancer l’assistant |
| Échec à « Terminer » / init | Ferme Skyrim ; vérifie OneDrive ; relance l’assistant |
| `Profil inconnu` | Le nom passé au script doit correspondre à une clé de `versions` |
| Erreur robocopy | Skyrim encore ouvert, ou fichier verrouillé par OneDrive |
| Python introuvable | Installer Python 3, cocher « Add to PATH » ; tester `python Skyrim-Profiles.pyw` |
| GUI ne démarre pas | Vérifier tkinter ; lancer `python Skyrim-Profiles.pyw` pour voir le message d’erreur |
| GUI : erreur JSON | Vérifier la syntaxe de `MyConfig.json` ; pas de virgule en trop |
| Antivirus bloque le ZIP | Voir [Antivirus et téléchargement GitHub](#antivirus-et-téléchargement-github) |

---

## Fichiers à ne pas versionner (Git)

- `MyConfig.json` — config locale
- `profiles/` — données de jeu (saves, logs…)
- `_Backups/` — snapshots automatiques

Le template **`MyConfig.example.json`** reste dans le dépôt comme modèle.

---

## Voir aussi

- [README.md](../README.md) — vue d’ensemble du projet
- [gui/README.md](../gui/README.md) — architecture de l’interface
