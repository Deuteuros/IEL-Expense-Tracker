# Context Root & Agent Mandate - IEL Expense Tracker

Ce fichier est la racine de contexte local pour l'assistant **Antigravity** lorsqu'il intervient sur le dépôt **IEL - Expense tracker**.

## Mandat du Projet
Le projet [IEL - Expense tracker](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker) est une application mobile de gestion de caisse et de dépenses offline-first, développée en Flutter/Dart. Elle doit s'intégrer à terme avec Cashew et Odoo.

## Compétences (Skills) Locales
* **`caisse-offline-first`** : Instructions de développement pour la résilience réseau, la persistance locale et la synchronisation.
  * Emplacement : [.antigravity/skills/caisse-offline-first/SKILL.md](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker/.antigravity/skills/caisse-offline-first/SKILL.md)

## Compétences (Skills) Globales
* **`git-manager`** : Gestion complète du dépôt Git — création de branches, merges, résolution de conflits, commits (Conventional Commits), push/pull sécurisé.
  * Plugin : `git-manager-plugin` (global, disponible dans tous les projets Antigravity)

## Sous-Agents Définis
* **`expense-database-architect`** : Expert de la persistance locale en SQLite (via Drift/Sqflite) et des schémas de synchronisation.
  * Configuration : [.antigravity/subagents/expense-database-architect.md](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker/.antigravity/subagents/expense-database-architect.md)

## Règle de Développement (Git & Branches)
* **Workflow de branchement** : Pour toute nouvelle fonctionnalité, l'assistant doit obligatoirement utiliser Git en créant une branche dédiée (ex: `feature/nom-fonctionnalite`).
* **Validation & Rollback** : Travailler exclusivement sur cette branche pour isoler le code et permettre un retour arrière rapide en cas de blocage. Fusionner la branche vers la branche principale uniquement après validation fonctionnelle et tests de la fonctionnalité.

## Suivi Stratégique
* QG Stratégique Obsidian : `Efforts/Projects/IEL - Expense tracker.md` dans l'Ideaverse.
* Tâches d'implémentation courantes : [.antigravity/tasks/task.md](file:///home/deuteuros/Documents/10%20Projets/IEL%20-%20Expense%20tracker/.antigravity/tasks/task.md)
