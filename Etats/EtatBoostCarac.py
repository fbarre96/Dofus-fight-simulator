"""@summary: Rassemble les états boostant une caractéristique."""

from Etats.Etat import Etat


class EtatBoostCaracFixe(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur d'une caractéristique."""

    def __init__(self, nom="Pas de nom", debDans=0, duree=1, nomAttributCarac="", boostCarac=0, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés pour
                que l'état se désactive.
        @type: int
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
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracFixe(self.nom, self.debuteDans, self.duree, self.nomAttributCarac,
                                  self.boostCarac, self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        import Personnages
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        nomAttributLbl = ttk.Label(frame, text="Nom de l'attribut à modifier:")
        nomAttributLbl.grid(row=0, column=0, sticky="e")
        self.nomAttributCombobox = ttk.Combobox(frame, values=Personnages.Personnage.getAttributesList(), state="readonly")
        if self.nomAttributCarac != "":
            self.nomAttributCombobox.set(self.nomAttributCarac)
        self.nomAttributCombobox.grid(row=0, column=1, sticky="w")
        ret["nomAttributCarac"] = self.nomAttributCombobox
        modValueLbl = ttk.Label(frame, text="Modificateur :")
        modValueLbl.grid(row=1, column=0, sticky="e")
        self.modValueEntry = ttk.Entry(frame, width=5)
        self.modValueEntry.delete(0, "end")
        self.modValueEntry.insert(0, self.boostCarac)
        self.modValueEntry.grid(row=1, column=1, sticky="w")
        ret["boostCarac"] = self.modValueEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatBoostCaracFixe(infos["nom"], infos["debuteDans"], infos["duree"], infos["nomAttributCarac"], infos["boostCarac"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomAttributCarac"] = self.nomAttributCarac
        ret["boostCarac"] = self.boostCarac
        return ret

    def triggerInstantane(self, **kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        caracValue = getattr(personnage, self.nomAttributCarac)
        if isinstance(caracValue, bool):
            if isinstance(self.boostCarac, int):
                self.boostCarac = self.boostCarac == 1
            setattr(personnage, self.nomAttributCarac,
                    self.boostCarac)
            print("Modification de "+self.nomAttributCarac+":" +
                  str(caracValue)+" -> "+str(self.boostCarac))
        else:
            setattr(personnage, self.nomAttributCarac,
                    caracValue + self.boostCarac)
            print("Modification de "+self.nomAttributCarac+":" +
                  str(caracValue)+" -> "+str(caracValue + self.boostCarac))

    def triggerRafraichissement(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états
                     sont rafraichit (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerAvantRetrait(self, personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        caracValue = getattr(personnage, self.nomAttributCarac)
        if isinstance(caracValue, bool):
            if isinstance(self.boostCarac, int):
                self.boostCarac = self.boostCarac == 1
            setattr(personnage, self.nomAttributCarac,
                    not self.boostCarac)
            print("Fin de modification de "+self.nomAttributCarac+":" +
                  str(caracValue)+" -> "+str(not self.boostCarac))
        else:
            setattr(personnage, self.nomAttributCarac,
                    caracValue - self.boostCarac)
            print("Fin de modification de "+self.nomAttributCarac+":" +
                  str(caracValue)+" -> "+str(caracValue - self.boostCarac))
    
    def triggerFinTour(self, personnage, niveau):
        print("Trigger fin de tour "+str(self.nomAttributCarac))
        if self.nomAttributCarac == "PM" or self.nomAttributCarac == "PA":
            setattr(personnage, self.nomAttributCarac,
                    getattr(personnage, self.nomAttributCarac) + self.boostCarac)



class EtatBoostCaracPer(Etat):
    """@summary: Classe décrivant un état qui modifie la valeur
                    d'une caractéristique selon un pourcentage."""

    def __init__(self, nom, debDans, duree, nomAttributCarac, boostCaracPer, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int
        @nomAttributCarac: Le nom de l'attribut a boost
        @type: string qui doit être dans les attribut de la classe Personnage
        @boostCaracPer: le gain de Caractéristique a appliqué
        @type: int (négatif ou positif)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomAttributCarac = nomAttributCarac
        self.boostCaracPer = boostCaracPer
        self.boostCarac = 0
        super().__init__(nom, debDans, duree, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatBoostCaracPer(self.nom, self.debuteDans, self.duree, self.nomAttributCarac,
                                 self.boostCaracPer, self.lanceur, self.desc)

    def triggerRafraichissement(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états du joueur dont les états sont rafraichit
                     (au début de chaque tour ou quand sa durée est modifiée).
                     Les points de porté sont reboostés à chaque rafraîchissement de l'état.
        @personnage: Le personnage dont l'état est en train d'être rafraichit
        @type: Personnage
        @niveau: La grille de jeu en cours
        @type: Niveau"""
        self.triggerInstantane(joueurCaseEffet=personnage)

    def triggerInstantane(self, **kwargs):
        """@summary: Un trigger appelé au moment ou un état est appliqué.
                     change la carac du joueur selon le boost carac et le nom de l'attribut a boost
        @kwargs: les options non prévisibles selon les états.
        @type: **kwargs"""
        personnage = kwargs.get("joueurCaseEffet")
        caracValue = getattr(personnage, self.nomAttributCarac)
        pourcentageBoost = self.boostCaracPer
        self.boostCarac = int(caracValue * (pourcentageBoost/100.0))
        setattr(personnage, self.nomAttributCarac,
                caracValue + self.boostCarac)
        if self.nomAttributCarac == "vie":
            personnage.vieMax += self.boostCarac
        print("Modification de "+self.nomAttributCarac+":"+str(caracValue)+" -> " +
              str(caracValue + self.boostCarac) + " ("+str(self.boostCaracPer)+"%)")

    def triggerAvantRetrait(self, personnage):
        """@summary: Un trigger appelé au moment ou un état va être retirés.
                     Retire la vitalité bonus lorsque l'état se termine
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        caracValue = getattr(personnage, self.nomAttributCarac)
        setattr(personnage, self.nomAttributCarac,
                caracValue - self.boostCarac)
        if self.nomAttributCarac == "vie":
            personnage.vieMax -= self.boostCarac
        print("Fin de modification de "+self.nomAttributCarac+":"+str(caracValue) +
              " -> "+str(caracValue - self.boostCarac) + " ("+str(self.boostCaracPer)+"%)")
