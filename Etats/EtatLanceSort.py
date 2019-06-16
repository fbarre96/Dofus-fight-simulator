"""@summary: Rassemble les états qui lance des sorts."""

from Etats.Etat import Etat


class EtatLanceSortSiSubit(Etat):
    """@summary: Classe décrivant un état qui fait active un sort si le porteur subit des dégâts."""

    def __init__(self, nom, debDans, duree, sort, lanceurDuSort, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @sort: le sort qui sera lancé lorsque des dégâts seront subits
        @type: Sort
        @lanceurDuSort: Le lanceur du sort parmis Porteur,Attaquant
        @type: str
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.sort = sort
        self.lanceurDuSort = lanceurDuSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatLanceSortSiSubit(self.nom, self.debuteDans, self.duree, self.sort,
                                    self.lanceurDuSort, self.lanceur, self.desc)

    def triggerApresSubirDegats(self, cibleAttaque, niveau, attaquant, totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages viennent d'être subits.
                     Le personnage subissant les dégâts lance le sort donné.
        @cibleAttaque: le joueur qui a subit les dégâts
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if self.lanceurDuSort == "Porteur":
            self.sort.lance(cibleAttaque.posX, cibleAttaque.posY,
                            niveau, cibleAttaque.posX, cibleAttaque.posY)
        elif self.lanceurDuSort == "Attaquant":
            self.sort.lance(attaquant.posX, attaquant.posY,
                            niveau, attaquant.posX, attaquant.posY)
