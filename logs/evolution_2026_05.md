# Journal d'Évolution - Mai 2026

## 📅 [2026-05-08] - Migration Flutter & Résolution Environnement Linux
### 🛠 Migration Technique
- **Flutter Rewrite :** Réécriture complète de l'application originale Python/Flet vers Flutter/Dart.
- **Architecture Riverpod :** Implémentation d'une gestion d'état réactive pour les transactions, les résumés et les graphiques.
- **SQLite Desktop Support :** Migration vers `sqflite_common_ffi` pour assurer la persistance des données sur Linux Desktop, avec initialisation automatique dans `main.dart`.

### 🐛 Débogage & Système (Linux)
- **APT Fix :** Nettoyage des dépôts obsolètes (opensuse) qui bloquaient les mises à jour système.
- **Clang/C++ Linker Fix :** 
    - Résolution de l'erreur `fatal error: 'type_traits' file not found` par l'installation de `libstdc++-13-dev` et l'exportation des variables `C_INCLUDE_PATH` / `CPLUS_INCLUDE_PATH`.
    - Création d'un lien symbolique pour `libstdc++.so` afin d'aider le linker de Clang.
    - Installation du linker `lld-18` pour finaliser le build Linux.

### 💾 Fonctionnalités Clés
- **Historique (Tantara) :** Support du mode sélection multiple et suppression par lots.
- **Import/Export CSV :** Restauration de la compatibilité avec le format de données original.
    - **Robustesse :** Ajout de la gestion du BOM UTF-8, détection automatique du séparateur (`,` ou `;`) et normalisation des fins de ligne (`\n`).
    - **Mapping Dynamique :** Les portefeuilles sont désormais mappés par nom au lieu d'ID statiques.
- **Documentation :** Création du [RUN_GUIDE.md](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker/flutter_project/docs/RUN_GUIDE.md) pour pérenniser les commandes de compilation spécifiques à l'environnement.

## 📅 [2026-05-08] - Refonte Tantara & Fonction de Recherche
### 🛠 Interface Utilisateur (UX)
- **Sélecteur de Mois Horizontal :** Implémentation d'une barre défilante en haut de l'historique pour une navigation rapide entre les mois.
- **Barre de Résumé Contextuelle :** Affichage en temps réel des Entrées, Sorties et du Solde Net pour le mois sélectionné.
- **Groupement Quotidien :** Les transactions sont désormais regroupées par jour avec des en-têtes incluant le solde net de la journée.
- **Localisation Malgache :** Correction des noms de jours (ex: Alakamisy) et mois dans toute la vue historique.

### 🔍 Nouvelles Fonctionnalités
- **Recherche Avancée :** Intégration d'une barre de recherche dans l'AppBar permettant de filtrer instantanément par nom d'item ou par date précise (YYYY-MM-DD).

## 📅 [2026-05-08] - Renommage "CaisseCash" & Archivage Python
### 🏷 Identité de Marque
- **Nouveau Nom :** Application officiellement renommée **CaisseCash** (Jeu de mots avec "C'est cash" / Cash + Caisse).
- **Mise à jour Globale :** Renommage effectué dans `pubspec.yaml`, les manifestes Android/iOS, les titres de fenêtres (Linux/Windows/Web) et l'interface utilisateur.

### 📁 Organisation du Projet
- **Archivage Python :** La version originale Python/Flet a été déplacée dans le dossier `archive/` pour marquer le passage définitif à Flutter.

## 📅 [2026-05-10] - Saisie Intelligente (Smart Entry)
### 🛠 Interface Utilisateur (UX)
- **Autocomplétion Dynamique :** Implémentation de champs `Autocomplete` pour les items et les clients/fournisseurs, basés sur l'historique des transactions.
- **Remplissage Automatique de l'Unité :** L'unité est désormais automatiquement chargée depuis la base de données dès qu'un item connu est sélectionné ou saisi.

### 💾 Backend & État
- **Optimisation SQLite :** Ajout de requêtes pour extraire les items et clients uniques, ainsi que la dernière unité utilisée pour un item donné.
- **Providers de Suggestions :** Intégration de providers Riverpod dédiés pour alimenter les listes de suggestions en temps réel.
