# Guide de Lancement - Expense Tracker (Flutter)

Ce guide contient les commandes pour compiler et lancer l'application sur différentes plateformes.

## 1. Prérequis (Linux)
Pour compiler la version Desktop sur Linux, assure-toi d'avoir installé les dépendances système :
```bash
sudo apt-get update
sudo apt-get install -y build-essential clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev
```

### Dépannage : Erreur "Release file is missing" (APT)
Si `sudo apt-get update` échoue à cause d'un dépôt opensuse obsolète, il peut être dans **deux fichiers**. Lance ces commandes pour les supprimer :
```bash
sudo rm "/etc/apt/sources.list.d/home:selmf.list.distUpgrade"
sudo rm "/etc/apt/sources.list.d/home:selmf.sources"
```
Puis relance `sudo apt-get update` : il ne devrait plus y avoir d'erreur `404`.

### Dépannage : Erreur `-lstdc++` (clang++ ne trouve pas la bibliothèque C++)
```bash
sudo apt-get install --reinstall build-essential g++ libstdc++-12-dev
```

## 2. Configurer le chemin Flutter
Si Flutter n'est pas dans ton PATH global :
```bash
export PATH="$PATH:/home/deuteuros/flutter/3.38.6/bin"
```

## 3. Lancer l'application

### Version Linux Desktop (Recommandé pour le test)
```bash
flutter run -d linux
```

### Version Web (Chrome)
```bash
flutter run -d chrome
```

### Version Android (nécessite un émulateur ou un téléphone branché)
```bash
flutter run -d android
```

## 4. Compiler pour Android (APK)
```bash
flutter build apk --release
```
L'APK se trouvera dans : `build/app/outputs/flutter-apk/app-release.apk`
