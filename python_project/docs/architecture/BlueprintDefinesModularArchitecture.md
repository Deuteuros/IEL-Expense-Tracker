# Blueprint : IEL - Expense Tracker

## Overview
Recréation modulaire de l'application Cashew pour l'écosystème IEL.
- **Goal** : Transformer la saisie de dépenses en intelligence économique.
- **Constraint** : Offline-first, interface mobile-first intuitive.

## Stack Technique
- **Framework** : Flet (Python)
- **Data** : CSV Local (transition vers Supabase planifiée)
- **UI** : Material 3 "Golden Green"

## Data Schema (Standard)
| Champ | Description |
|-------|-------------|
| date | Date de l'opération |
| categorie | Type de flux (Achat/Vente) |
| item | Désignation |
| quantite | Volume |
| unite | Unité de mesure |
| prix_unitaire | Prix par unité |
| montant_total | Calcul auto (Qté * PU) |
| tiers | Fournisseur ou Client |

## Directives d'Implémentation
1. **Modularité** : Chaque vue doit être un composant indépendant dans \`views/\`.
2. **I18n** : Priorité au Malagasy, utiliser des clés de traduction.
3. **UX** : Design "WhatsApp-like" pour l'historique (Tantara).
