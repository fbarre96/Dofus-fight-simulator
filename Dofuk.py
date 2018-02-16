# -*- coding: utf-8 -*

from Tkinter import Tk
from Tkinter import LabelFrame
from Tkinter import Label
from Tkinter import StringVar
from Tkinter import Entry
from Tkinter import Button
from ttk import Combobox
#from tkinter import messagebox
#from tkinter.filedialog import askopenfilename
import pygame
import constantes
from pygame.locals import *
import Niveau
import Personnages


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

def Commence_combat(joueur):
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
    #Initialisation de l'ennemi
    monstre = Personnages.PersonnageMur("Poutch",5000,0,0,0,0,0,0, 0,0,0,0 ,0,0,0,0,0,2, "Poutch.png")
    #Initialisation du niveau
    niveau = Niveau.Niveau(fenetre, [joueur]+[monstre],myfont)
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


def LaunchSimu(evt, varClasse, varVie, varFor, varAgi, varCha, varInt,varPui,varDo, varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl):
    """@summary: Lance la simulation de combat
    @evt: l'événement qui lance la simulation
    @type: Event
    @varClasse: le nom d'une classe de Dofus. Indique quels sorts seront disponibles.
    @type: tkinter.VarStr
    @varVie: la vie total du personnage
    @type: tkinter.VarStr
    @varFor: la force total du personnage
    @type: tkinter.VarStr
    @varAgi l'agilité total du personnage
    @type: tkinter.VarStr
    @varCha: la chance total du personnage
    @type: tkinter.VarStr
    @varInt: l'intelligence total du personnage
    @type: tkinter.VarStr
    @varPui: la puissance total du personnage
    @type: tkinter.VarStr
    @varDo: les dommages supplémentaires du personnage
    @type: tkinter.VarStr
    @varDoFor: les dommages terre supplémentaires du personnage
    @type: tkinter.VarStr
    @varDoAgi les dommages air supplémentaires du personnage
    @type: tkinter.VarStr
    @varDoCha: les dommages eau supplémentaires du personnage
    @type: tkinter.VarStr
    @varDoInt: les dommages feu supplémentaires du personnage
    @type: tkinter.VarStr
    @varDoPou: les dommages de poussé supplémentaires du personnage
    @type: tkinter.VarStr
    @varPM: les points de mouvement du personnage
    @type: tkinter.VarStr
    @varPA: les points d'actions du personnage
    @type: tkinter.VarStr
    @varPO: les points de portée du personnage
    @type: tkinter.VarStr
    @varLvl: le niveau du personnage
    @type: tkinter.VarStr
    """
    pygame.init()
    joueur = Personnages.Personnage(varClasse.get(),varVie.get(),varFor.get(),varAgi.get(),varCha.get(),varInt.get(),varPui.get(),varDo.get(), varDoFor.get(),varDoAgi.get(),varDoCha.get(),varDoInt.get(),varDoPou.get(),varPM.get(),varPA.get(),varPO.get(),varLvl.get(),1,varClasse.get()+".png")
    Commence_combat(joueur)


def readSaveFile(varClasse, varVie,varFor, varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou, varPM,varPA,varPO,varLvl):
    """@summary: Lit le fichier de sauvegarde de personnage et prérempli les champs tkinter
    @varClasse: le nom d'une classe de Dofus. Indique quels sorts seront disponibles.
    @type: string
    @varVie: la vie total du personnage
    @type: int
    @varFor: la force total du personnage
    @type: int
    @varAgi l'agilité total du personnage
    @type: int
    @varCha: la chance total du personnage
    @type: int
    @varInt: l'intelligence total du personnage
    @type: int
    @varPui: la puissance total du personnage
    @type: int
    @varDo: les dommages supplémentaires du personnage
    @type: int
    @varDoFor: les dommages terre supplémentaires du personnage
    @type: int
    @varDoAgi les dommages air supplémentaires du personnage
    @type: int
    @varDoCha: les dommages eau supplémentaires du personnage
    @type: int
    @varDoInt: les dommages feu supplémentaires du personnage
    @type: int
    @varDoPou: les dommages de poussé supplémentaires du personnage
    @type: int
    @varPM: les points de mouvement du personnage
    @type: int
    @varPA: les points d'actions du personnage
    @type: int
    @varPO: les points de portée du personnage
    @type: int
    @varLvl: le niveau du personnage
    @type: int
    """
    try:
        with open("save.txt","r") as f:
            line = f.readline().strip()
            varClasse.set(line)
            line = f.readline().strip()
            varVie.set(line)
            line = f.readline().strip()
            varFor.set(line)
            line = f.readline().strip()
            varAgi.set(line)
            line = f.readline().strip()
            varCha.set(line)
            line = f.readline().strip()
            varInt.set(line)
            line = f.readline().strip()
            varPui.set(line)
            line = f.readline().strip()
            varDo.set(line)
            line = f.readline().strip()
            varDoFor.set(line)
            line = f.readline().strip()
            varDoAgi.set(line)
            line = f.readline().strip()
            varDoCha.set(line)
            line = f.readline().strip()
            varDoInt.set(line)
            line = f.readline().strip()
            varDoPou.set(line)
            line = f.readline().strip()
            varPM.set(line)
            line = f.readline().strip()
            varPA.set(line)
            line = f.readline().strip()
            varPO.set(line)
            line = f.readline().strip()
            varLvl.set(line)
    except IOError:
        pass

def writeSaveFile(varClasse, varVie,varFor, varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl):
    """@summary: Ecrit le fichier de sauvegarde de personnage avec les champs de tkinter
    @varClasse: le nom d'une classe de Dofus. Indique quels sorts seront disponibles.
    @type: string
    @varVie: la vie total du personnage
    @type: int
    @varFor: la force total du personnage
    @type: int
    @varAgi l'agilité total du personnage
    @type: int
    @varCha: la chance total du personnage
    @type: int
    @varInt: l'intelligence total du personnage
    @type: int
    @varPui: la puissance total du personnage
    @type: int
    @varDo: les dommages supplémentaires du personnage
    @type: int
    @varDoFor: les dommages terre supplémentaires du personnage
    @type: int
    @varDoAgi les dommages air supplémentaires du personnage
    @type: int
    @varDoCha: les dommages eau supplémentaires du personnage
    @type: int
    @varDoInt: les dommages feu supplémentaires du personnage
    @type: int
    @varDoPou: les dommages de poussé supplémentaires du personnage
    @type: int
    @varPM: les points de mouvement du personnage
    @type: int
    @varPA: les points d'actions du personnage
    @type: int
    @varPO: les points de portée du personnage
    @type: int
    @varLvl: le niveau du personnage
    @type: int
    """
    try:
        with open("save.txt","w") as f:
            f.write(varClasse.get().encode("utf-8")+"\n")
            f.write(varVie.get()+"\n")
            f.write(varFor.get()+"\n")
            f.write(varAgi.get()+"\n")
            f.write(varCha.get()+"\n")
            f.write(varInt.get()+"\n")
            f.write(varPui.get()+"\n")
            f.write(varDo.get()+"\n")
            f.write(varDoFor.get()+"\n")
            f.write(varDoAgi.get()+"\n")
            f.write(varDoCha.get()+"\n")
            f.write(varDoInt.get()+"\n")
            f.write(varDoPou.get()+"\n")
            f.write(varPM.get()+"\n")
            f.write(varPA.get()+"\n")
            f.write(varPO.get()+"\n")
            f.write(varLvl.get()+"\n")

    except IOError:
        pass

def main():
    #Créer la fenêtre Tkinter
    fenetre = Tk()
    frameCaracs = LabelFrame(fenetre, text="Caracteristiques")
    # Sélection de classe
    labelClasse = Label(frameCaracs, text="Classe")
    valeurClasse = (u"Xélor", u"Iop", u"Crâ",u"Sram")
    varClasse = StringVar()
    listeClasse = Combobox(frameCaracs, textvariable = varClasse, \
        values = valeurClasse, state = 'readonly')
    listeClasse.set(valeurClasse[0])
    # Input Vie
    labelVie = Label(frameCaracs, text="Vie")
    varVie = StringVar()
    entreeVie = Entry(frameCaracs, textvariable = varVie)
    # Input Caractéristiques de bases
    labelFor = Label(frameCaracs, text="Force")
    varFor = StringVar()
    entreeFor = Entry(frameCaracs, textvariable = varFor)
    labelAgi = Label(frameCaracs, text="Agilite")
    varAgi = StringVar()
    entreeAgi = Entry(frameCaracs, textvariable = varAgi)
    labelCha = Label(frameCaracs, text="Chance")
    varCha = StringVar()
    entreeCha = Entry(frameCaracs, textvariable = varCha)
    labelInt = Label(frameCaracs, text="Intelligence")
    varInt = StringVar()
    entreeInt = Entry(frameCaracs, textvariable = varInt)
    labelPui = Label(frameCaracs, text="Puissance")
    varPui = StringVar()
    entreePui = Entry(frameCaracs, textvariable = varPui)
    # Input Caractéristiques de dommages
    labelDo = Label(frameCaracs, text="Dommages")
    varDo = StringVar()
    entreeDo = Entry(frameCaracs, textvariable = varDo)
    labelDoFor = Label(frameCaracs, text="Do Force")
    varDoFor = StringVar()
    entreeDoFor = Entry(frameCaracs, textvariable = varDoFor)
    labelDoAgi = Label(frameCaracs, text="Do Agilite")
    varDoAgi = StringVar()
    entreeDoAgi = Entry(frameCaracs, textvariable = varDoAgi)
    labelDoCha = Label(frameCaracs, text="Do Chance")
    varDoCha = StringVar()
    entreeDoCha = Entry(frameCaracs, textvariable = varDoCha)
    labelDoInt = Label(frameCaracs, text="Do Intelligence")
    varDoInt = StringVar()
    entreeDoInt = Entry(frameCaracs, textvariable = varDoInt)
    # Input Dommages de poussé
    varDoPou = StringVar()
    labelDoPou = Label(frameCaracs, text="Do Pou")
    entreeDoPou = Entry(frameCaracs, textvariable = varDoPou)
    # Input Caractéristiques de personnage
    labelPM = Label(frameCaracs, text="PM")
    varPM = StringVar()
    entreePM = Entry(frameCaracs, textvariable = varPM)
    labelPA = Label(frameCaracs, text="PA")
    varPA = StringVar()
    entreePA = Entry(frameCaracs, textvariable = varPA)
    labelPO = Label(frameCaracs, text="PO")
    varPO = StringVar()
    entreePO = Entry(frameCaracs, textvariable = varPO)
    # Input level
    labelLvl = Label(frameCaracs, text="level")
    varLvl = StringVar()
    entreeLvl = Entry(frameCaracs, textvariable = varLvl)
    # Positionnement des éléments dans la fenêtre sous forme de tableau 2 colonnes X lignes
    r = 0
    labelClasse.grid(row=r, column=0)
    listeClasse.grid(row=r, column=1)
    r+=1
    labelVie.grid(row=r, column=0)
    entreeVie.grid(row=r, column=1)
    r+=1
    labelFor.grid(row=r, column=0)
    entreeFor.grid(row=r, column=1)
    r+=1
    labelAgi.grid(row=r, column=0)
    entreeAgi.grid(row=r, column=1)
    r+=1
    labelCha.grid(row=r, column=0)
    entreeCha.grid(row=r, column=1)
    r+=1
    labelInt.grid(row=r, column=0)
    entreeInt.grid(row=r, column=1)
    r+=1
    labelPui.grid(row=r, column=0)
    entreePui.grid(row=r, column=1)
    r+=1
    labelDo.grid(row=r, column=0)
    entreeDo.grid(row=r, column=1)
    r+=1
    labelDoFor.grid(row=r, column=0)
    entreeDoFor.grid(row=r, column=1)
    r+=1
    labelDoAgi.grid(row=r, column=0)
    entreeDoAgi.grid(row=r, column=1)
    r+=1
    labelDoCha.grid(row=r, column=0)
    entreeDoCha.grid(row=r, column=1)
    r+=1
    labelDoInt.grid(row=r, column=0)
    entreeDoInt.grid(row=r, column=1)
    r+=1
    labelDoPou.grid(row=r, column=0)
    entreeDoPou.grid(row=r, column=1)
    r+=1
    labelPM.grid(row=r, column=0)
    entreePM.grid(row=r, column=1)
    r+=1
    labelPA.grid(row=r, column=0)
    entreePA.grid(row=r, column=1)
    r+=1
    labelPO.grid(row=r, column=0)
    entreePO.grid(row=r, column=1)
    r+=1
    labelLvl.grid(row=r, column=0)
    entreeLvl.grid(row=r, column=1)
    r+=1
    #Pack de la fenêtre, détermine la taille de la fenêtre selon la taille des composants.
    frameCaracs.pack(fill="both", expand="yes")
    #Ajout du bouton pour lancer la simulation
    submit = Button(fenetre, text='OK')
    # Permet au gestionnaire d'événement d'ajouter des paramètres
    #Gestionnaire d'événement pour le clic du bouton
    def gest(evt):
        LaunchSimu(evt, varClasse, varVie,varFor, varAgi, varCha, varInt,varPui,varDo, varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)
    submit.bind("<Button-1>", gest)
    #Mise du bouton sur la droite de la fenetre
    submit.pack(side="right")
    #Remplissage des champs selon la sauvegarde.
    readSaveFile(varClasse, varFor, varVie,varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)
    #Boucle de la fenêtre. Tant que la fenêtre n'est pas fermé.
    fenetre.mainloop()
    #Quand la fenêtre est fermé, on écrit le fichier de sauvegarde
    writeSaveFile(varClasse, varFor, varVie,varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)


if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    
    
    main()