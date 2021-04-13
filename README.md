# data-Covid
Le but de ce projet est de présenter les données (librement disponibles) épidémiologiques de la Covid-19 et de la vaccination en France de façon à pouvoir : 
* comparer l'impact sur trois classes d'âge : 0-29, 30-59 et + de 60 ans
* comparer les régions entre elles

1. [Suivi des huit indicateurs pour toutes les régions](#example1)
2. [Suivi en parallèle de cinq indicateurs pour différentes régions](##example2)
3. [Suivi de chaque indicateur dans chaque région et ses départements](###example3)
4. [Informations importantes](#infos)
5. [Code source](#example4) 

### 1. Suivi des huit indicateurs pour toutes les régions <a name="example1"></a>
* ![Accès aux huit figures](/Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions)
* Suivi du taux de patients hospitalisés :
![Figure hosp](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-hosp.png)
* Suivi du taux de patients en réanimation :
![Figure réa](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-rea.png)
* Suivi du taux de décès hebdomadaire :
![Figure décès](Output/Figures%20Synth%C3%A8se%20de%20chaque%20indicateur%20pour%20l'ensemble%20des%20r%C3%A9gions/fig-hosp.png)
### 2. Suivi en parallèle de cinq indicateurs pour différentes régions<a name="example2"></a>
* ![Accès aux trois figures (+1)](/Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions)
* Suivi de cinq indicateurs dans les 4 régions les plus touchées :
![Figure 1 / 3](Output/Figures%20Suivi%20parall%C3%A8le%20de%205%20indicateurs%20sur%20l'ensemble%20des%20r%C3%A9gions/regions-1%20sur%203.png)
### 3. Suivi de chaque indicateur dans chaque région et ses départements <a name="example3"></a>
* Les données hospitalières à l'échelon départemental ne sont pas disponibles par classe d'âge
* Pour cette raison, seuls les cinq indicateurs concernant les tests virologiques et la vaccination sont présentés
* ![Accès aux (14 x 5) figures](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs) 
* Suivi de l'incidence en Île-de-France :
![Incidence Île-de-France](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/%C3%8Ele-de-France/fig-%C3%8Ele-de-France-incidence.png)
* Suivi de l'incidence en Nouvelle-Aquitaine :
![Incidence Nouvelle-Aquitaine](/Output/Figures%20Synth%C3%A8se%20pour%20chaque%20r%C3%A9gion%20de%205%20indicateurs/Nouvelle-Aquitaine/fig-Nouvelle-Aquitaine-incidence.png)
### 4. Informations importantes<a name="info"></a>
_Chaque indicateur est rapporté à la population de chaque classe d'âge :_
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
### 5. Code source <a name="example4"></a>
* Données de départ (disponible sur data.gouv.fr - source Santé Publique France) :
![Données de départ](/Data)
* Traitement des données :
![Classeur pour le traitement des données](/Code/v4%20Traitement%20des%20donn%C3%A9es.ipynb)
L'exécution de ce classeur prend 6 secondes
* Tracé des figures :
![Classeur pour le tracé des figures](/Code/v4%20Trac%C3%A9%20des%20figures.ipynb)
L'exécution de ce classeur prend (13 + 18 + 74) = 105 secondes
* Modules :
![my_package](/Code/my_package)
