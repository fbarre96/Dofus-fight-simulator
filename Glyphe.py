"""@summary: décrit la classe Glyphe
"""

class Glyphe:
    """@summary: Classe décrivant une glyphe dans le jeu Dofus.
     Une glyphe est une zone au sol qui déclenche un effet sur les joueurs
     se trouvant dessus au début de leur tour."""

    def __init__(self, zoneAction, nomSort, sortMono, sortDeplacement, sortSortie, dureeGlyphe,
                 centreX, centreY, lanceur, couleur):
        """@summary: Initialise une glyphe.
        @nomSort: le nom du sort à l'origine de la glyphe
        @type: string
        @sortMono: le sort qui va s'activer au début du tour du joueur qui se tient sur la glyphe.
                    Le sort va être lancé sur le joueur dans la glyphe dont c'est le tour uniquement
        @type: Sort
        @sortDeplacement: Le sort qui va s'activer sur un joueur qui rentre dans la glyphe
        @type: Sort
        @sortSortie: Le sort qui va s'activer sur un joueur qui sort de la glyphe
        @type: Sort
        @dureeGlyphe: Le nombre de début de tour du poseur que la glyphe va vivre
        @type: int
        @centreX: la coordonnée x du centre de la zone de la glyphe.
        @type: int
        @centreY: la coordonnée y du centre de la zone de la glyphe.
        @type: int
        @lanceur: le joueur ayant posé la glyphe.
        @type: Personnage
        @couleur: la coordonnée x du centre de la zone de la glyphe.
        @type: tuple (R,G,B)"""
        self.zoneAction = zoneAction
        self.nomSort = nomSort
        self.sortMono = sortMono
        self.sortDeplacement = sortDeplacement
        self.sortSortie = sortSortie
        self.duree = dureeGlyphe
        self.centreX = centreX
        self.centreY = centreY
        self.lanceur = lanceur
        self.couleur = couleur

    def actif(self):
        """@summary: Test si la glyphe est encore active
            @return: Retourne un booléen qui vaut vrai si la glyphe est encore active, faux sinon"""
        return self.duree > 0

    def aPorte(self, posX, posY):
        """@summary:Retourne vrai si la posX;posY donné est dans la zone du piège."""
        return self.zoneAction.testCaseEstDedans([self.centreX, self.centreY],
                                                 [posX, posY], None)
