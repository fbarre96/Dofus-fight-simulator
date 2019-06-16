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
        @kwargs: options supplémentaires, les options case_cible_x et case_cible_y doivent être mentionnées.
        @type: **kwargs"""
        generer_TF = self.kwargs.get("generer_TF", False)
        if generer_TF:
            joueurTF = niveau.gereDeplacementTF(joueurLanceur, [kwargs.get("case_cible_x"), kwargs.get(
                "case_cible_y")], joueurLanceur, kwargs.get("nom_sort"), True, generer_TF)
            if joueurTF != None:
                kwargs.get("cibles_traitees").append(joueurTF)
        else:
            joueurLanceur.bouge(niveau, kwargs.get(
                "case_cible_x"), kwargs.get("case_cible_y"))
                
class EffetTeleportePosPrec(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte un ennemi vers sa position précedente. L'historique des 2 derniers tours seulement est gardé."""

    def __init__(self, int_nbCase, **kwargs):
        """@summary: Initialise un effet téléportant sa cible vers sa position précédente. L'historique des 2 derniers tours seulement est gardé.
        @int_nbCase: le nombre de retour en arrière effectué. Par forcément égale au nombre de case reculés.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nbCase = int_nbCase
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetTeleportePosPrec(self.nbCase, **self.kwargs)

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
        joueurCaseEffet.tpPosPrec(
            self.nbCase, niveau, joueurLanceur, kwargs.get("nom_sort"))


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
                                 joueurLanceur, "Renvoi", AjouteHistorique=True)


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
                                 joueurLanceur, "Renvoi", AjouteHistorique=True)


class EffetTpSym(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte le lanceur symétriquement par rapport au point de symétrie qui est le joueur cible."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant le lanceur symétriquement par rapport au point de symétrie qui est le joueur cible.
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
        niveau.gereDeplacementTF(joueurLanceur, [
                                 arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)


class EffetTpSymSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport au point de symétrie qu'est le lanceur."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement par rapport au point de symétrie qu'est le lanceur.
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
        niveau.gereDeplacementTF(joueurCaseEffet, [
                                 arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)


class EffetTpSymCentre(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet téléporte la cible symétriquement par rapport au point de symétrie donné par case_cible_x et case_cible_y."""

    def __init__(self, **kwargs):
        """@summary: Initialise un effet téléportant la cible symétriquement par rapport au point de symétrie donné par case_cible_x et case_cible_y.
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
        @kwargs: options supplémentaires, l'option nom_sort, case_cible_x et case_cible_y doivent être mentionées
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            distanceX = (joueurCaseEffet.posX-kwargs.get("case_cible_x"))
            distanceY = (joueurCaseEffet.posY-kwargs.get("case_cible_y"))
            arriveeX = kwargs.get("case_cible_x")-distanceX
            arriveeY = kwargs.get("case_cible_y")-distanceY
            joueurTF = niveau.gereDeplacementTF(joueurCaseEffet, [
                                                arriveeX, arriveeY], joueurLanceur, kwargs.get("nom_sort"), AjouteHistorique=True)
            # Evite de retéléporter les cibles s'étant déplacé après un téléfrags
            if joueurTF != None:
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

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary: Appelé lors de l'application de l'effet.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires, les options cible_traitees et nom_sort doivent être mentionnées. L'option generer_TF peut être mentionnée.
        @type: **kwargs"""
        perso1AEchange = None
        if self.persoADeplace == "lanceur":
            perso1AEchange = joueurLanceur
        elif self.persoADeplace == "cible":
            perso1AEchange = niveau.getJoueurSur(kwargs.get(
                "case_cible_x"), kwargs.get("case_cible_y"))
        if perso1AEchange is None:
            return
        genereTF = kwargs.get("generer_TF", False)
        joueurTF = niveau.gereDeplacementTF(perso1AEchange, [
                                            joueurCaseEffet.posX, joueurCaseEffet.posY], joueurLanceur, kwargs.get("nom_sort"), True, genereTF)
        if joueurTF != None:
            kwargs.get("cibles_traitees").append(joueurTF)