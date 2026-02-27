# Guide de l'Intégrateur Principal (Votre Machine)

Comme votre PC est le point central de la fusion et que vous avez aussi travaillé sur une fonctionnalité, voici l'ordre exact des opérations pour ne rien mélanger.

## 1. Sécurisez votre propre travail
Avant d'importer le travail des autres, mettez votre travail "au propre" sur une branche dédiée.

```bash
cd "/home/deuteuros/Documents/10 Projets/AMLG - Odoo - Cashew/Expense tracker/apk"

# 1. Créer une branche pour VOTRE fonctionnalité (ex: i18n)
git checkout -b feat-ma-partie

# 2. Enregistrer vos changements
git add .
git commit -m "Mon travail sur [Nom de votre fonctionnalité]"

# 3. Revenir sur la branche principale pour accueillir les autres
git checkout master
```

## 2. Intégrez les travaux des collaborateurs (via USB)
Pour chaque clé USB que l'on vous apporte :

```bash
# A. Ajouter la clé comme une source temporaire
# (Remplacez NOM_COLLEGUE et CHEMIN_USB par les vraies valeurs)
git remote add [NOM_COLLEGUE] /media/deuteuros/[NOM_DE_LA_CLE]/[Fichier].bundle

# B. Récupérer les données
git fetch [NOM_COLLEGUE]

# C. Fusionner dans votre master
git merge [NOM_COLLEGUE]/feat-[nom-feature]

# D. (Optionnel) Nettoyer la source temporaire une fois fini
git remote remove [NOM_COLLEGUE]
```

## 3. Intégrez enfin votre propre travail
Maintenant que le `master` contient le travail de vos 3 collègues, ajoutez le vôtre :

```bash
git merge feat-ma-partie
```

## 4. Vérification finale
Une fois les 4 fonctionnalités réunies :
1. Lancez l'application : `python main.py`
2. Testez chaque bouton et chaque vue.
3. Si tout est OK, créez le pack de redistribution pour la semaine prochaine :
   ```bash
   git bundle create "logiciel_complet_semaine1.bundle" HEAD master
   ```

> [!TIP]
> **En cas de conflit de fichiers :**
> Si Git dit "Merge conflict", ouvrez les fichiers concernés. Les zones à problème seront marquées par `<<<<<<<` et `>>>>>>>`. Choisissez la version qui garde les deux fonctionnalités ou demandez à l'IA de corriger la syntaxe.
