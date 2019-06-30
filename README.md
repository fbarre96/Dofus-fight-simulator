# Dofuk - Simulateur de combat Dofus© d'Ankama

## /!\\/!\\/!\\DISCLAIMER/!\\/!\\/!\\
**Ceci est simulateur de combat du jeu de la société Ankama 'Dofus'©. Ce simulateur ne vise en aucun cas à remplacer le jeu réel.
C'est pourquoi cette simulation est limitée dans ses fonctionnalitées et dans sa précision.**

**Ce jeu étant souvent la cible de piratage, je vais maintenant décrire le comportement attendu du programme:**

Le programme:
1. Lit **uniquement** les fichiers images contenues dans le dossier d'installation
2. N'accède **jamais** à une connexion internet.
3. Ne modifie **jamais** le contenu des registres.
4. N'exécute **jamais** de programmes externes.
5. Ne demande pas d'authentifiants à l'utilisateur

## Installation
### Sous Windows:
* Télécharger le zip du dossier github
* Extraire le zip dans un dossier de votre choix
* Exécuter Dofus_FS.exe dans le dossier d'installation
* OU
* Installer python3 (bien ajouter dans l'installeur l'option pour ajouter Python à la variable PATH):
![Capture1](https://github.com/fbarre96/Dofuk/raw/master/Documentation/capture_python.png)

https://www.python.org/ftp/python/3.7.3/python-3.7.3.exe
* Ouvrir une console de commande : appuyer sur la touche Windows puis taper cmd et enfin appuyer sur 'entrée'
* Installer pygame: entrer dans la console de commande : `pip install pygame`.
* Exécuter Dofus_FS.py en double cliquant dessus

### Sous Linux (Ubuntu):
* Cloner le projet github ou télécharger le zip
* Installer python3 : `sudo apt-get install python`
* Installer tkinter : `sudo apt-get install python-tk`
* Installer pip python : `sudo apt-get install python-pip`
* Installer pygame : `python3 -m pip install pygame`
* Executer Dofuk avec python : `python Dofus_FS.py`

## Précisions:
Ce simulateur ne **remplace pas** Dofus©, il sert à visualiser ce que pourrait donner un stuff complet en jeu pour votre personnage ou bien à tester une autre classe.
Le moteur de combat a été codé entièrement à vu de nez (je n'ai pas fait de reverse sur Dofus) donc certains comportements peuvent être différents du vrai jeu (ordre de traitements de cibles concurrentes par exemple).
Ce projet est encore en cours de développement et non officiel, il n'est pas destiné a être stable pour le moment. 

## Limitations:
* Pour le moment seul 4 classes sont disponibles: Xélor, Iop, Sram et Crâ.
* Plusieurs bugs peuvent être présent, si vous en trouvez, j'apprécierais énormément un retour (voir section Améliorations).
* Certains sorts peuvent ne pas correspondre à la réalité, la raison est simple. Les seuls personnages dont je dispose sont un Xélor 200 et un sram 200 Ce sont donc les seules classes testées lorsque j'avais des doutes sur un sort. Les autres sorts ont été crée juste avec la description des sorts dans l'encyclopédie Dofus. Cette encyclopédie ne dit clairement pas tout. Notamment les sorts qui boost leur dommages dans certaines conditions. Testez donc les sorts avec les caractéristiques de vos personnages réels et donnez moi vos retours sur la précision des dégâts du simulateur.
* Les effets pièges sont uniquement ceux du piège de niveau max car les valeurs des autres niveaux ne sont pas visiblent une fois ce niveau dépassé. 


## Améliorations:
Pour tout bug, incohérence du simulateur ou demande d'ajout (état ou classe), postez une 'issue' sur le github. Joignez-y le maximum d'informations sur le bug ou l'intérêt de la modification souhaitée.
Si le programme crash brutalement, assurez vous de rejouer le bug en lancant le programme depuis une console pour obtenir les logs de crash.

Merci d'avance pour vos retours, en espérant que cela pourra aider certaines personnes.
