# Spécifications : Redesign de la Vue Tantara

Ce document définit le nouveau format visuel de l'onglet **Tantara** (Historique), inspiré des maquettes WhatsApp.

## 📅 1. Sélecteur de Mois (Panneau supérieur)
Au lieu d'un sélecteur vertical ou de simples onglets, nous utiliserons une liste horizontale défilante :
- **Format** : Texte du mois (ex: "janvier") avec l'année en petit en dessous si nécessaire.
- **Indicateur** : Une barre de soulignement épaisse (Material 3 style) sous le mois actif.
- **Interaction** : Le changement de mois filtre dynamiquement les données du CSV.

## 💰 2. Barre de Résumé Mensuel
Directement sous le sélecteur, une barre récapitulative affiche les flux du mois sélectionné :
- **Structure** : `[🔽 Total Dépenses]  [🔼 Total Entrées] = [Total Net]`
- **Couleurs** : Rouge pour les dépenses (MGA), Vert pour les entrées, Noir/Gris pour le net.
- **Style** : Conteneur arrondi avec un fond légèrement teinté (bleu très clair).

## 📊 3. Regroupement par Jours
L'historique n'est plus une liste continue mais une succession de blocs quotidiens.

### En-tête de Jour
- **Gauche** : Date complète en minuscules (ex: "vendredi 30 janvier").
- **Droite** : Solde net de la journée (ex: "697 700 MGA") en gris foncé.
- **Séparation** : Une ligne fine ou un espacement clair entre les jours.

### Carte Transaction
- **Icône** : Utilisation de `CircleAvatar` avec des couleurs pastel et des icônes thématiques (Bus pour transport, Sac pour courses, etc.).
- **Titre** : Nom de l'item en gras.
- **Sous-titre** : Détails (Quantité/Unité ou Fournisseur).
- **Montant** : Aligné à droite, en gras, avec un symbole de couleur (`-` rouge pour dépense, `+` vert pour entrée).

## 🛠️ 4. Refactoring Technique
- **Composant** : Passer de `ListTile` standards à des `Container` ou `Card` personnalisés pour un contrôle total sur le padding et les polices.
- **Performance** : Utilisation de Pandas pour le groupement par date (`df.groupby(df['date'].dt.date)`).
- **Compatibilité** : Maintenir le support du "Mode Sélection" (clic long) intégré dans le nouveau design.
