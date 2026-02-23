# Guide : Partage du Projet via Clé USB (Git Bundle)

Ce guide explique comment partager les progrès du projet sans utiliser Internet ou GitHub, en utilisant un fichier "bundle" Git.

## 📤 1. Sur la machine de l'EXPÉDITEUR
*(Celui qui a fait les modifications et veut les partager)*

### Étape A : Initialiser le dépôt (si ce n'est pas déjà fait)
```bash
cd "/home/deuteuros/Documents/10 Projets/AMLG - Odoo - Cashew/Expense tracker/apk"
git init
git add .
git commit -m "Description de vos changements"
```

### Étape B : Créer le fichier de partage sur la clé USB
```bash
# Remplacez /media/USB/ par le chemin réel de votre clé
git bundle create "/media/deuteuros/NOM_DE_LA_CLE/cashew.bundle" --all
```

---

## 📥 2. Sur la machine du COLLABORATEUR
*(Celui qui reçoit les fichiers pour la première fois)*

### Étape A : Cloner le projet depuis la clé USB
```bash
# Se placer là où vous voulez installer le projet
cd ~/Documents/Projets
git clone "/media/path/vers/cle/cashew.bundle" cashew_app
```

### Étape B : Installer l'environnement (revoir VENV_GUIDE.md)
```bash
cd cashew_app
python3 -m venv venv
./venv/bin/pip install -r requirements.txt
```

---

## 🔄 3. Mise à jour (Recréer un lien plus tard)
Si le collaborateur a déjà le projet et veut juste les nouvelles versions :

1. **Expéditeur** : Recrée un `cashew.bundle` sur la clé.
2. **Collaborateur** :
   ```bash
   git fetch "/media/path/vers/cle/cashew.bundle"
   git merge FETCH_HEAD
   ```

> [!TIP]
> Le fichier `.bundle` contient tout l'historique des commits. C'est plus propre que de copier-coller simplement les fichiers car cela préserve le travail de chaque agent et humain.
