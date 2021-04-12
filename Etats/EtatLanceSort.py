"""@summary: Rassemble les états qui lance des sorts."""

from Etats.Etat import Etat


class EtatLanceSortSiSubit(Etat):
    """@summary: Classe décrivant un état qui fait active un sort si le porteur subit des dégâts."""

    def __init__(self, nom, debDans, duree, sort, lanceurDuSort, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @sort: le sort qui sera lancé lorsque des dégâts seront subits
        @type: Sort
        @lanceurDuSort: Le lanceur du sort parmis Porteur,Attaquant
        @type: str
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.sort = sort
        self.lanceurDuSort = lanceurDuSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatLanceSortSiSubit(self.nom, self.debuteDans, self.duree, self.sort,
                                    self.lanceurDuSort, self.lanceur, self.desc)

    def triggerApresSubirDegats(self, cibleAttaque, niveau, attaquant, totalPerdu):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages viennent d'être subits.
                     Le personnage subissant les dégâts lance le sort donné.
        @cibleAttaque: le joueur qui a subit les dégâts
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if self.lanceurDuSort == "Porteur":
            self.sort.lance(cibleAttaque.posX, cibleAttaque.posY,
                            niveau, cibleAttaque.posX, cibleAttaque.posY)
        elif self.lanceurDuSort == "Attaquant":
            self.sort.lance(attaquant.posX, attaquant.posY,
                            niveau, attaquant.posX, attaquant.posY)

class EtatLanceSortSiChangementDeVie(Etat):
    """@summary: Classe décrivant un état qui fait active un sort si le porteur subit des dégâts."""

    def __init__(self, nom, debDans, duree, sort="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @sort: le sort qui sera lancé lorsque des dégâts seront subits
        @type: Sort
        @lanceur: Le lanceur du sort
        @type: str
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.sort = sort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatLanceSortSiChangementDeVie(self.nom, self.debuteDans, self.duree, self.sort,
                                     self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        nomSortlbl = ttk.Label(frame, text="Nom sort à lancer:")
        nomSortlbl.grid(row=0, column=0, sticky="e")
        self.nomSortEntry = ttk.Entry(frame, width=50)
        self.nomSortEntry.delete(0, "end")
        self.nomSortEntry.insert(0, self.sort)
        self.nomSortEntry.grid(row=0, column=1, sticky="w")
        ret["sort"] = self.nomSortEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatLanceSortSiChangementDeVie(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), infos["sort"], 
              None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["sort"] = self.sort
        return ret

    def triggerApresChangementDeVie(self, porteur, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages viennent d'être subits.
                     Le personnage subissant les dégâts lance le sort donné.
        """
        sortALance = porteur.getSort(self.sort)
        print("Lancement du sort par trigger changement de vie"+sortALancer.nom)
        sortALance.lance(porteur.posX, porteur.posY,
                        niveau, porteur.posX, porteur.posY)
        
