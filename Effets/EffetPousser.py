from Effets.Effet import Effet

class EffetPousser(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pousse un joueur à l'opposé une position donnée."""

    def __init__(self, int_nbCase, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
        """@summary: Initialise un effet poussant un joueur à l'opposé d'une position donnée
        @int_nbCase: le nombre de case dont le joueur cible va être poussé.
        @type: int
        @source: une string indiquant la provenance de la poussée (Lanceur|)
        @type: str
        @cible: une string indiquant la direction de la poussée (Lanceur|)
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        self.source = source
        self.cible = cible
        super(EffetPousser, self).__init__(**kwargs)

    def deepcopy(self):
        return EffetPousser(self.nbCase, self.source, self.cible, **self.kwargs)

    def determinerSensPousser(self, niveau, cible, sourceX, sourceY):
        """@summary: Retourne des données permettant de calculer le sens dans lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Personnage
        @sourceX: la coordonnée x depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int
        @sourceY: la coordonnée y depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int

        @return: Retoure un point dans les coordonnées d'un repère normé de centre (0,0). Par exemple, (1,0) est horizontal vers la droite. (0,1) vertical haut. (1,-1) anti-diagonal vers le bas. 
        """

        # Calcul de la direction de la poussée
        cible_posX = cible[0]
        cible_posY = cible[1]
        dist_lignes = abs(cible_posY - sourceY)
        dist_colognes = abs(cible_posX - sourceX)
        self.coordonnees = [0, 0]
        if dist_lignes == 0 and dist_colognes == 0:
            return
        self.coordonnees[0] = 1 if (dist_colognes >= dist_lignes) else 0
        self.coordonnees[1] = 1 if (dist_colognes <= dist_lignes) else 0
        if self.coordonnees[0] == 1 and cible_posX < sourceX:
            self.coordonnees[0] = -1
        if self.coordonnees[1] == 1 and cible_posY < sourceY:
            self.coordonnees[1] = -1
        return self.coordonnees[1]

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.case_from_x = kwargs.get("case_cible_x")
            self.case_from_y = kwargs.get("case_cible_y")
        elif self.source == "Lanceur":
            self.case_from_x = joueurLanceur.posX
            self.case_from_y = joueurLanceur.posY
        if self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAPousser = niveau.getJoueurSur(
                joueurCaseEffet.posX, joueurCaseEffet.posY)
        elif self.cible == "Lanceur":
            self.joueurAPousser = joueurLanceur
        self.determinerSensPousser(niveau, [
                                   self.joueurAPousser.posX, self.joueurAPousser.posY], self.case_from_x, self.case_from_y)
        niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.pousser(self, self.joueurAPousser, joueurLanceur,
                       True, self.case_from_x, self.case_from_y)


class EffetPousserJusque(EffetPousser):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pousse un joueur à l'opposé une position donnée."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet poussant un joueur à l'opposé d'une position donnée
        @int_nbCase: le nombre de case dont le joueur cible va être poussé.
        @type: int
        @source: une string indiquant la provenance de la poussée (Lanceur|)
        @type: str
        @cible: une string indiquant la direction de la poussée (Lanceur|)
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = 0
        super(EffetPousserJusque, self).__init__(0, "", "", **kwargs)

    def deepcopy(self):
        return EffetPousserJusque(**self.kwargs)

    def determinerSensPousser(self, niveau, cible, sourceX, sourceY):
        """@summary: Retourne des données permettant de calculer le sens dans lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Personnage
        @sourceX: la coordonnée x depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int
        @sourceY: la coordonnée y depuis laquelle le joueur se fait poussé. Si None est donné, c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int

        @return: Retoure un point dans les coordonnées d'un repère normé de centre (0,0). Par exemple, (1,0) est horizontal vers la droite. (0,1) vertical haut. (1,-1) anti-diagonal vers le bas. 
        """

        # Calcul de la direction de la poussée
        cible_posX = cible[0]
        cible_posY = cible[1]
        dist_lignes = abs(cible_posY - sourceY)
        dist_colognes = abs(cible_posX - sourceX)
        self.coordonnees = [0, 0]
        if dist_lignes == 0 and dist_colognes == 0:
            return
        self.coordonnees[0] = 1 if (dist_colognes >= dist_lignes) else 0
        self.coordonnees[1] = 1 if (dist_colognes <= dist_lignes) else 0
        if self.coordonnees[0] == 1 and cible_posX < sourceX:
            self.coordonnees[0] = -1
        if self.coordonnees[1] == 1 and cible_posY < sourceY:
            self.coordonnees[1] = -1
        return self.coordonnees[1]

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            return
        self.case_from_x = joueurLanceur.posX
        self.case_from_y = joueurLanceur.posY
        self.case_to_x = kwargs.get("case_cible_x")
        self.case_to_y = kwargs.get("case_cible_y")
        self.determinerSensPousser(niveau, [
                                   self.case_to_x, self.case_to_y], self.case_from_x, self.case_from_y)
        self.joueurAPousser = niveau.getJoueurSur(
            joueurLanceur.posX + self.coordonnees[0], joueurLanceur.posY + self.coordonnees[1])
        if self.joueurAPousser is None:
            return
        if self.coordonnees[0] != 0:
            self.nbCase = abs(self.case_to_x - self.joueurAPousser.posX)
        if self.coordonnees[1] != 0:
            self.nbCase = abs(self.case_to_y - self.joueurAPousser.posY)
        niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.pousser(self, self.joueurAPousser, joueurLanceur,
                       False, self.case_from_x, self.case_from_y)


class EffetAttire(EffetPousser):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet attire un joueur vers la position du lanceur."""

    def __init__(self, int_nbCase, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
        """@summary: Initialise un effet repoussant un joueur à l'opposé de la position du lanceur
        @int_nbCase: le nombre de case dont le joueur cible va être attiré.
        @type: int
        @source: string qui définit la provenance de l'attirance parmi CaseCible, Lanceur, JoueurCaseEffet
        @type: str
        @cible: string qui définit la cible de l'attirance parmi Lanceur, JoueurCaseEffet
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.source = source
        self.cible = cible
        self.kwargs = kwargs
        super(EffetAttire, self).__init__(int_nbCase, source, cible, **kwargs)

    def deepcopy(self):
        return EffetAttire(self.nbCase, self.source, self.cible, **self.kwargs)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.attire(self, self.joueurAAttirer, joueurLanceur,
                      self.case_from_x, self.case_from_y)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, case_cible_x et case_cible_y doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.case_from_x = kwargs.get("case_cible_x")
            self.case_from_y = kwargs.get("case_cible_y")
        elif self.source == "Lanceur":
            self.case_from_x = joueurLanceur.posX
            self.case_from_y = joueurLanceur.posY
        elif self.source == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.case_from_x = joueurCaseEffet.posX
            self.case_from_y = joueurCaseEffet.posY
        if self.cible == "Lanceur":
            self.joueurAAttirer = joueurLanceur
        elif self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAAttirer = joueurCaseEffet
        if self.joueurAAttirer != None:
            if self.joueurAAttirer.posX != self.case_from_x or self.joueurAAttirer.posY != self.case_from_y:
                super(EffetAttire, self).determinerSensPousser(niveau, [
                    self.joueurAAttirer.posX, self.joueurAAttirer.posY], self.case_from_x, self.case_from_y)
                #  changement de sens par rapport au sens de pousser
                self.coordonnees[0] *= -1
                self.coordonnees[1] *= -1
                # Pour les attirances en diagonale il faut que je le joueur attirer s'arrête devant l'attireur
                caseMax = self.determinerAttiranceMax()
                self.nbCase = caseMax if self.nbCase > caseMax else self.nbCase
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def determinerAttiranceMax(self):
        if self.coordonnees[0] != 0:
            return abs(self.joueurAAttirer.posX - self.case_from_x)
        else:
            return abs(self.joueurAAttirer.posY - self.case_from_y)