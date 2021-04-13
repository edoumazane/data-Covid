# data-Covid
Le but est de présenter les données épidémiologiques #Covid19France pour pouvoir : 
* comparer l'impact sur trois classes d'âge : **0-29**, **30-59** et **+ de 60 ans**
* comparer les régions entre elles
* sur toute la période 01/03/2020 - 01/06/2021
>Les figures sont mises à jour quotidiennement.
1. [Suivre en parallèle 5 indicateurs](##example2)
2. [Quelques infos importantes avant de continuer...](#infos)
3. [Comparer les régions pour un indicateur](#example1)
4. [Suivre un indicateur dans une région et ses départements](###example3)
5. [Code source](#example4) 
### 1. Suivre en parallèle 5 indicateurs<a name="example2"></a>
* ![accéder aux 3 figures (+1)](/Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions)
- exemple pour les 4 régions les plus touchées :
![Figure 1 / 3](Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions/regions-1%20sur%203.png)
### 3. Quelques infos importantes avant de continuer...<a name="info"></a>
+ _Le choix des couleurs (une par indicateur) met en relief la population + de 60 ans_
+ _Chaque indicateur est rapporté à la population de chaque classe d'âge :_
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
+ _Pour chaque indicateur, l'échelle des ordonnées (ymin, ymax) est immuable, quelles que soient la figure et l'entité géographique considérées_
+ _L'échelle du temps est également immuable_
+ _Les zones grisées représentent les 3 périodes de confinement à l'échelle nationale_

### 2. Suivi de chaque indicateur dans toutes les régions <a name="example1"></a>
* ![accéder aux 8 figures](/Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions)
* 3 exemples :
- taux d'**hospitalisation** :
![Figure hosp](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-hosp.png)
- taux de **réanimation** :
![Figure réa](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-rea.png)
- taux de **décès** :
![Figure décès](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-hosp.png)
### 3. Suivi de chaque indicateur dans chaque région et ses départements<a name="example3"></a>
* Les données hospitalières à l'échelon départemental ne sont pas disponibles par classe d'âge.
* Pour cette raison, seuls les 5 indicateurs qui concernent les tests virologiques et la vaccination sont présentés.
* ![accéder aux (14 x 5) figures](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs) 
* 3 exemples :
- l'**incidence** en **Île-de-France** :
![Incidence Île-de-France](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/%C3%8Ele-de-France/fig-%C3%8Ele-de-France-incidence.png)
- l'**incidence** en **Bretagne** :
![Incidence Bretagne](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/Bretagne/fig-Bretagne-incidence.png)
* la **vaccination** dans les départements et régions d'**Outre-mer** :
![Dose 2 Outre-Mer](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/Outre-mer%20(DROM)/fig-Outre-mer%20(DROM)-dose2.png)

### 5. Code source <a name="example4"></a>
* Fichiers de départ (téléchargés sur data.gouv.fr - source Santé Publique France) :
![Données de départ](/Data)
* _Jupyter notebook_ pour traiter les données :
![Traitement des données](/Code/v4%20Traitement%20des%20donn%C3%A9es.ipynb)
> L'exécution de ce classeur prend **6** secondes
* _Jupyter notebook_ pour tracer les figures :
![Classeur pour le tracé des figures](/Code/v4%20Trac%C3%A9%20des%20figures.ipynb)
> L'exécution de ce classeur prend (13 + 18 + 74) = **105** secondes
* Modules Python home-made... :
![my_package](/Code/my_package)