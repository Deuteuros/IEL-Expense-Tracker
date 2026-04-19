---
description: Comment lancer, tester et déboguer l'Expense Tracker IEL
---

# Workflow Lancement & Debug — Expense Tracker IEL

## 🚀 Lancer l'Application

### Mode Web (recommandé si `libmpv` absent)
// turbo
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
./venv/bin/python main.py --web
```

### Mode Desktop
// turbo
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
./venv/bin/python main.py
```

---

## 🔧 Environnement Virtuel

### Vérifier que le venv existe
// turbo
```bash
ls "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk/venv/bin/python"
```

### Recréer le venv si nécessaire
```bash
cd "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk"
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

### Installer un nouveau package
```bash
./venv/bin/pip install [package]
```
> **Penser à mettre à jour `requirements.txt`** après installation.

---

## 🐛 Debug Courant

### L'app ne démarre pas
1. Vérifier les erreurs dans le terminal.
2. Vérifier que `expense.csv` existe et a le bon format (8 colonnes).
3. Si erreur `libmpv` → utiliser le mode `--web`.

### Erreur CSV / Pandas
1. Vérifier le contenu de `expense.csv` :
// turbo
```bash
head -5 "/home/deuteuros/Documents/10 Projets/IEL - Applied Microeconomics Learning Group/IEL - Expense tracker/apk/expense.csv"
```

2. Format attendu des colonnes :
```
date,categorie_flux,item,quantite,unite,prix_unitaire_mga,montant_total_mga,fournisseur_client
```

### Erreur SegmentedButton
- **Ne pas utiliser `ft.SegmentedButton`** — il est buggé en Flet 0.80.2.
- Utiliser à la place :
```python
from components.segmented_control import CustomSegmentedControl, Segment
```

### Vérifier les processus Flet en cours
// turbo
```bash
ps aux | grep "main.py"
```

### Tuer un processus Flet bloqué
```bash
pkill -f "main.py"
```
