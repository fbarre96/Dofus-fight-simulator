"""@summary: Rassemble les effets de sort en rapport avec les runes."""

from Effets.Effet import Effet
from Rune import Rune
from EffectsTreeview import EffectsTreeview
class EffetRune(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose une rune sur la grille de jeu."""

    def __init__(self, duree=1, list_effets=[], str_nom="", couleur_r=0, couleur_g=0, couleur_b=0, **kwargs):
        """@summary: Initialise un effet posant une rune.
        @duree: Le nombrede tour où la rune sera présente (avant déclenchement)
        @type: int
        @sort_sort: le sort lancé sur la case centrale du piège
        @type: Sort
        @str_nom: le nom de la rune
        @type: string
        @tuple_couleur: la couleur du piège
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.duree = duree
        self.effets = list_effets
        self.nom = str_nom
        self.couleur_r = couleur_r
        self.couleur_g = couleur_g
        self.couleur_b = couleur_b
        super().__init__(**kwargs)

    def __str__(self):
        return "Pose une rune "+str(self.nom)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        frameTop = ttk.Frame(frame)
        nomLbl = ttk.Label(frameTop, text="Nom de la rune:")
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
        effetsTw = EffectsTreeview(frame, "Effets de la rune:", self.effets)
        effetsTw.pack(side="left")
        ret["effets"] = effetsTw
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["nom"] = self.nom
        ret["couleur_r"] = self.couleur_r
        ret["couleur_g"] = self.couleur_g
        ret["couleur_b"] = self.couleur_b
        ret["duree"] = self.duree
        effects = []
        for effet in self.effets:
            if isinstance(effet, Effet):
                effects.append(effet.getAllInfos())
            elif isinstance(effet, dict):
                effects.append(effet)
            else:
                raise Exception("Wrong type of object in effect piege treeview")
        ret["effets"] = effects
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return cls(infos["duree"], infos["effets"], infos["nom"], 
                    infos["couleur_r"], infos["couleur_g"], infos["couleur_b"], **infos["kwargs"])


    def __deepcopy__(self, memo):
        return EffetRune(self.duree, self.effets, self.nom, self.couleur_r, self.couleur_g, self.couleur_b, **self.kwargs)

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
        nouvelleRune = Rune(self.nom, self.duree, self.effets, kwargs.get(
            "caseCibleX"), kwargs.get("caseCibleY"), joueurLanceur, (self.couleur_r, self.couleur_g, self.couleur_b))
        niveau.poseRune(nouvelleRune)
