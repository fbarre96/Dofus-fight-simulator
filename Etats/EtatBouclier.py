# -*- coding: utf-8 -*
"""@summary: Rassemble les états donnant des points de bouclier."""

from Etats.Etat import Etat


class EtatBouclierPerLvl(Etat):
    """@summary: Classe décrivant un état qui modifie les points de bouclier par niveau."""

    def __init__(self, nom, debDans, duree, boostBouclier, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @boostPA: le gain de Vita
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.boostBouclier = boostBouclier
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBouclierPerLvl(self.nom, self.debuteDans, self.duree,
                                  self.boostBouclier, self.lanceur, self.desc)

    def triggerRafraichissement(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit
                     (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de vitas sont boostés dès le rafraîchessement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self, **kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change le bouclier du joueur selon le boost Vita
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        pourcentageBoost = self.boostBouclier
        self.boostBouclier = int(personnage.lvl * (pourcentageBoost/100.0))
        print("Modification de bouclier:"+str(self.boostBouclier))

    def triggerAvantRetrait(self, personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire les points de bouclier bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        print("Modification de bouclier: -"+str(self.boostBouclier))
