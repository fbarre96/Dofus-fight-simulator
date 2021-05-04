"""@summary: Rassemble les états boostant les dégâts de bases d'un sort."""

from Etats.Etat import Etat


class EtatBoostBaseDeg(Etat):
    """@summary: décrit un état qui modifie les dégâts de base d'un sort pour le porteur."""

    def __init__(self, nom, debDans, duree, nomSort="", boostbaseDeg=0, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @nomSort: le nom du sort dont les dégâts de base seront boostés
        @type: string
        @boostbaseDeg: le gain de dommage de base pour le sort concerné
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.boostbaseDeg = int(boostbaseDeg)
        self.nomSort = nomSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostBaseDeg(self.nom, self.debuteDans, self.duree, self.nomSort,
                                self.boostbaseDeg, self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        nomSortLbl = ttk.Label(frame, text="Nom du sort a boost:")
        nomSortLbl.grid(row=0, column=0, sticky="e")
        self.nomSortEntry = ttk.Entry(frame, width=40)
        self.nomSortEntry.delete(0, 'end')
        self.nomSortEntry.insert(0, self.nomSort)
        self.nomSortEntry.grid(row=0, column=1, sticky="w")
        ret["nomSort"] = self.nomSortEntry
        modValueLbl = ttk.Label(frame, text="Modificateur :")
        modValueLbl.grid(row=1, column=0, sticky="e")
        self.modValueEntry = ttk.Entry(frame, width=5)
        self.modValueEntry.delete(0, "end")
        self.modValueEntry.insert(0, self.boostbaseDeg)
        self.modValueEntry.grid(row=1, column=1, sticky="w")
        ret["boostbaseDeg"] = self.modValueEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostBaseDeg(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), infos["nomSort"], infos["boostbaseDeg"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomSort"] = self.nomSort
        ret["boostbaseDeg"] = self.boostbaseDeg
        return ret

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort, minjet, maxjet):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages sont en train d'être calculés.
             Les dégâts de base du sort sont boostés si le nom du sort correspond à l'état
        @dommages: La somme des dommages bonus qui ont été calculé jusque là
                   (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là
                  (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts.
                  (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base,
                 la nouvelle valeur point de caractéristiques."""
        if nomSort == self.nomSort:
            baseDeg += self.boostbaseDeg
        return dommages, baseDeg, caracs


class EtatBoostBaseDegLvlBased(EtatBoostBaseDeg):
    """@summary: Classe décrivant un état qui modifie les dégâts de base d'un sort
                 pour le porteur selon son lvl.
    Hérite de EtatBoostBaseDeg"""

    def __init__(self, nom, debDans, duree, nomSort="", boostbaseDeg=0, lanceur=None, desc=""):
        super().__init__(nom, debDans, duree, nomSort, boostbaseDeg, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostBaseDegLvlBased(self.nom, self.debuteDans, self.duree, self.nomSort,
                                        int(self.boostbaseDeg), self.lanceur, self.desc)

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostBaseDegLvlBased(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), infos["nomSort"], int(infos["boostbaseDeg"]), None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomSort"] = self.nomSort
        ret["boostbaseDeg"] = int(self.boostbaseDeg)
        return ret

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort, minjet, maxjet):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages sont en train d'être calculés.
                     Les dégâts de base du sort sont boostés si le nom du sort correspond à l'état
        @dommages: La somme des dommages bonus qui ont été calculé jusque là
                    (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là
                  (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts.
                    (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base,
                 la nouvelle valeur point de caractéristiques."""
        if nomSort == self.nomSort:
            baseDeg += int((self.boostbaseDeg/100.0)*(self.lanceur.lvl))
        return dommages, baseDeg, caracs



class EtatMinMaxBaseDeg(Etat):
    """@summary: décrit un état qui minimise les dégâts de base d'un sort pour le porteur."""

    def __init__(self, nom, debDans, duree, howToChoose="min", nomSort="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @nomSort: le nom du sort dont les dégâts de base seront boostés
        @type: string
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.howToChoose = howToChoose
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatMinMaxBaseDeg(self.nom, self.debuteDans, self.duree,
                                self.howToChoose, self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        modValueLbl = ttk.Label(frame, text="Modificateur :")
        modValueLbl.grid(row=1, column=0, sticky="e")
        self.modValueCombobox = ttk.Combobox(frame, values=("min", "max"), state="readonly")
        self.modValueCombobox.set("min")
        self.modValueCombobox.grid(row=1, column=1, sticky="w")
        ret["howToChoose"] = self.modValueCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatMinMaxBaseDeg(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), infos["howToChoose"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["howToChoose"] = self.howToChoose
        return ret

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort, minjet, maxjet):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages sont en train d'être calculés.
             Les dégâts de base du sort sont boostés si le nom du sort correspond à l'état
        @dommages: La somme des dommages bonus qui ont été calculé jusque là
                   (panoplie et autres états)
        @type: int
        @baseDeg: Le dégât de base aléatoire qui a été calculé jusque là
                  (jet aléatoire plus autres états)
        @type: int
        @caracs: La somme de point de caractéristiques calculé jusque là (panoplie et autres états)
        @type: int
        @nomSort: Le sort qui est provoque les dégâts.
                  (utile pour les états modifiant les dégâts de base d'un seul sort)
        @type: string

        @return: la nouvelle valeur dommages, la nouvelle valeur dégâts de base,
                 la nouvelle valeur point de caractéristiques."""
        if self.howToChoose == "min":
            return dommages, minjet, caracs
        else:
            return dommages, maxjet, caracs
