"""@summary: Rassemble les effets de sort en rapport avec les téléportations."""

from Effets.Effet import Effet


class EffetTp(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur sur la case ciblée."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant le lanceur sur la case ciblée.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __str__(self):
        return "Téléporte sur la cible"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        genererTFLbl = ttk.Label(frame, text="Peut Telefrag:")
        genererTFLbl.pack(side="left")
        genererTFVar = tk.BooleanVar()
        genererTFVar.set(self.kwargs.get("genererTF", False))
        genererTFCheckbutton = ttk.Checkbutton(frame, variable=genererTFVar)
        genererTFCheckbutton.pack(side="left")
        ret["kwargs:genererTF"] = genererTFVar
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(**infos["kwargs"])


    def __deepcopy__(self, memo):
        return EffetTp(**self.kwargs)

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
        genererTF = self.kwargs.get("genererTF", False)
        if genererTF:
            joueurTF = niveau.gereDeplacementTF(joueurLanceur,
                                                [kwargs.get("caseCibleX"),
                                                 kwargs.get("caseCibleY")],
                                                joueurLanceur, kwargs.get("nom_sort"),
                                                True, genererTF)
            if joueurTF is not None:
                kwargs.get("cibles_traitees").append(joueurTF)
        else:
            joueurLanceur.bouge(niveau, kwargs.get(
                "caseCibleX"), kwargs.get("caseCibleY"))


class EffetTeleportePosPrec(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte un ennemi vers sa position précedente.
    L'historique des 2 derniers tours seulement est gardé."""

    def __init__(self, int_nbCase=1, **kwargs):
        """@summary: Initialise un effet téléportant sa cible vers sa position précédente.
        L'historique des 2 derniers tours seulement est gardé.
        @int_nbCase: le nombre de retour en arrière effectué.
                     Par forcément égale au nombre de case reculés.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTeleportePosPrec(self.nbCase, **self.kwargs)

    def __str__(self):
        return "Téléporte la cible  à "+str(self.nbCase)+" précédente(s)"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nbCaseLbl = ttk.Label(frame, text="Nb pos prec:")
        nbCaseLbl.pack(side="left")
        nbCaseSpinbox = tk.Spinbox(frame, from_=1, to=9999, width=4)
        nbCaseSpinbox.delete(0, 'end')
        nbCaseSpinbox.insert(0, int(self.nbCase))
        nbCaseSpinbox.pack(side="left")
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nbCase"] = self.nbCase
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(int(infos["nbCase"]), **infos["kwargs"])


    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort doit être mentionée
        @type: **kwargs"""
        if joueurCaseEffet is None:
            return
        self.nomSort = kwargs.get("nom_sort")
        if self.pile:
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
        else:
            self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.tpPosPrec(
                self.nbCase, niveau, joueurLanceur, self.nomSort)


class EffetTeleporteDebutTour(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible vers sa position de début de tour."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible vers sa position de début de tour.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTeleporteDebutTour(**self.kwargs)

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
        niveau.gereDeplacementTF(joueurCaseEffet, joueurCaseEffet.posDebTour,
                                 joueurLanceur, "Renvoi", ajouteHistorique=True)


class EffetTeleporteDebutCombat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible vers sa position de début de combat."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible vers sa position de début de combat.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTeleporteDebutCombat(**self.kwargs)

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
        niveau.gereDeplacementTF(joueurCaseEffet, joueurCaseEffet.posDebCombat,
                                 joueurLanceur, "Renvoi", ajouteHistorique=True)


class EffetTpSym(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur symétriquement par rapport
    au point de symétrie qui est le joueur cible."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant le lanceur symétriquement
                     par rapport au point de symétrie qui est le joueur cible.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTpSym(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, doit être mentionée
        @type: **kwargs"""
        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurCaseEffet.posX+distanceX
        arriveeY = joueurCaseEffet.posY+distanceY
        niveau.gereDeplacementTF(joueurLanceur, [arriveeX, arriveeY],
                                 joueurLanceur, kwargs.get("nom_sort"), ajouteHistorique=True)


class EffetTpSymSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport
    au point de symétrie qu'est le lanceur."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement
        par rapport au point de symétrie qu'est le lanceur.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTpSymSelf(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort, doit être mentionée
        @type: **kwargs"""

        distanceX = (joueurCaseEffet.posX-joueurLanceur.posX)
        distanceY = (joueurCaseEffet.posY-joueurLanceur.posY)
        arriveeX = joueurLanceur.posX-distanceX
        arriveeY = joueurLanceur.posY-distanceY
        niveau.gereDeplacementTF(joueurCaseEffet, [arriveeX, arriveeY],
                                 joueurLanceur, kwargs.get("nom_sort"), ajouteHistorique=True)


class EffetTpSymCentre(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport
    au point de symétrie donné par caseCibleX et caseCibleY."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement
        par rapport au point de symétrie donné par caseCibleX et caseCibleY.
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTpSymCentre(**self.kwargs)

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, l'option nom_sort,
                 caseCibleX et caseCibleY doivent être mentionées
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            distanceX = (joueurCaseEffet.posX-kwargs.get("caseCibleX"))
            distanceY = (joueurCaseEffet.posY-kwargs.get("caseCibleY"))
            arriveeX = kwargs.get("caseCibleX")-distanceX
            arriveeY = kwargs.get("caseCibleY")-distanceY
            joueurTF = niveau.gereDeplacementTF(joueurCaseEffet, [arriveeX, arriveeY],
                                                joueurLanceur, kwargs.get("nom_sort"),
                                                ajouteHistorique=True)
            # Evite de retéléporter les cibles s'étant déplacé après un téléfrags
            if joueurTF is not None:
                kwargs.get("cibles_traitees").append(joueurTF)


class EffetEchangePlace(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet échange deux joueurs et peut provoquer un téléfrag"""

    def __init__(self, persoADeplace="lanceur", **kwargs):
        """@summary: Initialise un effet échangeant deux joueurs et puvant provoquer un téléfrag
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.persoADeplace = persoADeplace
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEchangePlace(self.persoADeplace, **self.kwargs)
    
    def __str__(self):
        return "Echange de place avec la cible"
    
    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        persoADeplaceLbl = ttk.Label(frame, text="Personnage à déplacer:")
        persoADeplaceLbl.pack(side="left")
        persoADeplaceCombobox = ttk.Combobox(frame, values=("lanceur", "cible"), state="readonly")
        persoADeplaceCombobox.delete(0, 'end')
        persoADeplaceCombobox.insert(0, self.persoADeplace)
        persoADeplaceCombobox.pack(side="left")
        ret["persoADeplace"] = persoADeplaceCombobox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["persoADeplace"] = self.persoADeplace
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["persoADeplace"], **infos["kwargs"])

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires,
                 les options cible_traitees et nom_sort doivent être mentionnées.
                 L'option genererTF peut être mentionnée.
        @type: **kwargs"""
        if joueurCaseEffet is None:
            return
        perso1AEchange = None
        if self.persoADeplace == "lanceur":
            perso1AEchange = joueurLanceur
        elif self.persoADeplace == "cible":
            perso1AEchange = niveau.getJoueurSur(kwargs.get(
                "caseCibleX"), kwargs.get("caseCibleY"))
        if perso1AEchange is None:
            return
        genereTF = kwargs.get("genererTF", False)
        joueurTF = niveau.gereDeplacementTF(perso1AEchange,
                                            [joueurCaseEffet.posX, joueurCaseEffet.posY],
                                            joueurLanceur, kwargs.get("nom_sort"), True, genereTF)
        if joueurTF is not None:
            kwargs.get("cibles_traitees").append(joueurTF)
