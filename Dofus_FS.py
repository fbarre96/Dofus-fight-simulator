# -*- coding: utf-8 -*
"""
Dofus_FS est un simulateur de combat pour Dofus.
"""
from tkinter import Tk
from tkinter import *

from tkinter.ttk import Combobox
from tkinter.ttk import Notebook, Scrollbar
from PIL import Image, ImageTk
import json
from pygame.locals import QUIT, RESIZABLE
import os
import pygame
import constantes
import Niveau
import Personnages
from importlib import import_module


def boucleEvenement(niveau, mouseXY, sortSelectionne):
    """@summary: Parours et dispatch les événements pygame
    @niveau: Les informations de niveau
    @type: Niveau
    @mouseXY: Les coordonnées actuelles de la souris
    @type: tableau de 2 entiers représentant les coordonnées x et y.
    @sortSelectionne: Le sort sélectionné dans la barre de sort.
    @type: Sort ou None
    @return: un entier indiquant si la simulation est terminée ainsi que le sort sélectionné."""
    continuer = 1
    # Parcours des événements pygame
    for event in pygame.event.get():  # On parcours la liste de tous les événements reçus
        if event.type == QUIT:  # Si un de ces événements est de type QUIT
            continuer = 0  # On arrête la boucle
        # Envoie de l'event au personnage en cours de jeu.
        sortSelectionne = niveau.tourDe.myIA.joue(
            event, niveau.tourDe, niveau, mouseXY, sortSelectionne)
    # Si le personnage actif n'est pas un joueur mais une IA, on n'envoie pas d'event.
    if not isinstance(niveau.tourDe, Personnages.Personnage):
        sortSelectionne = niveau.tourDe.myIA.joue(
            None, niveau.tourDe, niveau, mouseXY, sortSelectionne)
    return continuer, sortSelectionne


def commenceCombat(persos):
    """@summary: Boucle principale de la simulation de combat.
    @joueur: Le joueur qui affrontera le poutch
    @type: Personnage"""

    # Initialisation de la bibliothèque Pygame

    myfont = pygame.font.SysFont("monospace", 15)
    # Création de la fenêtre
    fenetreJeu = pygame.display.set_mode(
        (constantes.width_fenetre, constantes.height_fenetre), RESIZABLE)
    # Variable qui continue la boucle si = 1, stoppe si = 0
    pygame.display.set_caption("Dofus fight simulator")
    continuer = 1
    # Initialisation du niveau
    niveau = Niveau.Niveau(fenetreJeu, persos, myfont)
    sortSelectionne = None
    # Lancement du premier tour de jeu
    niveau.tourDe.debutTour(niveau)
    # Boucle principale de la simulation de combat
    while continuer == 1:
        # Sleep pour éviter la surconsommation du CPU
        pygame.time.Clock().tick(30)
        mouseXY = pygame.mouse.get_pos()
        # Réaffichage
        niveau.afficher(fenetreJeu, sortSelectionne, mouseXY)
        # Gestion des événements
        continuer, sortSelectionne = boucleEvenement(
            niveau, mouseXY, sortSelectionne)

        # Affichage
        pygame.display.flip()
    # Ferme la fenêtre pygame
    pygame.display.quit()


def launchSimu(persosToSave):
    """@summary: Lance la simulation de combat
    @evt: l'événement qui lance la simulation
    @type: Event
    @persosToSave: list of persos
    @type: list
    """
    pygame.init()
    effectlist = os.listdir("Effets")
    for effect in effectlist:
        if not effect.startswith("__") and effect.endswith(".py"):
            import_module("Effets."+effect[:-3])
    etatlist = os.listdir("Etats")
    for etat in etatlist:
        if not etat.startswith("__") and etat.endswith(".py"):
            import_module("Etats."+etat[:-3])
    persos = []
    for persoVw in persosToSave:
        perso = persoVw.perso
        joueur = Personnages.Personnage(perso["Perso"]["Nom"], perso["Perso"]["Classe"],
                                        perso["Perso"]["Level"], perso["Perso"]["Team"],
                                        perso["Primaires"], perso["Secondaires"], perso["Dommages"],
                                        perso["Resistances"], perso["Perso"]["Classe"]+".png")
        joueur.faireChargerSort(perso["Sorts"])
        persos.append(joueur)
    commenceCombat(persos)


def readSaveFile(path):
    """@summary: Lit le fichier de sauvegarde de personnage et prérempli les champs tkinter
    """
    with open(path, "r") as fichier:
        contenu = fichier.read()
        ret = json.loads(contenu)
    return ret


def writeSaveFile(path, playersTab):
    """@summary: Ecrit le fichier de sauvegarde de personnage avec les champs de tkinter
    """
    with open(path, "w") as fichier:
        fichier.write(json.dumps(playersTab))


class PersoView():
    """@summary: Stock les valeurs absolues dans des dictionnaires
                 Stock les inputs correspondants. Permet les transfères bidirectionels.
    """
    def __init__(self, values):
        self.perso = values
        self.caracTab = None
        self.framePerso = None
        self.inputs = dict()

    def save(self):
        """@summary: sauvegarde le perso donné au constructeur dans
                     un fichier json demandé à l'utilisateur
        """
        filename = filedialog.asksaveasfilename(initialdir="./persos/",
                                                title="Nom de la sauvegarde",
                                                defaultextension=".json",
                                                filetypes=(("json files", "*.json"),
                                                           ("all files", "*.*")))
        if filename.strip() != "":
            self.inputsToPerso()
            writeSaveFile(filename, self.perso)

    def inputsToPerso(self):
        """@summary: range sous forme de dictionnaires
                     les valeurs des inputs
        """
        perso = dict()
        for inputsCategory, inputsSub in self.inputs.items():
            if perso.get(inputsCategory, None) is None:
                perso[inputsCategory] = dict()
            for caracName, caracValue in inputsSub.items():
                if perso[inputsCategory].get(caracName, None) is None:
                    perso[inputsCategory][caracName] = caracValue.get()
        self.perso = perso

    def persoToInputs(self):
        """@summary: Remplis les champs inputs avec les valeurs
                     des dictionnaires.
        """
        for valuesCategory, valueDict in self.perso.items():
            for valueName, value in valueDict.items():
                if valueName == "Classe" or valuesCategory == "Sorts":
                    self.inputs[valuesCategory][valueName].set(value)
                else:
                    self.inputs[valuesCategory][valueName].delete(0, 'end')
                    self.inputs[valuesCategory][valueName].insert(END, value)
            
    def load(self):
        """@summary: charge dans le perso donné au constructeur
                     un fichier json demandé à l'utilisateur
        """
        filename = filedialog.askopenfilename(initialdir="./persos/", title="Choisir une sauvegarde",
                                              filetypes=(("json files", "*.json"),
                                                         ("all files", "*.*")))
        if filename.strip() != "":
            self.perso = readSaveFile(filename)
            self.persoToInputs()



class OpeningPage():
    """@summary: Widget servant à lancer la simulation après
                 avoir renseigné les persos
        """
    def __init__(self, fenetre):
        self.notebk = Notebook(fenetre)
        self.fenetre = fenetre
        self.persoViews = []
        self.caracsNotebk = []
        self.framesPersos = []

    def formSubmission(self, _):
        """@summary: Lance la simulation de combat avec les persos du notebook
        """
        persos = []
        for persoVw in self.persoViews:
            persoVw.inputsToPerso()
            persos.append(persoVw.perso)
            writeSaveFile("save.json", persos)
        launchSimu(self.persoViews)

    def addEmptyPage(self, _):
        """@summary: Ajoute un onglet avec un stub perso dans le notebook0
        """
        self.addPage(readSaveFile("./persos/empty.json"))

    def deleteActiveNotePage(self):
        """@summary: Supprime l'onglet actif et les valeurs de personnages
                     associés.
        """
        nomPanneau = self.notebk.tab(self.notebk.select())["text"]
        indPanneau = int(nomPanneau.split(" ")[1])
        self.notebk.forget(self.notebk.select())
        del self.persoViews[indPanneau-1]

    def addPageSorts(self, persoVw):
        tab_names = [persoVw.caracsNotebk.tab(i, option="text") for i in persoVw.caracsNotebk.tabs()]
        if "Sorts" in tab_names:
            persoVw.caracsNotebk.forget(tab_names.index("Sorts"))
        classe = persoVw.perso["Perso"]["Classe"]
        lvl = persoVw.perso["Perso"]["Level"]
        frameSorts = LabelFrame(persoVw.framePerso, text="Sorts")
        sorts, sortsDebtCombat = Personnages.Personnage.chargerSorts(classe, lvl, {}, True)
        variantesFrame = ScrolledWindow(frameSorts, width=400, height=400)
        persoVw.images = []
        if "Sorts" not in persoVw.inputs:
            persoVw.inputs["Sorts"] = dict()
        addedSpells = {}
        for sort in sorts:
            if not sort.lancableParJoueur:
                continue
            isVariante = sort.nom_variante != "" and sort.nom_variante in addedSpells
            root_pic1 = Image.open(sort.image)                       # Open the image like this first
            persoVw.images.append(ImageTk.PhotoImage(root_pic1))
            ind = len(addedSpells)
            imgLbl = Label(variantesFrame.scrollwindow, image=persoVw.images[-1], anchor="nw")
            imgLbl.grid(row=addedSpells[sort.nom_variante] if isVariante else ind, column=2 if isVariante else 0, sticky="e")
            varSort = IntVar()
            varSort.set(persoVw.perso["Sorts"].get(sort.nom, 0))
            persoVw.inputs["Sorts"][sort.nom] = varSort
            cbSort = Checkbutton(variantesFrame.scrollwindow, text=sort.nom, variable=varSort, onvalue=1, offvalue=0, anchor="w")
            cbSort.grid(row=addedSpells[sort.nom_variante] if isVariante else ind, column=3 if isVariante else 1, sticky="w")
            
            addedSpells[sort.nom] = ind
        persoVw.caracsNotebk.add(frameSorts, text="Sorts")

    def onClassChange(self, event):
        nomPanneau = self.notebk.tab(self.notebk.select())["text"]
        indPanneau = int(nomPanneau.split(" ")[1])
        persoVw = self.persoViews[indPanneau-1]
        self.addPageSorts(persoVw)
        

    def addPage(self, values):
        """@summary: Ajoute un onglet avec les valeurs de personnages données.
        """
        self.persoViews.append(PersoView(values))
        persoVw = self.persoViews[-1]
        self.framesPersos.append(Frame(self.notebk))
        framePerso = self.framesPersos[-1]
        persoVw.framePerso = framePerso
        self.caracsNotebk.append(Notebook(framePerso))
        caracNotebk = self.caracsNotebk[-1]
        caracNotebk.pack()
        persoVw.caracsNotebk = caracNotebk
        for inputsCategory, inputValues in persoVw.perso.items():
            frameCaracs = LabelFrame(framePerso, text=inputsCategory)
            if persoVw.inputs.get(inputsCategory, None) is None:
                persoVw.inputs[inputsCategory] = dict()
            j = 0
            if inputsCategory == "Sorts":
                self.addPageSorts(persoVw)
                continue
            for inputName, inputValue in inputValues.items():
                if inputName == "Classe":
                    classesDisponibles = \
                        Combobox(frameCaracs,
                                 textvariable=StringVar(),
                                 values=["Cra", "Xelor", "Iop",
                                         "Sram", "Poutch", "Eniripsa", "Pandawa"],
                                 state='readonly')
                    classesDisponibles.bind('<<ComboboxSelected>>', self.onClassChange)
                    persoVw.inputs[inputsCategory][inputName] = classesDisponibles
                    persoVw.inputs[inputsCategory][inputName].set(inputValue)

                else:
                    persoVw.inputs[inputsCategory][inputName] = \
                        Entry(frameCaracs, textvariable=StringVar(), width=10)
                    persoVw.inputs[inputsCategory][inputName].insert(END, inputValue)
                lblCarac = Label(frameCaracs,
                                 text=inputName+":")
                lblCarac.grid(row=j, column=0)
                persoVw.inputs[inputsCategory][inputName].grid(row=j, column=1)
                j += 1
            caracNotebk.add(frameCaracs, text=inputsCategory)
        # Pack de la fenêtre, détermine la taille de la fenêtre selon la taille des composants.
        #framePerso.pack(fill="both", expand="yes")
        self.notebk.add(framePerso, text="Perso "+str(len(self.persoViews)))
        saveBtn = Button(framePerso, text='Sauvegarder ce perso', command=persoVw.save)
        loadBtn = Button(framePerso, text='Charger un perso', command=persoVw.load)
        deleteThisBtn = Button(framePerso, text="Supprimer ce perso",
                               command=self.deleteActiveNotePage)
        # Mise du bouton sur la droite de la fenetre
        saveBtn.pack(side="left")
        # Mise du bouton sur la droite de la fenetre
        loadBtn.pack(side="left")
        deleteThisBtn.pack(side="left")

    def main(self):
        """@summary: Lance la création des personnages pour ensuite lancer la simulation
        """
        # Créer la fenêtre Tkinter
        values = readSaveFile("save.json")
        self.notebk.pack()

        for inputPerso in values:
            self.addPage(inputPerso)

        self.notebk.enable_traversal()
        # Ajout du bouton pour lancer la simulation
        submit = Button(self.fenetre, text='Lancer la simulation')
        # Permet au gestionnaire d'événement d'ajouter des paramètres
        # Gestionnaire d'événement pour le clic du bouton
        submit.bind("<Button-1>", self.formSubmission)
        # Mise du bouton sur la droite de la fenetre
        submit.pack(side="right")
        addPersoBtn = Button(self.fenetre, text='Ajouter un perso')
        addPersoBtn.bind("<Button-1>", self.addEmptyPage)
        addPersoBtn.pack(side="right")

class ScrolledWindow(Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected 
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.canv_w  = kwargs.get("width", 10)
        self.canv_h  = kwargs.get("height", 10)
        # creating a scrollbars
        self.yscrlbr = Scrollbar(self.parent)
        self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')         
        # creating a canvas
        self.canv = Canvas(self.parent)
        self.canv.config(relief = 'flat',
                         width = self.canv_w,
                         heigh = self.canv_h, bd = 2)
        # placing a canvas into frame
        self.canv.grid(column = 0, row = 0, sticky = 'nsew')
        # accociating scrollbar comands to canvas scroling
        self.yscrlbr.config(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = Frame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, self.canv_w, self.canv_h))

        self.yscrlbr.lift(self.scrollwindow)        
        self.scrollwindow.bind('<Configure>', self._configure_window)  
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")  

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        try:
            self.canv.config(scrollregion='0 0 %s %s' % size)
        except:
            return
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width = min(self.scrollwindow.winfo_reqwidth(), self.canv_w))
        if self.scrollwindow.winfo_reqheight() != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height = min(self.scrollwindow.winfo_reqheight(), self.canv_h))

if __name__ == "__main__":
    # Importation des bibliothèques nécessaires
    fenetre_tk = Tk()
    page = OpeningPage(fenetre_tk)
    page.main()
    fenetre_tk.mainloop()
