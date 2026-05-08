# Guide de Lancement - CaisseCash (Flutter)

Ce guide contient les commandes pour compiler et lancer l'application.

## 1. Prérequis (Linux)
Lance ces commandes directement à la racine du projet :
```bash
sudo apt-get update
sudo apt-get install -y build-essential clang cmake ninja-build pkg-config libgtk-3-dev liblzma-dev lld-18 libstdc++-13-dev
```

### Dépannage : Erreur headers C++
Si tu as l'erreur `type_traits file not found`, lance ces exports :
```bash
export C_INCLUDE_PATH=/usr/include/c++/13:/usr/include/x86_64-linux-gnu/c++/13:$C_INCLUDE_PATH
export CPLUS_INCLUDE_PATH=/usr/include/c++/13:/usr/include/x86_64-linux-gnu/c++/13:$CPLUS_INCLUDE_PATH
```

## 2. Configurer le chemin Flutter
```bash
export PATH="$PATH:/home/deuteuros/flutter/3.38.6/bin"
```

## 3. Lancer l'application
```bash
flutter pub get
flutter run -d linux
```

### Version Web (Chrome)
```bash
{{ ... }}
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
