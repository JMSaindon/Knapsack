<img align="left" height="160" src=img/logotrans.png>

Le contenu de ce dépôt correspond à un rendu de TP dans le cadre de l'option IA enseignée à l'Enseirb-Matmeca. Cela vaut pour le module d'Algorithme de recherche. Le TP choisi porte sur les algorithmes génétiques et présente une possible résolution du problème bien connus du sac à dos.   

Auteur : Jean-Marie Saindon      
Encadrant : Laurent Simon   

---

# Knapsack

## Quickstart

- modules nécessaires: numpy et matplotlib
- Réglez les paramètres que vous souhaitez pour la simulation en haut du fichier `SacADos.py`
- commande : `$ python SacADos.py`

## Description

Une version corrigée de ce TP ayant été diffusée, je précise que ma version a été réalisée sans consulation de celle-ci et que seules les entrées (paramètres en haut du fichier) et sorties (print en bas du fichier) ont été modifiées pour lui correspondre et ainsi permettre une meilleure prise en main et esthétisme.

<p align="center">
  <img src=img/Opti.PNG>
</p>

### Implémentation
La résolution du problème du sac à dos par le biais d'un algorithme génétique a été implémenté en python de la façon suivante :

Tout d'abord, 4 classes principales ont été créées: Parameters, Object, Individual et Population. Parameters est une classe regroupant simplement les différentes variables essentielles du problème du sac à dos et de la résolution génétique, à savoir : les valeurs maximales et minimales des coût et poids des objets, les objets eux-mêmes, la taille des populations, le nombre de génération déroulées par les simulation, etc. Object est, quant à elle, une classe simple représentant un objet, avec donc son coût et son poids.

Individual est une classe qui opte pour une représentation de la solution au problème sous forme de tableau numpy remplit de 0 ou de 1 selon la présence ou non de l'objet correspondant dans la liste des objets. Enfin, Population contient simplement une liste de Individual.

### Résultats

Afin de dérouler l'algorithme génétique et de trouver les meilleurs paramètres pour aboutir à la solution optimale, on génère une centaine de populations différentes avec des tailles et des taux de mutation aléatoires. Chacune de ces populations évolue sur 100 générations et le meilleur individu de la dernière évolution est sélectionné pour représenter sa population. Le meilleur représentant (celui ayant la meilleur maximisation du coût) est alors choisi comme solution finale de l'algorithme.

Mon implémentation offre des résultats satisfaisants en suivant ce procédé. Sur quelques simulations, le pourcentage moyen d'optimalité tournais autour des 90 \% (avec notamment 91.37 \% sur les simulations représentées ci-dessous).

<p align="center">
  <img src=img/Graphique2.png>
</p>

La vérification de l'optimalité se fait par rapport au résultat de la librairie knapsack de python. (Attention cette librairie est extrêmement lente)
