"""@summary: Rassemble les effets de sort en rapport avec les propagations."""

from Etats.Etat import Etat
from Effets.Effet import Effet
from copy import deepcopy
from Zones import TypeZoneCercle

class EffetPropage(Effet):
    """@summary: Classe décrivant un effet de sort. Les sorts sont découpés en 1 ou + effets.
    Cet effet propage un sort à la cible la plus proche dans la portée du sort
    (Flèche fulminante par exemple)."""

    def __init__(self, tailleZoneRebond=2, **kwargs):
        """@summary: Initialise un effet de propagation de sort.
        @zone_zone: la zone de propagation possible à partir de la dernière cible
        @type: Zone
        @kwargs: Options de l'effets
        @type: **kwargs"""
        self.kwargs = kwargs
        self.tailleZoneRebond = tailleZoneRebond
        super().__init__(**kwargs)

    def __deepcopy__(self, memo):
        return EffetPropage(self.tailleZoneRebond, **self.kwargs)

    def __str__(self):
        return "Rebondis à "+str(self.tailleZoneRebond)+" PO"

    def buildUI(self, topframe, callbackDict):
        import tkinter.ttk as ttk
        import tkinter as tk
        ret = {}
        frame = ttk.Frame(topframe)
        tailleZoneLbl = ttk.Label(frame, text="Taille zone de rebond:")
        tailleZoneLbl.pack(side="left")
        tailleZoneSpinbox = tk.Spinbox(frame, from_=0, to=99, width=3)
        tailleZoneSpinbox.insert(0, self.tailleZoneRebond)
        tailleZoneSpinbox.pack(side="left")
        ret["tailleZoneRebond"] = tailleZoneSpinbox
        frame.pack()
        return ret

    def getAllInfos(self):
        ret = super().getAllInfos()
        ret["tailleZoneRebond"] = self.tailleZoneRebond
        return ret

    @classmethod
    def craftFromInfos(cls, infos):
        return EffetPropage(int(infos["tailleZoneRebond"]),  **infos["kwargs"])


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

        # Etat temporaire pour marqué la cible comme déjà touché par la propagation
        joueurCaseEffet.appliquerEtat(
            Etat("temporaire", 0, 1), joueurLanceur, -1, niveau)
        # Récupérations des joueurs respectant les critères du sort les plus proches,
        # etat requis = pas temporaire
        joueursAppliquables = niveau.getJoueurslesPlusProches(joueurCaseEffet.posX,
                                                              joueurCaseEffet.posY, joueurLanceur,
                                                              TypeZoneCercle(self.tailleZoneRebond), ["!temporaire"],
                                                              self.ciblesPossibles)
        # La liste n'est vraie que si elle n'est pas vide
        if joueursAppliquables:
            sort_backref = self.getSort()
            sort_ref = deepcopy(sort_backref)
            sort_ref.coutPA = 0
            sort_ref.nbTourEntreDeux = 0
            sort_ref.nbLancerParTour = 999
            sort_ref.nbLancerParTourParJoueur = 9
            sort_ref.porte = self.tailleZoneRebond
            previsus_recues = sort_ref.lance(joueurCaseEffet.posX, joueurCaseEffet.posY, niveau,
                            joueursAppliquables[0].posX, joueursAppliquables[0].posY, joueurLanceur)
            if previsus_recues is not None:
                for previsu_recue in previsus_recues:
                    perso = niveau.getJoueurAvecUid(previsu_recue.uid)
                    perso.msgsPrevisu = previsu_recue.msgsPrevisu
                                