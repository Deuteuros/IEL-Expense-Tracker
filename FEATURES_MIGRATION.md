# Spécifications de Migration : Python -> Flutter

Ce document sert de base de connaissances pour la réécriture du projet "IEL - Expense tracker" en Dart/Flutter.

## 1. Structure des Données (SQLite)

La base de données actuelle est `data/cashew.db`. Elle contient deux tables principales :

### Table `wallets`
| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Clé primaire |
| `name` | TEXT | Nom du portefeuille (ex: 'Caisse') |
| `balance` | REAL | Solde actuel |

### Table `transactions`
| Colonne | Type | Description |
| :--- | :--- | :--- |
| `id` | INTEGER | Clé primaire |
| `date` | TEXT | Date au format `YYYY-MM-DD` |
| `categorie_flux` | TEXT | Type : 'Miditra' (Entrée), 'Fandaniana' (Dépense), 'Vente', 'Achat' |
| `item` | TEXT | Nom de l'article |
| `quantite` | REAL | Quantité |
| `unite` | TEXT | Unité (kg, l, etc.) |
| `prix_unitaire` | REAL | Prix par unité |
| `montant_total_mga` | REAL | Montant total en Ariary |
| `fournisseur_client` | TEXT | Nom du client ou fournisseur |
| `portefeuille_id` | INTEGER | Clé étrangère vers `wallets(id)` |

---

## 2. Fonctionnalités à Implémenter

### A. Navigation (3 Onglets)
1.  **Témoin (Dashboard/Summary)** :
    *   Affichage du solde total (Revenus - Dépenses).
    *   Graphique d'évolution du solde sur les 30 derniers jours.
    *   Top 5 des dépenses par item.
2.  **Tantara (History)** :
    *   Liste des transactions groupées par mois.
    *   Filtre par mois.
3.  **Fikirakirana (Management)** :
    *   Import/Export CSV.
    *   Configuration des portefeuilles (Wallets).

### B. Ajout de Transaction (FAB - Floating Action Button)
*   **Saisie rapide** : Calcul automatique du `montant_total` (`quantite` * `prix_unitaire`).
*   **Validation** : Empêcher l'ajout si les champs obligatoires sont vides.
*   **Feedback** : Utilisation de SnackBar pour confirmer l'ajout.

### C. Utilitaires
*   **Formatage des nombres** : Séparateur de milliers (espace) pour les Ariary (ex: `10 000 Ar`).
*   **Consentement** : Boîte de dialogue au premier lancement ("Fepetra fampiasana").

---

## 3. Assets & Design
*   **Couleurs** : Thème principal basé sur le vert (`green`).
*   **Icônes** : Material Icons (Home, History, Settings).
*   **Logo** : Utiliser l'image `assets/icon.png`.

---

## 4. Stack Flutter Recommandée
*   **State Management** : Riverpod.
*   **Database** : `sqflite` (avec `path_provider`).
*   **UI** : Material 3.
*   **Charts** : `fl_chart`.
*   **Files** : `file_picker`, `csv`.
