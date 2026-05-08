# 🗺️ Roadmap : CaisseCash (IEL)

> Dernière mise à jour : 2026-05-08

Cette roadmap définit l'évolution de **CaisseCash**, l'application de gestion de flux financiers de l'ISS Economics Lab (IEL), migrée avec succès de Python/Flet vers Flutter/Dart.

---

## ✅ Étape 1 : Migration Flutter & Fondations (Terminé)
- **Migration complète** : Passage de Python/Flet à Dart/Flutter pour de meilleures performances mobiles.
- **Data Schema** : Standardisation de la base SQLite et support natif via `sqflite`.
- **Identité** : Adoption du nom **CaisseCash** et refonte visuelle Material 3.
- **Compilation Linux** : Stabilisation de l'environnement de build Desktop.

---

## ✅ Étape 2 : MVP & UX Tantara (Terminé)
- **Vue Tantara v2** :
    - **Sélecteur de Mois Horizontal** : Navigation fluide par défilement.
    - **Barre de Résumé Mensuel** : Aperçu immédiat Entrées / Sorties / Solde Net.
    - **Groupement Quotidien** : Organisation par jour avec sous-totaux.
- **Audit & Import** : 
    - **Import CSV Robuste** : Gestion automatique des séparateurs, du BOM et mapping dynamique des portefeuilles.
- **Recherche** : Filtrage par nom d'item et par date précise.

---

## 🔄 Étape 3 : Saisie Intelligente & Optimisations (En Cours)
- ⬜ **Smart Entry (Saisie Intelligente)** : 
    - Autocomplétion dynamique des items.
    - Chargement auto de l'unité.
    - Autocomplétion des fournisseurs/clients.
- ⬜ **Logo & Build Mobile** : Finalisation de l'intégration du logo et génération d'APK pour Android.
- ✅ **Localisation Malagasy** : Intégration des jours (Alakamisy, etc.) et mois en malgache.

---

> [!NOTE]
> **Consigne Technique** : Se référer au `docs/migration.md` pour l'historique de transition et au `docs/RUN_GUIDE.md` pour les commandes de build.
