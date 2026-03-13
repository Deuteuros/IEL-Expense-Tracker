---
description: Comment manipuler les données CSV de l'Expense Tracker (import, export, migration, nettoyage)
---

# Workflow Données — Expense Tracker AMLG

## 📊 Structure des Données

### Fichier Principal : `expense.csv`
```
date,categorie_flux,item,quantite,unite,prix_unitaire_mga,montant_total_mga,fournisseur_client
```

### Catégories de Flux
| Valeur | Signification | Utilisé dans |
|--------|---------------|--------------|
| `Miditra` | Revenu (entrée) | Formulaire app |
| `Fandaniana` | Dépense (sortie) | Formulaire app |
| `Vente` | Vente directe | Journal Canteen CSV |
| `Achat_OPEX` | Achat opérationnel | Journal Canteen CSV |
| `Achat_CAPEX` | Investissement | Journal Canteen CSV |
| `Income` | (Ancien) Revenu | Anciennes données |
| `Expense` | (Ancien) Dépense | Anciennes données |

> **Important :** Le code doit toujours gérer les deux nomenclatures (anciennes + nouvelles).

---

## 📥 Importer des Données CSV Externes

### Vérifier la compatibilité d'un fichier source
// turbo
```bash
head -1 "/home/deuteuros/Documents/10 Projets/AMLG - Odoo - Cashew/Expense tracker/apk/Journal d'activité Canteen depuis 2025.csv"
```
Les colonnes doivent correspondre exactement au schéma ci-dessus.

### Import manuel via Python
```python
import pandas as pd

# Lire le fichier source
source = pd.read_csv("Journal d'activité Canteen depuis 2025.csv")

# Lire les données existantes
existing = pd.read_csv("expense.csv")

# Fusionner sans doublons
merged = pd.concat([existing, source]).drop_duplicates(
    subset=['date', 'item', 'montant_total_mga'],
    keep='first'
)

# Sauvegarder
merged.to_csv("expense.csv", index=False)
```

---

## 🔍 Analyses Rapides

### Voir le résumé des données
```python
import pandas as pd
df = pd.read_csv("expense.csv")
print(f"Total lignes: {len(df)}")
print(f"Période: {df['date'].min()} → {df['date'].max()}")
print(f"Catégories: {df['categorie_flux'].value_counts().to_dict()}")
print(f"Revenus: {df[df['categorie_flux'].isin(['Miditra', 'Vente', 'Income'])]['montant_total_mga'].sum():,.0f} Ar")
print(f"Dépenses: {df[df['categorie_flux'].isin(['Fandaniana', 'Achat_OPEX', 'Achat_CAPEX', 'Expense'])]['montant_total_mga'].sum():,.0f} Ar")
```

### Top 10 des items les plus coûteux
```python
df.groupby('item')['montant_total_mga'].sum().sort_values(ascending=False).head(10)
```

---

## 🧹 Nettoyage

### Supprimer les doublons
```python
df = pd.read_csv("expense.csv")
before = len(df)
df = df.drop_duplicates()
df.to_csv("expense.csv", index=False)
print(f"Supprimé {before - len(df)} doublons")
```

### Corriger les dates invalides
```python
df['date'] = pd.to_datetime(df['date'], errors='coerce')
invalid = df[df['date'].isna()]
print(f"{len(invalid)} dates invalides trouvées")
```

---

## ⚠️ Règles de Sécurité des Données

1. **Toujours faire une copie** avant de modifier `expense.csv` directement.
2. Ne jamais supprimer de données sans confirmation de l'utilisateur.
3. Les prix sont en **Ariary (MGA)** — pas de conversion de devises.
4. Les données du journal Canteen remontent à **octobre 2025**.
