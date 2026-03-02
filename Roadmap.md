# 🗺️ Roadmap

> Dernière mise à jour : 2026-03-02

---

## Statuts

| Icône | Signification |
|-------|---------------|
| ✅ | Terminé |
| 🔄 | En cours / Partiellement implémenté |
| ⬜ | À faire |

---

## ✅ Fonctionnalité 2 — Suppression au clic long (Tantara)
**Objectif :** Permettre la suppression d'une ou plusieurs transactions dans l'onglet historique.

- Utilisation de `on_long_press` sur les `ListTile` dans `views/history.py`
- Mode Sélection avec Checkboxes au clic long
- Confirmation via `ft.AlertDialog` avant suppression du CSV
- Rafraîchissement automatique via `refresh_view()`

---

## ✅ Fonctionnalité 3 — Évolution du Schéma & Vue Tantara
**Objectif :** Étendre la structure de `expense.csv` et améliorer la lisibilité de l'historique.

- **Schéma CSV :** `date`, `categorie_flux`, `item`, `quantite`, `unite`, `prix_unitaire_mga`, `montant_total_mga`, `fournisseur_client`
- **Formulaire de saisie :** Champs Item, Quantité, Unité, Prix Unitaire, Fournisseur/Client — calcul automatique du total
- **Vue liste :** Affichage enrichi (ex: "Riz - 50kg"), groupement par Semaine / Mois / Année

---

## 🔄 Fonctionnalité 4 — Collecte de Données & Insights (Freemium)
**Objectif :** Créer un écosystème de données circulaires pour générer des statistiques de marché pour la communauté AMLG.

- ✅ **Consentement (Opt-in) :** Dialogue au premier lancement via `config.py`
- ⬜ **Agrégation locale :** Calculer des moyennes locales (ex: "Coût moyen du riz : X Ar") avant tout envoi — ne jamais exporter de données individuelles brutes
- ⬜ **Export Supabase :** Service dans `database.py` avec `supabase-py`
  - Variables requises : `SUPABASE_URL`, `SUPABASE_KEY` (dans `config.json`)
  - Données exportées : `[date, item, categorie, prix_moyen_calcule, code_postal_anonyme]`

---

## ⬜ Fonctionnalité 1 — Sélecteur de Langue (I18n)
**Objectif :** Permettre de basculer l'interface entre Malagasy, Français et Anglais.

- **Extraction :** Centraliser toutes les chaînes dans un dictionnaire (ex: `i18n.py`)
- **Composant UI :** `ft.PopupMenuButton` dans l'`AppBar` ou dans un onglet Paramètres
- **Persistance :** Sauvegarder la préférence dans `config.json`

---

## ⬜ Fonctionnalité 5 — Import du Journal Canteen (CSV Existant)
**Objectif :** Utiliser `Journal d'activité Canteen depuis 2025.csv` comme source de données initiale pour pré-remplir l'application avec l'historique réel de la cantine.

- **Compatibilité :** Le fichier CSV existant partage déjà le même schéma que `expense.csv` : `date`, `categorie_flux`, `item`, `quantite`, `unite`, `prix_unitaire_mga`, `montant_total_mga`, `fournisseur_client`
- **Import :** Ajouter une fonction d'import dans `database.py` qui lit le fichier source et fusionne les lignes dans `expense.csv` sans doublons (vérification par `date` + `item` + `montant_total_mga`)
- **UI :** Ajouter un bouton "Importer un fichier CSV" dans un onglet Paramètres avec un `ft.FilePicker`
- **Validation :** Vérifier la structure des colonnes avant import et afficher un résumé (ex: "243 lignes importées, 0 doublon ignoré")

---

## ⬜ Fonctionnalité 6 — Redesign de la Vue Tantara (inspiré WhatsApp)
**Objectif :** Retravailler le design de l'onglet historique (Tantara) en s'inspirant des captures WhatsApp pour une interface plus lisible et moderne.

- **Layout :** Adopter un style de liste à bulles/cartes avec séparation visuelle par date (en-têtes de jour)
- **Carte transaction :** Afficher clairement l'item, la quantité+unité, le montant en gras, et la catégorie avec un code couleur (Vente = vert, Achat_OPEX = rouge, Achat_CAPEX = orange)
- **Images de référence :** Importer les captures WhatsApp dans `Documentation/design_references/` pour servir de maquette
- **Composant :** Refactoriser `views/history.py` avec des `ft.Card` ou `ft.Container` stylisés au lieu des `ListTile` actuels

---

> [!IMPORTANT]
> **Modularité avant tout :** Chaque fonctionnalité doit être implémentée sans casser le `main.py` actuel. Utiliser des fonctions de service dans `database.py` ou de nouveaux fichiers dans `views/`.
