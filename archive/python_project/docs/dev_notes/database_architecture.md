# Architecture de la Base de Données (Hybride SQLite/CSV)

Ce document détaille la structure interne de persistance pour l'application Cashew.

## 🏗️ Modèle de Données (SQLite)

La base `cashew.db` contient trois tables principales pour assurer la rapidité des calculs et la gestion multi-portefeuille (Wallet).

### Table : `wallets`
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique. |
| `name` | TEXT | Nom du compte (ex: "Caisse", "Mobile Money"). |
| `type` | TEXT | Type de compte. |
| `balance` | REAL | Solde actuel (calculé ou stocké). |

### Table : `transactions`
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique. |
| `date` | TEXT | Date au format ISO8601 (`YYYY-MM-DD`). |
| `categorie_flux` | TEXT | Achat, Vente, Perte, Correction. |
| `item` | TEXT | Désignation du produit/service. |
| `quantite` | REAL | Volume. |
| `unite` | TEXT | Unité de mesure (kg, l, u). |
| `prix_unitaire` | REAL | Prix unitaire. |
| `montant_total` | REAL | Valeur totale transaction. |
| `tiers` | TEXT | Client ou Fournisseur. |
| `wallet_id` | INTEGER | FK vers `wallets.id`. |

## 🔄 Mécanisme de Synchronisation

1. **Import CSV** :
   - Lecture du fichier `expense.csv` via Pandas.
   - Nettoyage des données (doublons, formats de date).
   - Insertion massive dans SQLite (TRUNCATE then INSERT ou Upsert).

2. **Écriture (Ajout Manuel)** :
   - Insertion immédiate dans SQLite.
   - Append asynchrone ou immédiat dans le fichier `expense.csv` pour garantir la persistance "portable".

3. **Calculs (Analyses)** :
   - Toutes les fonctions `get_summary()`, `get_charts()` interrogent SQLite.
   - Utilisation de `strftime` SQL pour extraire les mois présents et filtrer les données.

## 🛠️ Avantages
- **Performance** : Les graphiques (Pie, Line) sont calculés en SQL, beaucoup plus rapide que de parcourir un CSV.
- **Robustesse** : Moins de risques de corruption de fichier lors d'écritures concurrentes.
- **Mobilité** : SQLite est le standard mobile, facilitant une future compilation APK.
