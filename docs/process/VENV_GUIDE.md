# Guide de Collaboration : Environnement Virtuel (venv)

Ce projet utilise un environnement virtuel Python pour isoler les dépendances. Pour éviter les erreurs liées aux chemins absolus (comme celles rencontrées lors du passage d'une machine à une autre), suivez ces étapes.

## ⚙️ Première Installation (ou Réparation)

Si vous venez de cloner le projet ou si vous rencontrez des erreurs de "ModuleNotFoundError", exécutez ces commandes à la racine du dossier `apk/` :

```bash
# 1. Supprimer l'ancien venv s'il existe
rm -rf venv

# 2. Créer le nouvel environnement
python3 -m venv venv

# 3. Mettre à jour pip et installer les dépendances
./venv/bin/python -m pip install --upgrade pip
./venv/bin/python -m pip install -r requirements.txt
```

## 🚀 Lancement de l'Application

### Mode Standard (Desktop)
```bash
./venv/bin/python main.py
```
*Note : Nécessite `libmpv1` sur votre système Linux.*

### Mode Navigateur (Recommandé pour les tests rapides)
Si vous avez des erreurs d'affichage ou de bibliothèque système :
```bash
./venv/bin/python main.py --web
```

## ⚠️ Règles d'Or pour le Vibe Coding
1. **Ne jamais committer le dossier `venv/`** sur GitHub.
2. Si vous installez une nouvelle bibliothèque, mettez à jour les dépendances :
   ```bash
   ./venv/bin/pip freeze > requirements.txt
   ```
3. Toujours utiliser le chemin `./venv/bin/python` pour garantir que vous utilisez les bonnes versions de Pandas et Flet.
