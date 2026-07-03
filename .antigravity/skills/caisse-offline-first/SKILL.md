---
name: caisse-offline-first
description: Directives pour concevoir et développer une caisse mobile résiliente hors ligne (offline-first) sous Flutter.
---

# Skill: Caisse Offline-First

Ce skill définit les principes directeurs de développement d'applications financières déconnectées sous Flutter.

## DIRECTIVES D'ARCHITECTURE
1. **SSOT Locale (Single Source of Truth)** :
   * L'application doit toujours écrire et lire dans la base de données locale (SQLite/Drift).
   * L'interface utilisateur ne s'abonne qu'aux flux de la base de données locale (Stream queries).
2. **Synchronisation Asynchrone** :
   * Les requêtes de synchronisation réseau (Cashew API, Odoo API) doivent tourner en tâche de fond.
   * Utiliser une table de file d'attente (Outbox Pattern) pour enregistrer les mutations locales en attente d'envoi.
3. **Résilience et Sécurité** :
   * Toutes les transactions de caisse doivent être atomiques.
   * Gérer explicitement les conflits de synchronisation (par exemple, fusion par horodatage ou stratégie "Last-Write-Wins").

## PROTOCOLE DE REFACTORING / CODE
* Avant de modifier un modèle de données, créer une migration SQL valide.
* Ne jamais bloquer le thread UI avec des opérations d'E/S de base de données lourdes. Utiliser des isolats Dart ou des requêtes paginées.
