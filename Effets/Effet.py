# -*- coding: utf-8 -*
"""
@summary: Décrit un Effet de sort générique, déclare les fonctions stub
"""
import Zones
from tkinter import ttk
import tkinter as tk

class Effet(object):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
                 Cette classe est 'abstraite' et doit être héritée."""
    subclasses = []
    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.subclasses.append(cls)
    
    @classmethod
    def isAffected(cls, effectStr, **kwargs):
        return False

    @classmethod
    def effectFactory(cls, effect_infos, **kwargs):
        if isinstance(effect_infos, str):
            for classe in cls.subclasses:
                if classe.isAffected(effect_infos, **kwargs):
                    return classe.craftEffect(effect_infos, **kwargs)

            return EffetToDo.craftEffect(str(effect_infos), **kwargs)
        elif isinstance(effect_infos, dict):
            for classe in cls.subclasses:
                if classe.__name__.replace("Effet", "") == effect_infos["effetType"]:
                    return classe.craftFromInfos(effect_infos)
        else:
            raise TypeError("Effect factory expect an effect descrption or a json dict crafted by an effect")
    @classmethod
    def getEffectList(cls):
        return [str(classe.__name__).replace("Effet", '') for classe in cls.subclasses]

    @classmethod
    def getObjectFromName(cls, name):
        for classe in cls.subclasses:
            if str(classe.__name__).replace("Effet", '') == name:
                return classe()
        return None
    @classmethod
    def standardizeStat(cls, statName):
        if statName == "Portée":
            return "PO"
        if statName == "Érosion":
            return "erosion"
        return statName

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(**infos["kwargs"])

    def buildUI(self, topframe, callbackDict):
        ret = {}
        return ret
    def __init__(self, **kwargs):
        """@summary: Initialise un Effet.
        @kwargs: Options de l'effets
        , possibilitées: etat_requis (string séparé par |, aucun par défaut),
                        etat_requis_cibles (string séparé par |, aucun par défaut),
                        etat_requis_lanceur (string séparé par |, aucun par défaut),
                        consomme_etat (booléen, Faux par défaut),
                        cibles_possibles (string, "Allies|Ennemis|Lanceur" par défaut)
                        cibles_exclues (string, aucune par défaut)
                        cible_non_requise (booléen, Faux par défaut).
                                    Indique si l'effet peut être lancé s'il n'a pas de cible direct
                                    (autrement dit si le sort est lancé sur une case vide).
                        zone (Zone, Zones.TypeZoneCercle(0) par défaut = sort mono cible)
        @type: **kwargs"""
        self.etatRequisCibleDirect = kwargs.get('etat_requis', "").split("|")
        if self.etatRequisCibleDirect[-1] == "":
            self.etatRequisCibleDirect = []
        self.etatRequisCibles = kwargs.get('etat_requis_cibles', "").split("|")
        if self.etatRequisCibles[-1] == "":
            self.etatRequisCibles = []
        self.etatRequisLanceur = kwargs.get('etat_requis_lanceur', "").split("|")
        if self.etatRequisLanceur[-1] == "":
            self.etatRequisLanceur = []
        self.consommeEtat = kwargs.get('consomme_etat', False)
        self.ciblesPossibles = kwargs.get(
            'cibles_possibles', "Allies|Ennemis|Lanceur").split("|")
        self.ciblesExclues = kwargs.get('cibles_exclues', "").split("|")
        self.ciblesPossiblesDirect = kwargs.get('cibles_possibles_direct',
                                                "|".join(self.ciblesPossibles)).split("|")
        self.cibleNonRequise = kwargs.get('cible_non_requise', False)
        if kwargs.get('zone', None) is not None:
            self.typeZone = kwargs.get('zone', Zones.TypeZoneCercle(0))
            del kwargs["zone"]
            kwargs["typeZone"] = self.typeZone.__class__.__name__.replace("TypeZone", "")
            kwargs["tailleZone"] = int(self.typeZone.zonePO)
        else:
            self.typeZone = Zones.TypeZone.getZoneFromName(kwargs.get("typeZone", "Cercle"), kwargs.get("tailleZone", 0))
        self.pile = kwargs.get("pile", True)
        self.kwargs = kwargs

    def getAllInfos(self):
        ret = {}
        ret["kwargs"] = self.kwargs
        ret["effetType"] = self.__class__.__name__.replace("Effet", "")
        return ret

    def setCritique(self, val):
        """
        @summary: indique à l'effet qu'il a été lancé avec un sort qui a été critique
        @val: la nouvelle valeur pour le booléen critique
        @type: bool
        """
        self.kwargs["isCC"] = val

    def isCC(self):
        """
        @summary: demance à l'effet s'il a été lancé avec un sort qui a été critique
        @return: bool
        """
        return self.kwargs.get("isCC", False)

    def setSort(self, sort):
        self.kwargs["sort"] = sort
    
    def getSort(self):
        return self.kwargs.get("sort")


    def setNomSortTF(self, val):
        """
        @summary: indique à l'effet le nom du sort a l'origine du téléfrag
        @val: la nouvelle valeur pour le nom du sort
        @type: string
        """
        self.kwargs["nomSortTF"] = val

    def getNomSortTF(self):
        """
        @summary: demance à l'effet le nom du sort à l'origine du téléfrag
        @return: le nom du sort
        """
        return self.kwargs.get("nomSortTF", "")

    def isReverseTreatmentOrder(self):
        """
        @summary: demande à l'effet s'il doit rechercher ses cibles dans le sens inverse.
                  Depuis l'extérieur vers l'intérieur.
        @return: un booléen
        """
        return self.kwargs.get("reversedTreatmentOrder", False)

    def __deepcopy__(self, memo):
        """
        @summary: implémente une copie profonde de l'état
        @return: Renvoie une copie profonde exacte de l'effet
        """
        return Effet(**self.kwargs)

    def setDegatsSubits(self, valPerdu, typeDegats):
        """
        @summary: indique à l'effet les degats subits et le type de dégats
        @valPerdu: Le nombre de points de vie perdus
        @type: int
        @typeDegats: Le type des dégats
        @type: str (Air, Terre, Feu, Eau, Arme...)
        @return: un booléen
        """
        self.kwargs["degatsSubits"] = valPerdu
        self.kwargs["typeDegats"] = typeDegats

    def getDegatsSubits(self):
        """
        @summary: retourne la valeur de degats subits et le type de degats
        @return: renvoie un tuple (degats subits, type de dégats) avec type (int, str)
                défaut est (0,"")
        """
        return self.kwargs.get("degatsSubits", 0), self.kwargs.get("typeDegats", "")

    def estLancable(self, joueurLanceur, joueurCibleDirect):
        # pylint: disable=unused-argument
        """@summary: Test si un effet peut etre lance selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé
                            à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""
        msg = ""
        # Test si une cible direct n'existe pas si l'effet doit être jouée
        if (joueurCibleDirect is None and not self.cibleNonRequise):
            msg = "DEBUG : Invalide : Cible direct non renseigne et pas faire au vide"
            return msg, False
        # Test si un état est requis sur la cible direct et qu'une cible direct existe
        # une liste est vraie si elle n'est pas vide
        if (joueurCibleDirect is None and self.etatRequisCibleDirect):
            msg = "DEBUG : Invalide : Cible direct non renseigne et etatRequis "+ \
                "pour cible direct (" + str(self.etatRequisCibleDirect)+")"
            return msg, False
        if not joueurLanceur.aEtatsRequis(self.etatRequisLanceur):
            msg = "DEBUG : Invalide :etatRequis pour lanceur non present" + \
                str(self.etatRequisLanceur)+" n'est pas présent sur le lanceur"
            return msg, False
        if joueurCibleDirect is not None:
            if not((joueurCibleDirect.team == joueurLanceur.team and \
                joueurCibleDirect.uid != joueurLanceur.uid and \
                "Allies" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.team != joueurLanceur.team and \
                joueurCibleDirect.uid != joueurLanceur.uid and \
                "Ennemis" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.team == joueurLanceur.team and \
                joueurCibleDirect.uid == joueurLanceur.uid and \
                "Lanceur" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.classe in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.invocateur is not None and \
                "Invoc" in self.ciblesPossiblesDirect) \
                    or \
                (joueurCibleDirect.invocateur is not None and \
                joueurCibleDirect.invocateur.uid == joueurCibleDirect.uid and \
                "Invocateur" in self.ciblesPossiblesDirect)):

                msg = "DEBUG : Invalide : Cible Direct non possible "+\
                        str(joueurCibleDirect.classe)+"/"+str(self.ciblesPossiblesDirect)
                return msg, False
            # Test si la cible firect n'est pas une case vide qu'il a bien les états requis
            if not joueurCibleDirect.aEtatsRequis(self.etatRequisCibleDirect):
                msg = "DEBUG : Invalide :etatRequis pour cible direct non present"
                return msg, False
        return msg, True

    def cibleValide(self, joueurLanceur, joueurCible, ciblesDejaTraitees):
        """@summary: Test si un joueur cible est un cible valide selon les options de l'effets.
        @joueurLanceur: Le joueur lançant l'effet
        @type: Personnage
        @joueurCible: Le joueur dans la zone d'effet testé
        @type: Personnage
        @joueurCibleDirect: Le joueur sur lequel l'effet est lancé
                            à la base (peut-être identique à joueurCible.
        @type: Personnage ou None
        @ciblesDejaTraitees: Les cibles déjà touchées par l'effet
        @type: tableau de Personnage
        @return: booléen indiquant vrai si la cible est valide, faux sinon"""

        # Test si la cible est dans les cibles possibles
        msg = ""
        if joueurCible is None:
            joueurCibleTeam = -1
            joueurCibleUid = -1
            joueurCibleClasse = ""
            joueurCibleInvocateur = ""
        else:
            joueurCibleTeam = joueurCible.team
            joueurCibleUid = joueurCible.uid
            joueurCibleClasse = joueurCible.classe
            joueurCibleInvocateur = joueurCible.invocateur
        if (joueurCibleTeam == joueurLanceur.team and joueurCibleUid != joueurLanceur.uid
                and "Allies" in self.ciblesPossibles) \
            or (joueurCibleTeam == joueurLanceur.team and joueurCibleUid == joueurLanceur.uid
                and "Lanceur" in self.ciblesPossibles) \
            or (joueurCibleTeam != joueurLanceur.team and "Ennemis" in self.ciblesPossibles) \
            or (joueurCibleClasse in self.ciblesPossibles) \
            or (joueurCibleInvocateur is not None and "Invoc" in self.ciblesPossibles) \
            or (joueurLanceur.invocateur is not None and "Invocateur" in self.ciblesPossibles
                and joueurCibleUid == joueurLanceur.invocateur.uid):
            # Test si la cible est exclue
            if joueurCibleClasse in self.ciblesExclues \
               or (joueurCibleUid == joueurLanceur.uid and "Lanceur" in self.ciblesExclues) \
               or (joueurCibleInvocateur is not None and "Invoc" in self.ciblesExclues) \
               or (joueurLanceur.invocateur is not None and "Invocateur" in self.ciblesExclues
                       and joueurCibleUid == joueurLanceur.invocateur.uid):
                if joueurCibleClasse != "":
                    msg = "DEBUG : Invalide : Cible Exclue "+\
                        str(joueurCibleClasse)+"/"+str(self.ciblesExclues)
                    return msg, False
            # Test si la cible est déjà traitée
            if joueurCible in ciblesDejaTraitees:
                msg = "DEBUG : Invalide : Cible deja traitee "+\
                    str(joueurCible) + str(ciblesDejaTraitees)
                return msg, False
            # Test si la cible est une case vide et que l'effet ne nécessite pas d'etat pour la cibl
            # une liste est vraie si elle n'est pas vide
            if joueurCible is None and self.etatRequisCibles:
                msg = "DEBUG : Invalide : Cible  non renseigne et etatRequis pour cible"
                return msg, False
            # Test si la cible n'est pas une case vide qu'il a bien les états requis
            if joueurCible is not None:
                if not joueurCible.aEtatsRequis(self.etatRequisCibles):
                    msg = "DEBUG : Invalide :etatRequis pour cible non present"
                    return msg, False

            # La cible a passé tous les tests
            return msg, True
        msg = "DEBUG : Invalide : Cible "+ joueurCibleClasse + \
                " pas dans la liste des cibles possibles ("+str(self.ciblesPossibles)+")"
        return msg, False

    def aPorteZone(self, departZoneX, departZoneY, testDansZoneX, testDansZoneY, joueurX, joueurY):
        """@summary: Test si une case appartient à une zone donnée.
                     Wrapper pour la fonction testCaseEstDedans polymorphique.
        @departZoneX: L'abcisse de la case de départ de la zone,
                      souvent le centre et souvent le centre de l'effet
        @type: int
        @departZoneY: L'ordonnée de la case de départ de la zone,
                      souvent le centre et souvent le centre de l'effet
        @type: int
        @testDansZoneX: L'abcisse de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @testDansZoneY: L'ordonnée de la case dont ou souhait savoir si elle est dans la zone'
        @type: int
        @joueurX: L'abcisse de la case sur laquelle le joueur lançant l'effet se trouve.
                  Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @joueurY: L'ordonnée de la case sur laquelle le joueur lançant l'effet se trouve.
                  Utile pour certaines zones dépendants de la position du lanceur.
        @type: int
        @return: booléen indiquant vrai si la case testée est dans la zone, faux sinon"""

        # Le lanceur peut pas etre dans la zone si y a le - a la fin du type zone
        toRet = self.typeZone.testCaseEstDedans([departZoneX, departZoneY],
                                                [testDansZoneX, testDansZoneY],
                                                [joueurX, joueurY])
        return toRet

    def appliquerEffet(self, niveau, joueurCaseEffet, joueurLanceur, **kwargs):
        # pylint: disable=unused-argument
        """@summary: Applique les modifications sur le jeu créées par l'effet.
        @niveau: la grille de simulation de combat.
        @type: Niveau
        @joueurCaseEffet: Le joueur sur se tenant sur une case de la zone d'effet traitée.
        @type: Personnage
        @joueurLanceur: Le joueur ayant lancé l'effet
        @type: Personnage
        @kwargs: Les paramètres optionnels supplémentaires pour chaque effet.s
        @type: **kwargs"""

        # Comportement neutre non défini
        niveau.ajoutFileEffets(self)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # pylint: disable=unused-argument
        """@summary: activer un effet. Appeler dans Niveau.depileEffets"""
        print("Activation non définie")

    def afficher(self):
        """@summary: Affiche un effet dans la console (DEBUG)"""
        print("Effet etatRequis:"+self.etatRequisCibleDirect +
              " consommeEtat:"+str(self.consommeEtat) +
              " ciblesPossibles:"+str(self.ciblesPossibles) +
              " cibles_exclues:"+str(self.ciblesExclues))

class EffetToDo(Effet):
    def __init__(self, effectStr, **kwargs):
        self.kwargs = kwargs
        self.effectStr = effectStr

    def __deepcopy__(self, memo):
        """
        @summary: implémente une copie profonde de l'état
        @return: Renvoie une copie profonde exacte de l'effet
        """
        return EffetToDo(self.effectStr, **self.kwargs)

    def __str__(self):
        return "TODO : "+str(self.effectStr)

    @classmethod
    def isAffected(cls, effectStr, **kwargs):
        return False

    @classmethod
    def craftEffect(cls, effectStr, **kwargs):
        return EffetToDo(effectStr, **kwargs)
    
    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["effectStr"] = self.effectStr
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetToDo(infos["effectStr"], **infos["kwargs"])

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        effetLbl = ttk.Label(frame, text="TODO:")
        effetLbl.pack(side="left")
        effetEntry = ttk.Entry(frame, width=100)
        effetEntry.delete(0, 'end')
        effetEntry.insert(0, self.effectStr)
        effetEntry.pack(side="left")
        frame.pack()
        return ret
    
class ChildDialogEffect:
    """
    Open a child dialog of a tkinter application to fill effects
    """
    def __init__(self, parent, effect=None):
        """
        Open a child dialog of a tkinter application to edit an effect.

        Args:
            parent: the tkinter parent view to use for this window construction.
            effect: Effect to edit.
        """
        self.parent = parent
        self.app = tk.Toplevel(parent)
        self.app.resizable(False, False)
        self.rvalue = None
        self.parent = parent
        self.effect = effect if effect is not None else Effet()
        self.initUI(self.effect)
        try:
            self.app.wait_visibility()
            self.app.transient(parent)
            self.app.grab_set()
        except tk.TclError:
            pass

    def effectTypeModified(self, _event=None):
        for widget in self.effectFrame.winfo_children():
            widget.destroy()
        if self.effect.__class__.__name__.replace("Effet", "") == self.typeEffetCombobox.get():
            self.effectWidgets = self.effect.buildUI(self.effectFrame, self.callbackModifiedVal)
        else:
            typeEffet = self.typeEffetCombobox.get()
            effect = Effet.getObjectFromName(typeEffet)
            self.effectWidgets = effect.buildUI(self.effectFrame, self.callbackModifiedVal)
            self.effect = effect

    def callbackModifiedVal(self, modifiedValue):
        for effetWidget_key, effetWidget_val in modifiedValue.items():
            self.effectWidgets[effetWidget_key] = effetWidget_val
        
    
    def initUI(self, effect):
        appFrame = ttk.Frame(self.app)
        typeEffetFrame = ttk.Frame(appFrame)
        typeEffetLbl = ttk.Label(typeEffetFrame, text="Effet :")
        typeEffetLbl.pack(side="left")
        self.typeEffetCombobox = ttk.Combobox(typeEffetFrame, values=sorted(Effet.getEffectList()), state="readonly")
        self.typeEffetCombobox.set(effect.__class__.__name__.replace("Effet", ""))
        self.typeEffetCombobox.bind('<<ComboboxSelected>>', self.effectTypeModified) 
        self.typeEffetCombobox.pack(side="left")
        typeZoneLbl = ttk.Label(typeEffetFrame, text="Zone :")
        typeZoneLbl.pack(side="left")
        self.typeZoneCombobox = ttk.Combobox(typeEffetFrame, values=sorted(Zones.TypeZone.getZoneList()), state="readonly")
        self.typeZoneCombobox.pack(side="left")
        if effect.kwargs.get("zone", None) is not None:
            self.typeZoneCombobox.set(effect.kwargs.get("zone").__class__.__name__.replace("TypeZone", ""))
        else:
            self.typeZoneCombobox.set(effect.kwargs.get("typeZone", "Cercle"))
        self.tailleZoneSpinbox = tk.Spinbox(typeEffetFrame, from_=0, to=99, width=3)
        self.tailleZoneSpinbox.delete(0, 'end')
        if effect.kwargs.get("zone", None) is not None:
            self.tailleZoneSpinbox.insert(0, int(effect.kwargs.get("zone").zonePO))
        else:
            self.tailleZoneSpinbox.insert(0, int(effect.kwargs.get("tailleZone", 0)))
        self.tailleZoneSpinbox.pack(side="left")
        typeEffetFrame.pack(side="top", fill=tk.X)

        self.effectFrame = ttk.LabelFrame(appFrame, text="Caractéristiques de l'effet")
        self.effectTypeModified()
        self.effectFrame.pack(side="top", fill=tk.X)

        etatsFrame = ttk.LabelFrame(appFrame, text="Etats")
        helpStr = ttk.Label(etatsFrame, text="Utilisez le pipe '|' comme séparateur. Le '!' devant un état pour l'interdire.")
        helpStr.grid(row=0, column=0, columnspan=2)
        etatCibleDirectLbl = ttk.Label(etatsFrame, text="Condition état sur la cible:")
        etatCibleDirectLbl.grid(row=1, column=0, sticky="e")
        self.etatCibleDirectEntry = ttk.Entry(etatsFrame, width=100)
        self.etatCibleDirectEntry.grid(row=1, column=1, sticky="w")
        self.etatCibleDirectEntry.insert(0, effect.kwargs.get("etat_requis", ""))
        etatCibleLbl = ttk.Label(etatsFrame, text="Condition état requis sur les cibles en zone:")
        etatCibleLbl.grid(row=2, column=0, sticky="e")
        self.etatCibleEntry = ttk.Entry(etatsFrame, width=100)
        self.etatCibleEntry.grid(row=2, column=1, sticky="w")
        self.etatCibleEntry.insert(0, effect.kwargs.get("etat_requis_cibles", ""))
        etatLanceurLbl = ttk.Label(etatsFrame, text="Condition état requis sur le lanceur:")
        etatLanceurLbl.grid(row=3, column=0, sticky="e")
        self.etatLanceurEntry = ttk.Entry(etatsFrame, width=100)
        self.etatLanceurEntry.grid(row=3, column=1, sticky="w")
        self.etatLanceurEntry.insert(0, effect.kwargs.get("etat_requis_lanceur", ""))
        consommeEtatLbl = ttk.Label(etatsFrame, text="Consomme les états requis:")
        consommeEtatLbl.grid(row=4, column=0)
        self.consommeVar = tk.BooleanVar()
        self.consommeVar.set(effect.kwargs.get("consomme_etat", False))
        consommeEtatCheckbutton = ttk.Checkbutton(etatsFrame, variable=self.consommeVar)
        consommeEtatCheckbutton.grid(row=4, column=1, sticky="w")
        etatsFrame.pack(side="top", fill=tk.X)

        ciblesFrame = ttk.LabelFrame(appFrame, text="Cibles")
        cibleRequiseLbl = ttk.Label(ciblesFrame, text="Cible requise:")
        cibleRequiseLbl.grid(row=0, column=0, sticky="e")
        self.cibleRequiseVar = tk.BooleanVar()
        self.cibleRequiseVar.set(not effect.kwargs.get("cible_non_requise", False))
        cibleRequiseCheckbutton = ttk.Checkbutton(ciblesFrame, variable=self.cibleRequiseVar)
        cibleRequiseCheckbutton.grid(row=0, column=1, sticky="w")
        ciblesPossiblesDirectLbl = ttk.Label(ciblesFrame, text="Cible Direct doit être:")
        ciblesPossiblesDirectLbl.grid(row=1, column=0, sticky="e")
        self.ciblesPossiblesDirectEntry = ttk.Entry(ciblesFrame, width=100)
        self.ciblesPossiblesDirectEntry.grid(row=1, column=1, sticky="w")
        self.ciblesPossiblesDirectEntry.insert(tk.END, effect.kwargs.get("cibles_possibles_direct", "Allies|Ennemis|Lanceur"))
        ciblesPossiblesDirectHelpLbl = ttk.Label(ciblesFrame, text="(Defaut = cible affectées)")
        ciblesPossiblesDirectHelpLbl.grid(row=1, column=2)
        ciblesPossiblesLbl = ttk.Label(ciblesFrame, text="Cible Affectés:")
        ciblesPossiblesLbl.grid(row=2, column=0, sticky="e")
        self.ciblesPossiblesEntry = ttk.Entry(ciblesFrame, width=100)
        self.ciblesPossiblesEntry.grid(row=2, column=1, sticky="w")
        self.ciblesPossiblesEntry.insert(tk.END, effect.kwargs.get("cibles_possibles", "Allies|Ennemis|Lanceur"))
        ciblesPossiblesHelpLbl = ttk.Label(ciblesFrame, text="(Allies, Ennemis, Lanceur, nom de classe, Invoc)")
        ciblesPossiblesHelpLbl.grid(row=2, column=2)
        ciblesExcluesLbl = ttk.Label(ciblesFrame, text="Cibles exclues:")
        ciblesExcluesLbl.grid(row=3, column=0, sticky="e")
        self.ciblesExcluesEntry = ttk.Entry(ciblesFrame, width=100)
        self.ciblesExcluesEntry.grid(row=3, column=1, sticky="w")
        self.ciblesExcluesEntry.insert(tk.END, effect.kwargs.get("cibles_exclues", ""))
        ciblesExcluesHelpLbl = ttk.Label(ciblesFrame, text="(Lanceur, nom de classe, Invocateur, Invoc)")
        ciblesExcluesHelpLbl.grid(row=3, column=2)
        ciblesFrame.pack(side="top", fill=tk.X)
        nonpileFrame = ttk.Frame(appFrame)
        nonpileLbl = ttk.Label(nonpileFrame, text="Résoudre immédiatement:")
        nonpileLbl.pack(side="left")
        self.nonpileVar = tk.BooleanVar()
        self.nonpileVar.set(not effect.kwargs.get("pile", True))
        nonpileCheckbutton = ttk.Checkbutton(nonpileFrame, variable=self.nonpileVar)
        nonpileCheckbutton.pack(side="left")
        reverseTreatmentOrderLbl = ttk.Label(nonpileFrame, text="Effet appliqué ext. vers int.:")
        reverseTreatmentOrderLbl.pack(side="left")
        self.reverseTreatmentOrderVar = tk.BooleanVar()
        self.reverseTreatmentOrderVar.set(effect.kwargs.get("reverseTreatmentOrder", False))
        reverseTreatmentOrderCheckbutton = ttk.Checkbutton(nonpileFrame, variable=self.reverseTreatmentOrderVar)
        reverseTreatmentOrderCheckbutton.pack(side="left")
        nonpileFrame.pack(side="top")
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.pack(pady=10)
        appFrame.pack(ipadx=10, ipady=10)

    def setAttributesWithWidgetDict(self, obj, widgets):
        for attr_name, widget in widgets.items():
            if attr_name.startswith("kwargs:"):
                obj.kwargs[attr_name.replace("kwargs:", "")] = widget.get()
            else:
                if isinstance(widget, dict):
                    sub_object = getattr(obj, attr_name)
                    self.setAttributesWithWidgetDict(sub_object, widget)
                else:
                    try:
                        attr_value = widget.get()
                    except AttributeError: #was not a widget
                        attr_value = widget
                    setattr(obj, attr_name, attr_value)

    def onOk(self):
        """
        Called when the user clicked the validation button.
        """
        typeEffet = self.typeEffetCombobox.get()
        self.setAttributesWithWidgetDict(self.effect, self.effectWidgets)
        self.effect.kwargs["typeZone"] = self.typeZoneCombobox.get()
        self.effect.kwargs["tailleZone"] = self.tailleZoneSpinbox.get()
        if self.effect.kwargs.get("zone", None) is not None:
            self.effect.kwargs.remove("zone")
        self.effect.kwargs["etat_requis"] = self.etatCibleDirectEntry.get()
        self.effect.kwargs["etat_requis_cibles"] = self.etatCibleEntry.get()
        self.effect.kwargs["etat_requis_lanceur"] = self.etatLanceurEntry.get()
        self.effect.kwargs["consomme_etat"] = self.consommeVar.get()
        self.effect.kwargs["cible_non_requise"] = not self.cibleRequiseVar.get()
        self.effect.kwargs["cibles_possibles"] = self.ciblesPossiblesEntry.get()
        self.effect.kwargs["cibles_possibles_direct"] = self.ciblesPossiblesDirectEntry.get()
        self.effect.kwargs["cibles_exclues"] = self.ciblesExcluesEntry.get()
        self.effect.kwargs["pile"] = not self.nonpileVar.get()
        self.rvalue = self.effect
        self.app.destroy()