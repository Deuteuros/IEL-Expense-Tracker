# Architecture de la Base de Données (CaisseCash)

Ce document détaille la structure de persistance pour l'application Flutter **CaisseCash**.

## 🏗️ Modèle de Données (SQLite)

L'application utilise SQLite via le package `sqflite` (Android) et `sqflite_common_ffi` (Linux/Desktop).

### Table : `wallets`
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique. |
| `name` | TEXT | Nom du compte (ex: "Caisse", "Banque"). |
| `balance` | REAL | Solde actuel stocké. |

### Table : `transactions`
| Colonne | Type | Description |
|---------|------|-------------|
| `id` | INTEGER (PK) | Identifiant unique. |
| `date` | TEXT | Date au format `YYYY-MM-DD`. |
| `categorie_flux` | TEXT | Type : 'Miditra' (Revenu), 'Fandaniana' (Dépense), 'Vente', 'Achat'. |
| `item` | TEXT | Désignation du produit/service. |
| `quantite` | REAL | Volume. |
| `unite` | TEXT | Unité de mesure (kg, l, u). |
| `prix_unitaire` | REAL | Prix unitaire. |
| `montant_total_mga` | REAL | Montant total en Ariary. |
| `fournisseur_client` | TEXT | Nom du tiers. |
| `portefeuille_id` | INTEGER | FK vers `wallets.id`. |

## 🔄 Mécanismes Clés

1. **Initialisation Desktop** : 
   - Sur Linux, le moteur SQLite est initialisé manuellement via `sqfliteFfiInit()` dans `main.dart`.
   - La base de données est stockée dans le répertoire local de l'application.

2. **Import CSV** :
   - Lecture via le package `csv`.
   - Détection automatique du BOM UTF-8 et des séparateurs (`,` ou `;`).
   - Mapping dynamique des portefeuilles par nom pour garantir l'intégrité entre le CSV et la DB locale.

3. **Calculs & Performance** :
   - Les totaux mensuels et les données de graphiques sont calculés via des requêtes SQL brutes (`SUM`, `GROUP BY`) pour une performance optimale même avec des milliers de transactions.

## 🛠️ Avantages de la Stack Flutter
- **Portabilité native** : Le même code SQL fonctionne sur Linux et Android.
- **Réactivité** : L'utilisation de `riverpod` permet de rafraîchir l'interface dès qu'une modification est faite en base de données.
