import random

from Effets.Effet import Effet
import Zones

class EffetDegats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet inflige des dégâts à une cible."""

    def __init__(self, int_minJet, int_maxJet, str_typeDegats, **kwargs):
        """@summary: Initialise un effet de dégâts.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.minJet = int_minJet
        self.maxJet = int_maxJet
        self.typeDegats = str_typeDegats.lower()
        self.kwargs = kwargs
        super(EffetDegats, self).__init__(**kwargs)

    def deepcopy(self):
        cpy = EffetDegats(self.minJet, self.maxJet,
                          self.typeDegats, **self.kwargs)
        return cpy

    def calculDegats(self, niveau, joueurCaseEffet, joueurLanceur, nomSort, case_cible_x, case_cible_y, howToChoose="alea"):
        if joueurCaseEffet == None:
            return None

        carac = 0
        dos = 0
        resFixes = 0
        rePer = 0
        if self.typeDegats == "eau":
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.cha
                dos += joueurLanceur.doEau
            resFixes += joueurCaseEffet.reEau
            rePer = joueurCaseEffet.rePerEau
        elif self.typeDegats == "air":
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.agi
                dos += joueurLanceur.doAir
            resFixes += joueurCaseEffet.reAir
            rePer = joueurCaseEffet.rePerAir
        elif self.typeDegats == "terre":
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.fo
                dos += joueurLanceur.doTerre
            resFixes += joueurCaseEffet.reTerre
            rePer = joueurCaseEffet.rePerTerre
        elif self.typeDegats == "feu":
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.int
                dos += joueurLanceur.doFeu
            resFixes += joueurCaseEffet.reFeu
            rePer = joueurCaseEffet.rePerFeu
        elif self.typeDegats == "neutre":
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.fo
                dos += joueurLanceur.doNeutre
            resFixes += joueurCaseEffet.reNeutre
            rePer = joueurCaseEffet.rePerNeutre
        if self.kwargs.get("piege", False) == True:
            if self.kwargs.get("bypassDmgCalc", False) == False:
                carac += joueurLanceur.doPiegesPui
                dos += joueurLanceur.doPieges
        if self.isCC():
            if self.kwargs.get("bypassDmgCalc", False) == False:
                dos += joueurLanceur.doCri
            resFixes += joueurCaseEffet.reCc
        if self.kwargs.get("bypassDmgCalc", False) == False:
            if nomSort != "cac":
                dos += joueurLanceur.doSorts
            else:
                dos += joueurLanceur.doArmes
            dos += joueurLanceur.do
            carac += joueurLanceur.pui

        distance = Zones.getDistancePoint([joueurCaseEffet.posX, joueurCaseEffet.posY], [
                                          joueurLanceur.posX, joueurLanceur.posY])

        if howToChoose == "min":
            baseDeg = self.minJet
        elif howToChoose == "max":
            baseDeg = self.maxJet
        else:
            baseDeg = random.randrange(self.minJet, self.maxJet+1)

        # Etats du lanceur
        total = 0
        for etat in joueurLanceur.etats:
            if etat.actif():
                dos, baseDeg, carac = etat.triggerAvantCalculDegats(
                    dos, baseDeg, carac, nomSort)
        total += baseDeg + (baseDeg * ((carac) / 100)) + dos
        if distance == 1:
            if self.kwargs.get("bypassDmgCalc", False) == False:
                total += int((joueurLanceur.doMelee/100.0) * total)
                rePer += joueurCaseEffet.reMelee
        else:
            if self.kwargs.get("bypassDmgCalc", False) == False:
                total += int((joueurLanceur.doDist/100.0) * total)
                rePer += joueurCaseEffet.reDist
        # appliquer les effets des etats sur les degats total du joueur cible
        eloignement = Zones.getDistancePoint(
            [joueurCaseEffet.posX, joueurCaseEffet.posY], [case_cible_x, case_cible_y])
        total = total * (10-eloignement)/10
        total = int(total)

        vaSubir = total - resFixes
        vaSubir = (vaSubir) - int((rePer/100)*vaSubir)
        for etat in joueurLanceur.etats:
            if etat.actif():
                vaSubir = etat.triggerApresCalculDegats(
                    vaSubir, self.typeDegats, joueurCaseEffet, joueurLanceur)

        for etat in joueurCaseEffet.etats:
            if etat.actif():
                vaSubir = etat.triggerApresCalculDegats(
                    vaSubir, self.typeDegats, joueurCaseEffet, joueurLanceur)
        if vaSubir < 0:
            vaSubir = 0

        return vaSubir

    def appliquerDegats(self, niveau, joueurCaseEffet, joueurLanceur):
        """@summary: calcul les dégâts à infligés et applique ces dégâts à la cible.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage

        @return: Le total de dégâts infligés"""
        joueurCaseEffet.subit(joueurLanceur, niveau,
                              self.total, self.typeDegats, not self.isPrevisu())
        return self.total

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
            if self.isPrevisu():
                total_min = self.calculDegats(niveau, joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), "min")
                total_max = self.calculDegats(niveau, joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("case_cible_x"), kwargs.get("case_cible_y"), "max")
                self.total = total_min
                joueurCaseEffet.msgsPrevisu.append(
                    str(total_min)+"-"+str(total_max))
            else:
                self.total = self.calculDegats(niveau, joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("case_cible_x"), kwargs.get("case_cible_y"))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            self.appliquerDegats(niveau, joueurCaseEffet, joueurLanceur)


class EffetVolDeVie(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible et soigne le lanceur de la moitié des dégâts infligés."""

    def __init__(self, int_minJet, int_maxJet, str_typeDegats, **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetVolDeVie, self).__init__(
            int_minJet, int_maxJet, str_typeDegats, **kwargs)

    def deepcopy(self):
        return EffetVolDeVie(self.minJet, self.maxJet, self.typeDegats, **self.kwargs)

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

        # Utilisation du parent EffetDegats
        if joueurCaseEffet is not None:
            self.total = super(EffetVolDeVie, self).calculDegats(niveau, joueurCaseEffet, joueurLanceur, kwargs.get(
                "nom_sort", ""), kwargs.get("case_cible_x"), kwargs.get("case_cible_y"))
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # Et enfin le vol de  vie

        if joueurCaseEffet is not None:
            # Le soin est majoré à la vie de début du combat
            if joueurLanceur.vie > joueurLanceur._vie:
                joueurLanceur.vie = joueurLanceur._vie
            self.appliquerDegats(niveau, joueurCaseEffet, joueurLanceur)
            # Soin

            joueurLanceur.vie += (self.total/2)
            joueurLanceur.vie = int(joueurLanceur.vie)
            if not self.isPrevisu():
                print(joueurLanceur.nomPerso+" vol " +
                      str(int(self.total/2)) + "PV")


class EffetDegatsSelonPMUtilises(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible divisés selon le ratio PM."""

    def __init__(self, int_minJet, int_maxJet, str_typeDegats, **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super(EffetDegatsSelonPMUtilises, self).__init__(
            int_minJet, int_maxJet, str_typeDegats, **kwargs)

    def deepcopy(self):
        return EffetDegatsSelonPMUtilises(self.minJet, self.maxJet, self.typeDegats, **self.kwargs)

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

        # Utilisation du parent EffetDegats
        if joueurCaseEffet is not None:
            self.total = super(EffetDegatsSelonPMUtilises, self).calculDegats(niveau, joueurCaseEffet, joueurLanceur, kwargs.get(
                "nom_sort", ""), kwargs.get("case_cible_x"), kwargs.get("case_cible_y"))
            ratioPM = abs(float(joueurLanceur.PM) / float(joueurLanceur._PM))
            ratioPM = max(ratioPM, 0)
            self.total = int(ratioPM * self.total)
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)

