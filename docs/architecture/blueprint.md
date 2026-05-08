# Blueprint : CaisseCash (IEL)

## Overview
Application modulaire de gestion de flux financiers pour l'écosystème ISS Economics Lab (IEL).
- **Objectif** : Transformer la saisie brute en intelligence économique actionnable.
- **Contraintes** : Offline-first, interface mobile-first intuitive, performance native.

## Stack Technique
- **Framework** : Flutter (Dart)
- **State Management** : Riverpod (Gestion réactive et découplage)
- **Data** : SQLite (via `sqflite` et `sqflite_common_ffi` pour le Desktop)
- **UI** : Material 3 "Outfit Design" (typographie Outfit, couleurs harmonieuses)

## Architecture du Projet
- `lib/models/` : Définition des structures de données (Transactions, Portefeuilles).
- `lib/services/` : Logique d'accès aux données (DatabaseHelper, Import/Export).
- `lib/providers/` : Couche de gestion d'état et logique métier asynchrone.
- `lib/views/` : Composants d'interface (Témoin, Tantara, Fikirakirana).
- `lib/widgets/` : Composants UI réutilisables (Graphiques, Dialogues).

## Principes Directeurs
1. **Performance Native** : Utilisation de Flutter pour une fluidité maximale sur Android et Desktop.
2. **Localisation Malagasy** : Interface pensée en Malagasy par défaut.
3. **UX Intuitive** : Historique "WhatsApp-like" groupé par jour pour une lecture naturelle.
4. **Data Integrity** : Import CSV robuste avec validation des schémas.
