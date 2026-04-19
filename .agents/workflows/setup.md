---
description: Comment installer le projet Expense Tracker sur un nouveau PC (collaborateur)
---

# Workflow Installation — Expense Tracker IEL

> Ce workflow est pour installer le projet sur le PC d'un **nouveau collaborateur** à partir d'un bundle Git.

## 📋 Prérequis

- Python 3.10+ installé
- Un fichier `expense_tracker_vX.bundle` (fourni par l'intégrateur sur clé USB)

---

## 🚀 Installation Pas à Pas

### 1. Créer le dossier de travail
```bash
mkdir -p "/home/$USER/Documents/Expense Tracker"
cd "/home/$USER/Documents/Expense Tracker"
```

### 2. Cloner depuis le bundle
```bash
git clone /chemin/vers/expense_tracker_vX.bundle apk
cd apk
```

### 3. Créer l'environnement virtuel
```bash
python3 -m venv venv
```

### 4. Installer les dépendances
```bash
./venv/bin/pip install -r requirements.txt
```

### 5. Vérifier l'installation
// turbo
```bash
./venv/bin/python -c "import flet; print(f'Flet {flet.version}')"
```

### 6. Lancer l'application
// turbo
```bash
./venv/bin/python main.py --web
```

---

## 🔧 Résolution de Problèmes

### Erreur `libmpv`
→ Utiliser le mode web : `./venv/bin/python main.py --web`

### Erreur `ModuleNotFoundError`
→ Vérifier que le venv est utilisé : `./venv/bin/pip list`

### Le bundle ne se clone pas
→ Vérifier la validité : `git -c core.pager=cat bundle verify /chemin/vers/fichier.bundle`

---

## 🌿 Après Installation : Commencer à Développer

1. Créer une branche feature : `git checkout -b feat-[nom]`
2. Développer avec l'agent IA (voir workflow `/dev`)
3. Quand terminé, créer un bundle pour l'intégrateur (voir workflow `/bundle`)
