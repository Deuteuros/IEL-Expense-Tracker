# Guide d'Implémentation GitHub & Workflow de Collaboration

Pour que l'équipe puisse collaborer efficacement en "vibe coding", nous allons utiliser GitHub. Voici la marche à suivre pour configurer le dépôt et travailler ensemble.

## 1. Initialisation du Dépôt (Premier utilisateur)

À la racine du dossier `apk/` :

```bash
git init
git add .
git commit -m "Initial commit: Modular architecture for Expense Tracker"
# Ensuite, créez un dépôt sur GitHub et liez-le :
# git remote add origin https://github.com/VOTRE_NOM/NOM_DU_PROJET.git
# git push -u origin main
```

## 2. Structure Git Recommandée

- **Main (Branche Stable) :** Version qui fonctionne toujours.
- **Develop (Branche de travail) :** Où les agents et les humains poussent leurs changements "vibe coding".

## 3. Workflow Multi-Agents / Multi-Humains

Pour éviter les conflits de version sur le fichier `expenses.csv` ou les fichiers de code :

1. **Pull avant de coder :** Toujours faire un `git pull` avant de commencer pour avoir la dernière version de l'architecture.
2. **Branches de fonctionnalités :** Créer une branche pour chaque gros changement (ex: `git checkout -b feat-odoo-sync`).
3. **Commit clairs :** Expliquez brièvement ce qu'une session de "vibe coding" a produit.

## 4. Ce qu'il ne faut PAS envoyer sur GitHub (Ignorer)

Nous utilisons un fichier `.gitignore` pour exclure :
- `venv/` (Trop lourd, spécifique à la machine).
- `__pycache__/` (Fichiers compilés inutiles).
- `expenses.csv` (Si vous voulez garder vos données privées, sinon ignorez-le seulement dans le guide).

## 5. Utilisation des Issues pour les Agents
Si un agent IA travaille avec vous, demandez-lui de lire le fichier `RECAP_EVOLUTION.md` et les fichiers de documentation `.org` pour comprendre l'état actuel avant de commencer.
