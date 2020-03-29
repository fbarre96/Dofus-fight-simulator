"""@summary: Une IA d'invoc
"""

class DumbIA():
    """
    @summary: Décrit un IA bête et méchante qui tente de lancer tout ses sorts,
              dans l'ordre.
    """

    def __init__(self):
        self.interactif = False

    def getCible(self, niveau, sort, joueurLanceur):
        """@summary: Retourne le joueur a ciblé par un sort.
        """
        casesPOSort = niveau.getZonePorteSort(sort, joueurLanceur.posX, joueurLanceur.posY,
                                              joueurLanceur.PO)
        for case in casesPOSort:
            res, msg = sort.estLancableSurCible(niveau, joueurLanceur, case[0], case[1])
            if res:
                return case[0], case[1]
        return None, None

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
        print("Nié! a moi de jouer")
        for sort in joueur.sorts:
            print(str(sort))
            cibleX, cibleY = self.getCible(niveau, sort, joueur)
            print("Cible trouvée :"+str(cibleX)+" ; "+str(cibleY))
            while cibleX is not None:
                sort.lance(niveau.tourDe.posX,
                           niveau.tourDe.posY, niveau, cibleX, cibleY)
                cibleX, cibleY = self.getCible(niveau, sort, joueur)
        niveau.finTour()
