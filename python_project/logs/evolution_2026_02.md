# Journal d'Évolution - Février 2026

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

## 📅 [2026-02-20] - Version Alpha (Vibe Coding)
### ✅ Accomplissements :
- **UI :** Thème Material 3 "Golden Green".
- **Localisation :** Traduction intégrale de l'interface vers le Malagasy.
- **Performance :** Migration vers les graphiques natifs Flet pour optimiser l'usage mobile.
- **UX :** Introduction du Floating Action Button (FAB) et du dialogue d'ajout multi-entrée.
