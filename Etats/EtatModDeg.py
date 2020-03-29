"""@summary: Rassemble les états qui modifient les dégâts totaux infligés."""

from Etats.Etat import Etat


class EtatModDegPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les dégâts totaux
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

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatModDegPer(self.nom, self.debuteDans, self.duree, self.pourcentage,
                             self.provenance, self.lanceur, self.desc)

    def buildUI(self, topframe,callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        pourcentageLbl = ttk.Label(frame, text="Modificateur en pourcent:")
        pourcentageLbl.grid(row=0, column=0, sticky="e")
        pourcentageSpinbox = tk.Spinbox(frame, from_=-1000, to=1000, width=5)
        pourcentageSpinbox.delete(0, 'end')
        pourcentageSpinbox.insert(0, self.pourcentage)
        pourcentageSpinbox.grid(row=0, column=1, sticky="w")
        ret["pourcentage"] = pourcentageSpinbox
        provenanceLbl = ttk.Label(frame, text="En provenance de:")
        provenanceLbl.grid(row=1, column=0, sticky="e")
        provenanceCombobox = ttk.Combobox(frame, values=("Tout", "Allies", "Ennemis", "melee"))
        provenanceCombobox.set(self.provenance)
        provenanceCombobox.grid(row=1, column=1, sticky="w")
        ret["provenance"] = provenanceCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatModDegPer(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), int(infos["pourcentage"]), infos["provenance"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage"] = self.pourcentage
        ret["provenance"] = self.provenance
        return ret

    def triggerApresCalculDegats(self, total, typeDeg, cible, attaquant):
        """@summary: Un trigger appelé pour tous les états des 2 joueurs impliqués
                     lorsque des dommages ont terminé d'être calculé.
                     Modifie les dégâts par un pourcentage si les dommages sont
                     des dommages de sort (pas de poussé)
        @total: Le total de dégâts qui va être infligé.
        @type: int
        @typeDeg: Le type de dégâts qui va être infligé
        @type: string

        @return: la nouvelle valeur du total de dégâts."""
        if self.provenance == "Allies" and cible.team != attaquant.team:
            return total
        if self.provenance == "Ennemis" and cible.team == attaquant.team:
            return total
        if self.provenance == "melee" and \
           abs(cible.posX - attaquant.posX) + abs(cible.posY - attaquant.posY) != 1:
            return total
        if typeDeg != "doPou":
            return int((total * self.pourcentage)/100)
        return total
