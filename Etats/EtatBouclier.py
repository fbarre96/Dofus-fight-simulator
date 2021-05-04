# -*- coding: utf-8 -*
"""@summary: Rassemble les états donnant des points de bouclier."""

from Etats.Etat import Etat


class EtatBouclierPerLvl(Etat):
    """@summary: Classe décrivant un état qui modifie les points de bouclier par niveau."""

    def __init__(self, nom, debDans, duree, boostBouclier=100, lanceur=None, desc=""):
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

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        import Personnages
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        boostBouclierLbl = ttk.Label(frame, text="bouclier en % du level:")
        boostBouclierLbl.grid(row=2, column=0, sticky="e")
        self.boostBouclierSpinbox = tk.Spinbox(frame, from_=-999, to=999, width=4)
        self.boostBouclierSpinbox.delete(0, 'end')
        self.boostBouclierSpinbox.insert(0, int(self.boostBouclier))
        self.boostBouclierSpinbox.grid(row=2, column=1, sticky="w")
        ret["boostBouclier"] = self.boostBouclierSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBouclierPerLvl(infos["nom"], infos["debuteDans"], infos["duree"], infos["boostBouclier"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["boostBouclier"] = self.boostBouclier
        return ret

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
