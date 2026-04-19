# Configuration Technique Antigravity

Ce fichier définit les contraintes et préférences d'implémentation pour Antigravity sur ce projet.

## 🎨 Design System (Golden Green)
- **Palette** : Base Verte (WhatsApp-like), accents dorés pour les éléments premium.
- **Framework** : Flet (Python).
- **Style** : Mobile-first, Material 3, coins arrondis, micro-animations.

## 💾 Gestion des Données (CSV First)
- **Mode** : Offline-first.
- **Stockage** : Fichiers CSV dans `data/`.
- **Intégrité** : Toujours passer par les classes du domaine pour valider les transactions avant écriture.

## 🌍 Localisation & I18n
- **Langue par défaut** : Malagasy (`mg`).
- **Standard** : Utiliser `Translator-MG` pour toute nouvelle chaîne.
- **Format** : Les clés de traduction doivent être explicites.

## 📄 Documentation IA
- **Format** : Markdown ou Org-mode.
- **Emplacement** : `docs/dev_notes/`.
- **Structure** : Date, Objectif, Changements techniques, Prochaines étapes.

## 🧩 Workflow
1. Analyse du `BLUEPRINT.md`.
2. Validation des données par `DATA_SCHEMA.md`.
3. Implémentation modulaire dans `src/views/`.
4. Test avec données CSV simulées.
