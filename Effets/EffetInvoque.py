# -*- coding: utf-8 -*
"""@summary: Rassemble les effets de sort en rapport avec les invocations."""
from copy import deepcopy

from Effets.Effet import Effet



class EffetInvoque(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet invoque un personnage"""
    # La liste des invocations disponibles.
    
    def __init__(self, str_nomInvoque="", compteCommeInvocation=True, **kwargs):
        """@summary: Initialise un effet invoquant un personnage.
        @str_nomInvoque: le nom de l'invocation
                        (pré-définies dans le dictionnaire invocs_liste)
        @type: string
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.compteCommeInvocation = compteCommeInvocation
        self.nomInvoque = str_nomInvoque
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetInvoque(self.nomInvoque, self.compteCommeInvocation, **self.kwargs)
    
    def __str__(self):
        return "Invoque "+str(self.nomInvoque)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomInvocLbl = ttk.Label(frame, text="Nom invocation:")
        nomInvocLbl.pack(side="left")
        nomInvocEntry = ttk.Entry(frame, width=50)
        nomInvocEntry.delete(0, 'end')
        nomInvocEntry.insert(0, self.nomInvoque)
        nomInvocEntry.pack(side="left")
        ret["nomInvoque"] = nomInvocEntry
        compteInvoqueLbl = ttk.Label(frame, text="Compté comme invoc:")
        compteInvoqueLbl.pack(side="left")
        self.compteInvoqueVar = tk.BooleanVar()
        self.compteInvoqueVar.set(self.compteCommeInvocation)
        compteInvoqueCheckbutton = ttk.Checkbutton(frame, variable=self.compteInvoqueVar)
        compteInvoqueCheckbutton.pack(side="left")
        ret["compteCommeInvocation"] = self.compteInvoqueVar
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomInvoque"] = self.nomInvoque
        ret["compteCommeInvocation"] = self.compteCommeInvocation
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetInvoque(infos["nomInvoque"], infos["compteCommeInvocation"], **infos["kwargs"])

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires,
                 les options caseCibleX et caseCibleY doivent être mentionnées.
        @type: **kwargs"""
        import Personnages
        from IAs.DumbIA import DumbIA
        from IAs.PasseIA import PasseIA
        from IAs.JoueurIA import JoueurIA
        invocs_liste = {
            "Cadran de Xelor": Personnages.Personnage("Cadran de Xelor", "Cadran de Xelor",
                                        100, 1, {"Vitalite": 1000}, {}, {}, {},
                                        "cadran_de_xelor.png", DumbIA()),
            "Cawotte": Personnages.Personnage("Cawotte", "Cawotte", 1, 1,
                                {"Vitalite": 660}, {}, {}, {}, "cawotte.jpg", PasseIA()),
            "Synchro": Personnages.Personnage("Synchro", "Synchro", 1, 1,
                                {"Vitalite": 1200}, {}, {}, {}, "synchro.png", PasseIA()),
            "Complice": Personnages.Personnage("Complice", "Complice", 1, 1,
                                {"Vitalite": 650}, {}, {}, {}, "complice.png", PasseIA()),
            "Balise de Rappel": Personnages.Personnage("Balise de Rappel", "Balise de Rappel",
                                        1, 1, {"Vitalite": 1000}, {}, {}, {},
                                        "balise_de_rappel.png", DumbIA()),
            "Balise Tactique": Personnages.Personnage("Balise Tactique", "Balise Tactique",
                                        1, 1, {"Vitalite": 255}, {}, {}, {"Neutre%":10, "Terre%":10, "Feu%":10, "Eau%":10, "Air%":10},
                                        "balise_tactique.png", PasseIA()),
            "Stratege Iop": Personnages.Personnage("Stratege Iop", "Stratège Iop", 1, 1,
                                    {"Vitalite": 1385}, {}, {}, {}, "conquete.png", PasseIA()),
            "Double": Personnages.Personnage("Double", "Double", 1, 1,
                                {"Vitalite": 1}, {}, {}, {}, "sram.png"),
            "Comploteur": Personnages.Personnage("Comploteur", "Comploteur", 1, 1,
                                    {"Vitalite": 1}, {}, {}, {}, "sram.png"),
            "Lapino": Personnages.Personnage("Lapino", "Lapino",
                                1, 1, {"Vitalite": 1200, "PA":5, "PM":4},
                                {"Esquive PA":75, "Esquive PM":75}, {},
                                {"Neutre%":20, "Terre%":20, "Feu%":5, "Eau%":-5, "Air%":30},
                                "mot_d_amitie.jpg"),
            "Lapino protecteur": Personnages.Personnage("Lapino protecteur", "Lapino protecteur",
                                            1, 1, {"Vitalite": 1200, "PA":5, "PM":4},
                                            {"Esquive PA":75, "Esquive PM":75}, {},
                                            {"Neutre%":10, "Terre%":15, "Feu%":0, "Eau%":-10, "Air%":25},
                                            "mot_d_affection.jpg"),
            "Fiole": Personnages.Personnage("Fiole", "Fiole",
                                1, 1, {"Vitalite": 600, "PA":6, "PM":0},
                                {"Esquive PA":90, "Esquive PM":90}, {},
                                {"Neutre%":0, "Terre%":0, "Feu%":0, "Eau%":0, "Air%":0},
                                "mot_de_seduction.jpg", DumbIA()),
            "Tonneau Attractif": Personnages.Personnage("Tonneau Attractif", "Tonneau Attractif",
                                            1, 1, {"Vitalite": 1315, "PA":8, "PM":-1},
                                            {"Esquive PA":52, "Esquive PM":52}, {},
                                            {"Neutre%":20, "Terre%":-10, "Feu%":20,
                                            "Eau%":-10, "Air%":30},
                                            "ivresse.jpg", DumbIA()),
            "Tonneau Incapacitant": Personnages.Personnage("Tonneau Incapacitant", "Tonneau Incapacitant",
                                            1, 1, {"Vitalite": 1052, "PA":4, "PM":0},
                                            {"Esquive PA":0, "Esquive PM":0}, {},
                                            {"Neutre%":20, "Terre%":30, "Feu%":-10,
                                                "Eau%":20, "Air%":-10},
                                            "ebriete.jpg", DumbIA()),
            "Pandawasta": Personnages.Personnage("Pandawasta", "Pandawasta",
                                    1, 1, {"Vitalite": 1025, "PA":6, "PM":5},
                                    {"Esquive PA":10, "Esquive PM":10, "Tacle":35}, {},
                                    {"Neutre%":25, "Terre%":25, "Feu%":25,
                                    "Eau%":25, "Air%":25},
                                    "lien_spiritueux.jpg", JoueurIA()),
            "Bambou": Personnages.Personnage("Bambou", "Bambou",
                                1, 1, {"Vitalite": 657, "PA":0, "PM":0},
                                {"Esquive PA":0, "Esquive PM":0, "Tacle":0}, {},
                                {"Neutre%":0, "Terre%":0, "Feu%":0,
                                "Eau%":0, "Air%":0},
                                "bambou.jpg", PasseIA()),
        }
        print("Invoque une "+str(self.nomInvoque))
        invocs_liste[self.nomInvoque].faireChargerSort(False)
        invoc = deepcopy(invocs_liste[self.nomInvoque])
        invoc.invocateur = joueurLanceur
        invoc.team = joueurLanceur.team
        invoc.lvl = joueurLanceur.lvl
        _, res = self.estLancable(invoc.invocateur, None)
        if res:
            joueurLanceur.invocations.append(invoc)
            
            niveau.invoque(invoc, kwargs.get("caseCibleX"),
                           kwargs.get("caseCibleY"))

    def estLancable(self, joueurLanceur, joueurCibleDirect):
        """@summary: Test si un effet peut etre lance selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé à la base
                            (peut-être identique à joueurCible).
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""
        msg, res = super().estLancable(joueurLanceur, joueurCibleDirect)
        if not res:
            return msg, res
        if self.compteCommeInvocation:
            if len(joueurLanceur.invocations) + 1 > joueurLanceur.invocationLimite:
                return "Limite d'invocation atteinte", False
        return "", True


class EffetDouble(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet est unique pour le double du sram"""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet invoquant un personnage.
        @str_nomInvoque: le nom de l'invocation
                         (pré-définies dans le dictionnaire invocs_liste)
        @type: string
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetDouble(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires,
                 les options caseCibleX et caseCibleY doivent être mentionnées.
        @type: **kwargs"""
        copyJoueurLanceur = deepcopy(joueurLanceur)
        saveJoueurCaseEffet = deepcopy(joueurCaseEffet)
        joueurCaseEffet = copyJoueurLanceur

        joueurCaseEffet.posX = saveJoueurCaseEffet.posX
        joueurCaseEffet.posY = saveJoueurCaseEffet.posY
        joueurCaseEffet.uid = saveJoueurCaseEffet.uid
        joueurCaseEffet.nomPerso = saveJoueurCaseEffet.nomPerso
        joueurCaseEffet.etats = saveJoueurCaseEffet.etats
        joueurCaseEffet.historiqueDeplacement = saveJoueurCaseEffet.historiqueDeplacement
        joueurCaseEffet.posDebTour = saveJoueurCaseEffet.posDebTour
        joueurCaseEffet.posDebCombat = saveJoueurCaseEffet.posDebCombat
        joueurCaseEffet.invocateur = saveJoueurCaseEffet.invocateur
        joueurCaseEffet.invocations = saveJoueurCaseEffet.invocations
        joueurCaseEffet.sorts = saveJoueurCaseEffet.sorts
        joueurCaseEffet.classe = saveJoueurCaseEffet.classe
        i = 0
        while i < len(niveau.joueurs):
            if niveau.joueurs[i].uid == joueurCaseEffet.uid:
                del niveau.joueurs[i]
                niveau.joueurs.insert(i, joueurCaseEffet)
                break
            i += 1
        if joueurCaseEffet.invocateur is not None:
            i = 0
            while i < len(joueurCaseEffet.invocateur.invocations):
                if joueurCaseEffet.invocateur.invocations[i].uid == joueurCaseEffet.uid:
                    del joueurCaseEffet.invocateur.invocations[i]
                    joueurCaseEffet.invocateur.invocations.insert(
                        i, joueurCaseEffet)
                    break
                i += 1
