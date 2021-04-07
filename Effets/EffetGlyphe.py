"""@summary: Rassemble les effets de sort en rapport avec les glyphes."""

from Effets.Effet import Effet
from Glyphe import Glyphe
from Zones import TypeZone

class EffetGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une glyphe sur la grille de jeu."""

    def __init__(self, typeZoneStr="cercle", tailleZoneGlyphe=0, nomSortEntre="", nomSortDeplacement="", nomSortSortie="", int_duree=1,
                 str_nom="", couleur_r=0, couleur_g=0, couleur_b=0, **kwargs):
        """@summary: Initialise un effet posant une glyphe.
        @sort_sort: le sort monocible qui est lancé sur les joueurs restants dans la glyphe
        @type: Sort
        @sortDeplacement: Le sort monocible qui est lancé sur les joueurs entrants dans la glyphe
        @type: Sort
        @sortSortie: Le sort monocible qui est lancé sur les joueurs sortants de la glyphe
        @type: Sort
        @int_duree: le nombre de tour où la glyphe sera active
        @type: int
        @str_nom: le nom de la glyphe
        @type: string
        @tuple_couleur: la couleur de la glyphe
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.typeZoneStr = typeZoneStr
        self.tailleZoneGlyphe = tailleZoneGlyphe
        self.kwargs = kwargs
        self.nomSortEntre = nomSortEntre
        self.nomSortDeplacement = nomSortDeplacement
        self.nomSortSortie = nomSortSortie
        self.duree = int_duree
        self.nom = str_nom
        self.couleur_r = couleur_r
        self.couleur_g = couleur_g
        self.couleur_b = couleur_b
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetGlyphe(self.typeZoneStr, self.tailleZoneGlyphe, self.nomSortEntre, self.nomSortDeplacement, self.nomSortSortie,
                           self.duree, self.nom, self.couleur_r, self.couleur_g, self.couleur_b, **self.kwargs)

    def __str__(self):
        return "Pose une glyphe "+str(self.nom)+" de taille "+str(self.tailleZoneGlyphe)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        frameTop = ttk.Frame(frame)
        typeZoneLbl = ttk.Label(frameTop, text="Type zone:")
        typeZoneLbl.pack(side="left")
        typeZoneCombobox = ttk.Combobox(frameTop, values=TypeZone.getZoneList(), state="readonly")
        typeZoneCombobox.set(self.typeZoneStr)
        typeZoneCombobox.pack(side="left")
        ret["typeZoneStr"] = typeZoneCombobox
        tailleZoneLbl = ttk.Label(frameTop, text="Taille zone:")
        tailleZoneLbl.pack(side="left")
        tailleZoneSpinbox = tk.Spinbox(frameTop, from_=0, to=99, width=3)
        tailleZoneSpinbox.delete(0, 'end')
        tailleZoneSpinbox.insert(0, int(self.tailleZoneGlyphe))
        tailleZoneSpinbox.pack(side="left")
        ret["tailleZoneGlyphe"] = tailleZoneSpinbox
        nomLbl = ttk.Label(frameTop, text="Nom du glyphe:")
        nomLbl.pack(side="left")
        nomEntry = ttk.Entry(frameTop, width=50)
        nomEntry.delete(0, 'end')
        nomEntry.insert(0, self.nom)
        nomEntry.pack(side="left")
        ret["nom"] = nomEntry
        dureeLbl = ttk.Label(frameTop, text="Durée:")
        dureeLbl.pack(side="left")
        dureeSpinbox = tk.Spinbox(frameTop, from_=0, to=99, width=2)
        dureeSpinbox.delete(0, 'end')
        dureeSpinbox.insert(0, self.duree)
        dureeSpinbox.pack(side="left")
        ret["duree"] = dureeSpinbox
        frameTop.pack(side="top")
        frameSort = ttk.Frame(frame)
        nomSortEntreLbl = ttk.Label(frameSort, text="Nom du sort d'entré:")
        nomSortEntreLbl.pack(side="left")
        nomSortEntreEntry = ttk.Entry(frameSort, width=30)
        nomSortEntreEntry.delete(0, 'end')
        nomSortEntreEntry.insert(0, self.nomSortEntre)
        nomSortEntreEntry.pack(side="left")
        ret["nomSortEntre"] = nomSortEntreEntry
        nomSortDeplacementLbl = ttk.Label(frameSort, text="Nom du sort de déplacement:")
        nomSortDeplacementLbl.pack(side="left")
        nomSortDeplacementEntry = ttk.Entry(frameSort, width=30)
        nomSortDeplacementEntry.delete(0, 'end')
        nomSortDeplacementEntry.insert(0, self.nomSortDeplacement)
        nomSortDeplacementEntry.pack(side="left")
        ret["nomSortDeplacement"] = nomSortDeplacementEntry
        nomSortSortieLbl = ttk.Label(frameSort, text="Nom du sort de sortie:")
        nomSortSortieLbl.pack(side="left")
        nomSortSortieEntry = ttk.Entry(frameSort, width=30)
        nomSortSortieEntry.delete(0, 'end')
        nomSortSortieEntry.insert(0, self.nomSortSortie)
        nomSortSortieEntry.pack(side="left")
        frameSort.pack(side="top")
        ret["nomSortSortie"] = nomSortSortieEntry
        frameCouleur = ttk.Frame(frame)
        couleurLbl = ttk.Label(frameCouleur, text="Couleur (R,G,B):")
        couleurLbl.pack(side="left")
        couleurRSpinbox = tk.Spinbox(frameCouleur, from_=0, to=255, width=3)
        couleurRSpinbox.delete(0, "end")
        couleurRSpinbox.insert(0, str(self.couleur_r))
        couleurRSpinbox.pack(side="left")
        ret["couleur_r"] = couleurRSpinbox
        couleurGSpinbox = tk.Spinbox(frameCouleur, from_=0, to=255, width=3)
        couleurGSpinbox.delete(0, "end")
        couleurGSpinbox.insert(0, str(self.couleur_g))
        couleurGSpinbox.pack(side="left")
        ret["couleur_g"] = couleurGSpinbox
        couleurBSpinbox = tk.Spinbox(frameCouleur, from_=0, to=255, width=3)
        couleurBSpinbox.delete(0, "end")
        couleurBSpinbox.insert(0, str(self.couleur_b))
        couleurBSpinbox.pack(side="left")
        ret["couleur_b"] = couleurBSpinbox
        frameCouleur.pack(side="top")
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["tailleZoneGlyphe"] = self.tailleZoneGlyphe
        ret["typeZoneStr"] = self.typeZoneStr
        ret["nom"] = self.nom
        ret["nomSortEntre"] = self.nomSortEntre
        ret["nomSortDeplacement"] = self.nomSortDeplacement
        ret["nomSortSortie"] = self.nomSortSortie
        ret["couleur_r"] = self.couleur_r
        ret["couleur_g"] = self.couleur_g
        ret["couleur_b"] = self.couleur_b
        ret["duree"] = self.duree
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["typeZoneStr"], infos["tailleZoneGlyphe"], infos["nomSortEntre"], infos["nomSortDeplacement"], infos["nomSortSortie"], infos["duree"], infos["nom"], 
                    infos["couleur_r"], infos["couleur_g"], infos["couleur_b"], **infos["kwargs"])

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
        print("Create zone action "+str(self.typeZoneStr)+ " size : "+str(self.tailleZoneGlyphe))
        self.zoneAction = TypeZone.getZoneFromName(self.typeZoneStr, self.tailleZoneGlyphe)
        sortEntre = joueurLanceur.getSort(self.nomSortEntre)
        sortDeplacement = joueurLanceur.getSort(self.nomSortDeplacement)
        sortSortie = joueurLanceur.getSort(self.nomSortSortie)
        nouvelleGlyphe = Glyphe(self.zoneAction, self.nom, sortEntre, sortDeplacement,
                                sortSortie, self.duree, kwargs.get("caseCibleX"),
                                kwargs.get("caseCibleY"), joueurLanceur, (self.couleur_r, self.couleur_g, self.couleur_b))
        niveau.poseGlyphe(nouvelleGlyphe)


class EffetActiveGlyphe(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet relance les effets d'une glyphe"""

    def __init__(self, strNomGlyphe="", **kwargs):
        """@summary: Initialise un effet lançant un sort à une entité/joueur
        @strNomGlyphe: la glyphe devant être réactivé
        @type: string

        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.strNomGlyphe = strNomGlyphe
        super().__init__(**kwargs)

    def __str__(self):
        return "Déclenche la glyphe "+str(self.strNomGlyphe)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        nomGlypheLbl = ttk.Label(frame, text="Nom de la glyphe:")
        nomGlypheLbl.pack(side="left")
        nomGlypheEntry = ttk.Entry(frame, width=50)
        nomGlypheEntry.delete(0, 'end')
        nomGlypheEntry.insert(0, self.strNomGlyphe)
        nomGlypheEntry.pack(side="left")
        ret["strNomGlyphe"] = nomGlypheEntry
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["strNomGlyphe"] = self.strNomGlyphe
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["strNomGlyphe"], **infos["kwargs"])

    def __deepcopy__(self, memo):
        return EffetActiveGlyphe(self.strNomGlyphe, **self.kwargs)

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
        niveau.activerGlyphe(self.strNomGlyphe)
