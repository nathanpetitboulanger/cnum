> *Remarques sur la fiche bilan :*

- *sauf indication contraire, les parties sont à renseigner de façon
    collective pour chaque groupe projet. Pour les parties à renseigner
    de façon individuelle, rédigez une sous-partie par participant*
- *effectuez les analyses dejfaçon tout d'abord précise et détaillée
    ensuite suivie d'une synthèse*
- *vous n'êtes **pas** dans ce bilan évalué sur l'atteinte des
    objectifs (partie A), le choix des méthodes et l'identification des
    risques (B), votre niveau d'apprentissage (C), votre niveau de
    compétence (D). Vous êtes évalués sur l'analyse que vous en faites.
    Vous pouvez donc être le plus objectif dans cette analyse critique.*

# Nom du projet : Automatisation de l'emploi du temps de l'UE SEABV

Nom des participants : TAUZIN Pierre, PETITBOULANGER Nathan, NGUYEN-DUC
Mathis

Page web du dépot GitHub : <https://github.com/nathanpetitboulanger/cnum>

Page web du projet :
<https://cnum.toile-libre.org/2026/EDT/projetedt.html>

## A) Bilan sur le produit

1. Confrontez ici le produit que vous avez réalisé au cahier des
    charges. Dans quelle mesure les fonctions sont-elles opérationnelles
    ? Dans quelle mesure les attributs décrits dans la fiche projet
    correspondent-ils à ceux du produit fini ?

**Fonctions opérationnelles :** La lecture de l\'EDT graphique, la
synchronisation avec la liste et l\'export iCal sont fonctionnels.
L\'extraction par couleur pour identifier le public marche bien.

**Attributs :** La précision d\'extraction est proche des 98% prévus
grâce aux Regex. Le temps de traitement est très rapide, moins de 10
secondes pour un semestre.

**Synthèse :** Le produit transforme bien un dessin Excel en base de
données exploitable pour le calcul des heures.

1. Quelle note pensez-vous recevoir de la part de votre commanditaire,
    en expliquant pourquoi ?

16/20. L'outil répond au besoin du gain de temps et de l'automatisation.
Il sera utilisé par le commanditaire.

## B) Bilan sur les méthodes

1. Confrontez ici les méthodes proposées dans la fiche projet
    (techniques et organisationnelles) à ce qui a été fait en pratique.
    Avez vous rencontré d'autres difficultés techniques ou
    organisationnelles ? Les tâches ont-elles pris le temps prévu ?
    Aviez vous correctement identifié tous les risques ?

**Technique :** Nous avons utilisé Python et les API Google Sheets comme
prévu.

**Organisation :** Les tâches ont suivi l\'ordre du PBS. La répartition
du travail en équipe complète a bien fonctionné.

**Risques :** Le risque de dépassement de délais était réel sur la
partie synchronisation. Nous n\'avions pas prévu la difficulté des
cellules fusionnées multiples.

**Synthèse :** Les méthodes étaient adaptées, mais la phase de tests a
pris plus de temps que les 4h prévues par personne.

1. Si vous aviez à réaliser de nouveau ce projet, mais maintenant
    éclairé de l'expérience que vous avez gagnée, que feriez vous
    différemment, en expliquant pourquoi ?

Nous passerions plus de temps sur la phase de modélisation (T1) au
début. Anticiper tous les cas particuliers de formatage dès le départ
évite de réécrire le code du moteur de lecture plus tard.

## C) Bilan sur les apprentissages

1. (individuel) Indiquez ce que la réalisation de ce projet vous a
    permis d'apprendre (en terme de savoir, savoir-faire, savoir-être).

**Mathis Nguyen-Duc :**

Utiliser une API google sheets en Python, gérer des fichiers Ical.

**Nathan Petitboulanger :**

Acquisition d'une expertise solide en matière de gestion de version décentralisée avec GIT, essentielle pour la collaboration agile et l'intégrité du code. Parallèlement, j'ai développé une habileté certaine à interagir et à piloter des processus complexes via GEMINI-CLI, en tirant parti de ses fonctionnalités avancées pour accélérer le cycle de développement et l'automatisation des tâches.

**Pierre Tauzin :**

Utilisation générale de python, découverte de l'API google sheet, de git, utilisation des commandes bash, et du logiciel Neovim

1. (individuel) Quelles sont les suites en terme d'apprentissage que
    vous envisagez, en expliquant pourquoi ?

**Mathis Nguyen-Duc** : Approfondir le code HTML ou Java

**Pierre Tauzin** : Approfondir l'utilisation de python, de git et de bash

**Nathan Petitboulanger** : Dans une optique de diversification de mes compétences et d'expansion vers des horizons technologiques innovantes, je compte m'immerger dans l'apprentissage approfondi du JavaScript. Cette démarche vise à me doter des outils nécessaires pour concevoir et implémenter des interfaces web dynamiques et des expériences utilisateur enrichies, consolidant ainsi ma capacité à livrer des solutions full-stack performantes et interactives.

## D) Bilan sur les compétences

> "*Une compétence est un savoir-agir complexe qui s'appuie sur la
> mobilisation et la combinaison efficaces d'un ensemble de ressources
> internes et externes dans une famille de situations*" (J. Tardiff)

1. Identifiez les ressources internes et externes (ouvrage, tutoriel,
    personne, IA, ...) que vous avez mobilisées pour réaliser votre
    produit et de façon très spécifique ce qu'elles vous ont apporté (en
    terme de savoir, savoir-faire, savoir-être). Indiquez de façon
    claire et quantifiée la contribution de l'IA au projet. Explicitez
    comment ces ressources ont du être combinées pour répondre à la
    demande et argumentez dans quelle mesure la tâche était complexe.

- Documentation de la bibliothèque Gspread
- Tutoriels API Google
- IA Gemini
  - Gemini nous a aidé à comprendre des fonctions spécifiques et à corriger des bugs de Regex.

1. (individuel) Effectuez le lien explicite avec le référentiel de
    compétence ENSAT, en indiquant de façon argumentée sur quel
    compétence ce projet vous a permis de progresser et quel
    apprentissage critique il vous permettrait de valider.

**Mathis Nguyen-Duc** :

Concevoir et mettre en oeuvre une solution numérique. Le projet m'a
donné la capacité à automatiser un flux de données complexe pour aider à
la décision logistique.

**Nathan Petitboulanger** :

Ce projet fut un catalyseur pour le développement et la validation de compétences fondamentales. J'ai significativement progressé dans ma capacité à **communiquer** des concepts techniques complexes de manière claire et percutante, favorisant une compréhension partagée au sein de l'équipe et avec les parties prenantes. Sur le plan de la **conception** numérique, j'ai affûté mon acuité à transformer des besoins fonctionnels en solutions robustes et évolutives, en intégrant les meilleures pratiques du génie logiciel. L'**organisation** d'une codebase structurée et maintenable est devenue une seconde nature, assurant la pérennité et la facilité d'intervention sur le projet. Enfin, l'élaboration et la mise en œuvre d'une **architecture** logicielle cohérente et performante m'ont permis de bâtir un socle technique solide, gage de la scalabilité et de la résilience du produit final.

**Pierre Tauzin** :

**Communiquer** des connaissance, **Concevoir** un project numérique.
**Organiser** une code base. Mettre au point une architecture
