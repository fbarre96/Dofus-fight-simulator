from Etats.Etat import Etat
from Effets.Effet import Effet

class EffetPropage(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet propage un sort à la cible la plus proche dans la portée du sort (Flèche fulminante par exemple)."""

    def __init__(self, sort_sort, zone_zone, **kwargs):
        """@summary: Initialise un effet de propagation de sort.
        @sort_sort: le sort qui va être propagé
        @type: Sort
        @zone_zone: la zone de propagation possible à partir de la dernière cible
        @type: Zone
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.zone = zone_zone
        self.sort = sort_sort
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetPropage(self.sort, self.zone, **self.kwargs)

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

        # Etat temporaire pour marqué la cible comme déjà touché par la propagation
        joueurCaseEffet.appliquerEtat(
            Etat("temporaire", 0, 1), joueurLanceur)
        # Récupérations des joueurs respectant les critères du sort les plus proches, etat requis = pas temporaire
        joueursAppliquables = niveau.getJoueurslesPlusProches(
            joueurCaseEffet.posX, joueurCaseEffet.posY, joueurLanceur, self.zone, ["!temporaire"], self.ciblesPossibles)
        if len(joueursAppliquables) > 0:
            self.sort.lance(joueurCaseEffet.posX, joueurCaseEffet.posY, niveau,
                            joueursAppliquables[0].posX, joueursAppliquables[0].posY, joueurLanceur)