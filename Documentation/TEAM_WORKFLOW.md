# Hub AMLG : Protocole de Co-Développement (Offline Git)

Ce document centralise toutes les instructions pour collaborer efficacement sur l'Expense Tracker sans connexion Internet, en utilisant des clés USB et des bundles Git.

---

## 🎭 1. Rôles et Responsabilités

### 🏰 L'Intégrateur Principal (Propriétaire du PC Central)
- Maintient la branche `master` stable.
- Fusionne les travaux des collaborateurs.
- Génère le bundle de distribution hebdomadaire.
- Gère la résolution des conflits complexes.

### 🏹 Le Collaborateur (Économiste / Mathématicien)
- Développe une fonctionnalité isolée sur une branche dédiée (`feat-nom`).
- Prépare un bundle Git contenant uniquement ses changements.
- Synchronise son `master` local avec le bundle de l'intégrateur.

---

## 🚀 2. Protocole pour les Collaborateurs (Développement)

### A. Initialisation
Avant de commencer, vérifiez que votre environnement est prêt (`VENV_GUIDE.md`) et que vous êtes sur une base propre.

### B. Créer une fonctionnalité
1. Créez une branche : `git checkout -b feat-[nom-votre-tache]`
2. Travaillez avec votre IA (donnez-lui le prompt en bas de page).
3. Enregistrez vos progrès : `git add .` et `git commit -m "Description"`

### C. Exporter pour partage (USB)
Une fois fini, créez le paquet pour l'intégrateur :
```bash
git bundle create "[nom_tache].bundle" master..feat-[nom-tache]
```
Copiez ce fichier `.bundle` sur la clé USB commune.

---

## 📥 3. Protocole pour l'Intégrateur (Fusion)

### A. Sécuriser le PC Central
Toujours committer les travaux en cours sur une branche locale avant d'importer l'extérieur.

### B. Fusionner un bundle
```bash
# Ajouter la clé comme remote temporaire
git remote add [NOM_COLLEGUE] /media/deuteuros/CLE_USB/[nom_tache].bundle

# Récupérer et fusionner
git fetch [NOM_COLLEGUE]
git merge [NOM_COLLEGUE]/feat-[nom-tache]

# Nettoyer
git remote remove [NOM_COLLEGUE]
```

### C. Résolution de conflits
Priorité : **Structure de données (Schéma)** > **UI (Design)**. En cas de doute, demandez à l'IA d'analyser les deux versions.

---

## 🔄 4. Synchronisation Collective (Redistribution)

Quand l'intégrateur partage le `final_expense_tracker_vX.bundle` :
1. Copiez le bundle dans votre dossier `apk/`.
2. Lancez :
```bash
git remote add update ./final_expense_tracker_vX.bundle
git fetch update master
git checkout master
git merge update/master
git remote remove update
```

---

## 🤖 5. Instructions pour les Agents IA
Si vous utilisez un agent (comme Gemini ou Claude) pour coder, fournissez-lui ce contexte :

> "Nous travaillons en mode **Vibe Coding** hors-ligne. 
> 1. Respecte la modularité (`views/`, `components/`).
> 2. Utilise `CustomSegmentedControl` au lieu de `SegmentedButton` (bug Flet 0.80.2).
> 3. Ne tente jamais de `git push` ou `git pull` sur une URL Internet.
> 4. Prépare toujours mes changements sous forme de `git bundle`."

---

## 🛠️ 6. Standards Techniques
- **Modularité** : Chaque vue dans un fichier séparé dans `views/`.
- **Ignore** : `venv/`, `__pycache__`, et `.apk` ne doivent jamais être dans les bundles.
- **Portabilité** : Utilisez toujours `./venv/bin/python main.py --web` si `libmpv` est absent.
