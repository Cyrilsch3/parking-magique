# 🚗 Parking Magique

**Parking Magique** est une application de gestion de parking développée en **Python** avec une **interface graphique PyQt6**.  
Elle permet de gérer les places de parking, les entrées/sorties de véhicules, les abonnements clients et les tarifs, avec un système de sauvegarde automatique.

Projet réalisé dans le cadre du cours **DEV II**.

---

## ✨ Fonctionnalités

### 🅿️ Gestion des places
- Affichage graphique des places par étage
- Codes couleur :
  - 🟢 Place libre
  - 🔴 Place occupée
  - 🔵 Place réservée (abonnement)
- Entrée et sortie des véhicules avec calcul automatique du prix

### 👤 Gestion des abonnements
- Création d’abonnements (avec ou sans place réservée)
- Modification de la plaque ou de la place réservée
- Prolongation de la durée d’un abonnement
- Calcul automatique de la date de fin

### 💰 Gestion des tarifs
- Minutes gratuites
- Prix par tranche horaire
- Prix maximum (> 10h)
- Tarifs abonnements (simple / réservé)
- Paramétrage via l’interface graphique

### 💾 Sauvegarde
- Sauvegarde automatique au format JSON
- Conservation des **5 dernières sauvegardes**
- Chargement automatique de la dernière sauvegarde au démarrage

---

## 🛠️ Technologies utilisées

- **Python 3**
- **PyQt6** (interface graphique)
- **JSON** (sauvegarde des données)

---

## ✅ Prérequis minimum

### 🔹 Logiciel
- **Python 3.10 ou supérieur**

Vérifier l’installation :
```bash
python --version
```

### 🔹 Bibliothèques Python à installer
```bash
pip install PyQt6 python-dateutil
```

| Bibliothèque       | Rôle |
|-------------------|------|
| PyQt6             | Interface graphique |
| python-dateutil   | Gestion avancée des dates (abonnements) |

Les autres modules utilisés sont inclus par défaut avec Python.

---

## ▶️ Lancer l’application

Depuis le dossier du projet :

```bash
python GUI.py
```

ou (macOS / Linux) :
```bash
python3 GUI.py
```

---

## 📌 Remarques
- Les données de démonstration (places et abonnés) sont chargées automatiquement si aucune sauvegarde n’est trouvée.
- Les places réservées ne sont **pas occupées physiquement** tant que l’abonné n’est pas présent.
- Le calcul du prix respecte les paramètres configurés dans le menu **Tarifs**.

---

## 👨‍🎓 Auteur
Projet réalisé par **Thomas Charlier**, **Sofiane Amqrane**, **Cyril Schweicher**, **Gaspard Munguia Coca**

Dans le cadre du cours **DEV II – EPHEC**
