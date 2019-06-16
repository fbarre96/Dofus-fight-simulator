from Effets.Effet import Effet
import Niveau

class EffetGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une glyphe sur la grille de jeu."""

    def __init__(self, sort_sort, sort_deplacement, sort_sortie, int_duree, str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant une glyphe.
        @sort_sort: le sort monocible qui est lancé sur les joueurs restants dans la glyphe
        @type: Sort
        @sort_deplacement: Le sort monocible qui est lancé sur les joueurs entrants dans la glyphe
        @type: Sort
        @sort_sortie: Le sort monocible qui est lancé sur les joueurs sortants de la glyphe
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
        self.sort_deplacement = sort_deplacement
        self.sort_sortie = sort_sortie
        self.duree = int_duree
        self.nom = str_nom
        self.couleur = tuple_couleur
        super(EffetGlyphe, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetGlyphe(self.sort, self.sort_deplacement, self.sort_sortie, self.duree, self.nom, self.couleur, **self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        nouvelleGlyphe = Niveau.Glyphe(self.nom, self.sort, self.sort_deplacement, self.sort_sortie, self.duree, kwargs.get(
            "case_cible_x"), kwargs.get("case_cible_y"), joueurLanceur, self.couleur)
        niveau.poseGlyphe(nouvelleGlyphe)


class EffetActiveGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet relance les effets d'une glyphe"""

    def __init__(self, str_nomGlyphe, **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @str_nomGlyphe: la glyphe devant être réactivé
        @type: string

        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.str_nomGlyphe = str_nomGlyphe
        super(EffetActiveGlyphe, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetActiveGlyphe(self.str_nomGlyphe, **self.kwargs)

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

        niveau.activerGlyphe(self.str_nomGlyphe)