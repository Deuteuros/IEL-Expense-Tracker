# Procédure de Build Android (APK)

Ce document explique comment générer l'APK pour Android une fois que l'environnement est prêt.

## Commande de Build

Si le build a été interrompu, vous pouvez le relancer avec cette commande depuis la racine du projet :

```bash
./venv/bin/python3 -c "from flet.cli import main; import sys; sys.argv=['flet', 'build', 'apk', 'src']; main()"
```

### Ce que fait cette commande :
1. Elle utilise l'interpréteur Python du projet.
2. Elle lance le module de build de Flet.
3. Elle cible le dossier `src/` (où se trouve `main.py`).

### Où trouver l'APK ?
Une fois la compilation terminée avec succès, le fichier APK se trouvera dans :
`src/build/apk/` (ou un dossier similaire nommé `dist` ou `build` créé par Flet).

### Notes :
- La première exécution a déjà téléchargé le SDK Flutter et le SDK Android, donc les prochaines tentatives seront beaucoup plus rapides.
- Assurez-vous que votre connexion internet est active si Gradle a besoin de télécharger des dépendances supplémentaires.
