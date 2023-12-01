.. raw:: html

    <style> .blue {color:blue} </style>

.. role:: blue

.. raw:: html

    <style> .red {color:red} </style>

.. role:: red

HOW TO DEFINE AN UNSTEADY TEST-CASE ?
==============================================================

L'objectif ici est de mettre en place un cas-test **instationnaire**, c'est a dire qu'on pretera attention aux resultats obtenus pendant le transitoire. Ceux-ci devront etre justes puisqu'ici, nous ne nous interesserons pas seulement a ce qui se passe une fois que le regime stationnaire est etabli. Nous chercherons a comprendre et a analyser les resultats obtenus durant l'etablissement et l'evolution des phenomenes physiques.

Pour ce faire, nous repartirons de la fiche :doc:`HowToDefStatCaseWithT` en transformant la cavite carree en cavite rectangulaire. L'agrandissemnt vertical de la cavite fait apparaitre d'autres tourbillons contre-directionnels. Ceux-ci ne sont pas stationnaires et bougent en permanence ce qui ne permet pas de trouver une solution stationnaire a ce probleme.

Figure

Reprenons point par point, la constitution  du jeu de donnes :

* **Le maillage** : rien ne change par mise a part, une augmentation du nombre de mailles selon Y.
* **La physique resolue** : on se pose les memes questions que pour la fiche :doc:`HowToDefStatCaseWithT` : peut-on utiliser l'approximation de Boussinesq ? Non, on resout donc une probleme Quasi-Compressible en utilisatant le mot cle :blue:`Pb_Thermohydraulique_QC`
* **Les proprietes des fluides** : celles-ci sont definies de la meme facon que pour la fiche :doc:`HowToDefStatCaseWithT`
* **Le schema en temps** : celui-ci doit etre change car il n'est plus possible de travail avec un schema implicite. On passe alors a des schemas explicites. Les mouvements etant incessants, il est necessaire d'utiliser des schemas d'ordre eleve en temps. Tous les schemas doivent avoir le meme ordre (schema en temps/schema de diffusion/schema de convection) sinon une simplification trop forte sur l'un des termes est faite, perturbant l'ensemble des resultats. Le gradient de Pression doit avoir un ordre de moins que les autres, il est donc recommande d'utiliser un schema d'ordre 2 et plus particuliereement le **schema Range-Kutta d'ordre 2**
