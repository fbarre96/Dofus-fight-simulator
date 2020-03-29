"""@summary: Rassemble les états qui redistribuent les dégâts subits autour du blessé."""

from Etats.Etat import Etat
from Effets.EffetDegats import EffetDegats
import Zones


class EtatRedistribuerPer(Etat):
    """@summary: Classe décrivant un état qui redistribue en partie les dégâts
                 subits autour du personnage endommagé"""

    def __init__(self, nom, debDans, duree, pourcentage, cibles, tailleZone, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @pourcentage: le pourcentage des gégâts qui sera redistribué
        @type: int
        @cibles: la liste des cibles qui peuvent être touchés par la redistribution
        @type: string, les cibles séparées par des '|'
        @tailleZone: le rayon du cercle de redistribution
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        self.cibles = cibles
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatRedistribuerPer(self.nom, self.debuteDans, self.duree, self.pourcentage,
                                   self.cibles, self.tailleZone, self.lanceur, self.desc)

    def triggerApresSubirDegats(self, cibleAttaque, niveau, attaquant, totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages vont être subits.
                     Redistribue une partie des dégâts qui vont être subit dans la zone définit.
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        totalPerdu = int(totalPerdu*(self.pourcentage/100.0))
        effetRedistribution = EffetDegats(totalPerdu, totalPerdu, "renvoie",
                                          zone=Zones.TypeZoneCercle(self.tailleZone),
                                          bypassDmgCalc=True,
                                          cibles_possibles=self.cibles, cibles_exclues="Lanceur")
        niveau.lancerEffet(effetRedistribution, cibleAttaque.posX, cibleAttaque.posY,
                           "Redistribution", cibleAttaque.posX, cibleAttaque.posY)
