"""@summary: décrit la classe Piege
"""
import constantes

class Piege:
    """@summary: Classe décrivant un piège dans le jeu Dofus.
     Un piège est une zone au sol qui se déclenche
     lorsque qu'un joueur marche dessus."""

    def __init__(self, nomSort, zoneDeclenchement, effets, centreX, centreY,
                 lanceur, couleur, icone=None):
        """@summary: Initialise un piège.
        @nomSort: le nom du sort à l'origine du piège
        @type: string
        @zoneDeclenchement: la zone où si un joueur marche le piège se déclenche.
        @type: Zones.TypeZone
        @sortMono: le sort qui va s'activer au début du tour du joueur qui se tient sur la glyphe.
                   Le sort va être lancé sur le joueur dans la glyphe dont c'est le tour uniquement.
        @type: Sort
        @centreX: la coordonnée x du centre de la zone du piège.
        @type: int
        @centreY: la coordonnée y du centre de la zone du piège.
        @type: int
        @lanceur: le joueur ayant posé le piège.
        @type: Personnage
        @couleur: la coordonnée x du centre de la zone du piège.
        @type: tuple (R,G,B)"""
        self.zoneDeclenchement = zoneDeclenchement
        self.nomSort = nomSort
        self.effets = effets
        self.centreX = centreX
        self.centreY = centreY
        self.lanceur = lanceur
        self.invisible = True
        self.couleur = couleur
        if icone is not None:
            self.icone = icone
        else:
            self.icone = "images/" + \
                constantes.normaliser(nomSort.lower())+".jpg"

    def getDistanceDuPoint(self, x, y):
        return abs(self.centreX - x) + abs(self.centreY - y)

    def aPorteDeclenchement(self, x, y):
        return self.zoneDeclenchement.testCaseEstDedans([self.centreX, self.centreY], [x, y], None)
