"""@summary: Décrit un effet de sort faisant lancé un sort à
             toutes les entités correspondant à une donnée."""

from Effets.Effet import Effet
from Zones import TypeZoneCercle

class EffetEntiteLanceSort(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet fait lancer un sort à une entité/joueur"""

    def __init__(self, str_nomEntites="", nomSort="", caseCible="Entite", **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @str_nomEntites: les entités devant lancer le sort
        @type: string
        @sort_sort: le sort qui sera lancé par les entités
        @type: Sort
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEntites = str_nomEntites
        self.nomSort = nomSort
        self.caseCible = caseCible
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEntiteLanceSort(self.nomEntites, self.nomSort, self.caseCible, **self.kwargs)

    def __str__(self):
        return str(self.nomEntites)+" va lancer "+str(self.nomSort)+" sur "+str(self.caseCible)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomEntitesLbl = ttk.Label(frame, text="Lanceur(s) du sort:")
        nomEntitesLbl.pack(side="left")
        nomEntitesEntry = ttk.Entry(frame, width=50)
        nomEntitesEntry.delete(0, 'end')
        nomEntitesEntry.insert(0, self.nomEntites)
        nomEntitesEntry.pack(side="left")
        ret["nomEntites"] = nomEntitesEntry
        nomSortLbl = ttk.Label(frame, text="Nom du sort à lancer:")
        nomSortLbl.pack(side="left")
        nomSortEntry = ttk.Entry(frame, width=50)
        nomSortEntry.delete(0, 'end')
        nomSortEntry.insert(0, self.nomSort)
        nomSortEntry.pack(side="left")
        ret["nomSort"] = nomSortEntry
        caseCibleLbl = ttk.Label(frame, text="Case cible du sort:")
        caseCibleLbl.pack(side="left")
        caseCibleCombobox = ttk.Combobox(frame, values=("Entite", "CaseCible"), state="readonly")
        caseCibleCombobox.set(self.caseCible)
        caseCibleCombobox.pack(side="left")
        ret["caseCible"] = caseCibleCombobox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomEntites"] = self.nomEntites
        ret["nomSort"] = self.nomSort
        ret["caseCible"] = self.caseCible
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["nomEntites"], infos["nomSort"], infos["caseCible"], **infos["kwargs"])

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        joueursLanceurs = niveau.getJoueurslesPlusProches(joueurCaseEffet.posX, joueurCaseEffet.posY, joueurLanceur, TypeZoneCercle(99), None, self.nomEntites)
        sortALance = joueurLanceur.getSort(self.nomSort)
        for joueur in joueursLanceurs:
            cibleX = joueur.posX
            cibleY = joueur.posY
            if self.caseCible == "CaseCible":
                cibleX = kwargs.get("caseCibleX")
                cibleY = kwargs.get("caseCibleY")
            sortALance.lance(joueur.posX, joueur.posY,
                            niveau, cibleX, cibleY)
