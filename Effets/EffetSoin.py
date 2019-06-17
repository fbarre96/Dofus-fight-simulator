"""@summary: Rassemble les effets de sort en rapport avec les soins."""
import random

from Effets.Effet import Effet

class EffetSoin(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet soinges une cible."""

    def __init__(self, valSoinMin, valSoinMax, **kwargs):
        """@summary: Initialise un effet de dégâts.
        @valSoinMin: jet de soin minimum
        @type: int
        @valSoinMax: jet de soin maximum
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.valSoinMin = valSoinMin
        self.valSoinMax = valSoinMax
        self.valSoin = 0
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetSoin(self.valSoinMin, self.valSoinMax, **self.kwargs)
        return cpy

    def calculSoin(self, joueurCaseEffet, joueurLanceur, howToChoose="alea"):
        """@summary: Calcul les soins qui seront donnés.
        @joueurCaseEffet: le joueur qui sera soigné
        @type: Personnage
        @joueurLanceur: Le joueur à l'origine de l'effet
        @type: Personnage"""
        if joueurCaseEffet is None:
            return None
        if howToChoose == "min":
            baseSoin = self.valSoinMin
        elif howToChoose == "max":
            baseSoin = self.valSoinMax
        else:
            baseSoin = random.randrange(self.valSoinMin, self.valSoinMax+1)
        self.valSoin = baseSoin + joueurLanceur.soins
        if joueurCaseEffet.vie + self.valSoin > joueurCaseEffet.vieMax:
            self.valSoin = joueurCaseEffet.vieMax - joueurCaseEffet.vie
        return self.valSoin

    def appliquerSoin(self, joueurCaseEffet):
        """@summary: calcul les soi,s à infligés et applique ces soins à la cible.
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage

        @return: Le total de soins infligés"""
        joueurCaseEffet.soigne(self.valSoin, not self.isPrevisu())
        return self.valSoin

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet,
                     wrapper pour la fonction appliquer dégâts.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            self.valSoin = self.calculSoin(joueurCaseEffet, joueurLanceur)
            if self.isPrevisu():
                joueurCaseEffet.msgsPrevisu.append("Soin "+str(self.valSoin))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            self.appliquerSoin(joueurCaseEffet)


class EffetSoinPerPVMax(EffetSoin):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet soinges une cible à hauteur d'un pourcentage de ses pv maxs."""

    def __init__(self, pourcentage, **kwargs):
        """@summary: Initialise un effet de dégâts.
        @pourcentage: le pourcentage de la vie max à soigner
        @type: int (1 à 100)
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.pourcentage = pourcentage
        self.kwargs = kwargs
        super().__init__(0, **kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetSoinPerPVMax(self.pourcentage, **self.kwargs)
        return cpy

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet,
                     wrapper pour la fonction appliquer dégâts.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            self.valSoin = int((self.pourcentage/100.0) * joueurCaseEffet.vieMax)
            self.valSoin = self.calculSoin(joueurCaseEffet, joueurLanceur)
            if self.isPrevisu():
                joueurCaseEffet.msgsPrevisu.append("Soin "+str(self.valSoin))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)


class EffetSoinSelonSubit(EffetSoin):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet soinges une cible à hauteur d'un pourcentage des dégats subits
    DOIT AVOIR UN SETTER DEGATS SUBITS ."""

    def __init__(self, pourcentage, **kwargs):
        """@summary: Initialise un effet de soin.
        @pourcentage: le pourcentage de la vie max à soigner
        @type: int (1 à 100)
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.pourcentage = pourcentage
        self.kwargs = kwargs
        super().__init__(0, 0, **kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetSoinSelonSubit(self.pourcentage, **self.kwargs)
        return cpy

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet,
                    wrapper pour la fonction appliquer soin.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            print("Effet soin selon subit : "+str(self.getDegatsSubits()))
            subitDegats, _ = self.getDegatsSubits()
            self.valSoinMin = self.valSoinMax = int((self.pourcentage/100.0) * subitDegats)
            self.valSoin = self.calculSoin(joueurCaseEffet, joueurLanceur)
            if self.isPrevisu():
                joueurCaseEffet.msgsPrevisu.append("Soin "+str(self.valSoin))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
