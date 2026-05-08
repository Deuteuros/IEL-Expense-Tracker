# Résolution de l'erreur PEP 668 (Externally Managed Environment)

C'est une protection de Zorin OS / Ubuntu. Puisqu'on ne peut pas facilement mettre à jour ce `pip` corrompu, la solution la plus saine est de **le supprimer** de votre dossier local. Cela forcera le système à utiliser sa version propre et stable.

## 🛠️ ÉTAPE 1 : Nettoyage Radical du Pip corrompu
On supprime uniquement la version locale qui pose problème pour Python 3.12 :

```bash
# Suppression du pip local 3.12
rm -rf /home/deuteuros/.local/lib/python3.12/site-packages/pip
rm -rf /home/deuteuros/.local/lib/python3.12/site-packages/pip-25.1.1.dist-info
```

## 🛠️ ÉTAPE 2 : Vérification
Vérifiez que `pip` pointe maintenant vers une version système (généralement dans `/usr/lib/...`) :

```bash
python3.12 -m pip --version
```

## 🛠️ ÉTAPE 3 : Relancer le Build
Maintenant que le conflit est résolu, relancez le build (toujours sans Conda) :

```bash
# Nettoyage du build précédent
rm -rf "src/build/"

# Configuration environnement
export JAVA_HOME="/opt/tinyMediaManager/jre"
export ANDROID_HOME="/home/deuteuros/Android/sdk"
export FLUTTER_BIN="/home/deuteuros/flutter/3.38.6/bin"
export PATH="$JAVA_HOME/bin:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools:$FLUTTER_BIN:$PATH"

# Build final
./venv/bin/python3 -c "from flet.cli import main; import sys; sys.argv=['flet', 'build', 'apk', 'src']; main()"
```

---

*Note : Si `python3.12 -m pip --version` vous dit "No module named pip" après la suppression, c'est qu'il n'est pas installé sur le système. Dans ce cas, installez-le proprement avec `sudo apt install python3-pip`.*
