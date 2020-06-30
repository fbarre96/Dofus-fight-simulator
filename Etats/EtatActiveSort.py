"""@summary: Rassemble les états activant des sorts."""

from Etats.Etat import Etat


class EtatActiveSort(Etat):
    """@summary: Classe décrivant un état qui active un sort à chaque tour actif."""

    def __init__(self, nom, debDans, duree, nomSort="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @sort: le sort qui sera lancé au rafraîchissement de l'effet
        @type: Sort

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomSort = nomSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatActiveSort(self.nom, self.debuteDans, self.duree,
                              self.nomSort, self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        nomSortLbl = ttk.Label(frame, text="Nom du sort à lancer:")
        nomSortLbl.grid(row=0, column=0, sticky="e")
        self.nomSortEntry = ttk.Entry(frame, width=40)
        self.nomSortEntry.delete(0, 'end')
        self.nomSortEntry.insert(0, self.nomSort)
        self.nomSortEntry.grid(row=0, column=1, sticky="w")
        ret["nomSort"] = self.nomSortEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatActiveSort(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), infos["nomSort"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomSort"] = self.nomSort
        return ret

    def triggerRafraichissement(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit
                     (au début de chaque tour ou quand sa durée est modifiée).
                     Le sort est lancé à ce moment.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        sort = personnage.getSort(self.nomSort)
        sort.lance(personnage.posX, personnage.posY,
                        niveau, personnage.posX, personnage.posY)
