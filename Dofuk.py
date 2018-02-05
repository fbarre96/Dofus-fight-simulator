# -*- coding: utf-8 -*
import platform
os = platform.system()
if "Windows" in os:
    from Tkinter import Tk
    from Tkinter import LabelFrame
    from Tkinter import Label
    from Tkinter import StringVar
    from Tkinter import Entry
    from Tkinter import Button
    from ttk import Combobox
    #from tkinter import messagebox
    #from tkinter.filedialog import askopenfilename
else:
    from tkinter import Tk
    from tkinter import LabelFrame
    from tkinter import Label
    from tkinter import StringVar
    from tkinter import Entry
    from tkinter import Button
    from tkinter.ttk import Combobox
    #from tkinter import messagebox
    #from tkinter.filedialog import askopenfilename
from constantes import *
from zones import *
from classes import *
from pygame.locals import *

def BoucleDEvenement(niveau,mouse_xy,sortSelectionne):
    
    continuer = 1
    for event in pygame.event.get():   #On parcours la liste de tous les événements reçus
        if event.type == QUIT:     #Si un de ces événements est de type QUIT
            continuer = 0      #On arrête la boucle
        sortSelectionne=niveau.tourDe.joue(event,niveau,mouse_xy,sortSelectionne)

    if not type(niveau.tourDe) is Personnage:
        sortSelectionne=niveau.tourDe.joue(None,niveau,mouse_xy,sortSelectionne)
    return continuer,sortSelectionne

def Commence_combat(joueur):
    #Initialisation de la bibliothèque Pygame
    
    myfont = pygame.font.SysFont("monospace", 15)
    #Création de la fenêtre
    fenetre = pygame.display.set_mode((width_fenetre,height_fenetre), RESIZABLE)
    #Variable qui continue la boucle si = 1, stoppe si = 0
    pygame.display.set_caption("Dofuk")
    continuer = 1
    monstre = PersonnageMur("Poutch",5000,0,0,0,0,0,0, 0,0,0,0 ,0,0,0,0,0,2, "Poutch.png")
    niveau = Niveau(fenetre, [joueur]+[monstre],myfont)
    sortSelectionne = None
    
    niveau.tourDe.debutTour(niveau)
    #Boucle infinie
    while continuer == 1:
        pygame.time.Clock().tick(30)
        mouse_xy = pygame.mouse.get_pos()
        niveau.afficher(fenetre, sortSelectionne,mouse_xy)
        continuer,sortSelectionne=BoucleDEvenement(niveau,mouse_xy,sortSelectionne)

        
        pygame.display.flip()
    pygame.display.quit()


def LaunchSimu(evt, varClasse, varVie, varFor, varAgi, varCha, varInt,varPui,varDo, varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl):
    pygame.init()
    joueur = Personnage(varClasse.get(),varVie.get(),varFor.get(),varAgi.get(),varCha.get(),varInt.get(),varPui.get(),varDo.get(), varDoFor.get(),varDoAgi.get(),varDoCha.get(),varDoInt.get(),varDoPou.get(),varPM.get(),varPA.get(),varPO.get(),varLvl.get(),1,varClasse.get()+".png")
    Commence_combat(joueur)


def readSaveFile(varClasse, varVie,varFor, varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou, varPM,varPA,varPO,varLvl):
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
    fenetre = Tk()
    frameCaracs = LabelFrame(fenetre, text="Caracteristiques")
    # Quel classe a été sélectionné ?
    labelClasse = Label(frameCaracs, text="Classe")
    valeurClasse = (u"Xélor", u"Iop", u"Crâ")
    varClasse = StringVar()
    listeClasse = Combobox(frameCaracs, textvariable = varClasse, \
        values = valeurClasse, state = 'readonly')
    listeClasse.set(valeurClasse[0])
    labelVie = Label(frameCaracs, text="Vie")
    varVie = StringVar()
    entreeVie = Entry(frameCaracs, textvariable = varVie)
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
    
    varDoPou = StringVar()
    labelDoPou = Label(frameCaracs, text="Do Pou")
    entreeDoPou = Entry(frameCaracs, textvariable = varDoPou)
    
    labelPM = Label(frameCaracs, text="PM")
    varPM = StringVar()
    entreePM = Entry(frameCaracs, textvariable = varPM)
    labelPA = Label(frameCaracs, text="PA")
    varPA = StringVar()
    entreePA = Entry(frameCaracs, textvariable = varPA)
    labelPO = Label(frameCaracs, text="PO")
    varPO = StringVar()
    entreePO = Entry(frameCaracs, textvariable = varPO)

    labelLvl = Label(frameCaracs, text="level")
    varLvl = StringVar()
    entreeLvl = Entry(frameCaracs, textvariable = varLvl)
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
    frameCaracs.pack(fill="both", expand="yes")
    submit = Button(fenetre, text='OK')
    # Permet au gestionnaire d'événement d'ajouter des paramètres
    def gest(evt):
        LaunchSimu(evt, varClasse, varVie,varFor, varAgi, varCha, varInt,varPui,varDo, varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)
    submit.bind("<Button-1>", gest)
    submit.pack(side="right")
    readSaveFile(varClasse, varFor, varVie,varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)
    fenetre.mainloop()
    writeSaveFile(varClasse, varFor, varVie,varAgi, varCha, varInt,varPui,varDo,varDoFor,varDoAgi,varDoCha,varDoInt,varDoPou,varPM,varPA,varPO,varLvl)


if __name__ == "__main__":
    #Importation des bibliothèques nécessaires
    #TODO : Modularite
    
    
    main()