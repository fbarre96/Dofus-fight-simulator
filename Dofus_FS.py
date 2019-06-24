# -*- coding: utf-8 -*
"""
Dofus_FS est un simulateur de combat pour Dofus.
"""
from tkinter import Tk
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import Button
from tkinter import Label
from tkinter import Frame
from tkinter import END
from tkinter.ttk import Combobox
from tkinter.ttk import Checkbutton
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
    fenetre = pygame.display.set_mode(
        (constantes.width_fenetre, constantes.height_fenetre), RESIZABLE)
    # Variable qui continue la boucle si = 1, stoppe si = 0
    pygame.display.set_caption("Dofus fight simulator")
    continuer = 1
    # Initialisation du niveau
    niveau = Niveau.Niveau(fenetre, persos, myfont)
    sortSelectionne = None
    # Lancement du premier tour de jeu
    niveau.tourDe.debutTour(niveau)
    # Boucle principale de la simulation de combat
    while continuer == 1:
        # Sleep pour éviter la surconsommation du CPU
        pygame.time.Clock().tick(30)
        mouseXY = pygame.mouse.get_pos()
        # Réaffichage
        niveau.afficher(fenetre, sortSelectionne, mouseXY)
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
    for perso in persosToSave:
        joueur = Personnages.Personnage(perso["Classe"]["Nom"], perso["Classe"]["Classe"],
                                        perso["Level"]["Level"], perso["Team"]["Team"],
                                        perso["Primaires"], perso["Secondaires"], perso["Dommages"],
                                        perso["Resistances"], perso["Classe"]["Classe"]+".png")
        persos.append(joueur)
    commenceCombat(persos)


def readSaveFile():
    """@summary: Lit le fichier de sauvegarde de personnage et prérempli les champs tkinter
    """
    with open("save.txt", "r") as fichier:
        contenu = fichier.read()
        ret = json.loads(contenu)
    return ret


def writeSaveFile(playersTab):
    """@summary: Ecrit le fichier de sauvegarde de personnage avec les champs de tkinter
    """
    with open("save.txt", "w") as fichier:
        fichier.write(json.dumps(playersTab))


class ToggledFrame(Frame):
    """@summary: définit une frame qui peut se minimiser
    """
    def __init__(self, parent, text, *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.titleFrame = Frame(self)
        self.titleFrame.pack(fill="x", expand=1)

        Label(self.titleFrame, text=text).pack(
            side="left", fill="x", expand=1)

        self.toggleButton = Checkbutton(self.titleFrame, width=2, text='+', command=self.toggle,
                                        variable=self.show, style='Toolbutton')
        self.toggleButton.pack(side="left")

        self.subFrame = Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        """@summary: Minimise ou maximise la frame.
        """
        if bool(self.show.get()):
            self.subFrame.pack(fill="x", expand=1)
            self.toggleButton.configure(text='-')
        else:
            self.subFrame.forget()
            self.toggleButton.configure(text='+')


def main():
    """@summary: Lance la création des personnages pour ensuite lancer la simulation
    """
    # Créer la fenêtre Tkinter
    fenetre = Tk()
    values = readSaveFile()
    inputs = dict()
    for i, inputPerso in enumerate(values):
        framePerso = ToggledFrame(fenetre, "Perso "+str(i+1))
        for inputsCategory, inputValues in inputPerso.items():
            frameCaracs = ToggledFrame(framePerso.subFrame, inputsCategory)
            j = 0
            for inputName, inputValue in inputValues.items():
                inputSelector = str(i)+"|"+inputsCategory+"|"+inputName
                if inputName == "Classe":
                    classesDisponibles = \
                        Combobox(frameCaracs.subFrame,
                                 textvariable=StringVar(),
                                 values=["Cra", "Xelor", "Iop",
                                         "Sram", "Poutch", "Eniripsa", "Pandawa"],
                                 state='readonly')
                    inputs[inputSelector] = classesDisponibles
                    inputs[inputSelector].set(inputValue)
                    lblCarac = Label(frameCaracs.subFrame, text=inputName+":")
                    lblCarac.grid(row=j, column=0)
                    inputs[inputSelector].grid(row=j, column=1)
                else:
                    inputs[inputSelector] = Entry(frameCaracs.subFrame, textvariable=StringVar(),
                                                  width=5)
                    inputs[inputSelector].insert(END, inputValue)
                    lblCarac = Label(frameCaracs.subFrame,
                                     text=inputName+":")
                    lblCarac.grid(row=j, column=0)
                    inputs[str(i)+"|"+inputsCategory+"|" +
                           inputName].grid(row=j, column=1)
                j += 1
            frameCaracs.pack(fill="both", expand="yes")
        # Pack de la fenêtre, détermine la taille de la fenêtre selon la taille des composants.
        framePerso.pack(fill="both", expand="yes")

    # Ajout du bouton pour lancer la simulation
    submit = Button(fenetre, text='OK')
    # Permet au gestionnaire d'événement d'ajouter des paramètres
    # Gestionnaire d'événement pour le clic du bouton

    def gest(evt):
        # evt est obligatoire car tkinter le donne comme argument
        # pylint: disable=unused-argument
        persosToSave = []
        for i, inputPerso in enumerate(values):
            persosToSave.append(dict())
            for inputsCategory, inputValues in inputPerso.items():
                persosToSave[i][inputsCategory] = dict()
                for inputName in inputValues.keys():
                    persosToSave[i][inputsCategory][inputName] = inputs[str(
                        i)+"|"+inputsCategory+"|"+inputName].get()
        writeSaveFile(persosToSave)
        launchSimu(persosToSave)
    submit.bind("<Button-1>", gest)
    # Mise du bouton sur la droite de la fenetre
    submit.pack(side="right")
    # Remplissage des champs selon la sauvegarde.

    # Boucle de la fenêtre. Tant que la fenêtre n'est pas fermé.
    fenetre.mainloop()
    # Quand la fenêtre est fermé, on écrit le fichier de sauvegarde


if __name__ == "__main__":
    # Importation des bibliothèques nécessaires

    main()
