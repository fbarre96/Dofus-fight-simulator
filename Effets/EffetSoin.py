from Effets.Effet import Effet

class EffetSoin(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet soinges une cible."""

    def __init__(self, valSoin, **kwargs):
        """@summary: Initialise un effet de dégâts.
        @pourcentage: le pourcentage de la vie max à soigner
        @type: int (1 à 100)
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.valSoin = valSoin
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetSoin(self.valSoin, **self.kwargs)
        return cpy

    def calculSoin(self, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet == None:
            return None
        self.valSoin += joueurLanceur.soins
        if joueurCaseEffet.vie + self.valSoin > joueurCaseEffet.vieMax:
            self.valSoin = joueurCaseEffet.vieMax - joueurCaseEffet.vie
        return self.valSoin

    def appliquerSoin(self, niveau, joueurCaseEffet, joueurLanceur):
        """@summary: calcul les soi,s à infligés et applique ces soins à la cible.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage

        @return: Le total de soins infligés"""
        joueurCaseEffet.soigne(joueurLanceur, niveau,
                               self.valSoin, not self.isPrevisu())
        return self.valSoin

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet, wrapper pour la fonction appliquer dégâts.
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
            self.appliquerSoin(niveau, joueurCaseEffet, joueurLanceur)


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
        """@summary: Appelé lors de l'application de l'effet, wrapper pour la fonction appliquer dégâts.
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
        """@summary: Initialise un effet de dégâts.
        @pourcentage: le pourcentage de la vie max à soigner
        @type: int (1 à 100)
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.pourcentage = pourcentage
        self.kwargs = kwargs
        super().__init__(0, **kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetSoinSelonSubit(self.pourcentage, **self.kwargs)
        return cpy

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet, wrapper pour la fonction appliquer dégâts.
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
            self.valSoin = int((self.pourcentage/100.0) * subitDegats)
            self.valSoin = self.calculSoin(joueurCaseEffet, joueurLanceur)
            if self.isPrevisu():
                joueurCaseEffet.msgsPrevisu.append("Soin "+str(self.valSoin))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
