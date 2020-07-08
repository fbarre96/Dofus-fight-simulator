"""
@summary: Décrit un effet de sort infligeant des dégats
"""
import random

from Effets.Effet import Effet
import Zones

class EffetDegats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet inflige des dégâts à une cible."""


    def __init__(self, int_minJet=0, int_maxJet=0, str_typeDegats="neutre", **kwargs):
        """@summary: Initialise un effet de dégâts.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés
                         [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.minJet = int_minJet
        self.maxJet = int_maxJet
        self.typeDegats = str_typeDegats.lower()
        self.kwargs = kwargs
        self.total = 0
        super().__init__(**kwargs)

    @classmethod
    def isAffected(cls, effectStr, **kwargs):
        if "a utilisé de PM" in kwargs.get("desc", ""):
            return False
        return "(dommages " in effectStr

    @classmethod
    def craftEffect(cls, effectStr, **kwargs):
        effetsCaracs = effectStr.split(" ")
        degMin = effetsCaracs[0]
        if effetsCaracs[1] == "à":
            degMax = effetsCaracs[2]
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        else:
            degMax = degMin
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        kwargs["effectStr"] = effectStr
        return EffetDegats(int(degMin), int(degMax), degType, **kwargs)
    
    def __str__(self):
        return str(self.minJet)+" à "+str(self.maxJet)+" (dommages "+self.typeDegats.capitalize()+")"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        jetMinLbl = ttk.Label(frame, text="Jet min:")
        jetMinLbl.pack(side="left")
        jetMinSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        jetMinSpinbox.delete(0, 'end')
        jetMinSpinbox.insert(0, int(self.minJet))
        jetMinSpinbox.pack(side="left")
        ret["minJet"] = jetMinSpinbox
        jetMaxLbl = ttk.Label(frame, text="Jet max:")
        jetMaxLbl.pack(side="left")
        jetMaxSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        jetMaxSpinbox.delete(0, 'end')
        jetMaxSpinbox.insert(0, int(self.maxJet))
        jetMaxSpinbox.pack(side="left")
        ret["maxJet"] = jetMaxSpinbox
        degTypeLbl = ttk.Label(frame, text="Type:")
        degTypeLbl.pack(side="left")
        degTypeCombobox = ttk.Combobox(frame, values=("terre", "feu", "air", "chance", "neutre", "meilleur"), state="readonly")
        degTypeCombobox.set(self.typeDegats)
        degTypeCombobox.pack(side="left")
        ret["typeDegats"] = degTypeCombobox
        bypassDmgCalcLbl = ttk.Label(frame, text="Bypass dommage calc (!):")
        bypassDmgCalcLbl.pack(side="left")
        bypassDmgCalcVar = tk.BooleanVar()
        bypassDmgCalcVar.set(self.kwargs.get("bypassDmgCalc", False))
        bypassDmgCalcCheckbutton = ttk.Checkbutton(frame, variable=bypassDmgCalcVar)
        bypassDmgCalcCheckbutton.pack(side="left")
        ret["kwargs:bypassDmgCalc"] = bypassDmgCalcVar
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["minJet"] = self.minJet
        ret["maxJet"] = self.maxJet
        ret["typeDegats"] = self.typeDegats
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(int(infos["minJet"]), int(infos["maxJet"]), infos["typeDegats"], **infos["kwargs"])


    def __deepcopy__(self, memo):
        cpy = EffetDegats(self.minJet, self.maxJet,
                          self.typeDegats, **self.kwargs)
        return cpy

    def calculDegats(self, joueurCaseEffet, joueurLanceur, nomSort,
                     caseCibleX, caseCibleY, howToChoose="alea"):
        """
        @summary: Calcul les dégats qui seront infligés
        @joueurCaseEffet: Le joueur qui doit subir des dégats
        @type: Personnage
        @joueurLanceur: Le joueur qui infligera des dégâts
        @type: Personnage
        @nomSort: le nom du sort à l'origine de ces dégâts
        @type: str
        @caseCibleX: La coordonné X de la case qui a été ciblé pour le sort
        @type: int
        @caseCibleY: La coordonné Y de la case qui a été ciblé pour le sort
        @type: int
        @howToChoose: Indique si le calcul doit être minimal, maximal ou aléatoire
        @type: str parmi ("min","max","alea") alea sera choisi par défaut
        """
        if joueurCaseEffet is None:
            return None
        carac = 0
        dos = 0
        resFixes = 0
        rePer = 0
        if self.typeDegats == "meilleur":
            if joueurLanceur.agi >= joueurLanceur.int and joueurLanceur.agi >= joueurLanceur.cha and joueurLanceur.agi >= joueurLanceur.fo:
                self.typeDegats = "air"
            elif joueurLanceur.int >= joueurLanceur.agi and joueurLanceur.int >= joueurLanceur.cha and joueurLanceur.int >= joueurLanceur.fo:
                self.typeDegats = "feu"
            elif joueurLanceur.cha >= joueurLanceur.agi and joueurLanceur.cha >= joueurLanceur.int and joueurLanceur.cha >= joueurLanceur.fo:
                self.typeDegats = "eau"
            elif joueurLanceur.fo >= joueurLanceur.agi and joueurLanceur.fo >= joueurLanceur.cha and joueurLanceur.fo >= joueurLanceur.int:
                self.typeDegats = "terre"
            else:
                self.typeDegats = "neutre"
        if self.typeDegats == "eau":
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.cha
                dos += joueurLanceur.doEau
            resFixes += joueurCaseEffet.reEau
            rePer = joueurCaseEffet.rePerEau
        elif self.typeDegats == "air":
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.agi
                dos += joueurLanceur.doAir
            resFixes += joueurCaseEffet.reAir
            rePer = joueurCaseEffet.rePerAir
        elif self.typeDegats == "terre":
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.fo
                dos += joueurLanceur.doTerre
            resFixes += joueurCaseEffet.reTerre
            rePer = joueurCaseEffet.rePerTerre
        elif self.typeDegats == "feu":
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.int
                dos += joueurLanceur.doFeu
            resFixes += joueurCaseEffet.reFeu
            rePer = joueurCaseEffet.rePerFeu
        elif self.typeDegats == "neutre":
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.fo
                dos += joueurLanceur.doNeutre
            resFixes += joueurCaseEffet.reNeutre
            rePer = joueurCaseEffet.rePerNeutre
        if self.kwargs.get("piege", False):
            if not self.kwargs.get("bypassDmgCalc", False):
                carac += joueurLanceur.doPiegesPui
                dos += joueurLanceur.doPieges
        if self.isCC():
            if not self.kwargs.get("bypassDmgCalc", False):
                dos += joueurLanceur.doCri
            resFixes += joueurCaseEffet.reCc
        if not self.kwargs.get("bypassDmgCalc", False):
            dos += joueurLanceur.do
            carac += joueurLanceur.pui

        distance = Zones.getDistancePoint([joueurCaseEffet.posX, joueurCaseEffet.posY],
                                          [joueurLanceur.posX, joueurLanceur.posY])

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
                    dos, baseDeg, carac, nomSort, self.minJet, self.maxJet+1)
        total += baseDeg + (baseDeg * int(carac / 100.0)) + dos
        if not self.kwargs.get("bypassDmgCalc", False):
            if nomSort != "cac":
                total += int((joueurLanceur.doSorts/100.0) * total)
            else:
                total += int((joueurLanceur.doArmes/100.0) * total)
            if distance == 1:
                total += int((joueurLanceur.doMelee/100.0) * total)
                rePer += joueurCaseEffet.reMelee
            else:
                total += int((joueurLanceur.doDist/100.0) * total)
                rePer += joueurCaseEffet.reDist

        # appliquer les effets des etats sur les degats total du joueur cible
        eloignement = Zones.getDistancePoint(
            [joueurCaseEffet.posX, joueurCaseEffet.posY], [caseCibleX, caseCibleY])
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
                print("Allait subir : "+str(vaSubir))
                vaSubir = etat.triggerApresCalculDegats(
                    vaSubir, self.typeDegats, joueurCaseEffet, joueurLanceur)
                print("Changer a subit : "+str(vaSubir))
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
                              self.total, self.typeDegats)
        return self.total

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        """@summary:
        Appelé lors de l'application de l'effet, wrapper pour la fonction appliquer dégâts.
        @niveau: la grille de simulation de combat
        @type: Niveau
        @joueurCaseEffet: le joueur se tenant sur la case dans la zone d'effet
        @type: Personnage
        @joueurLanceur: le joueur lançant l'effet
        @type: Personnage
        @kwargs: options supplémentaires
        @type: **kwargs"""
        if joueurCaseEffet is not None:
            if niveau.isPrevisu():
                totalMin = self.calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"), "min")
                totalMax = self.calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"), "max")
                self.total = totalMin
                joueurCaseEffet.msgsPrevisu.append(
                    str(totalMin)+"-"+str(totalMax))
            else:
                self.total = self.calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"))
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            self.appliquerDegats(niveau, joueurCaseEffet, joueurLanceur)


class EffetVolDeVie(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible et soigne le lanceur de la moitié des dégâts infligés.
    """

    def __init__(self, int_minJet=0, int_maxJet=0, str_typeDegats="neutre", **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés
                         parmi [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(
            int_minJet, int_maxJet, str_typeDegats, **kwargs)

    @classmethod
    def isAffected(cls, effectStr, **kwargs):
        return "(vol " in effectStr
    
    @classmethod
    def craftEffect(cls, effectStr, **kwargs):
        #10 à 12 (vol Eau)
        effetsCaracs = effectStr.split(" ")
        degMin = effetsCaracs[0]
        if effetsCaracs[1] == "à":
            degMax = effetsCaracs[2]
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        else:
            degMax = degMin
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        kwargs["effectStr"] = effectStr
        return EffetVolDeVie(int(degMin), int(degMax), degType, **kwargs)
    
    def __str__(self):
        return str(self.minJet)+" à "+str(self.maxJet)+" (vol "+self.typeDegats.capitalize()+")"

    def __deepcopy__(self, memo):
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
            self.total = super().calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"))
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # Et enfin le vol de  vie

        if joueurCaseEffet is not None:
            # Le soin est majoré à la vie de début du combat
            if joueurLanceur.vie > joueurLanceur.vieMax:
                joueurLanceur.vie = joueurLanceur.vieMax
            self.appliquerDegats(niveau, joueurCaseEffet, joueurLanceur)
            # Soin

            joueurLanceur.vie += (self.total/2)
            joueurLanceur.vie = int(joueurLanceur.vie)
            if not niveau.isPrevisu():
                print(joueurLanceur.nomPerso+" vol " +
                      str(int(self.total/2)) + "PV")

class EffetDegatsSelonPVRestants(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts si les pv restants de la cible sont dans le seuil défini.
    """

    def __init__(self, int_minJet=0, int_maxJet=0, str_typeDegats="neutre", int_seuil_bas=0, int_seuil_haut=100, **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés
                         parmi [terre,feu,air,chance,neutre]
        @type: int
        @int_seuil_bas: le seuil de santé minimal ou le joueur doit etre strictement supérieur
        @type: int
        @int_seuil_haut: le seuil de santé maximal ou le joueur doit etre inférieur ou égal
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.seuilBas = int_seuil_bas
        self.seuilHaut = int_seuil_haut
        super().__init__(
            int_minJet, int_maxJet, str_typeDegats, **kwargs)

    def __str__(self):
        return str(self.minJet)+" à "+str(self.maxJet)+" ("+self.typeDegats.capitalize()+")"

    def __deepcopy__(self, memo):
        return EffetDegatsSelonPVRestants(self.minJet, self.maxJet, self.typeDegats, self.seuilBas, self.seuilHaut, **self.kwargs)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        jetMinLbl = ttk.Label(frame, text="Jet min:")
        jetMinLbl.pack(side="left")
        jetMinSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        jetMinSpinbox.delete(0, 'end')
        jetMinSpinbox.insert(0, int(self.minJet))
        jetMinSpinbox.pack(side="left")
        ret["minJet"] = jetMinSpinbox
        jetMaxLbl = ttk.Label(frame, text="Jet max:")
        jetMaxLbl.pack(side="left")
        jetMaxSpinbox = tk.Spinbox(frame, from_=0, to=99999, width=5)
        jetMaxSpinbox.delete(0, 'end')
        jetMaxSpinbox.insert(0, int(self.maxJet))
        jetMaxSpinbox.pack(side="left")
        ret["maxJet"] = jetMaxSpinbox
        degTypeLbl = ttk.Label(frame, text="Type:")
        degTypeLbl.pack(side="left")
        degTypeCombobox = ttk.Combobox(frame, values=("terre", "feu", "air", "chance", "neutre", "meilleur"), state="readonly")
        degTypeCombobox.set(self.typeDegats)
        degTypeCombobox.pack(side="left")
        ret["typeDegats"] = degTypeCombobox
        jetSeuilMinLbl = ttk.Label(frame, text="Seuil bas en % >:")
        jetSeuilMinLbl.pack(side="left")
        jetSeuilMinSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        jetSeuilMinSpinbox.delete(0, 'end')
        jetSeuilMinSpinbox.insert(0, int(self.seuilBas))
        jetSeuilMinSpinbox.pack(side="left")
        ret["seuilBas"] = jetSeuilMinSpinbox
        jetSeuilMaxLbl = ttk.Label(frame, text="Seuil max en % <=:")
        jetSeuilMaxLbl.pack(side="left")
        jetSeuilMaxSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        jetSeuilMaxSpinbox.delete(0, 'end')
        jetSeuilMaxSpinbox.insert(0, int(self.seuilHaut))
        jetSeuilMaxSpinbox.pack(side="left")
        ret["seuilHaut"] = jetSeuilMaxSpinbox
        bypassDmgCalcLbl = ttk.Label(frame, text="Bypass dommage calc (!):")
        bypassDmgCalcLbl.pack(side="left")
        bypassDmgCalcVar = tk.BooleanVar()
        bypassDmgCalcVar.set(self.kwargs.get("bypassDmgCalc", False))
        bypassDmgCalcCheckbutton = ttk.Checkbutton(frame, variable=bypassDmgCalcVar)
        bypassDmgCalcCheckbutton.pack(side="left")
        ret["kwargs:bypassDmgCalc"] = bypassDmgCalcVar
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["minJet"] = self.minJet
        ret["maxJet"] = self.maxJet
        ret["typeDegats"] = self.typeDegats
        ret["seuilBas"] = self.seuilBas
        ret["seuilHaut"] = self.seuilHaut
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(int(infos["minJet"]), int(infos["maxJet"]), infos["typeDegats"], int(infos["seuilBas"]), int(infos["seuilHaut"]), **infos["kwargs"])

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
            if (joueurCaseEffet.vie / joueurCaseEffet.vieMax)*100 < self.seuilBas and (joueurCaseEffet.vie / joueurCaseEffet.vieMax)*100 <= self.seuilHaut:
                self.total = super().calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                    "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"))
                if self.pile:
                    niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
                else:
                    self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # Et enfin le vol de  vie

        if joueurCaseEffet is not None:
            # Le soin est majoré à la vie de début du combat
            if joueurLanceur.vie > joueurLanceur.vieMax:
                joueurLanceur.vie = joueurLanceur.vieMax
            self.appliquerDegats(niveau, joueurCaseEffet, joueurLanceur)
            # Soin

            joueurLanceur.vie += (self.total/2)
            joueurLanceur.vie = int(joueurLanceur.vie)
            if not niveau.isPrevisu():
                print(joueurLanceur.nomPerso+" vol " +
                      str(int(self.total/2)) + "PV")

class EffetDegatsSelonPMUtilises(EffetDegats):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible divisés selon le ratio PM."""

    def __init__(self, int_minJet=0, int_maxJet=0, str_typeDegats="neutre", **kwargs):
        """@summary: Initialise un effet de vol de vie.
        @int_minJet: le jet minimum possible de dégâts de base de l'effet
        @type: int
        @int_maxJet: le jet maximum possible de dégâts de base de l'effet
        @type: int
        @str_typeDegats: l'élément dans lequel les dégâts seront infligés
                         parmi [terre,feu,air,chance,neutre]
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        super().__init__(
            int_minJet, int_maxJet, str_typeDegats, **kwargs)

    def __deepcopy__(self, memo):
        return EffetDegatsSelonPMUtilises(self.minJet, self.maxJet, self.typeDegats, **self.kwargs)

    @classmethod
    def isAffected(cls, effectStr, **kwargs):
        return "a utilisé de PM" in kwargs.get("desc", "") and "(dommages " in effectStr

    @classmethod
    def craftEffect(cls, effectStr, **kwargs):
        #10 à 12 (vol Eau)
        effetsCaracs = effectStr.split(" ")
        degMin = effetsCaracs[0]
        if effetsCaracs[1] == "à":
            degMax = effetsCaracs[2]
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        else:
            degMax = degMin
            # enleve la parenthese de fin d'effet de dommage
            degType = effetsCaracs[-1][:-1]
        kwargs["effectStr"] = effectStr
        return EffetDegatsSelonPMUtilises(int(degMin), int(degMax), degType, **kwargs)

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
            self.total = super().calculDegats(joueurCaseEffet, joueurLanceur, kwargs.get(
                "nom_sort", ""), kwargs.get("caseCibleX"), kwargs.get("caseCibleY"))
            ratioPM = abs(float(joueurLanceur.PM) / float(joueurLanceur.PMBase))
            ratioPM = max(ratioPM, 0)
            self.total = int(ratioPM * self.total)
            niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)


class EffetDegatsPerPv(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Hérite de EffetsDegats.
    Cet effet inflige des dégâts à une cible égal à un pourcentage de sa vie restante."""

    def __init__(self, pourcentage, **kwargs):
        """@summary: Initialise un effet de dégat fixe.
        @pourcentage: Le porucentage de la vie qui sera enlevé à la cible
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.pourcentage = pourcentage
        self.kwargs = kwargs
        self.total = 0
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetDegatsPerPv(self.pourcentage, **self.kwargs)

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
            self.total = int((self.pourcentage / 100.0) * joueurCaseEffet.vie)
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.subit(joueurLanceur, niveau,
                                  self.total, "")
            if not niveau.isPrevisu():
                print(joueurLanceur.nomPerso+" perd " +
                      str(int(self.total)) + "PV")
            