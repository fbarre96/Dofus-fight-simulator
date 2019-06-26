# -*- coding: utf-8 -*
"""@summary: Rassemble les effets de sort en rapport avec les invocations."""
from copy import deepcopy

from Effets.Effet import Effet
import Personnages


class EffetInvoque(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet invoque un personnage"""
    # La liste des invocations disponibles.

    def __init__(self, str_nomInvoque, compteCommeInvocation, **kwargs):
        """@summary: Initialise un effet invoquant un personnage.
        @str_nomInvoque: le nom de l'invocation
                        (pré-définies dans le dictionnaire Personnages.invocs_liste)
        @type: string
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.compteCommeInvocation = compteCommeInvocation
        self.nomInvoque = str_nomInvoque
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetInvoque(self.nomInvoque, self.compteCommeInvocation, **self.kwargs)

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
        invoc = deepcopy(Personnages.invocs_liste[self.nomInvoque])
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
                         (pré-définies dans le dictionnaire Personnages.invocs_liste)
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
