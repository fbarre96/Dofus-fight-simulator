"""@summary: Rassemble les états qui déclenche un effet."""

from Etats.Etat import Etat


class EtatEffetFinTour(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur termine son tour."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état ou
                "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetFinTour(self.nom, self.debuteDans, self.duree, self.effet,
                                self.nomSort, self.quiLancera, self.lanceur, self.desc)

    def triggerFinTour(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Active un effet à la fin du tour du personnage ciblant la position du
                     personnage qui finit son tour,
                     le lanceur peut être lui-même ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, personnage)


class EtatEffetDebutTour(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur débute son tour."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état
               ou "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetDebutTour(self.nom, self.debuteDans, self.duree, self.effet,
                                  self.nomSort, self.quiLancera, self.lanceur, self.desc)

    def triggerDebutTour(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour commence.
                     Active un effet au début du tour ciblant
                     la case du personnage dont le tour débute
                     avec comme lanceur le personnage dont le tour débute  ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: Personnage grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, personnage)


class EtatEffetSiSubit(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur subit des dégâts."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera,
                 cible, typeDeg="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'un dégât subit
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui lancera l'effet
        @type: string ("lanceur" ou "cible")
        @cible: Le personnage qui subira l'effet
        @type: string ("attaquant" ou "cible")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.cible = cible
        self.typeDeg = typeDeg
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiSubit(self.nom, self.debuteDans, self.duree, self.effet, self.nomSort,
                                self.quiLancera, self.cible, self.typeDeg, self.lanceur, self.desc)

    def triggerAvantSubirDegats(self, cibleAttaque, niveau, totalPerdu, typeDegats, attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages vont être subits.
                     Active un effet ciblant le lanceur ou la cible avant de subir les dégâts
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if totalPerdu > 0 and (self.typeDeg == typeDegats or self.typeDeg == ""):

            self.effet.setDegatsSubits(totalPerdu, typeDegats)
            joueurCible = cibleAttaque
            if self.cible == "attaquant":
                joueurCible = attaquant
            if self.quiLancera == "lanceur":
                niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                                   self.nomSort, joueurCible.posX, joueurCible.posY, self.lanceur)
            elif self.quiLancera == "cible":
                niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                                   self.nomSort, joueurCible.posX, joueurCible.posY, attaquant)

class EtatEffetSiMeurt(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur meurt."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera,
                 cible, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'un dégât subit
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui lancera l'effet
        @type: string ("lanceur" ou "cible")
        @cible: Le personnage qui subira l'effet
        @type: string ("attaquant" ou "cible")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.cible = cible
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiMeurt(self.nom, self.debuteDans, self.duree, self.effet, self.nomSort,
                                self.quiLancera, self.cible, self.lanceur, self.desc)

    def triggerAvantMort(self, niveau, porteur, mouru, meurtrier):
        """@summary: Un trigger appelé pour tous les états des joueurs
                     lorsque un perso meurt.
                     Active un effet ciblant le meurtier ou la victime ou le porteur avant la mort
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        joueurCible = porteur
        if self.cible == "meurtrier":
            joueurCible = meurtrier
        elif self.cible == "mouru":
            joueurCible = mouru
        celuiQuiLance = porteur
        if self.quiLancera == "meurtrier":
            celuiQuiLance = meurtrier
        elif self.quiLancera == "mouru":
            celuiQuiLance = mouru
        elif self.quiLancera == "lanceur":
            celuiQuiLance = self.lanceur
        niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                           self.nomSort, joueurCible.posX, joueurCible.posY, celuiQuiLance)

class EtatEffetSiPousse(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait pousser."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiPousse(self.nom, self.debuteDans, self.duree, self.effet, self.nomSort,
                                 self.quiLancera, self.lanceur, self.desc)

    def triggerCalculPousser(self, doPou, rePou, niveau, pousseur, joueurCible):
        """@summary: Un trigger appelé pour tous les états du pousseur qui aura
                     poussé sa cible contre un obstacle.
                     Active un effet sur le lanceur ou la cible au choix si
                     le joueur portant l'état est poussé
        @doPou: La caractéristique dommage de poussée du pousseur +
                les états l'ayant déjà éventuellement modifiée.
        @type: int
        @niveau: La grille de jeu
        @type: Niveau
        @pousseur: Le joueur qui à pousser
        @type: Personnage
        @joueurCible: Le joueur qui s'est fait pousser
        @type: Personnage

        @return: La nouvelle valeur de dommage de poussé"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, self.lanceur.posX, self.lanceur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, joueurCible)
        return doPou, rePou


class EtatEffetSiPiegeDeclenche(Etat):
    """@summary: Classe décrivant un état qui active un Effet
                 quand un joueur marche dans un piege."""

    def __init__(self, nom, debDans, duree, effet, nomSort,
                 quiLancera, cible, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet

        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.cible = cible
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiPiegeDeclenche(self.nom, self.debuteDans, self.duree, self.effet,
                                         self.nomSort, self.quiLancera, self.cible,
                                         self.lanceur, self.desc)

    def triggerAvantPiegeDeclenche(self, niveau, piege, joueurDeclencheur, porteur):
        if self.cible == "declencheur":
            joueurCible = joueurDeclencheur
        elif self.cible == "porteur":
            joueurCible = porteur
        else:
            joueurCible = self.lanceur
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, self.lanceur.posX, self.lanceur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, joueurCible)
        elif self.quiLancera == "porteur":
            niveau.lancerEffet(self.effet, porteur.posX, porteur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, porteur)


class EtatEffetSiTFGenere(Etat):
    """@summary: Classe décrivant un état qui active un Effet quand un joueur est téléfragé."""

    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera,
                 cible, porteurEstTF=False, sortInterdit="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passéq
                pour que l'état se désactive.
        @type: int
        @effet: l effet qui s'activera lors d'un TF
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.porteurEstTF = porteurEstTF
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        self.cible = cible
        self.sortInterdit = sortInterdit
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiTFGenere(self.nom, self.debuteDans, self.duree, self.effet, self.nomSort,
                                   self.quiLancera, self.cible, self.porteurEstTF,
                                   self.sortInterdit, self.lanceur, self.desc)

    def triggerApresTF(self, niveau, joueurOrigineTF, joueurEchangeTF,
                       porteur, reelLanceur, nomSort):
        if self.porteurEstTF and porteur.uid != joueurOrigineTF.uid \
                             and porteur.uid != joueurEchangeTF.uid:
            return
        if self.cible == "joueurOrigineTF":
            joueurCible = joueurOrigineTF
        elif self.cible == "joueurEchangeTF":
            joueurCible = joueurEchangeTF
        elif self.cible == "porteur":
            joueurCible = porteur
        elif self.cible == "reelLanceur":
            joueurCible = reelLanceur
        else:
            joueurCible = self.lanceur
        if self.quiLancera == "joueurOrigineTF":
            joueurLanceur = joueurOrigineTF
        elif self.quiLancera == "joueurEchangeTF":
            joueurLanceur = joueurEchangeTF
        elif self.quiLancera == "porteur":
            joueurLanceur = porteur
        elif self.quiLancera == "reelLanceur":
            joueurLanceur = reelLanceur
        else:
            joueurLanceur = self.lanceur
        if nomSort == self.sortInterdit:
            return
        if isinstance(self.effet, list):
            for eff in self.effet:
                eff.setNomSortTF(nomSort)
                sestApplique, _ = niveau.lancerEffet(eff, joueurLanceur.posX,
                                                     joueurLanceur.posY, self.nomSort,
                                                     joueurCible.posX, joueurCible.posY,
                                                     joueurLanceur)
                if not sestApplique:
                    break
        else:
            self.effet.setNomSortTF(nomSort)
            niveau.lancerEffet(self.effet, joueurLanceur.posX, joueurLanceur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, joueurLanceur)
