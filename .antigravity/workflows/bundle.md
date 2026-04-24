---
description: Comment créer et importer des bundles Git pour partager le projet via USB
---

# Workflow Bundles Git — Partage USB

> L'équipe travaille **hors-ligne**. Les échanges de code se font via des fichiers `.bundle` sur clé USB.

## 📦 Créer un Bundle de Distribution

### Bundle complet (pour un nouveau collaborateur ou redistribution)
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
git -c core.pager=cat bundle create "../expense_tracker_vX.bundle" --all
```
> Remplacer `vX` par le numéro de version approprié. Vérifier le dernier bundle existant :
// turbo
```bash
ls -lh "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/"*.bundle
```

### Bundle d'une branche feature (pour envoyer une feature à l'intégrateur)
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
git -c core.pager=cat bundle create "../[nom_tache].bundle" master..feat-[nom-branche]
```

### Vérifier un bundle
// turbo
```bash
git -c core.pager=cat bundle verify "/chemin/vers/fichier.bundle"
```

---

## 📥 Importer un Bundle

### D'un collaborateur (feature branch)
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
git remote add collegue /chemin/vers/fichier.bundle
git -c core.pager=cat fetch collegue
git checkout master
git -c core.pager=cat merge collegue/feat-[nom-branche]
git remote remove collegue
```

### Mettre à jour depuis un bundle master (en tant que collaborateur)
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
git remote add update /chemin/vers/expense_tracker_vX.bundle
git -c core.pager=cat fetch update master
git checkout master
git -c core.pager=cat merge update/master
git remote remove update
```

---

## ⚠️ Règles

- **Toujours commiter** les changements locaux AVANT d'importer un bundle externe.
- Si le bundle fait plus de **300 Mo**, vérifier que des fichiers volumineux (images, venv) ne sont pas dans l'historique git.
- Le fichier `.bundle` généré se trouve dans le dossier **parent** (`Expense tracker/`), pas dans `apk/`.
- **Nommage :** `expense_tracker_v1.bundle`, `expense_tracker_v2.bundle`, etc.
