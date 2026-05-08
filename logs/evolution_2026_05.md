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
- **Documentation :** Création du [RUN_GUIDE.md](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker/flutter_project/docs/RUN_GUIDE.md) pour pérenniser les commandes de compilation spécifiques à l'environnement.

## 📅 [2026-05-08] - Renommage "CaisseCash" & Archivage Python
### 🏷 Identité de Marque
- **Nouveau Nom :** Application officiellement renommée **CaisseCash** (Jeu de mots avec "C'est cash" / Cash + Caisse).
- **Mise à jour Globale :** Renommage effectué dans `pubspec.yaml`, les manifestes Android/iOS, les titres de fenêtres (Linux/Windows/Web) et l'interface utilisateur.

### 📁 Organisation du Projet
- **Archivage Python :** La version originale Python/Flet a été déplacée dans le dossier `archive/` pour marquer le passage définitif à Flutter.
