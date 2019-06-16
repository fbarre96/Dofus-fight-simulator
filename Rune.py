"""@summary: décrit la classe Rune
"""
class Rune:
    """@summary: Classe décrivant une rune dans le jeu Dofus.
     Une rune est une zone au sol qui se déclenche à la fin de sa durée de vie."""

    def __init__(self, nomRune, duree, effets, centreX, centreY, lanceur, couleur):
        """@summary: Initialise une rune.
        @nomSort: le nom du sort à l'origine de la rune
        @type: string
        @zoneDeclenchement: la zone où si un joueur marche le piège se déclenche.
        @type: Zones.TypeZone
        @sortMono: le sort qui va s'activer au début du tour du joueur qui se tient sur la rune. Le sort va être lancé sur le joueur dans la glyphe dont c'est le tour uniquement.
        @type: Sort
        @centreX: la coordonnée x du centre de la zone de la rune.
        @type: int
        @centreY: la coordonnée y du centre de la zone de la rune.
        @type: int
        @lanceur: le joueur ayant posé la rune.
        @type: Personnage
        @couleur: la coordonnée x du centre de la zone de la rune.
        @type: tuple (R,G,B)"""
        self.duree = duree
        self.nom = nomRune
        self.effets = effets
        self.centreX = centreX
        self.centreY = centreY
        self.lanceur = lanceur
        self.invisible = False
        self.couleur = couleur

    def actif(self):
        """@summary: Test si la rune est encore active
            @return: Retourne un booléen qui vaut vrai si la rune est encore active, faux sinon"""
        return self.duree > 0

    def activation(self, niveau):
        for effet in self.effets:
            niveau.lancerEffet(effet, self.centreX, self.centreY,
                               self.nom, self.centreX, self.centreY, self.lanceur)
