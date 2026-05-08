# Journal d'Évolution - Avril 2026

## 📅 [2026-04-19] - Migration SQLite & Modernisation Asynchrone
### 🛠 Refonte de l'Architecture
- **SQLite Integration :** Déploiement de `cashew.db` comme moteur de persistance haute performance.
- **Async Migration :** Conversion de l'application (`main.py`) vers le mode asynchrone (`asyncio`) pour stabiliser l'interface et supporter les fonctionnalités récentes.

### 💾 Gestion des Données
- **CSV Sync :** Implémentation des fonctions d'importation (mode ajout) et d'exportation vers `data/expense.csv`.
- **FilePicker Fix :** Adaptation du code pour Flet 0.8.2 (gestion directe des résultats `await pick_files()`).

### 🐛 Débogage & Maintenance
- **Color Fix :** Remplace les constantes obsolètes par les noms de couleurs standard pour la compatibilité Material 3.
- **Log System :** Création du répertoire `logs/` et décomposition de l'historique global pour une meilleure lisibilité.
- **Bug Hunter :** Identification du problème "Unknown control: FilePicker" sur Linux (lié à l'injection initiale dans l'overlay).

### 🚀 Vision :
- Planification du nouvel onglet **"Fikirakirana"** pour isoler les outils de gestion.

## 📅 [2026-04-22] - Correction Linux & Refonte UI
### 🛠 Interface & Navigation
- **Management Tab :** Création de l'onglet "Fikirakirana" (icône `...`) pour regrouper les outils techniques (Import/Export).
- **Summary Cleanup :** Allègement de la vue "Témoin" par suppression des boutons CSV devenus redondants.
- **Navigation :** Passage à un système de navigation à 3 destinations.

### 🐛 Débogage
- **FilePicker Fix :** Résolution du bug "Unknown control" sur Linux par injection forcée et mise à jour explicite de l'overlay lors de l'initialisation.

## 📅 [2026-04-24] - Résolution des erreurs de compilation Android
### 🐛 Débogage & Déploiement
- **Build Script Fix :** Mise à jour du script `build_apk.sh` pour utiliser directement l'exécutable Python de l'environnement virtuel (`./venv/bin/python3 ./venv/bin/flet`) et contourner les anciens chemins absolus.
- **CLI Argument :** Remplacement de l'argument déprécié `--project-name` par `--project` dans la commande de build.
- **Dependency Conflict :** Suppression de `kaleido` et `plotly` du fichier `src/requirements.txt` pour corriger les conflits de résolution `pip` lors du ciblage mobile.
- **APK Généré :** L'application a été compilée avec succès pour Android.

## 📅 [2026-04-25] - Seeding & Migration Flet 0.80+
### 💾 Gestion des Données
- **Database Seeding :** Génération automatique de 30 jours de transactions aléatoires (`scratch/seed_data.py`) pour tester les vues graphiques.

### 🐛 Débogage & Migration
- **Flet 0.80+ Migration :**
    - Remplacement de `ft.app()` par `ft.run()` (dépréciation).
    - Migration des graphiques vers le package séparé `flet-charts` (`fc.LineChart`, `fc.PieChart`, etc.).
    - Mise à jour des signatures de constructeurs (`data_points` -> `points`, `stroke_cap_round` -> `rounded_stroke_cap`).
    - Correction des constantes d'alignement (`ft.alignment.top_center` -> `ft.Alignment.TOP_CENTER`).
    - Correction des paramètres d'axe (`labels_size` -> `label_size`).

