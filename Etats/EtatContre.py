"""@summary: Rassemble les états qui contre une partie des dégâts subits."""

from Etats.Etat import Etat
from Effets.EffetDegats import EffetDegats
import Sort
import Zones


class EtatContre(Etat):
    """@summary: Classe décrivant un état qui renvoie une partie
                 des dégâts subits au corps à corps."""

    def __init__(self, nom, debDans, duree, pourcentage=50, tailleZone=0, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @pourcentage: le pourcentage des dégâts subits au corps-à-corps x qui seront répartis
        @type: int (pourcentage)
        @tailleZone: la rayon du cercle-zone dans laquelle les dégâts subits
                     seront réinfligés en partie
        @type: int

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.pourcentage = pourcentage
        self.tailleZone = tailleZone
        super().__init__(nom, debDans, duree, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        import tkinter as tk
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        pourcentageLbl = ttk.Label(frame, text="Pourcentage de renvoi:")
        pourcentageLbl.grid(row=0, column=0, sticky="e")
        pourcentageSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        pourcentageSpinbox.delete(0, 'end')
        pourcentageSpinbox.insert(0, int(self.pourcentage))
        pourcentageSpinbox.grid(row=0, column=1, sticky="w")
        ret["pourcentage"] = pourcentageSpinbox
        tailleZoneLbl = ttk.Label(frame, text="Taille cercle de renvoi:")
        tailleZoneLbl.grid(row=1, column=0, sticky="e")
        tailleZoneSpinbox = tk.Spinbox(frame, from_=0, to=99, width=2)
        tailleZoneSpinbox.delete(0, 'end')
        tailleZoneSpinbox.insert(0, int(self.tailleZone))
        tailleZoneSpinbox.grid(row=1, column=1, sticky="w")
        ret["tailleZone"] = tailleZoneSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatContre(infos["nom"], infos["debuteDans"], infos["duree"], infos["pourcentage"], infos["tailleZone"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage"] = self.pourcentage
        ret["tailleZone"] = self.tailleZone
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatContre(self.nom, self.debuteDans, self.duree,
                          self.pourcentage, self.tailleZone, self.lanceur, self.desc)

    def triggerAvantSubirDegats(self, cibleAttaque, niveau, totalPerdu, typeDegats, attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages vont être subits.
                     Redistribue une partie des dégâts qui vont être subit au corps-à-corps
                     sur la zone définit.
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        if cibleAttaque.team != attaquant.team:
            distance = abs(attaquant.posX-cibleAttaque.posX) + \
                abs(attaquant.posY-cibleAttaque.posY)
            if distance == 1:
                if typeDegats.lower() in ["terre", "eau", "air", "feu", "neutre"]:
                    retour = int(
                        ((self.pourcentage/100)*totalPerdu) + cibleAttaque.doRenvoi)
                    sortContre = \
                               Sort.Sort("Contre", 0, 0, 0, 1,
                                         [EffetDegats(retour, retour, typeDegats,
                                                      zone=Zones.TypeZoneCercle(self.tailleZone),
                                                      cibles_possibles="Ennemis",
                                                      bypassDmgCalc=True)],
                                         [], 0, 99, 99, 0, 0, "cercle", False)
                    sortContre.lance(cibleAttaque.posX, cibleAttaque.posY,
                                     niveau, attaquant.posX, attaquant.posY)
