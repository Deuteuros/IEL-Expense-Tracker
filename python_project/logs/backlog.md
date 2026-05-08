# Backlog & Visions Futures - Cashew (IEL)

- [x] Correction "Unknown control: FilePicker" sur Linux.
- [x] Refonte interface : Nouvel onglet "Fikirakirana" (Gestion).
- [x] Nettoyage vue "Témoin" (retrait des boutons redondants).

# Beta-test
- [x] Ajouter aussi l'année devant le mois pour la vue tantara
- [x] Adapter les textes et widget dans l'application pour différent longueur et largeur de smartphone
- [x] Vérifier bien que les textes sont toutes en malgache et si difficile à comprendre mettre du texte en français entre parenthèses
- [x] Pour la journée assurer que jeudi est appelé : Alakamisy
- [x] Pour le build, utiliser le paramètre `--product` pour changer le nom : `flet build apk src --product "Cashew" --org "mg.iel.cashew"`
- [x] Générer un logo et l'intégrer dans l'application
- [x] Tester l'application sur différents smartphone
- [x] Assurer que les textes dans l'onglet Ampidiro suivent aussi la largeur et la longueur du smartphone.
- [-] Faire que le logo soit le logo de l'application mobile dans le build

# Retour Beta-test
- [x] Correction de l'erreur `ModuleNotFoundError: No module named 'pandas'` lors du lancement de l'application sur Android. (Cause: `requirements.txt` manquant dans le dossier `src/`)

```
Traceback (most recent call last):
  File "<string>", line 95, in <module>
  File "<frozen runpy>", line 229, in run_module
  File "<frozen runpy>", line 88, in _run_code
  File "/data/user/0/com.flet.src/files/flet/app/main.py", line 2, in <module>
    import database
  File "/data/user/0/com.flet.src/files/flet/app/database.py", line 2, in <module>
    import pandas as pd
ModuleNotFoundError: No module named 'pandas'
```


## 🏁 Statut Final :
Le MVP est terminé et fonctionnel. Les fonctionnalités futures (M3+) ont été annulées pour se concentrer sur la stabilité de cette version.
