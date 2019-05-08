# -*- coding: utf-8 -*

from tkinter import Tk
from tkinter import LabelFrame
from tkinter import StringVar
from tkinter import IntVar
from tkinter import Entry
from tkinter import Button
from tkinter import END
from tkinter.ttk import Combobox
from tkinter.ttk import Checkbutton
from tkinter.ttk import Treeview

from tkinter import PhotoImage, Frame, Label, Widget
from tkinter.constants import *
#from tkinter import messagebox
#from tkinter.filedialog import askopenfilename
import pygame
import constantes
from pygame.locals import *
import Niveau
import Personnages
import json

def BoucleDEvenement(niveau,mouse_xy,sortSelectionne):
    """@summary: Parours et dispatch les événements pygame
    @niveau: Les informations de niveau
    @type: Niveau
    @mouse_xy: Les coordonnées actuelles de la souris
    @type: tableau de 2 entiers représentant les coordonnées x et y.
    @sortSelectionne: Le sort sélectionné dans la barre de sort.
    @type: Sort ou None
    @return: un entier indiquant si la simulation est terminée ainsi que le sort sélectionné."""
    continuer = 1
    #Parcours des événements pygame
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT:     #Si un de ces événements est de type QUIT
            continuer = 0      #On arrête la boucle
        #Envoie de l'event au personnage en cours de jeu.
        sortSelectionne=niveau.tourDe.joue(event,niveau,mouse_xy,sortSelectionne)
    #Si le personnage actif n'est pas un joueur mais une IA, on n'envoie pas d'event.
    if not type(niveau.tourDe) is Personnages.Personnage:
        sortSelectionne=niveau.tourDe.joue(None,niveau,mouse_xy,sortSelectionne)
    return continuer,sortSelectionne

def Commence_combat(persos):
    """@summary: Boucle principale de la simulation de combat.
    @joueur: Le joueur qui affrontera le poutch
    @type: Personnage"""

    #Initialisation de la bibliothèque Pygame
    
    myfont = pygame.font.SysFont("monospace", 15)
    #Création de la fenêtre
    fenetre = pygame.display.set_mode((constantes.width_fenetre,constantes.height_fenetre), RESIZABLE)
    #Variable qui continue la boucle si = 1, stoppe si = 0
    pygame.display.set_caption("Dofuk")
    continuer = 1
    #Initialisation du niveau
    niveau = Niveau.Niveau(fenetre, persos, myfont)
    sortSelectionne = None
    #Lancement du premier tour de jeu
    niveau.tourDe.debutTour(niveau)
    #Boucle principale de la simulation de combat
    while continuer == 1:
        #Sleep pour éviter la surconsommation du CPU
        pygame.time.Clock().tick(30)
        mouse_xy = pygame.mouse.get_pos()
        #Réaffichage 
        niveau.afficher(fenetre, sortSelectionne,mouse_xy)
        #Gestion des événements
        continuer,sortSelectionne=BoucleDEvenement(niveau,mouse_xy,sortSelectionne)

        #Affichage
        pygame.display.flip()
    #Ferme la fenêtre pygame
    pygame.display.quit()


def LaunchSimu(evt, persosToSave):
    """@summary: Lance la simulation de combat
    @evt: l'événement qui lance la simulation
    @type: Event
    @persosToSave: list of persos
    @type: list
    """
    pygame.init()
    persos = []
    for perso in persosToSave:
        joueur = Personnages.Personnage(perso["Classe"]["Classe"],perso["Level"]["Level"],perso["Team"]["Team"],perso["Primaires"],perso["Secondaires"],perso["Dommages"],perso["Resistances"],perso["Classe"]["Classe"]+".png")
        persos.append(joueur)
    Commence_combat(persos)


def readSaveFile():
    """@summary: Lit le fichier de sauvegarde de personnage et prérempli les champs tkinter
    """
    with open("save.txt","r") as f:
        contenu = f.read()
        ret = json.loads(contenu)
    return ret

def writeSaveFile(players_tab):
    """@summary: Ecrit le fichier de sauvegarde de personnage avec les champs de tkinter
    """
    with open("save.txt","w") as f:
        f.write(json.dumps(players_tab))

class ToggledFrame(Frame):

    def __init__(self, parent, text="", *args, **options):
        Frame.__init__(self, parent, *args, **options)

        self.show = IntVar()
        self.show.set(0)

        self.title_frame = Frame(self)
        self.title_frame.pack(fill="x", expand=1)

        Label(self.title_frame, text=text).pack(side="left", fill="x", expand=1)

        self.toggle_button = Checkbutton(self.title_frame, width=2, text='+', command=self.toggle,
                                            variable=self.show, style='Toolbutton')
        self.toggle_button.pack(side="left")

        self.sub_frame = Frame(self, relief="sunken", borderwidth=1)

    def toggle(self):
        if bool(self.show.get()):
            self.sub_frame.pack(fill="x", expand=1)
            self.toggle_button.configure(text='-')
        else:
            self.sub_frame.forget()
            self.toggle_button.configure(text='+')

def main():
    #Créer la fenêtre Tkinter
    fenetre = Tk()
    values = readSaveFile()
    inputs = dict()
    for i,input_perso in enumerate(values):
        framePerso = ToggledFrame(fenetre, "Perso "+str(i+1))
        for inputs_category, input_values in input_perso.items():
            frameCaracs = ToggledFrame(framePerso.sub_frame, inputs_category)
            j=0
            for input_name,input_value in input_values.items():
                if input_name == "Classe":
                    inputs[str(i)+"|"+inputs_category+"|"+input_name] = Combobox(frameCaracs.sub_frame, textvariable = StringVar(), values = ["Cra","Xelor","Iop","Sram","Poutch"], state = 'readonly')
                    inputs[str(i)+"|"+inputs_category+"|"+input_name].set(input_value)
                    lbl_carac = Label(frameCaracs.sub_frame,text=input_name+":")
                    lbl_carac.grid(row=j, column=0)
                    inputs[str(i)+"|"+inputs_category+"|"+input_name].grid(row=j, column=1)
                else:
                    inputs[str(i)+"|"+inputs_category+"|"+input_name] = Entry(frameCaracs.sub_frame, textvariable = StringVar(),width=5)
                    inputs[str(i)+"|"+inputs_category+"|"+input_name].insert(END, input_value)
                    lbl_carac = Label(frameCaracs.sub_frame,text=input_name+":")
                    lbl_carac.grid(row=j, column=0)
                    inputs[str(i)+"|"+inputs_category+"|"+input_name].grid(row=j, column=1)
                j+=1
            frameCaracs.pack(fill="both", expand="yes")
        #Pack de la fenêtre, détermine la taille de la fenêtre selon la taille des composants.
        framePerso.pack(fill="both", expand="yes")
    
    #Ajout du bouton pour lancer la simulation
    submit = Button(fenetre, text='OK')
    # Permet au gestionnaire d'événement d'ajouter des paramètres
    #Gestionnaire d'événement pour le clic du bouton
    def gest(evt):
        persosToSave = []
        for i,input_perso in enumerate(values):
            persosToSave.append(dict())
            for inputs_category, input_values in input_perso.items():
                persosToSave[i][inputs_category] = dict()
                for input_name,input_value in input_values.items():
                    persosToSave[i][inputs_category][input_name] = inputs[str(i)+"|"+inputs_category+"|"+input_name].get()
        writeSaveFile(persosToSave)
        LaunchSimu(evt,persosToSave)
    submit.bind("<Button-1>", gest)
    #Mise du bouton sur la droite de la fenetre
    submit.pack(side="right")
    #Remplissage des champs selon la sauvegarde.
    
    #Boucle de la fenêtre. Tant que la fenêtre n'est pas fermé.
    fenetre.mainloop()
    #Quand la fenêtre est fermé, on écrit le fichier de sauvegarde
    


if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    
    
    main()