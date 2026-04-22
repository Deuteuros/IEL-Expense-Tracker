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
