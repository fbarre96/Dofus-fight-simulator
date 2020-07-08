"""@summary: Rassemble les effets de sort en rapport avec les pièges."""
from Effets.Effet import Effet
from EffectsTreeview import EffectsTreeview
from Piege import Piege
from Zones import TypeZone

class EffetPiege(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet pose un piège sur la grille de jeu."""

    def __init__(self, typeZoneStr="Cercle", tailleZonePiege=0, list_effets=[], str_nom="piege", couleur_r=125, couleur_g=125, couleur_b=125, **kwargs):
        """@summary: Initialise un effet posant un piège.
        @zoneDeclenchement: la zone où si un joueur marche le piège se déclenche.
        @type: Zones.TypeZone
        @sort_sort: le sort lancé sur la case centrale du piège
        @type: Sort
        @str_nom: le nom du piège
        @type: string
        @tuple_couleur: la couleur du piège
        @type: tuple de couleur format RGB
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.typeZoneStr = typeZoneStr
        self.tailleZonePiege = tailleZonePiege
        self.effets = list_effets
        self.nom = str_nom
        self.couleur_r = couleur_r
        self.couleur_g = couleur_g
        self.couleur_b = couleur_b
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetPiege(self.typeZoneStr, self.tailleZonePiege, self.effets, self.nom,
                          self.couleur_r, self.couleur_g, self.couleur_b, **self.kwargs)

    def __str__(self):
        return "Pose un piège "+str(self.nom)+" de taille "+str(self.tailleZonePiege)

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        typeZoneLbl = ttk.Label(frame, text="Type zone:")
        typeZoneLbl.pack(side="left")
        typeZoneCombobox = ttk.Combobox(frame, values= TypeZone.getZoneList(), state="readonly")
        typeZoneCombobox.set(self.typeZoneStr)
        typeZoneCombobox.pack(side="left")
        ret["typeZoneStr"] = typeZoneCombobox
        tailleZoneLbl = ttk.Label(frame, text="Taille zone:")
        tailleZoneLbl.pack(side="left")
        tailleZoneSpinbox = tk.Spinbox(frame, from_=0, to=99, width=3)
        tailleZoneSpinbox.delete(0, 'end')
        tailleZoneSpinbox.insert(0, int(self.tailleZonePiege))
        tailleZoneSpinbox.pack(side="left")
        ret["tailleZonePiege"] = tailleZoneSpinbox
        nomLbl = ttk.Label(frame, text="Nom du piège:")
        nomLbl.pack(side="left")
        nomEntry = ttk.Entry(frame, width=50)
        nomEntry.delete(0, 'end')
        nomEntry.insert(0, self.nom)
        nomEntry.pack(side="left")
        ret["nom"] = nomEntry
        couleurLbl = ttk.Label(frame, text="Couleur (R,G,B):")
        couleurLbl.pack(side="left")
        couleurRSpinbox = tk.Spinbox(frame, from_=0, to=255, width=3)
        couleurRSpinbox.delete(0, "end")
        couleurRSpinbox.insert(0, str(self.couleur_r))
        couleurRSpinbox.pack(side="left")
        ret["couleur_r"] = couleurRSpinbox
        couleurGSpinbox = tk.Spinbox(frame, from_=0, to=255, width=3)
        couleurGSpinbox.delete(0, "end")
        couleurGSpinbox.insert(0, str(self.couleur_g))
        couleurGSpinbox.pack(side="left")
        ret["couleur_g"] = couleurGSpinbox
        couleurBSpinbox = tk.Spinbox(frame, from_=0, to=255, width=3)
        couleurBSpinbox.delete(0, "end")
        couleurBSpinbox.insert(0, str(self.couleur_b))
        couleurBSpinbox.pack(side="left")
        ret["couleur_b"] = couleurBSpinbox
        effetsTw = EffectsTreeview(frame, "Effets du piège:", self.effets)
        effetsTw.pack(side="left")
        ret["effets"] = effetsTw
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["tailleZonePiege"] = self.tailleZonePiege
        ret["typeZoneStr"] = self.typeZoneStr
        ret["nom"] = self.nom
        ret["couleur_r"] = self.couleur_r
        ret["couleur_g"] = self.couleur_g
        ret["couleur_b"] = self.couleur_b
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
        effets_liste = []
        for info_effet in infos["effets"]:
            info_effet["kwargs"]["piege"] = True
            effets_liste.append(Effet.effectFactory(info_effet))
        return cls(infos["typeZoneStr"], infos["tailleZonePiege"], effets_liste, infos["nom"], 
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
        zoneDeclenchement = TypeZone.getZoneFromName(self.typeZoneStr, self.tailleZonePiege)
        nouveauPiege = Piege(self.nom, zoneDeclenchement, self.effets, kwargs.get(
            "caseCibleX"), kwargs.get("caseCibleY"), joueurLanceur, (self.couleur_r, self.couleur_g, self.couleur_b))
        niveau.posePiege(nouveauPiege)
