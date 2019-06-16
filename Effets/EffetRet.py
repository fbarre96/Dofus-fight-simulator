import random

import Etats
from Effets.Effet import Effet

class EffetRetPA(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PA esquivables normalement (pas implémenté l'esquive).
    https://www.dofus.com/fr/forum/1003-divers/2281673-formule-calcul-retrait-ou-esquives-pa-pm"""

    def __init__(self, int_retrait, **kwargs):
        """@summary: Initialise un effet de retrait de PA.
        @int_retrait: le nombre de PA qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        super(EffetRetPA, self).__init__(**kwargs)

    def deepcopy(self):
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
            for i in range(self.retrait):
                esqPa = joueurCaseEffet.esqPA if joueurCaseEffet.esqPA != 0 else 1
                basePa = joueurCaseEffet._PA if joueurCaseEffet._PA != 0 else 1
                probaRet = 0.5 * (float(joueurLanceur.retPA)/float(esqPa)) * \
                    (float(joueurCaseEffet.PA)/float(basePa))
                rand = random.random()
                if rand <= probaRet:
                    totalRet += 1
            joueurCaseEffet.PA -= totalRet
            if not self.isPrevisu():
                print(joueurCaseEffet.nomPerso+" -" + str(totalRet) + "PA")


class EffetRetPM(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire des PM esquivables normalement (pas implémenté l'esquive)."""

    def __init__(self, int_retrait, pourNbTour=1, desenvoutable=True, **kwargs):
        """@summary: Initialise un effet de retrait de PM.
        @int_retrait: le nombre de PM qui vont être retiré au maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.retrait = int_retrait
        self.pourNbTour = pourNbTour
        self.desenvoutable = desenvoutable
        super(EffetRetPM, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetRetPM(self.retrait, self.pourNbTour, self.desenvoutable, **self.kwargs)

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
            for i in range(self.retrait):
                esqPm = joueurCaseEffet.esqPM if joueurCaseEffet.esqPM != 0 else 1
                basePm = joueurCaseEffet._PM if joueurCaseEffet._PM != 0 else 1
                probaRet = 0.5 * (float(joueurLanceur.retPM)/float(esqPm)) * \
                    (float(joueurCaseEffet.PM)/float(basePm))
                rand = random.random()
                if rand <= probaRet:
                    totalRet += 1
            if self.pourNbTour > 1:
                nomSort = kwargs.get("nom_sort", "Retrait PM")
                joueurCaseEffet.appliquerEtat(Etats.EtatBoostCaracFixe(
                    nomSort, 0, self.pourNbTour, "PM", -1*totalRet), joueurLanceur, -1, niveau)
                if not self.isPrevisu():
                    print(joueurCaseEffet.nomPerso+" -" + str(totalRet) +
                          "PM ("+str(self.pourNbTour)+" tours).")
            else:
                joueurCaseEffet.PM -= totalRet
                if not self.isPrevisu():
                    print(joueurCaseEffet.nomPerso+" -" + str(totalRet) + "PM")

