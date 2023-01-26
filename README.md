# Projet M2 AMIS groupe C

> Application de comparaison de structures moléculaire.

* Utilisation de modélisation des molécules en graphes;
* Extraction des données de fichier SDF présent sur la base de données ChEBI;
* Application de l'algorithme de McKay et utilisation de la bibliothèque nauty.c;
* Construction d'une base de données des groupes d'isomorphes;
* Comparaison des molécules deux à deux et recherche de MCIS;

## Installation et dépendances

Le programme nécessite l'utilisation de :
- Python3 et C
- Makefile

Il est favorable de lancer le programme sous Linux.

Pour installer les dépendances de l'application :
```bash
  pip install -r requirements.txt
```

## Lancement de l'application

Pour compiler le programme en C et lancer l'application :
```bash
  make
```

## Fichier de configuration
Le fichier `data/config.json` regroupe l'url du fichier SDF de la base de données ChEBI.
Cette url peut être remplacée par l'url d'un fichier de molécules de format SDF.
