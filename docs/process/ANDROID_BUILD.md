# Guide Complet : Réinstallation Propre et Build APK

Ce guide permet de repartir sur une base saine pour générer l'APK quand l'environnement Android/Flutter est instable. 

**Note :** Vous devez copier et coller ces commandes vous-même dans votre terminal.

---

## ÉTAPE 1 : Nettoyage complet
Avant de réinstaller, on supprime les résidus de builds précédents et les composants corrompus.

```bash
# Suppression du dossier build de l'application
rm -rf "src/build/"

# Suppression du NDK potentiellement corrompu
rm -rf /home/deuteuros/Android/sdk/ndk/27.0.12077973
```

---

## ÉTAPE 2 : Configuration de l'Environnement
Ces commandes définissent les variables nécessaires pour que votre terminal trouve Java, Android et Flutter.

```bash
# Définition des variables de session
export JAVA_HOME="/opt/tinyMediaManager/jre"
export ANDROID_HOME="/home/deuteuros/Android/sdk"
export FLUTTER_BIN="/home/deuteuros/flutter/3.38.6/bin"

# Mise à jour du PATH (pour trouver sdkmanager, flutter et java)
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$FLUTTER_BIN:$PATH"
```

---

## ÉTAPE 3 : Installation des Composants Android
On force l'installation de l'API 36 et du NDK requis par Flutter.

```bash
# Installation via le SDK Manager
sdkmanager "platforms;android-36" "build-tools;36.0.0" "ndk;27.0.12077973"

# (Optionnel) Accepter les licences si demandé
flutter doctor --android-licenses
```

---

## ÉTAPE 4 : Lancement du Build final
Une fois l'environnement prêt, lancez la compilation.

```bash
./venv/bin/python3 -c "from flet.cli import main; import sys; sys.argv=['flet', 'build', 'apk', 'src']; main()"
```

---

## 💡 Conseils en cas d'erreur
- **Problème Java :** Si `sdkmanager` se plaint de Java, vérifiez que le dossier `/opt/tinyMediaManager/jre` existe bien.
- **Vitesse :** Le premier build après cette procédure sera long car il doit tout retélécharger.
- **Localisation APK :** L'APK final sera dans `src/build/apk/`.
