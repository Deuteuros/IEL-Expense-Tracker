# Hub IEL : Journal de Bord Multi-Agents
**Objectif :** Centraliser l'évolution stratégique du projet entre humains et agents IA.

---

## 📅 [2026-02-22] - Expansion Technique & Nouveau Projet
### 🍳 Initialisation : Culinary Accountant
- **Nouveau Module :** Création du dossier `Culinary Accountant` pour transformer les données de `Torohevitra.xlsx` en module métier (COGS).
- **Synergie :** Brief technique (`PROJECT_BRIEF.md`) définissant l'interconnexion entre le suivi des dépenses et le coût de revient culinaire (approche Odoo).

### 🔄 Refactorisation Modulaire (Expense Tracker)
- **Architecture :** Passage d'un script unique à une structure modulaire (`main.py`, `database.py`, `views/`).
- **Standardisation :** Création de guides de collaboration (`VENV_GUIDE.md`, `GITHUB_COLLABORATION.md`, `USB_GIT_SHARE_GUIDE.md`, `MANUAL_ZIP_SHARE_GUIDE.md`).
- **Protocole de Fusion Safe :** Introduction d'une méthode de transfert par ZIP (excluant `venv`) pour garantir l'intégrité de l'ordinateur central.
- **Documentation Lettrée :** Migration vers des fichiers `.org` individuels pour chaque module technique.
- **Réparation venv :** Nettoyage complet et réinstallation des dépendances Flet pour garantir la portabilité.

---

## 📅 [2026-02-27] - Fusion Semaine 1 & Stabilisation Web
### 🤝 Intégration Collective
- **Multi-Features :** Fusion réussie de 4 branches de travail (Évolution Schéma, Vue Tantara, Suppression Long-Press, Consentement & Config).
- **Consolidation Documentation :** Réorganisation des guides éparpillés en un document unique `TEAM_WORKFLOW.md` dans `apk/Documentation/`.
- **Bundle v1 :** Création du premier pack de distribution (`final_expense_tracker_v1.bundle`) pour synchroniser toute l'équipe.

### 🐛 Débogage & Robustesse
- **Flet Web Fix :** Résolution du bug de sérialisation `set object` via la création d'un composant `CustomSegmentedControl` (Flet 0.80.2).
- **UI Stable :** Migration de `SegmentedButton` vers des `Tabs` et finalement vers un contrôle customisé pour garantir la portabilité navigateur.
- **Dépendances :** Identification et documentation de la dépendance manquante `libmpv.so.2` pour Linux Desktop.

---

## 📅 [2026-03-13] - Intégration Bundle & Modernisation UI
### 📦 Mise à jour via Bundle
- **Intégration :** Fusion réussie du bundle `expense_tracker_latest.bundle` apportant des améliorations majeures de design et de structure.
- **Data Precision :** Migration du schéma CSV (harmonisation des noms de colonnes : `prix_unitaire_mga` -> `prix_unitaire`).
- **Maintenance :** Réparation et isolation de l'environnement virtuel (`venv`) pour garantir la portabilité du projet sur de nouveaux postes.

### 🎨 Refonte de la Vue Tantara (Historique)
- **Design WhatsApp-like :** Transition d'une liste simple vers une interface à cartes avec groupement par jour.
- **Filtre Temporel :** Introduction d'un sélecteur de mois horizontal pour une navigation fluide dans l'historique.
- **Insights Rapides :** Ajout d'une barre de résumé (Entrées, Sorties, Balance) dynamique par mois.
- **UX :** Amélioration du mode sélection par clic long pour la suppression groupée.

---

## 📅 [2026-02-20] - Version Alpha (Vibe Coding)
### ✅ Accomplissements :
- **UI :** Thème Material 3 "Golden Green".
- **Localisation :** Traduction intégrale de l'interface vers le Malagasy.
- **Performance :** Migration vers les graphiques natifs Flet pour optimiser l'usage mobile.
- **UX :** Introduction du Floating Action Button (FAB) et du dialogue d'ajout multi-entrée.

---

## 🚀 Backlog & Visions Futures :
- [x] **M5 (Partiel) :** Refonte du schéma CSV (Data Precision : Item, Qty, Unité, Prix).
- [x] **M6 :** Vue Tantara augmentée : Suppression massive par clic long, affichage Qty/Unité et groupement temporel.
- [ ] **M1 :** Intégration du module Culinary avec les prix réels de l'Expense Tracker.
- [ ] **M2 :** Analyse de l'architecture Odoo pour implémenter un système de plugins (héritage de modèles).
- [ ] **M3 :** Synchronisation Cloud (Firebase/Supabase) pour le travail d'équipe.
- [ ] **M4 :** Migration vers un dépôt GitHub centralisé pour le déploiement continu.
- [ ] **M5 (FR/EN) :** Support multilingue complet (Malagasy déjà OK).
- [ ] **M7 :** Module "Observatoire Économique" (Collecte anonymisée Opt-in et Insights du Marché).
