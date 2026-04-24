---
description: Comment manipuler Git pour le projet Expense Tracker IEL (offline, bundles USB)
---

# Workflow Git — Expense Tracker IEL

> Ce workflow est destiné à l'agent IA. L'utilisateur ne connaît pas Git — l'agent doit exécuter toutes les commandes à sa place et expliquer simplement ce qui se passe.

## ⚠️ Règles Fondamentales

1. **JAMAIS de `git push` ni `git pull`** — il n'y a pas de remote Internet. Tout passe par des **bundles** sur clé USB.
2. **Toujours utiliser `git -c core.pager=cat`** devant les commandes git pour éviter les blocages du pager dans le terminal.
3. **Répertoire du projet** : `/home/deuteuros/Documents/10 Projets/Applied MicroEconomics Learning Group/IEL - Expense tracker/apk`
4. **Branche principale** : `master`

---

## 📋 Vérifications de routine

### Voir sur quelle branche on est
```bash
git -c core.pager=cat branch --show-current
```

### Voir le statut des fichiers (modifiés, ajoutés, supprimés)
```bash
git -c core.pager=cat status
```

### Voir les derniers commits
```bash
git -c core.pager=cat log --oneline -10
```

---

## 💾 Sauvegarder des modifications (Commit)

### 1. Ajouter tous les fichiers modifiés au staging
```bash
git add .
```

### 2. Vérifier ce qui va être commité
```bash
git -c core.pager=cat status
```

### 3. Créer le commit
```bash
git -c core.pager=cat commit -m "type: description courte

- Détail des changements ligne 1
- Détail des changements ligne 2"
```

**Types de commit courants** :
- `feat:` — nouvelle fonctionnalité
- `fix:` — correction de bug
- `docs:` — documentation uniquement
- `refactor:` — restructuration sans changement de comportement
- `style:` — design, mise en page

---

## 📦 Créer un Bundle (pour partager sur USB)

### Bundle complet (tout l'historique) — pour un nouveau collaborateur
```bash
git -c core.pager=cat bundle create ../expense_tracker_vX.bundle --all
```
> Remplacer `vX` par le numéro de version (v1, v2, v3...).

### Bundle partiel (une branche feature uniquement) — pour l'intégrateur
```bash
git -c core.pager=cat bundle create ../[nom_tache].bundle master..feat-[nom-tache]
```

### Vérifier qu'un bundle est valide
```bash
git -c core.pager=cat bundle verify ../expense_tracker_vX.bundle
```

---

## 📥 Recevoir un Bundle d'un Collaborateur (Intégrateur)

### 1. Ajouter le bundle comme remote temporaire
```bash
git remote add collegue /chemin/vers/le/fichier.bundle
```

### 2. Récupérer les données
```bash
git -c core.pager=cat fetch collegue
```

### 3. Voir les branches disponibles
```bash
git -c core.pager=cat branch -a
```

### 4. Fusionner dans master
```bash
git checkout master
git -c core.pager=cat merge collegue/feat-[nom-branche]
```

### 5. Nettoyer le remote temporaire
```bash
git remote remove collegue
```

---

## 📥 Recevoir une mise à jour master (Collaborateur)

Quand l'intégrateur partage un `expense_tracker_vX.bundle` :

```bash
git remote add update /chemin/vers/expense_tracker_vX.bundle
git -c core.pager=cat fetch update master
git checkout master
git -c core.pager=cat merge update/master
git remote remove update
```

---

## 🌿 Travailler sur une Branche feature

### Créer une nouvelle branche
```bash
git checkout -b feat-[nom-de-la-tache]
```

### Changer de branche
```bash
git checkout master         # retourner sur master
git checkout feat-[nom]     # aller sur une feature
```

### Lister toutes les branches
```bash
git -c core.pager=cat branch -a
```

---

## 🔥 Résoudre des Conflits

Si un merge génère des conflits :

1. **Lister les fichiers en conflit** :
   ```bash
   git -c core.pager=cat diff --name-only --diff-filter=U
   ```

2. **Ouvrir chaque fichier**, chercher les marqueurs `<<<<<<<`, `=======`, `>>>>>>>` et choisir la bonne version.

3. **Marquer comme résolu** :
   ```bash
   git add [fichier_résolu]
   ```

4. **Finaliser le merge** :
   ```bash
   git -c core.pager=cat commit -m "merge: résolution des conflits avec feat-[nom]"
   ```

**Priorité de résolution** : Structure de données (Schéma CSV) > Logique métier > UI (Design)

---

## 🚫 Fichiers à ne JAMAIS commiter

Le `.gitignore` doit contenir :
```
venv/
__pycache__/
*.pyc
.apk
*.bundle
build/
```

Si un fichier interdit a été commité par erreur :
```bash
git rm --cached [fichier]
git -c core.pager=cat commit -m "fix: retrait de [fichier] du suivi git"
```

---

## 🆘 Commandes de secours

### Annuler le dernier commit (garder les fichiers modifiés)
```bash
git reset --soft HEAD~1
```

### Annuler toutes les modifications non commitées
```bash
git checkout -- .
```

### Voir les différences avant de commiter
```bash
git -c core.pager=cat diff
```

### Voir l'historique d'un fichier spécifique
```bash
git -c core.pager=cat log --oneline -- [chemin/du/fichier]
```
