"""@summary: Rassemble les effets de sort en rapport avec les poussées et attirances."""
from Effets.Effet import Effet


class EffetPousser(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pousse un joueur à l'opposé une position donnée."""

    def __init__(self, int_nbCase=0, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
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
        self.coordonnees = [0, 0]
        self.caseFromX = None
        self.caseFromY = None
        self.caseToX = None
        self.caseToY = None
        self.joueurAPousser = None
        super().__init__(**kwargs)

    def __str__(self):
        return "Pousser de "+str(self.nbCase)+" case(s) depuis "+str(self.source)+" vers "+str(self.cible)

    def buildUI(self, topframe,callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nbCaseLbl = ttk.Label(frame, text="Nb cases:")
        nbCaseLbl.pack(side="left")
        nbCaseLblSpinbox = tk.Spinbox(frame, from_=0, to=99, width=3)
        nbCaseLblSpinbox.delete(0, 'end')
        nbCaseLblSpinbox.insert(0, int(self.nbCase))
        nbCaseLblSpinbox.pack(side="left")
        ret["nbCase"] = nbCaseLblSpinbox
        sourceLbl = ttk.Label(frame, text="Source poussé:")
        sourceLbl.pack(side="left")
        sourceCombobox = ttk.Combobox(frame, values=("CaseCible", "Lanceur", "JoueurCaseEffet"), state="readonly")
        sourceCombobox.set(self.source)
        sourceCombobox.pack(side="left")
        ret["source"] = sourceCombobox
        cibleLbl = ttk.Label(frame, text="Cible poussée:")
        cibleLbl.pack(side="left")
        cibleCombobox = ttk.Combobox(frame, values=("Lanceur", "JoueurCaseEffet"), state="readonly")
        cibleCombobox.set(self.cible)
        cibleCombobox.pack(side="left")
        ret["cible"] = cibleCombobox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nbCase"] = self.nbCase
        ret["source"] = self.source
        ret["cible"] = self.cible
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetPousser(int(infos["nbCase"]), infos["source"], infos["cible"], **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetPousser(self.nbCase, self.source, self.cible, **self.kwargs)

    def determinerSensPousser(self, cible, sourceX, sourceY):
        """@summary: Retourne des données permettant de calculer le sens
                    dans lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Personnage
        @sourceX: la coordonnée x depuis laquelle le joueur se fait poussé.
                  Si None est donné, c'est le joueur dont c'est le tour qui sera à
                  l'origine de la poussée.
        @type: int
        @sourceY: la coordonnée y depuis laquelle le joueur se fait poussé.
                  Si None est donné, c'est le joueur dont c'est le tour qui sera à
                  l'origine de la poussée.
        @type: int

        @return: Retoure un point dans les coordonnées d'un repère normé de centre (0,0).
                 Par exemple, (1,0) est horizontal vers la droite. (0,1) vertical haut.
                 (1,-1) anti-diagonal vers le bas.
        """

        # Calcul de la direction de la poussée
        ciblePosX = cible[0]
        ciblePosY = cible[1]
        distLignes = abs(ciblePosY - sourceY)
        distColonnes = abs(ciblePosX - sourceX)
        self.coordonnees = [0, 0]
        if distLignes == 0 and distColonnes == 0:
            return
        self.coordonnees[0] = 1 if (distColonnes >= distLignes) else 0
        self.coordonnees[1] = 1 if (distColonnes <= distLignes) else 0
        if self.coordonnees[0] == 1 and ciblePosX < sourceX:
            self.coordonnees[0] = -1
        if self.coordonnees[1] == 1 and ciblePosY < sourceY:
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
        @kwargs: options supplémentaires, caseCibleX et caseCibleY doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.caseFromX = kwargs.get("caseCibleX")
            self.caseFromY = kwargs.get("caseCibleY")
        elif self.source == "Lanceur":
            self.caseFromX = joueurLanceur.posX
            self.caseFromY = joueurLanceur.posY
        if self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAPousser = niveau.getJoueurSur(
                joueurCaseEffet.posX, joueurCaseEffet.posY)
        elif self.cible == "Lanceur":
            self.joueurAPousser = joueurLanceur
        self.determinerSensPousser([self.joueurAPousser.posX, self.joueurAPousser.posY],
                                   self.caseFromX, self.caseFromY)
        if self.pile:
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
        else:
            self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.pousser(self, self.joueurAPousser, joueurLanceur)


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
        super().__init__(0, "lanceur", "JoueurCaseEffet", **kwargs)

    def __deepcopy__(self, memo):
        return EffetPousserJusque(**self.kwargs)

    def __str__(self):
        return "Pousse la cible jusqu'à la case ciblée"

    def determinerSensPousser(self, cible, sourceX, sourceY):
        """@summary: Retourne des données permettant de calculer le sens dans
                     lequel un joueur sera poussé.
        @joueurCible: le joueur qui va être poussé
        @type: Personnage
        @sourceX: la coordonnée x depuis laquelle le joueur se fait poussé. Si None est donné,
                  c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int
        @sourceY: la coordonnée y depuis laquelle le joueur se fait poussé. Si None est donné,
                  c'est le joueur dont c'est le tour qui sera à l'origine de la poussée.
        @type: int

        @return: Retoure un point dans les coordonnées d'un repère normé de centre (0,0).
                 Par exemple, (1,0) est horizontal vers la droite.
                 (0,1) vertical haut. (1,-1) anti-diagonal vers le bas.
        """

        # Calcul de la direction de la poussée
        ciblePosX = cible[0]
        ciblePosY = cible[1]
        distLignes = abs(ciblePosY - sourceY)
        distColonnes = abs(ciblePosX - sourceX)
        self.coordonnees = [0, 0]
        if distLignes == 0 and distColonnes == 0:
            return
        self.coordonnees[0] = 1 if (distColonnes >= distLignes) else 0
        self.coordonnees[1] = 1 if (distColonnes <= distLignes) else 0
        if self.coordonnees[0] == 1 and ciblePosX < sourceX:
            self.coordonnees[0] = -1
        if self.coordonnees[1] == 1 and ciblePosY < sourceY:
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
        @kwargs: options supplémentaires, caseCibleX et caseCibleY doivent être mentionés
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            return
        self.caseFromX = joueurLanceur.posX
        self.caseFromY = joueurLanceur.posY
        self.caseToX = kwargs.get("caseCibleX")
        self.caseToY = kwargs.get("caseCibleY")
        self.determinerSensPousser([self.caseToX, self.caseToY],
                                   self.caseFromX, self.caseFromY)
        self.joueurAPousser = niveau.getJoueurSur(
            joueurLanceur.posX + self.coordonnees[0], joueurLanceur.posY + self.coordonnees[1])
        if self.joueurAPousser is None:
            return
        if self.coordonnees[0] != 0:
            self.nbCase = abs(self.caseToX - self.joueurAPousser.posX)
        if self.coordonnees[1] != 0:
            self.nbCase = abs(self.caseToY - self.joueurAPousser.posY)
        if self.pile:
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
        else:
            self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.pousser(self, self.joueurAPousser, joueurLanceur, False)


class EffetAttire(EffetPousser):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet attire un joueur vers la position du lanceur."""

    def __init__(self, int_nbCase=0, source="Lanceur", cible="JoueurCaseEffet", **kwargs):
        """
        @summary: Initialise un effet repoussant un joueur à l'opposé de la position du lanceur
        @int_nbCase: le nombre de case dont le joueur cible va être attiré.
        @type: int
        @source: string qui définit la provenance de l'attirance parmi CaseCible,
                 Lanceur, JoueurCaseEffet
        @type: str
        @cible: string qui définit la cible de l'attirance parmi Lanceur, JoueurCaseEffet
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.source = source
        self.cible = cible
        self.kwargs = kwargs
        self.joueurAAttirer = None
        super().__init__(int_nbCase, source, cible, **kwargs)

    def __str__(self):
        return "Attire de "+str(self.nbCase)+" vers "+str(self.source)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nbCaseLbl = ttk.Label(frame, text="Nb cases:")
        nbCaseLbl.pack(side="left")
        nbCaseLblSpinbox = tk.Spinbox(frame, from_=0, to=99, width=3)
        nbCaseLblSpinbox.delete(0, 'end')
        nbCaseLblSpinbox.insert(0, int(self.nbCase))
        nbCaseLblSpinbox.pack(side="left")
        ret["nbCase"] = nbCaseLblSpinbox
        sourceLbl = ttk.Label(frame, text="Source attirance:")
        sourceLbl.pack(side="left")
        sourceCombobox = ttk.Combobox(frame, values=("CaseCible", "Lanceur", "JoueurCaseEffet"), state="readonly")
        sourceCombobox.set(self.source)
        sourceCombobox.pack(side="left")
        ret["source"] = sourceCombobox
        cibleLbl = ttk.Label(frame, text="Cible attiré:")
        cibleLbl.pack(side="left")
        cibleCombobox = ttk.Combobox(frame, values=("Lanceur", "JoueurCaseEffet"), state="readonly")
        cibleCombobox.set(self.cible)
        cibleCombobox.pack(side="left")
        ret["cible"] = cibleCombobox
        frame.pack()
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetAttire(int(infos["nbCase"]), infos["source"], infos["cible"], **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetAttire(self.nbCase, self.source, self.cible, **self.kwargs)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        niveau.attire(self, self.joueurAAttirer, joueurLanceur)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, caseCibleX et caseCibleY doivent être mentionés
        @type: **kwargs"""
        if self.source == "CaseCible":
            self.caseFromX = kwargs.get("caseCibleX")
            self.caseFromY = kwargs.get("caseCibleY")
        elif self.source == "Lanceur":
            self.caseFromX = joueurLanceur.posX
            self.caseFromY = joueurLanceur.posY
        elif self.source == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.caseFromX = joueurCaseEffet.posX
            self.caseFromY = joueurCaseEffet.posY
        if self.cible == "Lanceur":
            self.joueurAAttirer = joueurLanceur
        elif self.cible == "JoueurCaseEffet":
            if joueurCaseEffet is None:
                return
            self.joueurAAttirer = joueurCaseEffet
        if self.joueurAAttirer is not None:
            if self.joueurAAttirer.posX != self.caseFromX \
               or self.joueurAAttirer.posY != self.caseFromY:
                super().determinerSensPousser([self.joueurAAttirer.posX, self.joueurAAttirer.posY],
                                              self.caseFromX, self.caseFromY)
                #  changement de sens par rapport au sens de pousser
                self.coordonnees[0] *= -1
                self.coordonnees[1] *= -1
                # Pour les attirances en diagonale
                # il faut que je le joueur attiré s'arrête devant l'attireur
                caseMax = self.determinerAttiranceMax()
                self.nbCase = caseMax if self.nbCase > caseMax else self.nbCase
                if self.pile:
                    niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
                else:
                    self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def determinerAttiranceMax(self):
        """
        @summary: Calcul le nombre de case maximal qui seront parcourues
                  Qui correspondent à la distance à l'attireur
        """
        if self.coordonnees[0] != 0:
            return abs(self.joueurAAttirer.posX - self.caseFromX)
        return abs(self.joueurAAttirer.posY - self.caseFromY)
