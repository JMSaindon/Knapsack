<img align="left" height="160" src=img/logotrans.png>

Le contenu de ce dépôt correspond à un rendu de TP dans le cadre de l'option IA enseignée à l'Enseirb-Matmeca. Cela vaut pour le module d'Algorithme de recherche. Le TP choisi porte sur les algorithmes génétiques et présente une possible résolution du problème bien connus du sac à dos.   

Auteur : Jean-Marie Saindon      
Encadrant : Laurent Simon   

---

# Knapsack

## Quickstart

- modules nécessaires: numpy et matplotlib
- Réglez les paramètres que vous souhaitez pour la simulation en haut du fichier [SacADos.py](SacADos.py)
- commande : `$ python SacADos.py`

## Description

Une version corrigée de ce TP ayant été diffusée, je précise que ma version a été réalisée sans consultation de celle-ci et que seules les entrées (paramètres en haut du fichier) et sorties (print en bas du fichier) ont été modifiées pour lui correspondre et ainsi me permettre de facilement vérifier son bon fonctionnement en comparaison.

<p align="center">
  <img src=img/knapsackv1res.PNG>
</p>

### Implémentation
La résolution du problème du sac à dos par le biais d'un algorithme génétique a été implémenté en python de la façon suivante :

Tout d'abord, 4 classes principales ont été créées: Parameters, Object, Individual et Population. Parameters est une classe regroupant simplement les différentes variables essentielles du problème du sac à dos et de la résolution génétique, à savoir : les valeurs maximales et minimales des coût et poids des objets, les objets eux-mêmes, la taille des populations, le nombre de génération déroulées par les simulation, etc. Object est, quant à elle, une classe simple représentant un objet, avec donc son coût et son poids.

Individual est une classe qui opte pour une représentation de la solution au problème sous forme de tableau numpy remplit de 0 ou de 1 selon la présence ou non de l'objet correspondant dans la liste des objets. Enfin, Population contient simplement une liste de Individual.

Dans la première version que j'avais implémenté, la mutation se faisait sur un unique gène et la reproduction était réalisée avec un cross point cenrtral.

Afin d'obtenir de meilleures performances, j'ai abouti a une deuxième version en ayant simplement ajouté la possibilité de mutations multiples (sur plusieurs gènes) et la reproduction par sélection aléatoire de chaque gène chez l'un ou l'autre des parents.

### Tests et Résultats

Afin de dérouler l'algorithme génétique et de trouver les meilleurs paramètres pour aboutir à la solution optimale, on génère une centaine de populations différentes avec des tailles et des taux de mutation aléatoires. Chacune de ces populations évolue sur 100 générations et le meilleur individu de la dernière évolution est sélectionné pour représenter sa population. Le meilleur représentant (celui ayant la meilleur maximisation du coût) est alors choisi comme solution finale de l'algorithme.

Ma premère implémentation offre des résultats satisfaisants en suivant ce procédé. Sur quelques simulations, le pourcentage moyen d'optimalité tourne autour des 90 \% (avec notamment 91.37 \% sur les simulations représentées ci-dessous) mais le pourcentage d'exactitude n'est que de 2 \%.

<p align="center">
  <img src=img/knapsackv1.png>
</p>

Ma deuxième version à quant à elle grandement amélioré les performances en faisant passer le pourcentage moyen d'optimalité vers les 97 \% (97.97 \% ici) et le pourcentage d'exactitude à 55 \%

<p align="center">
  <img src=img/knapsackv2.png>
</p>

<p align="center">
  <img src=img/knapsackv2res.PNG>
</p>

La vérification de l'optimalité se fait par rapport au résultat de la librairie knapsack de python. (Attention cette librairie est extrêmement lente)

---

09/02/2020
