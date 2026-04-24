# 🛠️ Processus : Développement de Fonctionnalités (DDD)

Ce processus définit le cycle de vie d'une nouvelle fonctionnalité dans le projet Cashew (IEL).

## 📋 Étapes du cycle DDD

1. **Analyse (Phase 1)** :
   - Lire le `docs/architecture/BLUEPRINT.md`.
   - Consulter la note de projet ou la spécification spécifique (ex: `docs/architecture/tantara_redesign_spec.md`).
2. **Blueprinting (Phase 2)** :
   - Définir le composant ou le module nécessaire dans `src/views/` ou `src/components/`.
   - Valider le schéma de données via `docs/architecture/DATA_SCHEMA.md`.
3. **Implémentation (Phase 3)** :
   - Écrire le code Flet (Python) de manière modulaire.
   - Utiliser les skills **UX Designer** et **Translator (Malagasy)**.
4. **Validation (Phase 4)** :
   - Tester avec un fichier CSV de données factices.
   - Vérifier le rendu mobile-first.
5. **Documentation (Phase 5)** :
   - Documenter les changements techniques dans `docs/dev_notes/` (format `.org` ou `.md`).

## 📄 Référence
Inspiré par le `docs/process/CONTRIBUTING.md`.
