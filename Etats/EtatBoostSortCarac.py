"""@summary: Rassemble les états boostant une caractéristique d'un sort."""

from Etats.Etat import Etat
from Sort import Sort

class EtatBoostSortCarac(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur d'une Sort."""

    def __init__(self, nom, debDans, duree, nomSort="", nomAttributCarac="",
                 boostCarac=0, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devra
                passé pour que l'état se désactive.
        @type: int
        @nomSort: Le sort dont les caracs doivent être modifiées
        @type: str
        @nomAttributCarac: Le nom de l'attribut a boost
        @type: string qui doit être dans les attribut de la classe Personnage
        @boostCarac: le gain de Caractéristique a appliqué
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomAttributCarac = nomAttributCarac
        self.boostCarac = int(boostCarac)
        self.nomSort = nomSort
        super().__init__(nom, debDans, duree, lanceur, desc)

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        import Personnages
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        nomSortLbl = ttk.Label(frame, text="Nom du sort à modifier:")
        nomSortLbl.grid(row=0, column=0, sticky="e")
        self.nomSortEntry = ttk.Entry(frame, width=50)
        self.nomSortEntry.delete(0, 'end')
        self.nomSortEntry.insert(0, self.nomSort)
        self.nomSortEntry.grid(row=0, column=1, sticky="w")
        ret["nomSort"] = self.nomSortEntry
        nomCaracLbl = ttk.Label(frame, text="Nom de la carac à modifier:")
        nomCaracLbl.grid(row=1, column=0, sticky="e")
        self.nomCaracCombobox = ttk.Combobox(frame, values=Sort.getCaracList(), state="readonly")
        if self.nomAttributCarac != "":
            self.nomCaracCombobox.set(self.nomAttributCarac)
        self.nomCaracCombobox.grid(row=1, column=1, sticky="w")
        ret["nomAttributCarac"] = self.nomCaracCombobox
        boostCaracLbl = ttk.Label(frame, text="Valeur du boost:")
        boostCaracLbl.grid(row=2, column=0, sticky="e")
        self.boostCaracSpinbox = tk.Spinbox(frame, from_=-999, to=999, width=4)
        self.boostCaracSpinbox.delete(0, 'end')
        self.boostCaracSpinbox.insert(0, int(self.boostCarac))
        self.boostCaracSpinbox.grid(row=2, column=1, sticky="w")
        ret["boostCarac"] = self.boostCaracSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostSortCarac(infos["nom"], infos["debuteDans"], infos["duree"], infos["nomSort"], infos["nomAttributCarac"], infos["boostCarac"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomSort"] = self.nomSort
        ret["nomAttributCarac"] = self.nomAttributCarac
        ret["boostCarac"] = self.boostCarac
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostSortCarac(self.nom, self.debuteDans, self.duree, self.nomSort,
                                  self.nomAttributCarac, self.boostCarac, self.lanceur, self.desc)

    def triggerRafraichissement(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit
                     (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def getSortToUpdate(self, perso):
        """@summary: Renvoie la variable sort correspondant au nom du sort
                     dans la variable nomSort de l'effet.
        @perso: Le personnage auquel appartient le sort
        @type: Personnage
        @return: le sort de type Sort
        """
        for sort in perso.sorts:
            if sort.nom == self.nomSort:
                return sort

    def triggerInstantane(self, **kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        sortToUpdate = self.getSortToUpdate(personnage)
        print("Boost sort "+str(self.nomSort)+" d perso "+str(personnage.classe))
        caracValue = getattr(sortToUpdate, self.nomAttributCarac)
        setattr(sortToUpdate, self.nomAttributCarac,
                caracValue + self.boostCarac)
        print("Modification du sort "+sortToUpdate.nom+" "+self.nomAttributCarac +
              ":"+str(caracValue)+" -> "+str(caracValue + self.boostCarac))
        niveau = kwargs.get("niveau", None)
        if niveau is not None:
            niveau.afficherSorts()

    def triggerAvantRetrait(self, personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        sortToUpdate = self.getSortToUpdate(personnage)
        caracValue = getattr(sortToUpdate, self.nomAttributCarac)
        setattr(sortToUpdate, self.nomAttributCarac,
                caracValue - self.boostCarac)
        print("Fin de modification du sort "+sortToUpdate.nom+" "+self.nomAttributCarac +
              ":"+str(caracValue)+" -> "+str(caracValue - self.boostCarac))
