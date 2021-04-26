# data-Covid

Ceci est la version v5:construction_worker_man: :
changements par rapport à v4 (en cours : :construction_worker_man: réalisé : :heavy_check_mark:)
* :heavy_check_mark: figures Type 3 : les départements sur 3 colonnes, ratio hauteur:largeur proche de celui région / France
* :heavy_check_mark: retrait de l'extrapolation des données hospitalières à l'échelon départemental
* :construction_worker_man: prise en compte du nouveau type de fichier VACSI (tot-a-dep)
* :construction_worker_man: plus facile de changer la définition des classes d'âge visualisées
* :construction_worker_man: création d'un nouvel indicateur : ratio réa/hosp et décès/hosp
* :construction_worker_man: création d'un nouveau type de figures (Type 4) permettant de visualiser tous les indicateurs pour une région
* :heavy_check_mark: indication des populations des classes d'âge considérées en bas de page, au national (Type 1 et Type 2) etau niveau régional (Type 4)
* :construction_worker_man: mise à jour du fichier README et de .gitignore

**Objectif - présenter les données épidémiologiques #Covid19France afin :**

* de comparer l'impact sur trois classes d'âge : **0-29**, **30-59** et **+ de 60 ans**
* de comparer les **régions** entre elles
* de donner un aperçu global sur l'ensemble de la période 01/03/2020 - 01/06/2021

>:clock8: Les figures sont mises à jour toutes les 24 à 48 h
>>:hatching_chick: C'est mon tout premier projet #dataviz sur GitHub
>>>:tada: Toute remarque ou participation est la bienvenue

>:bulb: Un jour je mettrai des slides expliquant (1) le calcul (2) la disposition des figures
>>:mag_right: Les figures sur cette page ne sont qu'un aperçu. Cliquez sur "accéder aux n figures" dans chaque catégorie pour naviguer

1. [Figures type 1 : suivre en parallèle 5 indicateurs](#example2)
2. [Quelques infos importantes avant de continuer...](#infos)
3. [Figures type 2 : comparer les régions pour un indicateur](#example1)
4. [Figures type 3 : suivre un indicateur dans une région et ses départements](#example3)
5. [Figures type 4 : suivre tous les indicateurs pour une région](#example4)
6. [... et enfin le code source](#example5)

### 1. Figures type 1 : suivre en parallèle 5 indicateurs<a name="example2"></a>

* ![accéder aux 4 figures](/Output/Type1)

>exemple : les 4 régions ayant le plus fort taux d'hospitalisation chez les + de 60 ans (autres régions sont disponibles dans le dossier)
>>![Figure 1 / 3](/Output/Type1/r%C3%A9gions%201%20sur%203.png)

### 2. Quelques infos importantes avant de continuer...<a name="info"></a>

* _Le choix des couleurs (une par indicateur) met en relief la population + de 60 ans_
* _Chaque indicateur est rapporté à la population de chaque classe d'âge :_
    * _taux pour 100 000 habitants :_
        * tests virologiques pratiqués par semaine
        * cas de tests positifs détectés par semaine (= incidence)
        * patients hospitalisés
        * patients en réanimation
        * patients décédés à l'hôpital
    * _taux exprimés en % :_
        * tests positifs sur 100 tests pratiqués (taux de positivité)
        * personnes vaccinées (au moins une dose)
        * personnes vaccinées (avec deux doses)
* _Pour chaque indicateur, l'échelle des ordonnées (ymin, ymax) est immuable, quelles que soient la figure et l'entité géographique considérées_
* _L'échelle du temps est également immuable_
* _Les zones grisées représentent les 3 périodes de confinement à l'échelle nationale_

### 3. Figures type 2 : comparer les régions pour un indicateur <a name="example1"></a>

* ![accéder aux 8 figures](/Output/Type2)

* 3 exemples :
> **incidence** :
>>![Figure hosp](/Output/Type2/fig-incidence.png)

> **réanimation** :
>>![Figure réa](/Output/Type2/fig-rea.png)

> **décès** :
>>![Figure décès](/Output/Type2/fig-deces.png)

### 4. Figures type 3 : suivre un indicateur dans une région et ses départements<a name="example3"></a>

* Les données hospitalières à l'échelon départemental ne sont pas disponibles par classe d'âge.
* Pour les données hospitalières (hosp, réa, décès), à l'échelon départemental la décomposition par classe d'âge n'est pas fournie par Santé publique France. En conséquence, le taux pour la population totale est représentée par un trait coloré fin. Cette représentation est reprise dans les graphes du haut (région + France). L'échelle des ordonnées est rectifiée pour mieux voir les variations.
* ![accéder aux 14 * 8 = 112 (!) figures](/Output/Type3)
* 4 exemples :

>**incidence** en **Île-de-France** :
>>![Incidence Île-de-France](/Output/Type3/%C3%8Ele-de-France/%C3%8Ele-de-France-incidence.png)

>**positivité** en **Bretagne** :
>>![Positivité Bretagne](/Output/Type3/Bretagne/Bretagne-positivite.png)

>**vaccination** dans les départements et régions d'**Outre-mer** :
>>![Dose 2 Outre-Mer](/Output/Type3/Outre-mer%20(DROM)/Outre-mer%20(DROM)-dose2.png)

### 5. Figures type 4 : suivre tous les indicateurs pour une région<a name="example4"></a>
:construction_worker_man:

### 6. ... et enfin le code source <a name="example5"></a>

* données brutes :
![fichiers téléchargés sur data.gouv.fr (données Santé Publique France)](/Data)
* traitement des données :

![_Jupyter notebook_ (carnet) pour traiter les données brutes](/Code/v4%20Traitement%20des%20donn%C3%A9es.ipynb)
> :clock8: L'exécution de ce carnet prend **6** secondes

* tracé des figures :

![_Jupyter notebook_ pour tracer les figures](/Code/v4%20Trac%C3%A9%20des%20figures.ipynb)
> :clock8: L'exécution de ce carnet prend (13 + 18 + 353) = **384** secondes (6 minutes)

* et pour faire fonctionner les calepins :
![home-baked Python modules](/Code/my_package)
