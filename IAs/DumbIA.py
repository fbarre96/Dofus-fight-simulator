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
            joueurSur = niveau.getJoueurSur(case[0], case[1])
            if joueurSur is not None:
                res, _, _ = sort.estLancable(joueurLanceur, joueurSur)
                if res:
                    return joueurSur
        return None

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
        for sort in joueur.sorts:
            cible = self.getCible(niveau, sort, joueur)
            if cible is not None:
                res, _, _ = sort.estLancable(joueur, cible)
                if res:
                    sort.lance(niveau.tourDe.posX,
                               niveau.tourDe.posY, niveau, cible.posX, cible.posY)
        niveau.finTour()
