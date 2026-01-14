# Test de Frappe — Jeu en Python

Un petit programme Python pour tester sa vitesse et sa précision de frappe sur le clavier. Inspiré des sites en ligne comme [Ratatype](https://www.ratatype.fr).

---

## Fonctionnalités

- Deux modes de jeu :
  1. **Mode Normal** : taper une seule phrase et obtenir le temps, la vitesse (mots/min) et la précision.
  2. **Mode 1 Minute** : taper un maximum de phrases en 60 secondes. Trois phrases sont affichées simultanément, et elles défilent automatiquement lorsqu'elles sont complétées.
  
- **Coloration dynamique** :
  - Lettres correctes : vert avec surlignage.
  - Lettres incorrectes : rouge jusqu'à correction.
  
- Blocage des erreurs de saisie :
  - Impossible de taper une lettre incorrecte.
  - Les touches non pertinentes (Backspace, Delete, flèches…) sont désactivées.

- **Score final** :
  - Précision sur l’ensemble des caractères tapés.
  - Vitesse en mots/minute.

- Interface moderne grâce à [CustomTkinter](https://github.com/TomSchimansky/CustomTkinter).

---

## Installation

1. Cloner le dépôt ou télécharger le fichier Python :

```bash
git clone https://github.com/Valentinhdn/TappingPro.git

cd TappingPro

pip install customtkinter

python TappingPro.py
```

## Compiler en .exe

Dans un terminal, entrer la commande suivante : 
```bash
python3 -m PyInstaller --onefile --windowed main.py
```
### Pour ajouter un logo à l'app :
```bash
python3 -m PyInstaller --onefile --windowed --icon=monlogo.ico main.py

```

