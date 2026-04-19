---
description: Comment développer une fonctionnalité pour l'Expense Tracker IEL (Flet Python)
---

# Workflow Développement — Expense Tracker IEL

> Ce workflow guide l'agent IA pour implémenter une fonctionnalité dans l'Expense Tracker. L'utilisateur travaille en mode **Vibe Coding** — il décrit ce qu'il veut, l'agent code.

## ⚠️ Règles Absolues

1. **Framework :** Flet 0.80.2 (Python). **Ne pas migrer** vers une version plus récente.
2. **Bug connu :** `ft.SegmentedButton` ne fonctionne pas en Flet 0.80.2. Utiliser le composant custom `components/segmented_control.py` (`CustomSegmentedControl`).
3. **Interface en Malagasy** par défaut (labels, boutons, titres). Exemples : "Tantara" = Historique, "Miditra" = Entrée, "Fandaniana" = Dépense, "Kisary" = Graphique, "Temoin" = Résumé.
4. **Pas de serveur distant** : pas de `git push/pull`, pas d'API externe (sauf Supabase si explicitement demandé).
5. **Modularité** : chaque vue dans `views/`, logique de données dans `database.py`, config dans `config.py`.

---

## 📁 Architecture du Projet

```
apk/
├── main.py              # Point d'entrée, navigation, dialogue de saisie
├── database.py          # Lecture/écriture CSV via Pandas
├── config.py            # Config JSON (consent, préférences)
├── requirements.txt     # flet==0.80.2, flet-charts, pandas, plotly, kaleido
├── expense.csv          # Données de production
├── config.json          # Fichier de configuration utilisateur
├── components/
│   └── segmented_control.py  # Composant custom (remplacement SegmentedButton)
├── views/
│   ├── summary.py       # Vue d'accueil (Temoin) — solde, revenus, dépenses
│   ├── history.py       # Vue historique (Tantara) — liste, filtres, suppression
│   └── charts.py        # Vue graphique (Kisary) — courbes cumulatives
├── Documentation/       # Guides markdown et org-mode
└── Roadmap.md           # Fonctionnalités à implémenter
```

---

## 🔧 Étapes de Développement

### 1. Consulter la Roadmap
```bash
cat Roadmap.md
```
Identifier la fonctionnalité à implémenter et son statut.

### 2. Comprendre le code existant
- Lire `main.py` pour la structure de navigation et le dialogue de saisie.
- Lire `database.py` pour les fonctions de données (CSV).
- Lire le fichier de vue concerné dans `views/`.

### 3. Implémenter
- **Nouvelle vue ?** → Créer `views/nouvelle_vue.py` avec une fonction `get_xxx_view()`.
- **Modification de vue ?** → Éditer le fichier dans `views/`.
- **Nouveau service données ?** → Ajouter dans `database.py`.
- **Nouvelle config ?** → Ajouter via `config.update_config()` / `config.get_config()`.

### 4. Tester
// turbo
```bash
cd "/home/deuteuros/Documents/10 Projets/Applied MicroEconomics Learning Group/IEL - Expense tracker/apk"
./venv/bin/python main.py --web
```
- Vérifier dans le navigateur à `http://localhost:PORT` (le port est affiché dans le terminal).
- Tester la fonctionnalité.
- Vérifier qu'il n'y a pas de régression sur les autres vues.

### 5. Commiter (voir workflow /git)
```bash
git add .
git -c core.pager=cat commit -m "feat: description de la fonctionnalité"
```

### 6. Mettre à jour la Roadmap
- Changer le statut de ⬜ à ✅ dans `Roadmap.md`.

---

## 🧩 Patterns Importants

### Schéma CSV (`expense.csv`)
```
date,categorie_flux,item,quantite,unite,prix_unitaire_mga,montant_total_mga,fournisseur_client
```
- `categorie_flux` : `Miditra` (revenu), `Fandaniana` (dépense), `Achat_OPEX`, `Achat_CAPEX`, `Vente`
- Les anciennes données utilisent aussi `Income` / `Expense` — le code doit gérer les deux.

### Navigation (3 onglets)
```python
# Dans main.py, la fonction navigate() gère les onglets :
# index 0 → get_summary_view()     (Temoin)
# index 1 → get_history_view(page) (Tantara)
# index 2 → get_charts_view()      (Kisary)
```

### Rafraîchissement global
```python
# Appeler page.refresh_view() pour rafraîchir la vue active
if hasattr(page, "refresh_view"):
    page.refresh_view()
```

### Dialogue modale
```python
dialog = ft.AlertDialog(
    title=ft.Text("Titre"),
    content=ft.Column([...]),
    actions=[ft.FilledButton("Action", on_click=callback)],
)
page.overlay.append(dialog)
dialog.open = True
page.update()
```
