# MVP : Cashew - Consulting Edition (IEL)

## 📌 Vision Stratégique
Le logiciel Cashew n'est plus un outil de saisie autonome, mais un **tableau de bord de restitution** pour le service de consulting de l'**ISS Economics Lab (IEL)**. 
- **Entrée** : Données auditées et transcrites en CSV par l'IEL durant la mission.
- **Sortie** : Application mobile intuitive pour le suivi de la santé financière de l'AGR.

## 🛠️ Fonctionnalités Prioritaires (MVP)

### 1. Import & Structure des Données
- **Bouton d'import CSV** : Permet de charger le fichier de données préparé par le consultant IEL.
- **Conformité au [DATA_SCHEMA]** : Utilisation stricte des colonnes (Désignation, Qté, Unité, Prix, Date).
- **Mode Lecture Seule** : Priorité à la consultation des données certifiées.

### 2. Vue "Tantara" (Historique Mensuel)
- **Navigation par Mois** : Sélecteur permettant de basculer entre les mois (ex: Janvier 2026, Février 2026).
- **Groupement Quotidien** : Affichage des transactions sous forme de bulles (type WhatsApp) groupées par jour.

### 3. Vue "Témoin" (Analyse de Performance)
- **Fenêtre Glissante de 30 Jours** : Affichage dynamique des données entre `J` (aujourd'hui) et `J-30`.
- **Indicateur de Caisse** : Évolution du solde de caisse sur l'intervalle glissant.
- **Recalcul Quotidien** : La fenêtre se déplace automatiquement chaque jour pour une vision temps réel de la tendance.

## 🎨 Interface & UX
- **Langue** : Localisation intégrale en **Malagasy**.
- **Design** : "WhatsApp-like" pour maximiser l'adoption par les clients locaux.
- **Framework** : Flet (Python) - Mobile First / Offline First.

## 🚫 Exclusions du MVP
- Synchronisation Cloud (Supabase).
- Saisie manuelle complexe (priorité à l'import IEL).
- Sélecteur de langue bilingue.
