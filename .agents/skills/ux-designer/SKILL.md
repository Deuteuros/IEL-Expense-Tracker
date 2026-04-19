---
name: UX Designer
description: Expert UI/UX pour Cashew (Flet/Material 3). Applique le design "WhatsApp-like" et "Golden Green".
---

# 🎨 Instructions : UX Designer (Flet)

Ce skill permet à l'agent de concevoir et d'implémenter des interfaces utilisateur mobiles-first avec le framework Flet.

## 📋 Directives de Design
1. **Couleurs (Golden Green)** : Priorité aux tons naturels (vert forêt, doré subtil, beige/blanc cassé).
2. **Style WhatsApp-like** :
   - Historique groupé par jours dans des blocs séparés.
   - Utilisation de `CircleAvatar` colorés pour les icônes de transaction.
   - Navigation simplifiée via une barre d'onglets en bas (BottomNavigationBar).
3. **Material 3** : Respecter les standards Google Material Design pour les cartes, boutons et sélecteurs.

## 🛠️ Actions supportées
- **Refactoring UI** : Transformer une liste classique en une vue structurée par jours.
- **Sélecteur de Mois** : Implémenter la liste horizontale défilante pour le mois actif.
- **Barre de Résumé** : Créer le conteneur arrondi `[🔽 Total Dépenses] [🔼 Total Entrées] = [Total Net]`.

## 📄 Référence
Voir `docs/architecture/tantara_redesign_spec.md` pour le détail des vues.
