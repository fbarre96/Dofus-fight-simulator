# Dofuk - Simulateur de combat Dofus© d'Ankama

## /!\\/!\\/!\\DISCLAIMER/!\\/!\\/!\\
**Ceci est simulateur de combat du jeu de la société Ankama 'Dofus'© 1v1. Ce simulateur ne vise en aucun cas à remplacé le jeu réel.
C'est pourquoi cette simulation est limitée dans ses fonctionnalitées et dans sa précision.**

**Ce jeu étant souvent la cible de piratage, je vais maintenant décrire le comportement attendu du programme:**

Le programme:
1. Lit **uniquement** les fichiers images contenues dans le dossier 'sorts' et dans le dossier 'images'
2. Lit et écrit **uniquement** un fichier 'save.txt' dans le dossier de l'exécution. Ce fichier contient simplement les paramètres du programmes, séparés par un saut de ligne.
3. N'accède **jamais** à une connexion internet.
4. Ne modifie **jamais** le contenu des registres.
5. N'exécute **jamais** de programmes externes.


## Installation
### Option 1:
Télécharger le dossier `dist` et lancer l'exécutable *Dofuk.exe*
N'AYEZ PAS CONFIANCE EN N'IMPORTE QUEL EXE CONCERCNANT DOFUS, si vous n'avez pas confiance en moi (bravo c'est bien, même si dans ce cas précis vous ne risquez rien) utilisez l'option 2 pour voir les sources que vous allez exécuter.

### Option 2:
* Installer python2.7, tkinter, pygame.
* Copier ou déplacer les dossiers `dist/images` et `dist/sorts` dans le dossier parent.
* Exécuter Dofuk.py avec l'interpréteur python 'python Dofuk.py' 
(ou installer py2exe pour Python 2.7 puis lancez le avec la commande `python setup.py py2exe`)


## Précisions:
Ce simulateur ne **remplace pas** Dofus©, il sert à visualiser ce que pourrait donner un stuff complet en jeu pour votre personnage ou bien à tester une autre classe. Le programme a donc peu de fonctionnalités avancées.
Le moteur de combat a été codé entièrement à vu de nez (je n'ai pas fait de reverse sur Dofus) donc certains comportements peuvent être différents du vrai jeu (ordre de traitements de cibles concurrentes par exemple)

## Limitations:
* Pour le moment seul 3 classes sont disponibles: Xélor, Iop et Crâ.
* Certains états et sorts ne sont tout simplement pas implémentés parce qu'ils apportent peu dans le test de la classe en 1v1 Poutch (Pesanteur, lourd par exemple). Servez vous de votre imagination.
* Plusieurs bugs peuvent être présent, si vous en trouvez, j'apprécierais énormément un retour (voir section Améliorations).
* Je me réserve le droit de ne pas corriger un bug mineur. Par exemple, l'anneau destructeur des Iops au corps à corps d'une cible ne déplace pas le Poutch.
* Certains sorts peuvent ne pas correspondre à la réalité, la raison est simple. Le seul personnage dont je dispose est un Xélor 18X. C'est donc la seule classe testée lorsque j'avais des doutes sur un sort. Les autres sorts ont été crée juste avec la description des sorts dans l'encyclopédie Dofus. Cette encyclopédie ne dit clairement pas tout. Notamment les sorts qui boost leur dommages dans certaines conditions. Testez donc les sorts avec les caractéristiques de vos personnages réels et donnez moi vos retours sur la précision des dégâts du simulateur.


## Améliorations:
Pour tout bug, incohérence du simulateur ou demande d'ajout (état ou classe), postez une 'issue' sur le github. Joignez-y le maximum d'informations sur le bug ou l'intérêt de la modification souhaitée.
Si le programme crash brutalement, assurez vous de rejouer le bug en lancant le programme depuis une console pour obtenir les logs de crash.

Merci d'avance pour vos retours, en espérant que cela pourra aider certaines personnes.
