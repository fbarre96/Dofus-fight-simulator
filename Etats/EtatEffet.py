"""@summary: Rassemble les états qui déclenche un effet."""

from Etats.Etat import Etat
from Effets.Effet import Effet, ChildDialogEffect
from copy import deepcopy

class EtatEffet(Etat):
    """Abstraction: claase pour tout les etats qui appliquent des effets"""
    def __init__(self, nom, debDans, duree, effet, nomSort, quiLancera, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état ou
                "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.effet = effet
        self.nomSort = nomSort
        self.quiLancera = quiLancera
        super().__init__(nom, debDans, duree, lanceur, desc)

    def buildUI(self, topframe, callbackDict, quiLanceraValues):
        from tkinter import ttk
        self.parent = topframe
        self.modCallback = callbackDict
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        frame.pack()
        effetBuilderlbl = ttk.Label(frame, text="Crafter un effet:")
        effetBuilderlbl.grid(row=0, column=0, sticky="e")
        self.effetDescEntry = ttk.Entry(frame, width=50, state="normal")
        self.effetDescEntry.delete(0, "end")
        self.effetDescEntry.insert(0, str(self.effet))
        self.effetDescEntry.grid(row=0, column=1, sticky="w")
        self.effetDescEntry.configure(state="readonly")
        effetBuilderButton = ttk.Button(frame, text="Craft effet", command=lambda: self.openEffectDialog())
        effetBuilderButton.grid(row=0, column=2, sticky="w")
        ret["effet"] = self.effet
        nomSortLbl = ttk.Label(frame, text="Nom du sort:")
        nomSortLbl.grid(row=1, column=0, sticky="e")
        self.nomSortEntry = ttk.Entry(frame, width=50)
        self.nomSortEntry.delete(0, "end")
        self.nomSortEntry.insert(0, self.nomSort)
        self.nomSortEntry.grid(row=1, column=1, sticky="w")
        ret["nomSort"] = self.nomSortEntry
        quiLanceraLbl = ttk.Label(frame, text="Qui lancera l'effet:")
        quiLanceraLbl.grid(row=2, column=0, sticky="e")
        self.quiLanceraCombobox = ttk.Combobox(frame, values=quiLanceraValues, state="readonly")
        self.quiLanceraCombobox.set(self.quiLancera)
        self.quiLanceraCombobox.grid(row=2, column=1, sticky="w")
        ret["quiLancera"] = self.quiLanceraCombobox
        return ret

    def openEffectDialog(self, _event=None):
        effectDialog = ChildDialogEffect(self.parent, self.effet)
        self.parent.wait_window(effectDialog.app)
        self.effet = effectDialog.rvalue
        self.effetDescEntry.delete(0, "end")
        self.effetDescEntry.configure(state="normal")
        self.effetDescEntry.insert(0, str(self.effet))
        self.effetDescEntry.configure(state="readonly")
        self.modCallback({"effet": self.effet})

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), infos["nomSort"], infos["quiLancera"], None, infos["desc"])

    def __str__(self):
        ret = super().__str__()
        ret += " "+self.desc+" ("+str(self.effet)+")"
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["effet"] = self.effet.getAllInfos()
        ret["nomSort"] = self.nomSort
        ret["quiLancera"] = self.quiLancera
        return ret

class EtatEffetFinTour(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur termine son tour."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="lanceur", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état ou
                "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @type: tableau
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)

    def buildUI(self, topframe, callbackDict):
        return super().buildUI(topframe, callbackDict, ["lanceur", "cible"])

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetFinTour(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                self.nomSort, self.quiLancera, self.lanceur, self.desc)

    def triggerFinTour(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour termine.
                     Active un effet à la fin du tour du personnage ciblant la position du
                     personnage qui finit son tour,
                     le lanceur peut être lui-même ou le lanceur de l'effet.
        @personnage: le joueur dont le tour finit
        @type: Personnage
        @niveau: La grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, personnage)


class EtatEffetDebutTour(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur débute son tour."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="cible", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui sera lancé lorsque le joueur terminera son tour
        @type: Effet
        @nomSort: le nom de sort à l'origine de l'effet
        @type: string
        @quiLancera: Le Personnage qui lancera l'effet
        @type: string ("lanceur" pour que le lanceur soit le poseur de l'état
               ou "cible" pour que ce soit celui qui possède l'état)

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetDebutTour(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                  self.nomSort, self.quiLancera, self.lanceur, self.desc)
    
    def buildUI(self, topframe, callbackDict):
        return super().buildUI(topframe, callbackDict, ["lanceur", "cible"])

    def triggerDebutTour(self, personnage, niveau):
        """@summary: Un trigger appelé pour tous les états d'un joueur lorsque son tour commence.
                     Active un effet au début du tour ciblant
                     la case du personnage dont le tour débute
                     avec comme lanceur le personnage dont le tour débute  ou le lanceur de l'effet.
        @personnage: le joueur dont le tour débute
        @type: Personnage
        @niveau: Personnage grille de jeu
        @type: Niveau"""
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, personnage.posX, personnage.posY,
                               self.nomSort, personnage.posX, personnage.posY, personnage)


class EtatEffetSiSubit(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur subit des dégâts."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="cible",
                 cible="cible", typeDeg="", provenance="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'un dégât subit
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui lancera l'effet
        @type: string ("lanceur" ou "cible")
        @cible: Le personnage qui subira l'effet
        @type: string ("attaquant" ou "cible")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.cible = cible
        self.typeDeg = typeDeg
        self.provenance = provenance
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict, ("lanceur", "cible"))
        frame = ttk.Frame(topframe)
        frame.pack()
        ciblelbl = ttk.Label(frame, text="Cible de l'effet:")
        ciblelbl.grid(row=0, column=0, sticky="e")
        self.cibleCombobox = ttk.Combobox(frame, values=("attaquant", "cible"), state="readonly")
        self.cibleCombobox.set(self.cible)
        self.cibleCombobox.grid(row=0, column=1, sticky="w")
        ret["cible"] = self.cibleCombobox
        typeDegLbl = ttk.Label(frame, text="Seulement de type :")
        typeDegLbl.grid(row=1, column=0, sticky="e")
        self.typeDegCombobox = ttk.Combobox(frame, values=("", "doPou", "feu", "terre", "air", "eau", "neutre", "melee", "distance"), state="readonly")
        self.typeDegCombobox.set(self.typeDeg)
        self.typeDegCombobox.grid(row=1, column=1, sticky="w")
        ret["typeDeg"] = self.typeDegCombobox
        provenanceLbl = ttk.Label(frame, text="Seulement de provenance:")
        provenanceLbl.grid(row=2, column=0, sticky="e")
        self.provenanceCombobox = ttk.Combobox(frame, values=("", "Allies", "Ennemis"), state="readonly")
        self.provenanceCombobox.set(self.provenance)
        self.provenanceCombobox.grid(row=2, column=1, sticky="w")
        ret["provenance"] = self.provenanceCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiSubit(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["cible"], infos["typeDeg"], infos["provenance"], None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["cible"] = self.cible
        ret["typeDeg"] = self.typeDeg
        ret["provenance"] = self.provenance
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiSubit(self.nom, self.debuteDans, self.duree, deepcopy(self.effet), self.nomSort,
                                self.quiLancera, self.cible, self.typeDeg,
                                self.provenance, self.lanceur, self.desc)

    def triggerAvantSubirDegats(self, cibleAttaque, niveau, totalPerdu, typeDegats, attaquant):
        """@summary: Un trigger appelé pour tous les états du joueur attaqué
                     lorsque des dommages vont être subits.
                     Active un effet ciblant le lanceur ou la cible avant de subir les dégâts
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        validate = False
        if totalPerdu > 0 and (self.typeDeg == typeDegats or self.typeDeg == ""):
            validate = True
        elif self.typeDeg == "melee" and \
         (abs(attaquant.posX - cibleAttaque.posX) + abs(attaquant.posY - cibleAttaque.posY) == 1):
            validate = True
        if not validate:
            return
        if self.provenance != "":
            if self.provenance == "Allies" and cibleAttaque.team != attaquant.team:
                return False
            elif self.provenance == "Ennemis" and cibleAttaque.team == attaquant.team:
                return False
        self.effet.setDegatsSubits(totalPerdu, typeDegats)
        joueurCible = cibleAttaque
        if self.cible == "attaquant":
            joueurCible = attaquant
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, attaquant)

class EtatEffetSiMeurt(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur meurt."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="porteur",
                 cible="porteur", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'un dégât subit
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui lancera l'effet
        @type: string ("lanceur" ou "meurtrier" ou "mouru")
        @cible: Le personnage qui subira l'effet
        @type: string ("meurtrier" ou "mouru")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.cible = cible
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)

    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict, ("porteur", "lanceur", "meurtrier", "mouru"))
        frame = ttk.Frame(topframe)
        frame.pack()
        ciblelbl = ttk.Label(frame, text="Cible de l'effet:")
        ciblelbl.grid(row=0, column=0, sticky="e")
        self.cibleCombobox = ttk.Combobox(frame, values=("meurtrier", "mouru", "porteur"), state="readonly")
        self.cibleCombobox.set(self.cible)
        self.cibleCombobox.grid(row=0, column=1, sticky="w")
        ret["cible"] = self.cibleCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiMeurt(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["cible"], None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["cible"] = self.cible
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiMeurt(self.nom, self.debuteDans, self.duree, deepcopy(self.effet), self.nomSort,
                                self.quiLancera, self.cible, self.lanceur, self.desc)

    def triggerAvantMort(self, niveau, porteur, mouru, meurtrier):
        """@summary: Un trigger appelé pour tous les états des joueurs
                     lorsque un perso meurt.
                     Active un effet ciblant le meurtier ou la victime ou le porteur avant la mort
        @cibleAttaque: le joueur qui va subir les dégâts
        @type: joueur
        @niveau: La grille de jeu
        @type: Niveau
        @totalPerdu: Le total de vie que le joueur va subir.
        @type: int
        @typeDeg:  Le type de dégâts qui va être subit
        @type: string
        @attaquant:  Le joueur à l'origine de l'attaque
        @type: Personnage"""
        joueurCible = porteur
        if self.cible == "meurtrier":
            joueurCible = meurtrier
        elif self.cible == "mouru":
            joueurCible = mouru
        celuiQuiLance = porteur
        if self.quiLancera == "meurtrier":
            celuiQuiLance = meurtrier
        elif self.quiLancera == "mouru":
            celuiQuiLance = mouru
        elif self.quiLancera == "lanceur":
            celuiQuiLance = self.lanceur
        niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                           self.nomSort, joueurCible.posX, joueurCible.posY, celuiQuiLance)

class EtatEffetSiDeplace(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait pousser."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="lanceur", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiDeplace(self.nom, self.debuteDans, self.duree, deepcopy(self.effet), self.nomSort,
                                 self.quiLancera, self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        return super().buildUI(topframe, callbackDict, ["lanceur", "cible"])

    def triggerApresDeplacementForce(self, niveau, deplace, deplaceur):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        print("Effet si deplace entree")
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, self.lanceur.posX, self.lanceur.posY,
                               self.nomSort, deplace.posX, deplace.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, deplace.posX, deplace.posY,
                               self.nomSort, deplace.posX, deplace.posY, deplace)


class EtatEffetSiPiegeDeclenche(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet
                 quand un joueur marche dans un piege."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="",
                 quiLancera="porteur", cible="declencheur", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: int

        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.cible = cible
        super().__init__(nom, debDans, duree, effet, nomSort,
                 quiLancera, lanceur, desc)

    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        ret = super().buildUI(topframe, callbackDict, ("porteur", "cible", "lanceur"))
        frame = ttk.Frame(topframe)
        frame.pack()
        ciblelbl = ttk.Label(frame, text="Cible de l'effet:")
        ciblelbl.grid(row=0, column=0, sticky="e")
        self.cibleCombobox = ttk.Combobox(frame, values=("porteur", "declencheur", "lanceur"), state="readonly")
        self.cibleCombobox.set(self.cible)
        self.cibleCombobox.grid(row=0, column=1, sticky="w")
        ret["cible"] = self.cibleCombobox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiPiegeDeclenche(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["cible"], None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["cible"] = self.cible
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiPiegeDeclenche(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                         self.nomSort, self.quiLancera, self.cible,
                                         self.lanceur, self.desc)

    def triggerAvantPiegeDeclenche(self, niveau, piege, joueurDeclencheur, porteur):
        if self.cible == "declencheur":
            joueurCible = joueurDeclencheur
        elif self.cible == "porteur":
            joueurCible = porteur
        else:
            joueurCible = self.lanceur
        if self.quiLancera == "lanceur":
            niveau.lancerEffet(self.effet, self.lanceur.posX, self.lanceur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, self.lanceur)
        elif self.quiLancera == "cible":
            niveau.lancerEffet(self.effet, joueurCible.posX, joueurCible.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, joueurCible)
        elif self.quiLancera == "porteur":
            niveau.lancerEffet(self.effet, porteur.posX, porteur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, porteur)


class EtatEffetSiTFGenere(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand un joueur est téléfragé."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="joueurOrigineTF",
                 cible="joueurEchangeTF", porteurEstTF=False, sortInterdit="", limiteParTour=99, lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passéq
                pour que l'état se désactive.
        @type: int
        @effet: l effet qui s'activera lors d'un TF
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.porteurEstTF = porteurEstTF
        self.cible = cible
        self.sortInterdit = sortInterdit
        self.limiteParTour = limiteParTour
        self.n_limiteParTour = 0
        self.sortsDejaTraites = []
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict, ("joueurOrigineTF", "joueurEchangeTF", "porteur", "reelLanceur"))
        frame = ttk.Frame(topframe)
        frame.pack()
        ciblelbl = ttk.Label(frame, text="Cible de l'effet:")
        ciblelbl.grid(row=0, column=0, sticky="e")
        self.cibleCombobox = ttk.Combobox(frame, values=("joueurOrigineTF", "joueurEchangeTF", "porteur", "reelLanceur"), state="readonly")
        self.cibleCombobox.set(self.cible)
        self.cibleCombobox.grid(row=0, column=1, sticky="w")
        ret["cible"] = self.cibleCombobox
        porteurEstTFlbl = ttk.Label(frame, text="Si porteur est TF:")
        porteurEstTFlbl.grid(row=1, column=0, sticky="e")
        self.porteurEstTFVar = tk.BooleanVar()
        self.porteurEstTFVar.set(self.porteurEstTF)
        porteurEstTFCheckbutton = ttk.Checkbutton(frame, variable=self.porteurEstTFVar)
        porteurEstTFCheckbutton.grid(row=1, column=1, sticky="w")
        ret["porteurEstTF"] = self.porteurEstTFVar
        sortInterditlbl = ttk.Label(frame, text="Sort interdit:")
        sortInterditlbl.grid(row=2, column=0, sticky="e")
        self.sortInterditEntry = ttk.Entry(frame, width=50)
        self.sortInterditEntry.delete(0, 'end')
        self.sortInterditEntry.insert(0, self.sortInterdit)
        self.sortInterditEntry.grid(row=2, column=1, sticky="w")
        ret["sortInterdit"] = self.sortInterditEntry
        limiteParTourLbl = ttk.Label(frame, text="Limite par tour:")
        limiteParTourLbl.grid(row=3, column=0, sticky="e")
        self.limiteParTourSpinbox = tk.Spinbox(frame, from_=-1, to=99999, width=5)
        self.limiteParTourSpinbox.delete(0, 'end')
        self.limiteParTourSpinbox.insert(-1, int(self.limiteParTour))
        self.limiteParTourSpinbox.grid(row=3, column=1, sticky="w")
        ret["limiteParTour"] = self.limiteParTourSpinbox
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiTFGenere(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["cible"], infos["porteurEstTF"], infos["sortInterdit"], int(infos.get("limiteParTour", 99)), None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["cible"] = self.cible
        ret["porteurEstTF"] = self.porteurEstTF
        ret["sortInterdit"] = self.sortInterdit
        ret["limiteParTour"] = self.limiteParTour
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiTFGenere(self.nom, self.debuteDans, self.duree, deepcopy(self.effet), self.nomSort,
                                   self.quiLancera, self.cible, self.porteurEstTF,
                                   self.sortInterdit, self.limiteParTour, self.lanceur, self.desc)

    def triggerApresTF(self, niveau, joueurOrigineTF, joueurEchangeTF,
                       porteur, reelLanceur, nomSort):
        if self.porteurEstTF and porteur.uid != joueurOrigineTF.uid \
                             and porteur.uid != joueurEchangeTF.uid:
            return
        if self.cible == "joueurOrigineTF":
            joueurCible = joueurOrigineTF
        elif self.cible == "joueurEchangeTF":
            joueurCible = joueurEchangeTF
        elif self.cible == "porteur":
            joueurCible = porteur
        elif self.cible == "reelLanceur":
            joueurCible = reelLanceur
        else:
            joueurCible = reelLanceur
        if self.quiLancera == "joueurOrigineTF":
            joueurLanceur = joueurOrigineTF
        elif self.quiLancera == "joueurEchangeTF":
            joueurLanceur = joueurEchangeTF
        elif self.quiLancera == "porteur":
            joueurLanceur = porteur
        elif self.quiLancera == "reelLanceur":
            joueurLanceur = reelLanceur
        else:
            joueurLanceur = reelLanceur
        if nomSort == self.sortInterdit:
            return
        if self.n_limiteParTour >= self.limiteParTour:
            return
        self.n_limiteParTour += 1
        if nomSort in self.sortsDejaTraites:
            return
        self.sortsDejaTraites.append(nomSort)
        if isinstance(self.effet, list):
            for eff in self.effet:
                eff.setNomSortTF(nomSort)
                sestApplique, _ = niveau.lancerEffet(eff, joueurLanceur.posX,
                                                     joueurLanceur.posY, self.nomSort,
                                                     joueurCible.posX, joueurCible.posY,
                                                     joueurLanceur)
                if not sestApplique:
                    break
        else:
            self.effet.setNomSortTF(nomSort)
            niveau.lancerEffet(self.effet, joueurLanceur.posX, joueurLanceur.posY,
                               self.nomSort, joueurCible.posX, joueurCible.posY, joueurLanceur)

class EtatEffetSiNouvelEtat(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait pousser."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="placeur",
                 nomEtatRequis="", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.nomEtatRequis = nomEtatRequis
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict, ("placeur", "cible", "lanceur"))
        frame = ttk.Frame(topframe)
        frame.pack()
        nomEtatRequislbl = ttk.Label(frame, text="Seulement si nom nouvel état:")
        nomEtatRequislbl.grid(row=0, column=0, sticky="e")
        self.nomEtatRequisEntry = ttk.Entry(frame, width=50)
        self.nomEtatRequisEntry.delete(0, "end")
        self.nomEtatRequisEntry.insert(0, self.nomEtatRequis)
        self.nomEtatRequisEntry.grid(row=0, column=1, sticky="w")
        ret["nomEtatRequis"] = self.nomEtatRequisEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiNouvelEtat(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["nomEtatRequis"], None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomEtatRequis"] = self.nomEtatRequis
        return ret


    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiNouvelEtat(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                     self.nomSort, self.quiLancera, self.nomEtatRequis,
                                     self.lanceur, self.desc)

    def triggerAvantApplicationEtat(self, niveau, nouvelEtat, joueurLanceur, joueurCible):
        """@summary: Un trigger appelé pour le joueur qui obtient un nouvel état.
                     Active un effet sur le lanceur ou la cible"""
        if self.nomEtatRequis != "" and self.nomEtatRequis != nouvelEtat.nom:
            return
        if self.quiLancera == "placeur":
            joueurQuiLance = joueurLanceur
        elif self.quiLancera == "cible":
            joueurQuiLance = joueurCible
        elif self.quiLancera == "lanceur":
            joueurQuiLance = self.lanceur
        cible = joueurCible
        niveau.lancerEffet(self.effet, cible.posX, cible.posY,
                           self.nomSort, cible.posX, cible.posY, joueurQuiLance)


class EtatEffetSiRetraitEtat(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait pousser."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="porteur", etatAccepte="",
                 lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @quiLancera: le personnage qui subira l'effet
        @type: string ("lanceur" ou "cible")

        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        self.etatAccepte = etatAccepte
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict, ("porteur", "lanceur"))
        frame = ttk.Frame(topframe)
        frame.pack()
        etatAccepteLbl = ttk.Label(frame, text="Seulement si nom état retiré:")
        etatAccepteLbl.grid(row=1, column=0, sticky="e")
        self.etatAccepteEntry = ttk.Entry(frame, width=50)
        self.etatAccepteEntry.delete(0, "end")
        self.etatAccepteEntry.insert(0, self.etatAccepte)
        self.etatAccepteEntry.grid(row=1, column=1, sticky="w")
        ret["etatAccepte"] = self.etatAccepteEntry
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EtatEffetSiRetraitEtat(infos["nom"], int(infos["debuteDans"]), int(infos["duree"]), Effet.effectFactory(infos["effet"]), 
                infos["nomSort"], infos["quiLancera"], infos["etatAccepte"], None, infos["desc"])

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["etatAccepte"] = self.etatAccepte
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiRetraitEtat(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                      self.nomSort, self.quiLancera,
                                      self.etatAccepte,
                                      self.lanceur, self.desc)

    def triggerApresRetrait(self, niveau, personnage, porteur, etatRetire):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un état va être retirés.
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        if self.etatAccepte != "" and self.etatAccepte != etatRetire.nom:
            return
        cible = porteur
        if self.quiLancera == "lanceur":
            joueurQuiLance = personnage
        else:
            joueurQuiLance = porteur
        niveau.lancerEffet(self.effet, cible.posX, cible.posY,
                           self.nomSort, cible.posX, cible.posY, joueurQuiLance)

class EtatEffetSiPorte(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait porté."""

    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="porte", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)
    
    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict, ("porte", "porteur"))
        return ret

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiPorte(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                self.nomSort, self.quiLancera,
                                self.lanceur, self.desc)

    def triggerApresPorte(self, niveau, porteur, porte):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        if self.quiLancera == "porteur":
            celuiQuiLancera = porteur
        else:
            celuiQuiLancera = porte
        niveau.lancerEffet(self.effet, celuiQuiLancera.posX, celuiQuiLancera.posY,
                           self.nomSort, porte.posX, porte.posY, celuiQuiLancera)

class EtatEffetSiLance(EtatEffet):
    """@summary: Classe décrivant un état qui active un Effet quand le porteur se fait porté."""
    def __init__(self, nom, debDans, duree, effet=None, nomSort="", quiLancera="lance", lanceur=None, desc=""):
        """@summary: Initialise l'état.
        @nom: le nom de l'état, servira également d'identifiant
        @type: string
        @debDans: le nombre de début de tour qui devront passés pour que l'état s'active.
        @type: int
        @duree: le nombre de début de tour après activation qui devront passés
                pour que l'état se désactive.
        @type: in
        @effet: l'effet qui s'activera lors d'une poussé
        @type: Effet
        @nomSort: le nom du sort qui inflige les dégâts
        @type: string
        @lanceur: le joueur ayant placé cet état
        @type: Personnage ou None
        @desc: la description de ce que fait l'états pour affichage.
        @type: string"""
        super().__init__(nom, debDans, duree, effet, nomSort, quiLancera, lanceur, desc)

    def __deepcopy__(self, memo):
        """@summary: Duplique un état (clone)
        @return: Le clone de l'état"""
        return EtatEffetSiLance(self.nom, self.debuteDans, self.duree, deepcopy(self.effet),
                                self.nomSort, self.quiLancera,
                                self.lanceur, self.desc)

    def buildUI(self, topframe, callbackDict):
        from tkinter import ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict, [])
        return ret

    def triggerApresLance(self, niveau, lanceur, celuiLance):
        # pylint: disable=unused-argument
        """@summary:
        Un trigger appelé au moment ou un personnage se fait porté
        Utile pour les modifications de caractéristiques qui disparaissent à la fin de l'état
        Cet état de base ne fait rien (comportement par défaut hérité).
        @personnage: les options non prévisibles selon les états.
        @type: Personnage"""
        niveau.lancerEffet(self.effet, celuiLance.posX, celuiLance.posY,
                           self.nomSort, celuiLance.posX, celuiLance.posY, lanceur)
                         