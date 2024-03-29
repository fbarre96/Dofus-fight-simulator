"""@summary: Décrit un effet de sort appliquant un état à un joueur. """

from copy import deepcopy
from Effets.Effet import Effet
from Etats.Etat import Etat

class EffetEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet applique un état à la cible."""

    def buildUI(self, topframe, callbackMod):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        self.callbackMod = callbackMod
        frame = ttk.Frame(topframe)
        typeEtatLbl = ttk.Label(frame, text="Type d'état:")
        typeEtatLbl.pack(side="left")
        self.typeEtatCombobox = ttk.Combobox(frame, values=sorted(Etat.getListEtat()), state="readonly")
        self.typeEtatCombobox.set(self.etat.__class__.__name__)
        self.typeEtatCombobox.pack(side="left")
        self.typeEtatCombobox.bind('<<ComboboxSelected>>', self.etatTypeModified) 
        self.etatCaracsFrame = ttk.LabelFrame(frame, text="Caractéristiques de l'état")
        self.etatCaracsFrame.pack(side="top")
        self.etatTypeModified()
        etatOptionFrame = ttk.Frame(frame)
        cumulMaxLbl = ttk.Label(etatOptionFrame, text="Cumul max:")
        cumulMaxLbl.grid(row=0, column=0, sticky="e")
        cumulMaxSpinbox = tk.Spinbox(etatOptionFrame, from_=-1, to=99, width=3)
        cumulMaxSpinbox.delete(0, 'end')
        cumulMaxSpinbox.insert(0, int(self.kwargs.get("cumulMax", -1)))
        cumulMaxSpinbox.grid(row=0, column=1, sticky="w")
        ret["kwargs:cumulMax"] = cumulMaxSpinbox
        remplaceNomLbl = ttk.Label(etatOptionFrame, text="Remplace le nom de l'état par le nom du sort:")
        remplaceNomLbl.grid(row=1, column=0, sticky="e")
        remplaceNomVar = tk.BooleanVar()
        remplaceNomVar.set(self.kwargs.get("remplaceNom", False))
        replaceNomCheckbutton = ttk.Checkbutton(etatOptionFrame, variable=remplaceNomVar)
        replaceNomCheckbutton.grid(row=1, column=1, sticky="w")
        ret["kwargs:remplaceNom"] = remplaceNomVar
        ret["etat"] = self.etatWidgets
        etatOptionFrame.pack(side="bottom")
        frame.pack()
        return ret
    
    def __str__(self):
        return "Etat "+str(self.etat)
    
    def callbackModifiedRetValue(self, newDict):
        for etatWidget_key, etatWidget_val in newDict.items():
            self.etatWidgets[etatWidget_key] = etatWidget_val
        self.callbackMod({"etat":self.etatWidgets})
   
    def etatTypeModified(self, _event=None):
        for widget in self.etatCaracsFrame.winfo_children():
            widget.destroy()
        if self.etat.__class__.__name__ == self.typeEtatCombobox.get():
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val
        else:
            typeEtat = self.typeEtatCombobox.get()
            etat = Etat.getObjectFromName(typeEtat)
            etat.nom = self.etat.nom
            etat.debuteDans = self.etat.debuteDans
            etat.duree = self.etat.duree
            self.etat = etat
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["etat"] = self.etat.getAllInfos()
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetEtat(Etat.factory(infos["etat"]), **infos["kwargs"])

    def __init__(self, etat_etat=None, **kwargs):
        """@summary: Initialise un effet appliquant un état.
        @etat_etat: l'état qui va être appliqué
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.etatWidgets = {}
        if etat_etat is not None:
            self.etat = etat_etat
        else:
            self.etat = Etat("TODO", 0, 1)
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtat(deepcopy(self.etat), **self.kwargs)

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
        if joueurCaseEffet is not None:
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        # On copie l'état parce que l'effet peut être appliquer plusieurs fois.
        etatCopier = deepcopy(self.etat)
        return joueurCaseEffet.appliquerEtat(etatCopier, joueurLanceur,
                                             int(self.kwargs.get("cumulMax", -1)), niveau)

class EffetEtatSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet place un état sur le lanceur."""
    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        typeEtatLbl = ttk.Label(frame, text="Type d'état:")
        typeEtatLbl.pack(side="left")
        self.typeEtatCombobox = ttk.Combobox(frame, values=sorted(Etat.getListEtat()), state="readonly")
        self.typeEtatCombobox.set(self.etat.__class__.__name__)
        self.typeEtatCombobox.pack(side="left")
        self.typeEtatCombobox.bind('<<ComboboxSelected>>', self.etatTypeModified) 
        self.etatCaracsFrame = ttk.LabelFrame(frame, text="Caractéristiques de l'état")
        self.etatCaracsFrame.pack(side="top")
        self.etatTypeModified()
        etatOptionFrame = ttk.Frame(frame)
        cumulMaxLbl = ttk.Label(etatOptionFrame, text="Cumul max:")
        cumulMaxLbl.grid(row=0, column=0, sticky="e")
        cumulMaxSpinbox = tk.Spinbox(etatOptionFrame, from_=-1, to=99, width=3)
        cumulMaxSpinbox.delete(0, 'end')
        cumulMaxSpinbox.insert(0, int(self.kwargs.get("cumulMax", -1)))
        cumulMaxSpinbox.grid(row=0, column=1, sticky="w")
        ret["kwargs:cumulMax"] = cumulMaxSpinbox
        ret["etat"] = self.etatWidgets
        etatOptionFrame.pack(side="bottom")
        frame.pack()
        return ret
    
    def __str__(self):
        return "EtatSelf "+str(self.etat)

    def callbackModifiedRetValue(self, newDict):
        for etatWidget_key, etatWidget_val in newDict.items():
            self.etatWidgets[etatWidget_key] = etatWidget_val
    
    def etatTypeModified(self, _event=None):
        for widget in self.etatCaracsFrame.winfo_children():
            widget.destroy()
        if self.etat.__class__.__name__ == self.typeEtatCombobox.get():
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val
        else:
            typeEtat = self.typeEtatCombobox.get()
            etat = Etat.getObjectFromName(typeEtat)
            etat.nom = self.etat.nom
            etat.debuteDans = self.etat.debuteDans
            etat.duree = self.etat.duree
            self.etat = etat
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["etat"] = self.etat.getAllInfos()
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetEtatSelf(Etat.factory(infos["etat"]), **infos["kwargs"])

    def __init__(self, etat_etat=None, **kwargs):
        """@summary: Initialise un effet placant un état sur le lanceur
        @etat_etat: l'état à placer sur le lanceur
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.etatWidgets = {}
        if etat_etat is not None:
            self.etat = etat_etat
        else:
            self.etat = Etat("TODO", 0, 1)
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtatSelf(deepcopy(self.etat), **self.kwargs)

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
        if joueurCaseEffet is None:
            return
        etatCopie = deepcopy(self.etat)
        return joueurLanceur.appliquerEtat(etatCopie, joueurLanceur,
                                           self.kwargs.get("cumulMax", -1), niveau)

class EffetEtatSelfTF(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet place un état sur le lanceur portant le nom du sort à l'origine d'un TF."""

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        typeEtatLbl = ttk.Label(frame, text="Type d'état:")
        typeEtatLbl.pack(side="left")
        self.typeEtatCombobox = ttk.Combobox(frame, values=sorted(Etat.getListEtat()), state="readonly")
        self.typeEtatCombobox.set(self.etat.__class__.__name__)
        self.typeEtatCombobox.pack(side="left")
        self.typeEtatCombobox.bind('<<ComboboxSelected>>', self.etatTypeModified) 
        self.etatCaracsFrame = ttk.LabelFrame(frame, text="Caractéristiques de l'état")
        self.etatCaracsFrame.pack(side="top")
        self.etatTypeModified()
        etatOptionFrame = ttk.Frame(frame)
        cumulMaxLbl = ttk.Label(etatOptionFrame, text="Cumul max:")
        cumulMaxLbl.grid(row=0, column=0, sticky="e")
        cumulMaxSpinbox = tk.Spinbox(etatOptionFrame, from_=-1, to=99, width=3)
        cumulMaxSpinbox.delete(0, 'end')
        cumulMaxSpinbox.insert(0, int(self.kwargs.get("cumulMax", -1)))
        cumulMaxSpinbox.grid(row=0, column=1, sticky="w")
        sortsExclusLbl = ttk.Label(frame, text="Sorts exclus:")
        sortsExclusLbl.pack(side="left")
        sortsExclusEntry = ttk.Entry(frame, width=30)
        sortsExclusEntry.delete(0, 'end')
        sortsExclusEntry.insert(0, self.sortsExclus)
        sortsExclusEntry.pack(side="left")
        remplaceNomFrame = ttk.Frame(frame)
        remplaceNomLbl = ttk.Label(remplaceNomFrame, text="Remplace le nom de l'état par le sort:")
        remplaceNomLbl.pack(side="left")
        remplaceNomVar = tk.BooleanVar()
        remplaceNomVar.set(self.kwargs.get("kwargs:remplaceNom", True))
        remplaceNomCheckbutton = ttk.Checkbutton(remplaceNomFrame, variable=remplaceNomVar)
        remplaceNomCheckbutton.pack(side="left")
        remplaceNomFrame.pack(side="bottom")
        ret["sortsExclus"] = sortsExclusEntry
        ret["kwargs:cumulMax"] = cumulMaxSpinbox
        ret["kwargs:remplaceNom"] = remplaceNomVar
        ret["etat"] = self.etatWidgets
        etatOptionFrame.pack(side="bottom")
        frame.pack()
        return ret
    
    def __str__(self):
        return "EtatSelfTF "+str(self.etat)

    def callbackModifiedRetValue(self, newDict):
        for etatWidget_key, etatWidget_val in newDict.items():
            self.etatWidgets[etatWidget_key] = etatWidget_val
    
    def etatTypeModified(self, _event=None):
        for widget in self.etatCaracsFrame.winfo_children():
            widget.destroy()
        if self.etat.__class__.__name__ == self.typeEtatCombobox.get():
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val
        else:
            typeEtat = self.typeEtatCombobox.get()
            etat = Etat.getObjectFromName(typeEtat)
            etat.nom = self.etat.nom
            etat.debuteDans = self.etat.debuteDans
            etat.duree = self.etat.duree
            self.etat = etat
            self.etatWidgets.clear()
            new_etatWidgets = self.etat.buildUI(self.etatCaracsFrame, self.callbackModifiedRetValue)
            for etatWidget_key, etatWidget_val in new_etatWidgets.items():
                self.etatWidgets[etatWidget_key] = etatWidget_val

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["etat"] = self.etat.getAllInfos()
        ret["sortsExclus"] = self.sortsExclus
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetEtatSelfTF(Etat.factory(infos["etat"]), infos["sortsExclus"], **infos["kwargs"])

    def __init__(self, etat_etat=None, sortsExclus="", **kwargs):
        """@summary: Initialise un effet placant un état sur le lanceur
        @etat_etat: l'état à placer sur le lanceur
        @type: Etat
        @kwargs: Options de l'effets
        @type: **kwargs"""
        if etat_etat is not None:
            self.etat = etat_etat
        else:
            self.etat = Etat("TODO", 0, 1)
        self.etatWidgets = {}
        self.sortsExclus = sortsExclus
        self.kwargs = kwargs
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetEtatSelfTF(deepcopy(self.etat), self.sortsExclus, **self.kwargs)

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
        nomSort = self.getNomSortTF()
        if nomSort in self.sortsExclus:
            return False
        etatCopier = deepcopy(self.etat)
        if self.kwargs.get("remplaceNom", True):
            etatCopier.nom = nomSort
        return joueurLanceur.appliquerEtat(etatCopier, joueurLanceur,
                                           self.kwargs.get("cumulMax", -1), niveau)


class EffetRafraichirEtats(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet change la durée des états de la cible."""

    def __init__(self, int_deXTours=1, **kwargs):
        """@summary: Initialise un effet changeant la durée des états de la cible
        @int_deXTours: le nombre de tour qui vont être additionés (dans Z)
                       à chaque état de la cible.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.deXTours = int_deXTours
        super().__init__(**kwargs)

    def __str__(self):
        return "-"+str(self.deXTours)+" à la durée des états"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nbTourLbl = ttk.Label(frame, text="Retire à la durée des états:")
        nbTourLbl.pack(side="left")
        nbTourSpinbox = tk.Spinbox(frame, from_=1, to=99999, width=5)
        nbTourSpinbox.delete(0, 'end')
        nbTourSpinbox.insert(0, int(self.deXTours))
        nbTourSpinbox.pack(side="left")
        ret["deXTours"] = nbTourSpinbox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["deXTours"] = self.deXTours
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(int(infos["deXTours"]), **infos["kwargs"])


    def __deepcopy__(self, memo):
        return EffetRafraichirEtats(self.deXTours, **self.kwargs)

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
        joueurCaseEffet.changeDureeEffets(self.deXTours, niveau)


class EffetSetDureeEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet set la durée des états de la cible."""

    def __init__(self, nomEtat="", nouveauDebut=0, nouvelleDuree=1, **kwargs):
        """@summary: Initialise un effet changeant la durée des états de la cible
        @int_deXTours: le nombre de tour qui vont être additionés (dans Z)
                       à chaque état de la cible.
        @type: int
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = nomEtat
        self.nouveauDebut = nouveauDebut
        self.nouvelleDuree = nouvelleDuree
        super().__init__(**kwargs)

    def __str__(self):
        return "Modifie la durée de l'état "+str(self.nomEtat)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomEtatLbl = ttk.Label(frame, text="Nom état à modifier:")
        nomEtatLbl.pack(side="left")
        nomEtatEntry = ttk.Entry(frame, width=30)
        nomEtatEntry.delete(0, 'end')
        nomEtatEntry.insert(0, self.nomEtat)
        nomEtatEntry.pack(side="left")
        ret["nomEtat"] = nomEtatEntry
        nouveauDebutLbl = ttk.Label(frame, text="Nouveau début:")
        nouveauDebutLbl.pack(side="left")
        nouveauDebutSpinbox = tk.Spinbox(frame, from_=0, to=999, width=3)
        nouveauDebutSpinbox.delete(0, 'end')
        nouveauDebutSpinbox.insert(0, int(self.nouveauDebut))
        nouveauDebutSpinbox.pack(side="left")
        ret["nouveauDebut"] = nouveauDebutSpinbox
        nouvelleDureeLbl = ttk.Label(frame, text="Nouvelle durée:")
        nouvelleDureeLbl.pack(side="left")
        nouvelleDureeSpinbox = tk.Spinbox(frame, from_=0, to=999, width=3)
        nouvelleDureeSpinbox.delete(0, 'end')
        nouvelleDureeSpinbox.insert(0, int(self.nouvelleDuree))
        nouvelleDureeSpinbox.pack(side="left")
        ret["nouvelleDuree"] = nouvelleDureeSpinbox
       
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomEtat"] = self.nomEtat
        ret["nouveauDebut"] = self.nouveauDebut
        ret["nouvelleDuree"] = self.nouvelleDuree
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["nomEtat"], int(infos["nouveauDebut"]), int(infos["nouvelleDuree"]), **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetSetDureeEtat(self.nomEtat, self.nouveauDebut, self.nouvelleDuree, **self.kwargs)

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
        for etat in joueurCaseEffet.etats:
            if etat.actif() and etat.nom == self.nomEtat:
                etat.debuteDans = self.nouveauDebut
                etat.duree = self.nouvelleDuree


class EffetRetireEtat(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire les états de la cible qui portent un nom donné."""

    def __init__(self, str_nomEtat="", **kwargs):
        """@summary: Initialise un effet retirant les états de la cible selon un paramètre donné.
        @str_nomEtat: le nom de l'état qui va être retiré de la cible.
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = str_nomEtat
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetRetireEtat(self.nomEtat, **self.kwargs)

    def __str__(self):
        return "Retire état "+str(self.nomEtat)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomLbl = ttk.Label(frame, text="Nom état à retirer:")
        nomLbl.pack(side="left")
        nomEntry = ttk.Entry(frame, width=50)
        nomEntry.delete(0, 'end')
        nomEntry.insert(0, self.nomEtat)
        nomEntry.pack(side="left")
        ret["nomEtat"] = nomEntry
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomEtat"] = self.nomEtat
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetRetireEtat(infos["nomEtat"], **infos["kwargs"])


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
        if joueurCaseEffet is not None:
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.retirerEtats(niveau, self.nomEtat)

class EffetRetireEtatSelf(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet retire les états de la cible qui portent un nom donné."""

    def __init__(self, str_nomEtat="", **kwargs):
        """@summary: Initialise un effet retirant les états de la cible selon un paramètre donné.
        @str_nomEtat: le nom de l'état qui va être retiré de la cible.
        @type: str
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.nomEtat = str_nomEtat
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetRetireEtatSelf(self.nomEtat, **self.kwargs)

    def __str__(self):
        return "Retire état du lanceur "+str(self.nomEtat)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomLbl = ttk.Label(frame, text="Nom état à retirer:")
        nomLbl.pack(side="left")
        nomEntry = ttk.Entry(frame, width=50)
        nomEntry.delete(0, 'end')
        nomEntry.insert(0, self.nomEtat)
        nomEntry.pack(side="left")
        ret["nomEtat"] = nomEntry
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nomEtat"] = self.nomEtat
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetRetireEtatSelf(infos["nomEtat"], **infos["kwargs"])

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
        if joueurLanceur is not None:
            if self.pile:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
            else:
                self.activerEffet(niveau, joueurCaseEffet, joueurLanceur)

    def activerEffet(self, niveau, joueurCaseEffet, joueurLanceur):
        if joueurCaseEffet is not None:
            joueurCaseEffet.retirerEtats(niveau, self.nomEtat)


class EffetEtatSelonVie(EffetEtat):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    lance un etat si les degats subits sont dans un seuil précis
    DOIT AVOIR UN SETTER DEGATS SUBITS ."""

    def __init__(self, etat_etat=None, pourcentage_seuil_min=0, pourcentage_seuil_max=0, **kwargs):
        """@summary: Initialise un effet qui lance un etat selon les degats subits
        @pourcentage_seuil_min: le pourcentage de la vie min qui déclenche l'effet
        @type: int (1 à 100)
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.pourcentage_seuil_min = pourcentage_seuil_min
        self.pourcentage_seuil_max = pourcentage_seuil_max
        super().__init__(etat_etat, **kwargs)

    def __deepcopy__(self, memo):
        cpy = EffetEtatSelonVie(deepcopy(self.etat), self.pourcentage_seuil_min, self.pourcentage_seuil_max, **self.kwargs)
        return cpy

    def __str__(self):
        return "Applique l'etat "+str(self.etat)+" si la vie de l'utilisateur est entre "+str(self.pourcentage_seuil_min)+ " et "+str(self.pourcentage_seuil_max)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = super().buildUI(topframe, callbackDict)
        frame = ttk.Frame(topframe)
        pourcentageMinLbl = ttk.Label(frame, text="Pourcentage seuil min:")
        pourcentageMinLbl.pack(side="left")
        pourcentageMinSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        pourcentageMinSpinbox.delete(0, 'end')
        pourcentageMinSpinbox.insert(0, int(self.pourcentage_seuil_min))
        pourcentageMinSpinbox.pack(side="left")
        ret["pourcentage_seuil_min"] = pourcentageMinSpinbox
        pourcentageMaxLbl = ttk.Label(frame, text="Pourcentage seuil max:")
        pourcentageMaxLbl.pack(side="left")
        pourcentageMaxSpinbox = tk.Spinbox(frame, from_=0, to=100, width=3)
        pourcentageMaxSpinbox.delete(0, 'end')
        pourcentageMaxSpinbox.insert(0, int(self.pourcentage_seuil_max))
        pourcentageMaxSpinbox.pack(side="left")
        ret["pourcentage_seuil_max"] = pourcentageMaxSpinbox
        frame.pack()
        return ret
    
    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["pourcentage_seuil_min"] = self.pourcentage_seuil_min
        ret["pourcentage_seuil_max"] = self.pourcentage_seuil_max
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(Etat.factory(infos["etat"]), int(infos["pourcentage_seuil_min"]),int(infos["pourcentage_seuil_max"]), **infos["kwargs"])


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
            pourcentage_vie = (joueurCaseEffet.vie / joueurCaseEffet.vieMax)*100
            if  pourcentage_vie >= self.pourcentage_seuil_min and pourcentage_vie <= self.pourcentage_seuil_max:
                niveau.ajoutFileEffets(self, joueurCaseEffet, joueurLanceur)
