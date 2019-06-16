"""
@summary: Décrit un effet qui dévoile les pièges invisibles aux ennemis
"""

from Effets.Effet import Effet

class EffetDevoilePiege(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet dévoile les pièges invisibles."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet retirant l'invisiblité des pièges.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetDevoilePiege(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        caseEffetX = kwargs.get("caseEffetX")
        caseEffetY = kwargs.get("caseEffetY")
        for piege in niveau.pieges:
            if piege.aPorteDeclenchement(caseEffetX, caseEffetY):
                piege.invisible = False
                