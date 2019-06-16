"""@summary: Rassemble les effets de sort en rapport avec les pièges."""
from Effets.Effet import Effet
import Niveau


class EffetPiege(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose un piège sur la grille de jeu."""

    def __init__(self, zoneDeclenchement, list_effets, str_nom, tuple_couleur, **kwargs):
        """@summary: Initialise un effet posant un piège.
        @zoneDeclenchement: la zone où si un joueur marche le piège se déclenche.
        @type: Zones.TypeZone
        @sort_sort: le sort lancé sur la case centrale du piège
        @type: Sort
        @str_nom: le nom du piège
        @type: string
        @tuple_couleur: la couleur du piège
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.zoneDeclenchement = zoneDeclenchement
        self.effets = list_effets
        self.nom = str_nom
        self.couleur = tuple_couleur
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetPiege(self.zoneDeclenchement, self.effets, self.nom,
                          self.couleur, **self.kwargs)

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
        nouveauPiege = Niveau.Piege(self.nom, self.zoneDeclenchement, self.effets, kwargs.get(
            "caseCibleX"), kwargs.get("caseCibleY"), joueurLanceur, self.couleur)
        niveau.posePiege(nouveauPiege)
