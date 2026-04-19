# Schéma de Données : IEL - Expense Tracker

Ce document définit la structure des données pour l'écosystème IEL, inspirée du schéma Drift ORM de Cashew, mais adaptée pour une persistance locale via CSV et une extension modulaire.

## 1. Persistance : Format CSV
Le fichier principal est \`expenses.csv\`. Chaque ligne représente une transaction financière ou un flux de stock.

| Colonne | Type | Description | Référence Cashew |
|---------|------|-------------|------------------|
| \`date\` | ISO8601 | Date et heure de l'opération | \`dateCreated\` |
| \`categorie_flux\` | Enum | "Achat", "Vente", "Perte", "Correction" | \`income\` (mapping) |
| \`item\` | String | Désignation du produit ou service | \`name\` |
| \`quantite\` | Float | Volume ou nombre d'unités | N/A (IEL Extension) |
| \`unite\` | String | kg, litre, pièce, sac, etc. | N/A (IEL Extension) |
| \`prix_unitaire\` | Float | Prix pour une unité | N/A (Calculé) |
| \`montant_total\` | Float | Valeur totale (Qté * PU) | \`amount\` |
| \`tiers\` | String | Nom du fournisseur ou client | \`note\` / \`associatedTitle\` |
| \`portefeuille\` | UUID | Identifiant du compte (Cash, Mobile Money) | \`walletFk\` |
| \`module_tag\` | String | Tag pour extension (ex: "culinary_cogs") | N/A |

## 2. Énumérations & Standards

### Catégories de Flux
- **Achat** : Sortie d'argent / Entrée de stock (Signe négatif sur montant).
- **Vente** : Entrée d'argent / Sortie de stock (Signe positif sur montant).
- **Perte** : Ajustement de stock sans contrepartie financière.
- **Correction** : Ajustement de solde portefeuille.

### Unités de Mesure Standard (IEL)
- \`u\` : Unité / Pièce
- \`kg\` : Kilogramme
- \`l\` : Litre
- \`sac\` : Sac (standardiser le poids en note si besoin)
- \`pot\` : Format local (ex: pot de yaourt ou lait)

## 3. Logique de Calcul
- **Montant Total** : \`quantite * prix_unitaire\`. En cas de saisie manuelle du montant total, le \`prix_unitaire\` est déduit : \`montant_total / quantite\`.
- **COGS (Cost of Goods Sold)** : Le module Culinary utilise les lignes "Achat" pour calculer le prix de revient moyen pondéré.

## 4. Mapping de Migration (Cashew -> IEL)
| Cashew Table | IEL Column | Note |
|--------------|------------|------|
| \`Transactions.name\` | \`item\` | |
| \`Transactions.amount\` | \`montant_total\` | Inverser signe si \`income\` est false |
| \`Transactions.dateCreated\` | \`date\` | |
| \`Wallets.name\` | \`portefeuille\` | Utiliser le nom ou l'ID |
