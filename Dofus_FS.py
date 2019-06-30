# -*- coding: utf-8 -*
"""
Dofus_FS est un simulateur de combat pour Dofus.
"""
from tkinter import Tk
from tkinter import StringVar
from tkinter import LabelFrame
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import Frame
from tkinter import END
from tkinter import filedialog

from tkinter.ttk import Combobox
from tkinter.ttk import Notebook

import json
from pygame.locals import QUIT, RESIZABLE

import pygame
import constantes
import Niveau
import Personnages


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
    persos = []
    for persoVw in persosToSave:
        perso = persoVw.perso
        joueur = Personnages.Personnage(perso["Perso"]["Nom"], perso["Perso"]["Classe"],
                                        perso["Perso"]["Level"], perso["Perso"]["Team"],
                                        perso["Primaires"], perso["Secondaires"], perso["Dommages"],
                                        perso["Resistances"], perso["Perso"]["Classe"]+".png")
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
                if valueName == "Classe":
                    self.inputs[valuesCategory][valueName].set(value)
                else:
                    self.inputs[valuesCategory][valueName].delete(0, 'end')
                    self.inputs[valuesCategory][valueName].insert(END, value)
    def load(self):
        """@summary: charge dans le perso donné au constructeur
                     un fichier json demandé à l'utilisateur
        """
        filename = filedialog.askopenfilename(initialdir="./persos/", title="Chosir une sauvegarde",
                                              filetypes=(("json files", "*.json"),
                                                         ("all files", "*.*")))
        if filename.strip() != "":
            self.perso = readSaveFile(filename)
            self.persoToInputs()



class OpeningPage():
    def __init__(self, fenetre):
        self.notebk = Notebook(fenetre)
        self.fenetre = fenetre
        self.persoViews = []
        self.caracsNotebk = []
        self.framesPersos = []

    def formSubmission(self, evt):
        # evt est obligatoire car tkinter le donne comme argument
        # pylint: disable=unused-argument
        persos = []
        for persoVw in self.persoViews:
            persoVw.inputsToPerso()
            persos.append(persoVw.perso)
            writeSaveFile("save.json", persos)
        launchSimu(self.persoViews)
    
    def addEmptyPage(self, evt=None):
        self.addPage(readSaveFile("./persos/empty.json"))

    def deleteActiveNotePage(self):
        nomPanneau = self.notebk.tab(self.notebk.select())["text"]
        indPanneau = int(nomPanneau.split(" ")[1])
        self.notebk.forget(self.notebk.select())
        del self.persoViews[indPanneau]

    def addPage(self, values):
        self.framesPersos.append(Frame(self.notebk))
        framePerso = self.framesPersos[-1]
        self.persoViews.append(PersoView(values))
        persoVw = self.persoViews[-1]
        self.caracsNotebk.append(Notebook(framePerso))
        caracNotebk = self.caracsNotebk[-1]
        caracNotebk.pack()
        for inputsCategory, inputValues in persoVw.perso.items():
            frameCaracs = LabelFrame(framePerso, text=inputsCategory)
            if persoVw.inputs.get(inputsCategory, None) is None:
                persoVw.inputs[inputsCategory] = dict()
            j = 0
            for inputName, inputValue in inputValues.items():
                if inputName == "Classe":
                    classesDisponibles = \
                        Combobox(frameCaracs,
                                    textvariable=StringVar(),
                                    values=["Cra", "Xelor", "Iop",
                                            "Sram", "Poutch", "Eniripsa", "Pandawa"],
                                    state='readonly')
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


if __name__ == "__main__":
    # Importation des bibliothèques nécessaires
    fenetre_tk = Tk()
    page = OpeningPage(fenetre_tk)
    page.main()
    fenetre_tk.mainloop()
