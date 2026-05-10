# 🗺️ Roadmap & Backlog : CaisseCash (IEL)

> Dernière mise à jour : 2026-05-08

Ce document est l'unique point de référence pour la vision stratégique et le suivi des tâches techniques de **CaisseCash**.

---

## 🏁 État Actuel : MVP Stable
L'application a été migrée avec succès vers Flutter. Les fonctions de consultation, d'import et de recherche sont opérationnelles sur Linux Desktop.

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

## 🔄 Étape 3 : Saisie Intelligente & Déploiement (En Cours)

### 📋 Liste des Tâches (Backlog)
- [x] **Smart Entry (Saisie Intelligente)** : 
    - [x] Autocomplétion dynamique des items.
    - [x] Chargement auto de l'unité.
    - [x] Autocomplétion des fournisseurs/clients.
- [ ] **Build Android** : Génération de l'APK final via Flutter.
- [ ] **Icône d'Application** : S'assurer que le logo est correctement intégré au build mobile.
- [ ] **Tests Mobiles** : Valider la réactivité de l'onglet "Ampidiro" sur différents écrans.
- [ ] **Export de Backup** : Sauvegarde externe des données SQLite.

---

> [!NOTE]
> **Directive Technique** : Pour toute nouvelle fonctionnalité, mettre à jour ce document avant de commencer le développement.
