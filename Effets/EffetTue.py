"""@summary: Rassemble les effets de sort en rapport avec les kill instantanés."""

from Effets.Effet import Effet

class EffetTue(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet tue immédiatement les cibles."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet tueur.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTue(**self.kwargs)

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
        if joueurCaseEffet is not None:
            if niveau.isPrevisu():
                joueurCaseEffet.msgsPrevisu.append("Tue")
            else:
                niveau.tue(joueurCaseEffet, joueurLanceur)

    def __str__(self):
        return "Tue la cible"