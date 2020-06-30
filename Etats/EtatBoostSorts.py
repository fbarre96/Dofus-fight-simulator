"""@summary: Rassemble les états boostant tous les sorts."""

from Etats.Etat import Etat


class EtatBoostSortsPer(Etat):
    """@summary: Classe décrivant un état qui multiplie par un pourcentage les
                 dégats totaux des sorts que devrait donné le lanceur."""

    def __init__(self, nom, debDans, duree, pourcentage=100, lanceur=None, desc=""):
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
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        super().__init__(nom, debDans, duree, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        pourcentageLbl = ttk.Label(frame, text="Modif \x25 dégâts des sorts:")
        pourcentageLbl.grid(row=1, column=0, sticky="e")
        pourcentageSpinbox = tk.Spinbox(frame, from_=0, to=999, width=3)
        pourcentageSpinbox.delete(0, "end")
        pourcentageSpinbox.insert(0, self.pourcentage)
        pourcentageSpinbox.grid(row=1, column=1, sticky="w")
        ret["pourcentage"] = pourcentageSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostSortsPer(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), int(infos["pourcentage"]), None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage"] = self.pourcentage
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostSortsPer(self.nom, self.debuteDans, self.duree,
                                 self.pourcentage, self.lanceur, self.desc)

    def triggerApresCalculDegats(self, total, typeDeg, cible, attaquant):
        if typeDeg != "arme":
            print("Changer les degats : par "+str(self.pourcentage))
            return int(total * (1+(self.pourcentage/100.0)))
        else:
            return total


class EtatBoostPuissanceSorts(Etat):
    def __init__(self, nom, debDans, duree, boostPui=0, lanceur=None, desc=""):
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
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.boostPui = boostPui
        super().__init__(nom, debDans, duree, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        boostLbl = ttk.Label(frame, text="Boost puissance (sorts) de:")
        boostLbl.grid(row=1, column=0, sticky="e")
        boostSpinbox = tk.Spinbox(frame, from_=0, to=999, width=3)
        boostSpinbox.delete(0, "end")
        boostSpinbox.insert(0, self.boostPui)
        boostSpinbox.grid(row=1, column=1, sticky="w")
        ret["boostPui"] = boostSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostPuissanceSorts(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), int(infos["boostPui"]), None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["boostPui"] = self.boostPui
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostPuissanceSorts(self.nom, self.debuteDans, self.duree,
                                 self.boostPui, self.lanceur, self.desc)

    def triggerAvantCalculDegats(self, dommages, baseDeg, caracs, nomSort, minjet, maxjet):
        if nomSort != "arme":
            caracs += self.boostPui
        return dommages, baseDeg, caracs
