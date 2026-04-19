# 🗺️ Roadmap : Cashew - Consulting Edition (IEL)

> Dernière mise à jour : 2026-04-19 (Agent Gemini CLI)

Cette roadmap définit les priorités pour le développement solo du logiciel Cashew, optimisé pour le service de consulting de l'ISS Economics Lab (IEL).

---

## ✅ Étape 1 : Fondations & UX (Terminé)
- **Modularité** : Structure par vues (`views/`) et composants.
- **Data Schema** : `DataSchemaStandardizesTransactions.md`.
- **Suppression au clic long** : Gestion de l'historique (Tantara).
- **Design WhatsApp-like** : Première itération de l'interface visuelle.

---

## 🔄 Étape 2 : MVP Consulting Edition (En Cours)

### 2.1 Import & Audit (Priorité Haute)
- ⬜ **Bouton d'import CSV** : Fonctionnalité cœur pour charger les données préparées par l'IEL.
- ⬜ **Validation Automatique** : Vérification du schéma via le skill **Data Handler**.
- ⬜ **Fusion de données** : Import intelligent sans doublons.

### 2.2 Vue "Tantara" v2 (Redesign Spec)
- 🔄 **Sélecteur de Mois Horizontal** : Navigation fluide entre les périodes.
- ⬜ **Barre de Résumé Mensuel** : `[🔽 Dépenses] [🔼 Entrées] = [Total Net]`.
- ✅ **Regroupement par Jours** : `TantaraRedesignSpecifiesWhatsAppUX.md`.

### 2.3 Vue "Témoin" (Analyse Glissante)
- ⬜ **Intervalle 30 jours** : Calcul dynamique du solde entre `J` et `J-30`.
- ⬜ **Indicateur de Santé** : Visualisation simple de l'évolution de la caisse.

---

## ⬜ Étape 3 : Finalisation & Localisation (À venir)
- ⬜ **Localisation Malagasy intégrale** : Via le skill **Translator-MG**.
- ⬜ **Export de Backup** : Permettre au client de sauvegarder son journal.

---

> [!NOTE]
> **Directive Antigravity** : Toujours se référer au `docs/architecture/MvpFocusesOnConsultingService.md` avant toute implémentation technique.
