"""@summary: Rassemble les effets de sort en rapport avec les retrait PA et PM."""

import random

from Effets.Effet import Effet
from Etats.EtatBoostCarac import EtatBoostCaracFixe
class EffetRetPA(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PA esquivables normalement (pas implémenté l'esquive).
    https://www.dofus.com/fr/forum/1003-divers/2281673-formule-calcul-retrait-ou-esquives-pa-pm"""

    def __init__(self, int_retrait=1, **kwargs):
        """@summary: Initialise un effet de retrait de PA.
        @int_retrait: le nombre de PA qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        super().__init__(**kwargs)

    def __str__(self):
        return "Retrait "+str(self.retrait)+" PA (1 tour)"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        retraitLbl = ttk.Label(frame, text="Retrait de ? PA:")
        retraitLbl.pack(side="left")
        retraitSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        retraitSpinbox.delete(0, 'end')
        retraitSpinbox.insert(0, int(self.retrait))
        retraitSpinbox.pack(side="left")
        ret["retrait"] = retraitSpinbox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["retrait"] = self.retrait
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetRetPA(int(infos["retrait"]), **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetRetPA(self.retrait, **self.kwargs)

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
        if joueurCaseEffet is not None:
            totalRet = 0
            for _ in range(self.retrait):
                esqPa = joueurCaseEffet.esqPA if joueurCaseEffet.esqPA != 0 else 1
                basePa = joueurCaseEffet.PABase if joueurCaseEffet.PABase != 0 else 1
                probaRet = 0.5 * (float(joueurLanceur.retPA)/float(esqPa)) * \
                    (float(joueurCaseEffet.PA)/float(basePa))
                rand = random.random()
                if rand <= probaRet:
                    totalRet += 1
            joueurCaseEffet.PA -= totalRet
            if not niveau.isPrevisu():
                print(joueurCaseEffet.nomPerso+" -" + str(totalRet) + "PA")


class EffetRetPM(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PM esquivables normalement (pas implémenté l'esquive)."""

    def __init__(self, int_retrait=1, pourNbTour=1, vol=False, **kwargs):
        """@summary: Initialise un effet de retrait de PM.
        @int_retrait: le nombre de PM qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        self.pourNbTour = pourNbTour
        self.vol = vol
        super().__init__(**kwargs)

    def __str__(self):
        if self.vol:
            return "Vol "+str(self.retrait)+" PM ("+str(self.pourNbTour)+" tour)"
        return "Retrait "+str(self.retrait)+" PM ("+str(self.pourNbTour)+" tour)"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        retraitLbl = ttk.Label(frame, text="Retrait de ? PM:")
        retraitLbl.pack(side="left")
        retraitSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        retraitSpinbox.delete(0, 'end')
        retraitSpinbox.insert(0, int(self.retrait))
        retraitSpinbox.pack(side="left")
        ret["retrait"] = retraitSpinbox
        nbTourLbl = ttk.Label(frame, text="Combien de tours:")
        nbTourLbl.pack(side="left")
        nbTourSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        nbTourSpinbox.delete(0, 'end')
        nbTourSpinbox.insert(0, int(self.pourNbTour))
        nbTourSpinbox.pack(side="left")
        ret["pourNbTour"] = nbTourSpinbox
        volLbl = ttk.Label(frame, text="Vol les PM retirés:")
        volLbl.pack(side="left")
        self.volVar = tk.BooleanVar()
        self.volVar.set(self.vol)
        volCheckbutton = ttk.Checkbutton(frame, variable=self.volVar)
        volCheckbutton.pack(side="left")
        ret["vol"] = self.volVar
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["retrait"] = self.retrait
        ret["pourNbTour"] = self.pourNbTour
        ret["vol"] = self.vol
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetRetPM(int(infos["retrait"]), int(infos["pourNbTour"]), infos["vol"], **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetRetPM(self.retrait, self.pourNbTour, self.vol, **self.kwargs)

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
        if joueurCaseEffet is not None:
            totalRet = 0
            print(str(self.retrait))
            for _ in range(self.retrait):
                esqPm = joueurCaseEffet.esqPM if joueurCaseEffet.esqPM != 0 else 1
                basePm = joueurCaseEffet.PMBase if joueurCaseEffet.PMBase != 0 else 1
                probaRet = 0.5 * (float(joueurLanceur.retPM)/float(esqPm)) * \
                    (float(joueurCaseEffet.PM)/float(basePm))
                rand = random.random()
                print(str(rand)+ " <= "+str(probaRet))
                if rand <= probaRet:
                    totalRet += 1
            nomSort = kwargs.get("nom_sort", "Retrait PM")
            if self.pourNbTour > 1:
                joueurCaseEffet.appliquerEtat(EtatBoostCaracFixe(
                    nomSort, 0, self.pourNbTour, "PM", -1*totalRet), joueurLanceur, -1, niveau)
                if not niveau.isPrevisu():
                    print(joueurCaseEffet.nomPerso+" -" + str(totalRet) +
                          "PM ("+str(self.pourNbTour)+" tours).")
            else:
                joueurCaseEffet.PM -= totalRet
                if not niveau.isPrevisu():
                    print(joueurCaseEffet.nomPerso+" -" + str(totalRet) + "PM")
            if self.vol:
                joueurLanceur.appliquerEtat(EtatBoostCaracFixe(nomSort, 0, self.pourNbTour, "PM", totalRet), joueurLanceur, cumulMax=-1, niveau=niveau)