"""@summary: Rassemble les effets de sort en rapport avec les Portés de pandawa."""

from Effets.Effet import Effet

class EffetPorte(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet fait porter un joueur au lanceur."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet posant une rune.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetPorte(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, caseCibleX et caseCibleY doivent être mentionés
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            joueurLanceur.faitPorter(joueurCaseEffet)

class EffetLance(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet fait lanceur le joueu porté par le lanceur."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.cibleX = -1
        self.cibleY = -1
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetLance(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, caseCibleX et caseCibleY doivent être mentionés
        @type: **kwargs"""
        self.cibleX = kwargs.get("caseCibleX", -1)
        self.cibleY = kwargs.get("caseCibleY", -1)
        if niveau.getJoueurSur(self.cibleX, self.cibleY) is not None:
            print("Destination du lancer n'est pas vide")
            return False
        joueurLanceur.faitLancer(niveau, self.cibleX, self.cibleY)
