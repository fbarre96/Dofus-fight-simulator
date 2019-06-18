"""@summary: Décrit un effet de sort faisant lancé un sort à
             toutes les entités correspondant à une donnée."""

from Effets.Effet import Effet

class EffetEntiteLanceSort(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet fait lancer un sort à une entité/joueur"""

    def __init__(self, str_nomEntites, sort_sort, caseCible="Entite", **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @str_nomEntites: les entités devant lancer le sort
        @type: string
        @sort_sort: le sort qui sera lancé par les entités
        @type: Sort
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEntites = str_nomEntites
        self.sort = sort_sort
        self.caseCible = caseCible
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEntiteLanceSort(self.nomEntites, self.sort, self.caseCible, **self.kwargs)

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
        joueursLanceurs = niveau.getJoueurs(self.nomEntites)
        for joueur in joueursLanceurs:
            cibleX = joueur.posX
            cibleY = joueur.posY
            if self.caseCible == "CaseCible":
                cibleX = kwargs.get("caseCibleX")
                cibleY = kwargs.get("caseCibleY")
            self.sort.lance(joueur.posX, joueur.posY,
                            niveau, cibleX, cibleY)
