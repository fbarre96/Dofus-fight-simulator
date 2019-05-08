# -*- coding: utf-8 -*

from tkinter import Tk
from tkinter import LabelFrame
from tkinter import Label
from tkinter import StringVar
from tkinter import Entry
from tkinter import Button
from tkinter import END
from tkinter.ttk import Combobox
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

def Commence_combat(joueur,enemy):
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
    monstre = enemy
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


def LaunchSimu(evt, inputs, enemy_inputs):
    """@summary: Lance la simulation de combat
    @evt: l'événement qui lance la simulation
    @type: Event
    @inputs: dictionary of inputs
    @type: dict
    """
    pygame.init()
    vie = int(inputs["Vie"].get())
    fo = int(inputs["Force"].get())
    agi = int(inputs["Agilite"].get())
    cha = int(inputs["Chance"].get())
    inte = int(inputs["Intelligence"].get())
    pui = int(inputs["Puissance"].get())
    do = int(inputs["Dommages"].get())
    doFo = int(inputs["Do Force"].get())
    doAgi = int(inputs["Do Agilite"].get())
    doCha = int(inputs["Do Chance"].get())
    doInt = int(inputs["Do Intelligence"].get())
    doPou = int(inputs["Do Pou"].get())
    esqPA = int(inputs["Esquive PA"].get())
    esqPM = int(inputs["Esquive PM"].get())
    retPA = int(inputs["Retrait PA"].get())
    retPM = int(inputs["Retrait PM"].get())
    PM = int(inputs["PM"].get())
    PA = int(inputs["PA"].get())
    PO = int(inputs["PO"].get())
    Level = int(inputs["Level"].get())
    Classe = str(inputs["Classe"].get())

    enemy_vie = int(enemy_inputs["Vie"].get())
    enemy_fo = int(enemy_inputs["Force"].get())
    enemy_agi = int(enemy_inputs["Agilite"].get())
    enemy_cha = int(enemy_inputs["Chance"].get())
    enemy_inte = int(enemy_inputs["Intelligence"].get())
    enemy_pui = int(enemy_inputs["Puissance"].get())
    enemy_do = int(enemy_inputs["Dommages"].get())
    enemy_doFo = int(enemy_inputs["Do Force"].get())
    enemy_doAgi = int(enemy_inputs["Do Agilite"].get())
    enemy_doCha = int(enemy_inputs["Do Chance"].get())
    enemy_doInt = int(enemy_inputs["Do Intelligence"].get())
    enemy_doPou = int(enemy_inputs["Do Pou"].get())
    enemy_esqPA = int(enemy_inputs["Esquive PA"].get())
    enemy_esqPM = int(enemy_inputs["Esquive PM"].get())
    enemy_retPA = int(enemy_inputs["Retrait PA"].get())
    enemy_retPM = int(enemy_inputs["Retrait PM"].get())
    enemy_PM = int(enemy_inputs["PM"].get())
    enemy_PA = int(enemy_inputs["PA"].get())
    enemy_PO = int(enemy_inputs["PO"].get())
    enemy_Level = int(enemy_inputs["Level"].get())
    enemy_Classe = str(enemy_inputs["Classe"].get())
    joueur = Personnages.Personnage(Classe,vie,fo,agi,cha,inte,pui,do, doFo,doAgi,doCha,doInt,doPou,retPA,retPM,esqPA,esqPM,PM,PA,PO,Level,1,Classe+".png")
    enemy = Personnages.Personnage(enemy_Classe,enemy_vie,enemy_fo,enemy_agi,enemy_cha,enemy_inte,enemy_pui,enemy_do, enemy_doFo,enemy_doAgi,enemy_doCha,enemy_doInt,enemy_doPou,enemy_retPA,enemy_retPM,enemy_esqPA,enemy_esqPM,enemy_PM,enemy_PA,enemy_PO,enemy_Level,2,enemy_Classe+".png")
    Commence_combat(joueur,enemy)


def readSaveFile():
    """@summary: Lit le fichier de sauvegarde de personnage et prérempli les champs tkinter
    """
    try:
        with open("save.txt","r") as f:
            contenu = f.read()
            ret = json.loads(contenu)
            if type(ret) is list:
                return ret
            elif type(ret) is dict:
                return [ret,{}]
    except IOError:
        pass
    except ValueError:
        pass
    return {}

def writeSaveFile(players_tab):
    """@summary: Ecrit le fichier de sauvegarde de personnage avec les champs de tkinter
    """
    try:
        result = []
        for player_input in players_tab:
            values = dict()
            for key in list(player_input.keys()):
                values[key]=player_input[key].get()
            result.append(values)
        with open("save.txt","w") as f:
            f.write(json.dumps(result))

    except IOError:
        pass

def main():
    #Créer la fenêtre Tkinter
    fenetre = Tk()
    frameCaracs = LabelFrame(fenetre, text="Caracteristiques")
    values = readSaveFile()
    keysInputs = ["Classe","Level","Vie","Force","Agilite","Chance","Intelligence","Puissance","Dommages","Do Force","Do Agilite","Do Chance", "Do Intelligence","Do Pou","Retrait PA","Retrait PM","Esquive PA","Esquive PM","PA","PM","PO"]
    inputs = {}
    inputs["Classe"] = Combobox(frameCaracs, textvariable = StringVar(), \
        values = ("Xélor", "Iop", "Crâ","Sram"), state = 'readonly')
    inputs["Vie"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Force"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Agilite"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Chance"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Intelligence"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Puissance"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Dommages"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Do Force"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Do Agilite"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Do Chance"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Do Intelligence"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Do Pou"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Retrait PA"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Retrait PM"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Esquive PA"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Esquive PM"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["PA"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["PM"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["PO"] = Entry(frameCaracs, textvariable = StringVar())
    inputs["Level"] = Entry(frameCaracs, textvariable = StringVar())
    for row,key in enumerate(keysInputs):
        lbl = Label(frameCaracs, text=key)
        lbl.grid(row=row, column=0)
        inputs[key].insert(END,values[0][key])
        inputs[key].grid(row=row, column=1)
    
    enemy_inputs = {}
    enemy_inputs["Classe"] = Combobox(frameCaracs, textvariable = StringVar(), \
        values = ("Poutch", "Xélor", "Iop", "Crâ","Sram"), state = 'readonly')
    enemy_inputs["Vie"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Force"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Agilite"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Chance"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Intelligence"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Puissance"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Dommages"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Do Force"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Do Agilite"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Do Chance"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Do Intelligence"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Do Pou"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Retrait PA"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Retrait PM"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Esquive PA"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Esquive PM"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["PA"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["PM"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["PO"] = Entry(frameCaracs, textvariable = StringVar())
    enemy_inputs["Level"] = Entry(frameCaracs, textvariable = StringVar())
    for row,key in enumerate(keysInputs):
        lbl = Label(frameCaracs, text=key)
        lbl.grid(row=row, column=2)
        try:
            enemy_inputs[key].insert(END,values[1][key])
        except:
            pass
        enemy_inputs[key].grid(row=row, column=3)
    #Pack de la fenêtre, détermine la taille de la fenêtre selon la taille des composants.
    frameCaracs.pack(fill="both", expand="yes")
    
    #Ajout du bouton pour lancer la simulation
    submit = Button(fenetre, text='OK')
    # Permet au gestionnaire d'événement d'ajouter des paramètres
    #Gestionnaire d'événement pour le clic du bouton
    def gest(evt):
        writeSaveFile([inputs,enemy_inputs])
        LaunchSimu(evt, inputs,enemy_inputs)
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