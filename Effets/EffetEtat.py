"""@summary: Décrit un effet de sort appliquant un état à un joueur. """

from copy import deepcopy
from Effets.Effet import Effet


class EffetEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet applique un état à la cible."""

    def __init__(self, etat_etat, **kwargs):
        """@summary: Initialise un effet appliquant un état.
        @etat_etat: l'état qui va être appliqué
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.etat = etat_etat
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtat(self.etat, **self.kwargs)

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
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # On copie l'état parce que l'effet peut être appliquer plusieurs fois.
        etatCopier = deepcopy(self.etat)
        return joueurCaseEffet.appliquerEtat(etatCopier, joueurLanceur,
                                             self.kwargs.get("cumulMax", -1), niveau)

class EffetEtatSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet place un état sur le lanceur."""

    def __init__(self, etat_etat, **kwargs):
        """@summary: Initialise un effet placant un état sur le lanceur
        @etat_etat: l'état à placer sur le lanceur
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.etat = etat_etat
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtatSelf(self.etat, **self.kwargs)

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
        etatCopie = deepcopy(self.etat)
        return joueurLanceur.appliquerEtat(etatCopie, joueurLanceur,
                                           self.kwargs.get("cumulMax", -1), niveau)


class EffetEtatSelfTF(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet place un état sur le lanceur portant le nom du sort à l'origine d'un TF."""

    def __init__(self, etat_etat, sortsExclus, **kwargs):
        """@summary: Initialise un effet placant un état sur le lanceur
        @etat_etat: l'état à placer sur le lanceur
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.etat = etat_etat
        self.sortsExclus = sortsExclus
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtatSelfTF(self.etat, self.sortsExclus, **self.kwargs)

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
        nomSort = self.getNomSortTF()
        if nomSort in self.sortsExclus:
            return False
        etatCopier = deepcopy(self.etat)
        if self.kwargs.get("remplaceNom", True):
            etatCopier.nom = nomSort
        return joueurLanceur.appliquerEtat(etatCopier, joueurLanceur,
                                           self.kwargs.get("cumulMax", -1), niveau)


class EffetRafraichirEtats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet change la durée des états de la cible."""

    def __init__(self, int_deXTours, **kwargs):
        """@summary: Initialise un effet changeant la durée des états de la cible
        @int_deXTours: le nombre de tour qui vont être additionés (dans Z)
                       à chaque état de la cible.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.deXTours = int_deXTours
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetRafraichirEtats(self.deXTours, **self.kwargs)

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
        joueurCaseEffet.changeDureeEffets(self.deXTours, niveau)


class EffetSetDureeEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet set la durée des états de la cible."""

    def __init__(self, nomEtat, nouveauDebut, nouvelleDuree, **kwargs):
        """@summary: Initialise un effet changeant la durée des états de la cible
        @int_deXTours: le nombre de tour qui vont être additionés (dans Z)
                       à chaque état de la cible.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = nomEtat
        self.nouveauDebut = nouveauDebut
        self.nouvelleDuree = nouvelleDuree
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetSetDureeEtat(self.nomEtat, self.nouveauDebut, self.nouvelleDuree, **self.kwargs)

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
        for etat in joueurCaseEffet.etats:
            if etat.actif() and etat.nom == self.nomEtat:
                etat.debuteDans = self.nouveauDebut
                etat.duree = self.nouvelleDuree


class EffetRetireEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire les états de la cible qui portent un nom donné."""

    def __init__(self, str_nomEtat, **kwargs):
        """@summary: Initialise un effet retirant les états de la cible selon un paramètre donné.
        @str_nomEtat: le nom de l'état qui va être retiré de la cible.
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = str_nomEtat
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetRetireEtat(self.nomEtat, **self.kwargs)

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
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.retirerEtats(niveau, self.nomEtat)

class EffetRetireEtatSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire les états de la cible qui portent un nom donné."""

    def __init__(self, str_nomEtat, **kwargs):
        """@summary: Initialise un effet retirant les états de la cible selon un paramètre donné.
        @str_nomEtat: le nom de l'état qui va être retiré de la cible.
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = str_nomEtat
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetRetireEtatSelf(self.nomEtat, **self.kwargs)

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
        if joueurLanceur is not None:
            niveau.ajoutFileEffets(self, joueurLanceur, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.retirerEtats(niveau, self.nomEtat)
