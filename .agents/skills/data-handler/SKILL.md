---
name: Data Handler
description: Gestionnaire de données CSV structurées pour Cashew (IEL). Assure le respect du DATA_SCHEMA et l'intégrité des transactions financières.
---

# 📊 Instructions : Data Handler

Ce skill permet à l'agent de manipuler, valider et auditer les fichiers de données du projet Cashew.

## 📋 Règles d'or
1. **Conformité au Schéma** : Toute opération d'écriture doit respecter les colonnes suivantes : `date`, `categorie`, `item`, `quantite`, `unite`, `prix_unitaire`, `montant_total`, `tiers`.
2. **Types de données** :
   - `date` : Format ISO `YYYY-MM-DD`.
   - `quantite`, `prix_unitaire`, `montant_total` : Doivent être des nombres (float/int).
3. **Immutabilité des audits** : Ne jamais supprimer de données sans confirmation explicite. Préférer le "marquage" si nécessaire.

## 🛠️ Actions supportées
- **Audit de fichier client** : Analyser un CSV brut pour détecter les erreurs de saisie ou les types de données incorrects.
- **Conversion** : Transformer des données hétérogènes vers le format `DATA_SCHEMA`.
- **Calcul de Caisse** : Calculer le solde net sur une période donnée (ex: les 30 derniers jours pour la vue Témoin).

## 📄 Référence
Voir `docs/architecture/DATA_SCHEMA.md` pour les détails techniques.
