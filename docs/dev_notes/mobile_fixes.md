# Pistes de Correction pour Mobile (Android)

Ce document répertorie les pistes techniques pour corriger les bugs identifiés lors des tests mobiles du 11 mai 2026.

## 1. Export CSV (Backup)
**Problème** : `FilePicker.platform.saveFile` n'est pas supporté sur Android.
**Pistes de solution** :
- **Option A (Partage)** : Utiliser le package `share_plus` pour ouvrir le menu de partage Android une fois le fichier CSV généré dans un dossier temporaire.
- **Option B (Downloads)** : Utiliser `path_provider` pour obtenir le chemin du dossier `Downloads` et y enregistrer le fichier directement.
- **Option C (MediaStore)** : Utiliser un package comme `path_provider_android` pour interagir avec le stockage public.

## 2. Autocomplétion (Smart Entry)
**Problème** : Les suggestions ne s'affichent pas ou le champ ne réagit pas correctement sur mobile.
**Pistes de solution** :
- **Clavier/Focus** : Vérifier si le `SingleChildScrollView` du dialogue n'empêche pas l'affichage de l'overlay de `Autocomplete`.
- **Performance** : S'assurer que les providers Riverpod (`uniqueItemsProvider`) ne sont pas bloqués par une opération synchrone lourde.
- **UI** : Tester avec un package plus flexible comme `flutter_typeahead` qui gère mieux les contraintes d'espace sur petit écran.

## 3. Accès Base de Données
**Problème** : Risque de conflit si `sqflite_common_ffi` est activé par erreur sur Android.
**Action** : Vérifier que `main.dart` n'utilise que le plugin `sqflite` natif sur Android.
