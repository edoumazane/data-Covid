# data-Covid
Objectif - présenter les données épidémiologiques #Covid19France afin de : 
* comparer l'impact sur trois classes d'âge : **0-29**, **30-59** et **+ de 60 ans**
* comparer les **régions** entre elles
* couvrir toute la période 01/03/2020 - 01/06/2021
>:clock8: Les figures sont mises à jour toutes les 24 à 48 h 
>>:hatching_chick: C'est mon tout premier projet #dataviz sur GitHub 
>>>:tada: Toute participation est la bienvenue 
1. [Suivre en parallèle 5 indicateurs](##example2)
2. [Quelques infos importantes avant de continuer...](#infos)
3. [Comparer les régions pour un indicateur](#example1)
4. [Suivre un indicateur dans une région et ses départements](###example3)
5. [... et enfin le code source](#example4) 
### 1. Suivre en parallèle 5 indicateurs<a name="example2"></a>
* ![accéder aux 4 figures](/Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions)
- exemple pour les 4 régions les plus touchées :
![Figure 1 / 3](Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions/regions-1%20sur%203.png)
### 2. Quelques infos importantes avant de continuer...<a name="info"></a>
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

### 3. Comparer les régions pour un indicateur <a name="example1"></a>
* ![accéder aux 8 figures](/Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions)
* 3 exemples :
- **hospitalisation** :
![Figure hosp](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-hosp.png)
- **réanimation** :
![Figure réa](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-rea.png)
- **décès** :
![Figure décès](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-deces.png)
### 3. Suivre un indicateur dans une région et ses départements<a name="example3"></a>
* Les données hospitalières à l'échelon départemental ne sont pas disponibles par classe d'âge.
* Pour cette raison, seuls les 5 indicateurs qui concernent les tests virologiques et la vaccination sont présentés.
* ![accéder aux 14 * 5 = 70 figures](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs) 
* 3 exemples :
- **incidence** en **Île-de-France** :
![Incidence Île-de-France](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/%C3%8Ele-de-France/fig-%C3%8Ele-de-France-incidence.png)
- **incidence** en **Bretagne** :
![Incidence Bretagne](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/Bretagne/fig-Bretagne-incidence.png)
* **vaccination** dans les départements et régions d'**Outre-mer** :
![Dose 2 Outre-Mer](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/Outre-mer%20(DROM)/fig-Outre-mer%20(DROM)-dose2.png)

### 5. ... et enfin le code source <a name="example4"></a>
* données brutes :
![fichiers téléchargés sur data.gouv.fr - données Santé Publique France](/Data)
* traitement des données :
![Jupyter notebook pour traiter les données brutes](/Code/v4%20Traitement%20des%20donn%C3%A9es.ipynb)
> L'exécution de ce calepin prend **6** secondes
* tracé des figures :
![Jupyter notebook pour tracer les figures](/Code/v4%20Trac%C3%A9%20des%20figures.ipynb)
> L'exécution de ce calepin prend (13 + 18 + 74) = **105** secondes
* et pour faire fonctionner les calepins...
![home-baked Python modules](/Code/my_package)