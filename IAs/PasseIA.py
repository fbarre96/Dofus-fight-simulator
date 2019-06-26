"""@summary: Une IA d'invoc
"""

class PasseIA():
    """
    @summary: Décrit un IA qui passe jsute son tour.
    """

    def __init__(self):
        self.interactif = False

    def joue(self, event, joueur, niveau, mouseXY, sortSelectionne):
        # pylint: disable=unused-argument
        """@summary: Fonction appelé par la boucle principale pour demandé à un
        PersonnageSansPM d'effectuer ses actions.
        Dans la classe PersonnageSansPM, lancer son seul sort
        sur lui-même et terminé son tour (comportement temporaire).
        @event: les évenements pygames survenus
        @type: Event pygame
        @niveau: La grille de jeu
        @type: Niveau
        @mouseXY: Les coordonnées de la souris
        @type: int
        @sortSelectionne: Le sort sélectionné plus tôt dans la partie s'il y en a un
        @type: Sort"""
        print("--------------------------------")
        print("Tour de "+(niveau.tourDe.nomPerso))
        niveau.finTour()
