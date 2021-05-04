"""@summary: Rassemble les états qui redistribuent les dégâts subits autour du blessé."""

from Etats.Etat import Etat
from Effets.EffetDegats import EffetDegats
import Zones


class EtatRedistribuerPer(Etat):
    """@summary: Classe décrivant un état qui redistribue en partie les dégâts
                 subits autour du personnage endommagé"""

    def __init__(self, nom, debDans, duree, pourcentage=50, cibles="Ennemis", tailleZone=1, lanceur=None, desc=""):
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

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        pourcentageLbl = ttk.Label(frame, text="Pourcentage de de restribution:")
        pourcentageLbl.grid(row=0, column=0, sticky="e")
        pourcentageSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        pourcentageSpinbox.delete(0, 'end')
        pourcentageSpinbox.insert(0, int(self.pourcentage))
        pourcentageSpinbox.grid(row=0, column=1, sticky="w")
        ret["pourcentage"] = pourcentageSpinbox
        tailleZoneLbl = ttk.Label(frame, text="Taille cercle de renvoi:")
        tailleZoneLbl.grid(row=1, column=0, sticky="e")
        tailleZoneSpinbox = tk.Spinbox(frame, from_=0, to=99, width=2)
        tailleZoneSpinbox.delete(0, 'end')
        tailleZoneSpinbox.insert(0, int(self.tailleZone))
        tailleZoneSpinbox.grid(row=1, column=1, sticky="w")
        ret["tailleZone"] = tailleZoneSpinbox
        ciblesLbl = ttk.Label(frame, text="Cibles possibles :")
        ciblesLbl.grid(row=2, column=0, sticky="e")
        ciblesEntry = ttk.Entry(frame, width=20)
        ciblesEntry.delete(0, "end")
        ciblesEntry.insert(0, self.cibles)
        ciblesEntry.grid(row=2, column=1, sticky="w")
        ret["cibles"] = ciblesEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatRedistribuerPer(infos["nom"], infos["debuteDans"], infos["duree"], infos["pourcentage"], infos["cibles"], infos["tailleZone"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage"] = self.pourcentage
        ret["tailleZone"] = self.tailleZone
        ret["cibles"] = self.cibles
        return ret

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
