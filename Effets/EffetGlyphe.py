"""@summary: Rassemble les effets de sort en rapport avec les glyphes."""

from Effets.Effet import Effet
from Glyphe import Glyphe

class EffetGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une glyphe sur la grille de jeu."""

    def __init__(self, sort_sort, sortDeplacement, sortSortie, int_duree,
                 str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant une glyphe.
        @sort_sort: le sort monocible qui est lancé sur les joueurs restants dans la glyphe
        @type: Sort
        @sortDeplacement: Le sort monocible qui est lancé sur les joueurs entrants dans la glyphe
        @type: Sort
        @sortSortie: Le sort monocible qui est lancé sur les joueurs sortants de la glyphe
        @type: Sort
        @int_duree: le nombre de tour où la glyphe sera active
        @type: int
        @str_nom: le nom de la glyphe
        @type: string
        @tuple_couleur: la couleur de la glyphe
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.sort = sort_sort
        self.sortDeplacement = sortDeplacement
        self.sortSortie = sortSortie
        self.duree = int_duree
        self.nom = str_nom
        self.couleur = tuple_couleur
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetGlyphe(self.sort, self.sortDeplacement, self.sortSortie,
                           self.duree, self.nom, self.couleur, **self.kwargs)

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
        nouvelleGlyphe = Glyphe(self.nom, self.sort, self.sortDeplacement, self.sortSortie,
                                self.duree, kwargs.get("caseCibleX"),
                                kwargs.get("caseCibleY"), joueurLanceur, self.couleur)
        niveau.poseGlyphe(nouvelleGlyphe)


class EffetActiveGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet relance les effets d'une glyphe"""

    def __init__(self, strNomGlyphe, **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @strNomGlyphe: la glyphe devant être réactivé
        @type: string

        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.strNomGlyphe = strNomGlyphe
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetActiveGlyphe(self.strNomGlyphe, **self.kwargs)

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

        niveau.activerGlyphe(self.strNomGlyphe)
