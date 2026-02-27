# Roadmap des Nouvelles Fonctionnalités & Guidage IA

Ce document définit les prochaines étapes de développement. Chaque section contient des instructions précises pour l'agent IA en charge de l'implémentation.

## 1. Sélecteur de Langue (I18n)
**Objectif :** Permettre de basculer l'interface entre le Malagasy, le Français et l'Anglais.

### 🤖 Instructions pour l'Agent :
- **Extraction :** Déplacer toutes les chaînes de caractères codées en dur (hardcoded) vers un dictionnaire centralisé (ex: `i18n.py`).
- **Composant :** Ajouter un `ft.PopupMenuButton` dans la barre d'application (`AppBar`) ou un onglet de paramètres.
- **Persistance :** Sauvegarder la préférence de langue dans un fichier de configuration local (`config.json`) pour qu'elle persiste au redémarrage.

## 2. Suppression au clic long (Tantara)
**Objectif :** Permettre la suppression d'une ou plusieurs transactions dans l'onglet historique.

### 🤖 Instructions pour l'Agent :
- **Interaction :** Utiliser la propriété `on_long_press` des `ListTile` dans `views/history.py`.
- **UI :** Lors d'un clic long, passer en "Mode Sélection" (afficher des Checkboxes).
- **Confirmation :** Afficher un `ft.AlertDialog` avant de supprimer définitivement les lignes du CSV.
- **Rafraîchissement :** Appeler `refresh_view()` après la suppression.

## 3. Évolution du Schéma & Vue Tantara
**Objectif :** Étendre la structure de `expense.csv` et améliorer la lisibilité de l'historique.

### 🤖 Instructions pour l'Agent :
- **Migration du Schéma :** 
    - Colonnes : `"date"`, `"categorie_flux"`, `"item"`, `"quantite"`, `"unite"`, `"prix_unitaire_mga"`, `"montant_total_mga"`, `"fournisseur_client"`.
- **Interface de Saisie (Formulaire) :**
    - Ajouter des `ft.TextField` pour : **Item (Nom)**, **Quantité**, **Unité (kg, l, sac, etc.)**, **Prix Unitaire**, **Fournisseur/Client**.
    - Calculer automatiquement `montant_total_mga` (Quantité x Prix Unitaire) lors de la saisie.
- **Vue Liste (Tantara) :**
    - **Affichage :** Chaque ligne doit maintenant afficher l'item, la quantité et l'unité (ex: "Riz - 50kg").
    - **Groupement :** Ajouter un bouton de filtrage/groupement pour organiser la liste par **Semaine**, **Mois** ou **Année** (utiliser Pandas `.groupby()` ou un tri par date).

## 4. Collecte de Données & Insights (Modèle Freemium)
**Objectif :** Créer un écosystème de données circulaires où l'usage gratuit de l'app permet de générer des statistiques de marché pour la communauté AMLG.

### 🤖 Instructions pour l'Agent :
- **Consentement (Opt-in) :** Ajouter un écran "Conditions d'Utilisation" ou une case à cocher dans les paramètres pour activer la collecte. L'utilisateur doit savoir que ses données anonymisées aident à stabiliser l'économie locale.
- **Agrégation Prioritaire :** Toute donnée collectée doit être agrégée localement (ex: "Coût moyen du riz à Antananarivo : X Ar") avant tout export. Ne jamais collecter de noms, d'adresses précises ou de montants individuels bruts.
- **Architecture de "Don Manuel" :** Ajouter un bouton "Contribuer à la base de prix AMLG" qui exporte un JSON anonymisé contenant uniquement : `[Date, Item, Catégorie, Prix Unitaire]`.
- **Valeur Ajoutée (Freemium BI) :** Prévoir un module "Insights du Marché" qui affiche à l'utilisateur les prix moyens collectés par les autres membres de la communauté (benchmarking) en remerciement de sa contribution.

---
> [!IMPORTANT]
> **Modularité avant tout :** Chaque fonctionnalité doit être implémentée sans casser le `main.py` actuel. Utilisez des fonctions de service dans `database.py` ou de nouveaux fichiers dans `views/`.
