# 🗺️ Roadmap & Backlog : CaisseCash (IEL)

> Dernière mise à jour : 2026-05-08

Ce document est l'unique point de référence pour la vision stratégique et le suivi des tâches techniques de **CaisseCash**.

---

## 🏁 État Actuel : MVP Stable & Déploiement Mobile Réussi
L'application a été migrée avec succès vers Flutter. Les fonctions de consultation, de recherche, de saisie intelligente (Smart Entry) et d'export CSV / sauvegarde (Backup) sont entièrement opérationnelles et stabilisées sur Linux Desktop et Android Mobile (APK généré).

---

## ✅ Étape 1 : Migration & Fondations (Terminé)
- **Migration complète** : Passage de Python/Flet à Dart/Flutter.
- **Data Schema** : Support natif via `sqflite`.
- **Identité** : Nom **CaisseCash** et design Material 3.
- **Compilation Linux** : Environnement de build stabilisé.

---

## ✅ Étape 2 : MVP & UX Tantara (Terminé)
- **Vue Tantara v2** : Sélecteur horizontal, barre de résumé, groupement par jour.
- **Audit & Import** : Import CSV robuste et mapping dynamique.
- **Recherche** : Filtrage par texte et par date précise.
- **Localisation** : Malagasy intégral (Janoary, Alakamisy, etc.).

---

## ✅ Étape 3 : Saisie Intelligente & Déploiement (Terminé)

### 📋 Liste des Tâches (Backlog)
- [x] **Smart Entry (Saisie Intelligente)** : 
    - [x] Autocomplétion dynamique des items (Corrigé via un composant inline personnalisé sur mobile).
    - [x] Chargement auto de l'unité.
    - [x] Autocomplétion des fournisseurs/clients (Corrigé via un composant inline personnalisé sur mobile).
- [x] **Build Android** : Génération de l'APK final via Flutter.
- [x] **Icône d'Application** : S'assurer que le logo est correctement intégré au build mobile.
- [x] **Tests Mobiles** : Valider la réactivité de l'onglet "Ampidiro" sur différents écrans.
    - [x] *Bug* : Autocomplétion (Smart Entry) ne fonctionne pas sur mobile (Résolu avec le widget inline).
    - [x] *Bug* : Commande d'export (Backup) en échec sur mobile (Résolu via le menu de partage natif).
- [x] **Export de Backup** : Sauvegarde externe des données SQLite (Intégré via le partage natif sur mobile et FilePicker sur Desktop).

---

> [!NOTE]
> **Directive Technique** : Pour toute nouvelle fonctionnalité, mettre à jour ce document avant de commencer le développement.
