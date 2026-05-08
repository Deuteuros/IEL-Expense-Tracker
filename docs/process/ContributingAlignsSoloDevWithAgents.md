# Guide de Développement (Solo + Agents Antigravity)

Ce document définit les standards de développement pour le projet Cashew, géré en solo par le développeur principal assisté par les agents AI (Antigravity).

## 🧩 Workflow Solo-Agent
1. **Pilotage par Directives (DDD)** : Tout changement commence par une analyse du `BlueprintDefinesModularArchitecture.md` et des spécifications dans `docs/architecture/`.
2. **Utilisation d'Antigravity** :
   - L'agent **Architecte Cashew** valide la cohérence structurelle.
   - Les skills spécialisés (**Data Handler**, **UX Designer**, **Translator**) sont activés selon le besoin.
3. **Commit & Documentation** : Après chaque itération, documenter les changements dans les fichiers `.org` de `docs/dev_notes/` pour maintenir une mémoire projet claire.

## 🛠️ Standards Techniques (Antigravity-Ready)
- **Flet / Python** : Utiliser un découpage modulaire strict par vue dans `src/views/`.
- **Data First** : Ne jamais modifier la structure du CSV sans mettre à jour `DataSchemaStandardizesTransactions.md` au préalable.
- **I18n** : L'interface est en Malagasy par défaut. Toute nouvelle chaîne doit passer par le skill **Translator-MG**.

## 📄 Documentation IA
- Les agents doivent lire ce fichier et le dossier `.agents/` avant de générer du code.
- Prioriser la simplicité et la robustesse (Offline-First).
