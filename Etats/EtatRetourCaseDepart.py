"""@summary: Rassemble les états qui font revenir à la case du début de tour."""

from Etats.Etat import Etat


class EtatRetourCaseDepart(Etat):
    """@summary: Classe décrivant un état qui renvoie le porteur à sa case de début de tour
                 lorsqu'il termine son tour."""

    def __init__(self, nom, debDans, duree, nomSort, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @tabCarac: le tableau de donné dont dispose chaque état pour décrire ses données
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomSort = nomSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatRetourCaseDepart(self.nom, self.debuteDans, self.duree,
                                    self.nomSort, self.lanceur, self.desc)

    def triggerFinTour(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Le personnage retourne à sa case de début de tour lorsque son tour se termine
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        niveau.gereDeplacementTF(
            personnage, personnage.posDebTour, personnage, self.nomSort, AjouteHistorique=True)
