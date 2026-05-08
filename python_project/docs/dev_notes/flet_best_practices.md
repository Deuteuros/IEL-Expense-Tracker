# 📘 Guide des Bonnes Pratiques : Flet (Python) pour Cashew

Ce document sert de référence technique pour le développement du MVP Cashew afin d'éviter les erreurs d'implémentation et de garantir une UX premium.

---

## 1. Architecture des Vues (Multi-Page)
Flet utilise un modèle de navigation basé sur le `page.on_route_change` ou une gestion manuelle de conteneur.
- **Pratique recommandée** : Utiliser un `ft.Container` principal dans `main.py` dont on change le `content` dynamiquement lors de la navigation (NavigationBar).
- **Gestion d'état** : Pour partager des données entre les vues sans recharger les fichiers, utiliser une classe `State` globale ou passer des références d'objet lors de l'instanciation des vues.

## 2. Interface "WhatsApp-Like" (Tantara)
### Sélecteur de Mois
- **Contrôle** : `ft.ListView(horizontal=True, spacing=10, height=50)`.
- **Style** : Conteneurs avec `border_radius=20` et `bgcolor` variable selon la sélection.

### Groupement Quotidien
- **Logique** : Trier les transactions par date décroissante. Lors du rendu, comparer la date du message actuel avec celle du précédent. Si différente, insérer un `ft.Text` de séparation (ex: "Zoma 30 janoary").
- **Bulles de transaction** :
  - `ft.Container` avec `padding`, `border_radius` asymétrique (ou standard 15).
  - Icône circulaire pastel à gauche (CircleAvatar).
  - Montant aligné à droite, texte en gras.

## 3. Gestion des Données (CSV)
- **Bibliothèque** : Préférer `pandas` pour les lectures/écritures complexes (groupements, calculs de solde glissant) et le module `csv` standard pour les exports simples ultra-rapides.
- **Performance** : Ne jamais lire le fichier CSV à chaque rafraîchissement d'UI. Charger le DataFrame en mémoire au démarrage ou après un import, puis travailler sur la variable.

## 4. Esthétique Premium (Golden Green)
- **Couleurs** :
  - Seed Color : `ft.Colors.GREEN_700` ou `#2E7D32`.
  - Accents Dorés : `#FBC02D` ou `ft.Colors.AMBER_600`.
- **Material 3** : Toujours activer `use_material3=True` dans `ft.Theme`.
- **Typographie** : Utiliser des poids de police (Weight) différenciés au lieu d'augmenter drastiquement la taille.

## 5. Localisation (Malagasy)
- **Fichier de langue** : Centraliser les chaînes dans un dictionnaire ou via le skill `Translator-MG`.
- **Encodage** : Toujours spécifier `encoding='utf-8'` lors des manipulations de fichiers pour supporter les caractères spécifiques (même si le Malagasy standard n'en a pas beaucoup de complexes, c'est une sécurité).

---

## 📄 Référence de Code (Widget WhatsApp Bubble)
```python
def TransactionBubble(item, montant, is_depense=True):
    return ft.Container(
        content=ft.Row([
            ft.CircleAvatar(content=ft.Icon(ft.Icons.SHOPPING_BAG if is_depense else ft.Icons.ADD)),
            ft.Column([
                ft.Text(item, weight="bold"),
                ft.Text("Smally details...", size=12, color=ft.Colors.GREY_600),
            ], expand=True),
            ft.Text(
                f"{'-' if is_depense else '+'} {montant:,} Ar",
                color=ft.Colors.RED if is_depense else ft.Colors.GREEN,
                weight="bold"
            )
        ]),
        padding=10,
        bgcolor=ft.Colors.WHITE,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=2, color=ft.Colors.with_opacity(0.1, ft.Colors.BLACK))
    )
```
