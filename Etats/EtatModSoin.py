"""@summary: Rassemble les états qui modifient les soins totaux à donner."""

from Etats.Etat import Etat


class EtatModSoinPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les soins totaux
                 que devrait subir le porteur."""

    def __init__(self, nom, debDans, duree, pourcentage=0, provenance="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @pourcentage: le pourcentage de modification des dégâts qui seront subis.
        @type: int (pourcentage)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        self.provenance = provenance
        super().__init__(nom, debDans, duree, lanceur, desc)
        
    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        pourcentageLbl = ttk.Label(frame, text="% modification du soin:")
        pourcentageLbl.grid(row=0, column=0, sticky="e")
        self.pourcentageSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        self.pourcentageSpinbox.delete(0, 'end')
        self.pourcentageSpinbox.insert(0, self.pourcentage)
        self.pourcentageSpinbox.grid(row=0, column=1, sticky="w")
        ret["pourcentage"] = self.pourcentageSpinbox
        provenanceLbl = ttk.Label(frame, text="De provenance :")
        provenanceLbl.grid(row=1, column=0, sticky="e")
        self.provenanceCombobox = ttk.Combobox(frame, values=("Allies", "Ennemis"), state="readonly")
        self.provenanceCombobox.set(self.provenance)
        self.provenanceCombobox.grid(row=1, column=1, sticky="w")
        ret["provenance"] = self.provenanceCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatModSoinPer(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), int(infos["pourcentage"]), infos["provenance"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage"] = self.pourcentage
        ret["provenance"] = self.provenance
        return ret
    
    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatModSoinPer(self.nom, self.debuteDans, self.duree, self.pourcentage,
                              self.provenance, self.lanceur, self.desc)

    def triggerApresCalculSoins(self, total, cible, attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages ont terminé d'être calculé.
                     Modifie les soins par un pourcentage.
        @total: Le total de soint qui va être infligé.
        @type: int

        @return: la nouvelle valeur du total de dégâts."""
        if self.provenance == "Allies" and cible.team != attaquant.team:
            return total
        if self.provenance == "Ennemis" and cible.team == attaquant.team:
            return total
        return int((total * self.pourcentage)/100)
