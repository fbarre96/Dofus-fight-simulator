import tkinter as tk
import tkinter.ttk as ttk
import sys
import json
from PIL import Image, ImageTk
import os
from importlib import import_module
from dofus_sorts_downloader import normaliser
from Effets.Effet import Effet, ChildDialogEffect
from EffectsTreeview import EffectsTreeview
from copy import deepcopy
import Zones

class ChildDialogNouveauSort:
    def __init__(self, parent):
        """
        Open a child dialog of a tkinter application to edit an effect.

        Args:
            parent: the tkinter parent view to use for this window construction.
            effect: Effect to edit.
        """
        self.parent = parent
        self.app = tk.Toplevel(parent)
        self.app.resizable(False, False)
        self.rvalue = None
        self.parent = parent
        self.initUI()
        try:
            self.app.wait_visibility()
            self.app.transient(parent)
            self.app.grab_set()
        except tk.TclError:
            pass
    
    def initUI(self):
        appFrame = ttk.Frame(self.app)
        sortFrame = ttk.Frame(appFrame)
        sortLbl = ttk.Label(sortFrame, text="Nom du sort :")
        sortLbl.pack(side="left")
        self.sortEntry = ttk.Entry(sortFrame, width=50)
        self.sortEntry.pack(side="left")
        sortFrame.pack()
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.pack(pady=10)
        appFrame.pack(ipadx=10, ipady=10)

    def onOk(self):
        """
        Called when the user clicked the validation button.
        """
        self.rvalue = self.sortEntry.get()
        self.app.destroy()


class OpeningPage:
    def __init__(self, fenetre, outfilename, sort_values, iconFolder):
        self.lastOpenSpell = None
        self.outfilename = outfilename
        self.sorts_values = sort_values
        self.fenetre = fenetre
        self.iconFolder = iconFolder
        self.spellIcons = {}
        self.paSpinboxs = {}
        self.poMinSpinboxs = {}
        self.poMaxSpinboxs = {}
        self.poModValues = {}
        self.chaineValues = {}
        self.ldvValues = {}
        self.normalEffectTables = {}
        self.criticalEffectTables = {}
        self.typeLancerComboboxs = {}
        self.probaCritSpinboxs = {}
        self.nbLanceTourSpinboxs = {}
        self.nbLanceTourParJoueurSpinboxs = {}
        self.nbTourEntreDeuxLancerSpinboxs = {}
        self.levelObtentionValues = {}
        self.levelNotebook = None
        self.imgLbl = None
        self.titleLbl = None
        self.descLbl = None
        
        effectlist = os.listdir("Effets")
        for effect in effectlist:
            if not effect.startswith("__") and effect.endswith(".py"):
                import_module("Effets."+effect[:-3])
        effectlist = os.listdir("Etats")
        for effect in effectlist:
            if not effect.startswith("__") and effect.endswith(".py"):
                import_module("Etats."+effect[:-3])
        self.initUI()
        

    def editFrameUI(self, spellname=""):
        spell = self.sorts_values.get(spellname, dict())
        titleFrame = ttk.Frame(self.editframe)
        self.imgLbl = tk.Label(titleFrame, image=self.spellIcons.get(spellname), anchor="nw")
        self.imgLbl.pack(side="left", expand="no", anchor="nw", padx=25, pady=10)
        self.titleLbl = ttk.Label(titleFrame, anchor="center", text="Titre du sort", font=("Helvetica", 38, 'bold'))
        self.titleLbl.pack(side="left", fill=tk.BOTH, expand=True)
        titleFrame.pack(side="top", fill=tk.X)
        descFrame = ttk.Frame(self.editframe)
        self.descLbl = ttk.Label(descFrame, text="description du sort", font=("Helvetica", 12))
        self.descLbl.pack(side="left", expand="yes")
        descFrame.pack(side="top", fill=tk.X)
        debutCombatFrame = ttk.Frame(self.editframe)
        debutCombatLabel = ttk.Label(debutCombatFrame, text="Sort de début de combat:")
        debutCombatLabel.pack(side="left")
        self.debutCombatValue = tk.BooleanVar()
        debutCombatCheckbutton = ttk.Checkbutton(debutCombatFrame, variable=self.debutCombatValue)
        debutCombatCheckbutton.pack(side="left")
        debutCombatFrame.pack(side="top")
        lancableParJoueurFrame = ttk.Frame(self.editframe)
        lancableParJoueurLabel = ttk.Label(lancableParJoueurFrame, text="Sort lancable par le joueur:")
        lancableParJoueurLabel.pack(side="left")
        self.lancableParJoueurValue = tk.BooleanVar()
        lancableParJoueurCheckbutton = ttk.Checkbutton(lancableParJoueurFrame, variable=self.lancableParJoueurValue)
        lancableParJoueurCheckbutton.pack(side="left")
        lancableParJoueurFrame.pack(side="top")
        self.levelNotebook = ttk.Notebook(self.editframe)
        for i in range(1, 4):
            levelFrame = ttk.Frame(self.levelNotebook)
            mainCaracsFrame = ttk.Frame(levelFrame)
            paLbl = ttk.Label(mainCaracsFrame, text="PA:")
            paLbl.pack(side="left")
            self.paSpinboxs[str(i)] = tk.Spinbox(mainCaracsFrame, from_=0, to=12, width=3)
            self.paSpinboxs[str(i)].pack(side="left")
            poMinLabel = ttk.Label(mainCaracsFrame, text="PO ")
            poMinLabel.pack(side="left")
            self.poMinSpinboxs[str(i)] = tk.Spinbox(mainCaracsFrame, from_=0, to=99, width=3)
            self.poMinSpinboxs[str(i)].pack(side="left")
            
            poMaxLabel = ttk.Label(mainCaracsFrame, text=" - ")
            poMaxLabel.pack(side="left")
            self.poMaxSpinboxs[str(i)] = tk.Spinbox(mainCaracsFrame, from_=0, to=99, width=3)
            self.poMaxSpinboxs[str(i)].pack(side="left")
            poModLabel = ttk.Label(mainCaracsFrame, text="PO modifiable:")
            poModLabel.pack(side="left")
            self.poModValues[str(i)] = tk.IntVar()
            
            poModCheckbutton = ttk.Checkbutton(mainCaracsFrame, variable=self.poModValues[str(i)])
            poModCheckbutton.pack(side="left")
            mainCaracsFrame.pack(fill=tk.X, side="top", anchor='nw', padx=10, pady=5)
            effectsFrame = ttk.Frame(levelFrame)
            effectsFrame.rowconfigure(0, weight=1)
            effectsFrame.columnconfigure(0, weight=6)
            effectsFrame.columnconfigure(1, weight=1)
            effectsFrame.columnconfigure(2, weight=6)
            self.normalEffectTables[str(i)] = EffectsTreeview(effectsFrame, "Effets normaux:")
            self.normalEffectTables[str(i)].grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)

            buttonsEffectFrame = ttk.Frame(effectsFrame)
            normalToCritButton = ttk.Button(buttonsEffectFrame, text=">>", command=lambda:self.normalToCrit())
            normalToCritButton.pack()
            precLvlImportButton = ttk.Button(buttonsEffectFrame, text="<<Lvl-1", command=lambda: self.importFromPrecLevel())
            precLvlImportButton.pack()
            buttonsEffectFrame.grid(row=0, column=1, padx=5, pady=5)
            self.criticalEffectTables[str(i)] = EffectsTreeview(effectsFrame, "Effets critiques:")
            self.criticalEffectTables[str(i)].grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
            effectsFrame.pack(fill=tk.X, side="top")
            subCaracsFrame = ttk.Frame(levelFrame)
            chaineLabel = ttk.Label(subCaracsFrame, text="Effets chainés:")
            chaineLabel.grid(row=0, column=0, sticky="e", pady=5)
            self.chaineValues[str(i)] = tk.IntVar()
            chaineCheckbutton = ttk.Checkbutton(subCaracsFrame, variable=self.chaineValues[str(i)])
            chaineCheckbutton.grid(row=0, column=1, sticky="w", pady=5)
            
            ldvLabel = ttk.Label(subCaracsFrame, text="Ligne de vue:")
            ldvLabel.grid(row=1, column=0, sticky="e", pady=5)
            self.ldvValues[str(i)] = tk.IntVar()
            ldvCheckbutton = ttk.Checkbutton(subCaracsFrame, variable=self.ldvValues[str(i)])
            ldvCheckbutton.grid(row=1, column=1, sticky="w", pady=5)

            typeLancerLabel = ttk.Label(subCaracsFrame, text="Type de lancer:")
            typeLancerLabel.grid(row=2, column=0, sticky="e", pady=5)
            self.typeLancerComboboxs[str(i)] = ttk.Combobox(subCaracsFrame, values=["cercle", "ligne", "diagonale"], state="readonly")
            
            self.typeLancerComboboxs[str(i)].grid(row=2, column=1, sticky="w", pady=5)

            probaCritLabel = ttk.Label(subCaracsFrame, text="Proba. Critique:")
            probaCritLabel.grid(row=3, column=0, sticky="e", pady=5)
            self.probaCritSpinboxs[str(i)] = tk.Spinbox(subCaracsFrame, from_=0, to=100, width=3)
            
            self.probaCritSpinboxs[str(i)].grid(row=3, column=1, sticky="w", pady=5)

            nbLanceTourLabel = ttk.Label(subCaracsFrame, text="Nb. lancer par tour:")
            nbLanceTourLabel.grid(row=4, column=0, sticky="e", pady=5)
            self.nbLanceTourSpinboxs[str(i)] = tk.Spinbox(subCaracsFrame, from_=1, to=99, width=3)
            self.nbLanceTourSpinboxs[str(i)] .grid(row=4, column=1, sticky="w", pady=5)

            nbLanceTourParJoueurLabel = ttk.Label(subCaracsFrame, text="Nb. lancer par tour par joueur:")
            nbLanceTourParJoueurLabel.grid(row=5, column=0, sticky="e", pady=5)
            self.nbLanceTourParJoueurSpinboxs[str(i)] = tk.Spinbox(subCaracsFrame, from_=1, to=99, width=3)
            self.nbLanceTourParJoueurSpinboxs[str(i)].grid(row=5, column=1, sticky="w", pady=5)

            nbTourEntreDeuxLancerLabel = ttk.Label(subCaracsFrame, text="Nb. tour entre 2:")
            nbTourEntreDeuxLancerLabel.grid(row=6, column=0, sticky="e", pady=5)
            self.nbTourEntreDeuxLancerSpinboxs[str(i)] = tk.Spinbox(subCaracsFrame, from_=0, to=99, width=3)
            
            self.nbTourEntreDeuxLancerSpinboxs[str(i)].grid(row=6, column=1, sticky="w", pady=5)
            
            levelObtentionLbl = ttk.Label(subCaracsFrame, text="Change level to:")
            levelObtentionLbl.grid(row=7, column=0, sticky="e", pady=15)
            self.levelObtentionValues[str(i)] = tk.StringVar()
            self.levelObtentionValues[str(i)].trace("w", lambda name, index, mode, var=self.levelObtentionValues[str(i)], i=i: 
                self.levelModified(var, i))
            levelObtentionEntry = ttk.Entry(subCaracsFrame, width=3, textvariable=self.levelObtentionValues[str(i)])
            levelObtentionEntry.grid(row=7, column=1, sticky="w", pady=15)

            subCaracsFrame.pack(side="top", fill=tk.BOTH, padx=10, pady=5)
            levelFrame.pack(fill=tk.BOTH, padx=10, pady=5)
            self.levelNotebook.add(levelFrame, text="  "+"lvl"+" ")
        
        self.levelNotebook.pack(side="top", fill=tk.BOTH, expand="yes")
        okButton = ttk.Button(self.editframe, text="Appliquer", command=lambda: self.saveSpell())
        okButton.pack(anchor="center", side="bottom")
        self.editframe.pack(fill=tk.BOTH)
        if spellname != "":
            self.openSpell(spellname)

    def levelModified(self, var, indexLevel):
        newValue = var.get()
        self.levelNotebook.tab(int(indexLevel)-1, text="   "+str(newValue)+"   ")


    def normalToCrit(self):
        lvl = self.levelNotebook.index(self.levelNotebook.select())+1
        children = self.criticalEffectTables[str(lvl)].get_children()
        for child in children:
            self.criticalEffectTables[str(lvl)].delete(child)
        self.criticalEffectTables[str(lvl)].effectsValues.clear()
        effetDict = self.normalEffectTables[str(lvl)].effectsValues
        for key, val in effetDict.items():
            self.criticalEffectTables[str(lvl)].effectsValues[key] = deepcopy(val)
            self.criticalEffectTables[str(lvl)].insert('', 'end', str(key), text=str(self.criticalEffectTables[str(lvl)].effectsValues[key]))
    
    def importFromPrecLevel(self):
        precLvl = self.levelNotebook.index(self.levelNotebook.select())
        if precLvl == 0:
            return
        currentLvl = self.levelNotebook.index(self.levelNotebook.select())+1
        children = self.normalEffectTables[str(currentLvl)].get_children()
        for child in children:
            self.normalEffectTables[str(currentLvl)].delete(child)
        self.normalEffectTables[str(currentLvl)].effectsValues.clear()
        effetDict = self.normalEffectTables[str(precLvl)].effectsValues
        for key, val in effetDict.items():
            self.normalEffectTables[str(currentLvl)].effectsValues[key] = deepcopy(val)
            self.normalEffectTables[str(currentLvl)].insert('', 'end', str(key), text=str(self.normalEffectTables[str(currentLvl)].effectsValues[key]))
    
    def saveSpell(self):
        spellname = self.lastOpenSpell
        spell = self.sorts_values[spellname]
        spell["desc"] = self.descLbl.cget("text")
        spell["debutCombat"] = self.debutCombatValue.get()
        spell["lancableParJoueur"] = self.lancableParJoueurValue.get()
        for i in range(1, 4):
            level = self.levelNotebook.tab(i-1, option="text")
            if str(i) not in spell.keys() and level == "N/A":
                continue
            elif str(i) not in spell.keys():
                spell[str(i)] = {"Autres":{}, "level":level}
                spellAtLevel = spell[str(i)]
            else:
                spellAtLevel = spell[str(i)]
            spellAtLevel["level"] = level
            if spellAtLevel["level"] == "N/A":
                del self.sorts_values[spellname][str(i)]
                continue
            spellAtLevel["PA"] = str(self.paSpinboxs[str(i)].get())
            spellAtLevel["PO_min"] = str(self.poMinSpinboxs[str(i)].get())
            spellAtLevel["PO_max"] = str(self.poMaxSpinboxs[str(i)].get())
            spellAtLevel["Autres"]["Portée modifiable"] = "Oui" if self.poModValues[str(i)].get() == 1 else "Non"
            spellAtLevel["Autres"]["Chaîné"] = "Oui" if self.chaineValues[str(i)].get() == 1 else "Non"
            spellAtLevel["Autres"]["Ligne de vue"] = "Oui" if self.ldvValues[str(i)].get() == 1 else "Non"
            spellAtLevel["Autres"]["Lancer en diagonale"] = "Oui" if self.typeLancerComboboxs[str(i)].get() == "diagonale" else "Non"
            spellAtLevel["Autres"]["Lancer en ligne"] = "Oui" if self.typeLancerComboboxs[str(i)].get() == "ligne" else "Non"
            spellAtLevel["Autres"]["Probabilité de coup critique"] = str(self.probaCritSpinboxs[str(i)].get())+"%"
            spellAtLevel["Autres"]["Nb. de lancers par tour"] = str(self.nbLanceTourSpinboxs[str(i)].get())
            spellAtLevel["Autres"]["Nb. de lancers par tour par joueur"] = str(self.nbLanceTourParJoueurSpinboxs[str(i)].get())
            spellAtLevel["Autres"]["Nb. de tours entre deux lancers"] = str(self.nbTourEntreDeuxLancerSpinboxs[str(i)].get())
            spellAtLevel["Effets"] = []
            for effectsValue in self.normalEffectTables[str(i)].effectsValues.values():
                if effectsValue is not None:
                    spellAtLevel["Effets"].append(effectsValue.getAllInfos())
            spellAtLevel["EffetsCritiques"] = []
            for effectsValue in self.criticalEffectTables[str(i)].effectsValues.values():
                if effectsValue is not None:
                    spellAtLevel["EffetsCritiques"].append(effectsValue.getAllInfos())
            self.sorts_values[spellname][str(i)] = spellAtLevel
        with open(outfilename, "w") as f:
            f.write(json.dumps(self.sorts_values))

    def initUI(self):
        #PANED PART
        self.paned = tk.PanedWindow(self.fenetre, height=800)
        #RIGHT PANE : Canvas + frame
        self.editframe = ttk.Frame(self.paned)
        #LEFT PANE : Treeview
        self.frameTw = ttk.Frame(self.paned)
        style = ttk.Style(self.fenetre)
        style.configure('new.Treeview', rowheight=55)
        style.configure('TFrame', background='white')
        style.configure('TLabel', background='white')

        self.treevw = ttk.Treeview(self.frameTw, show="tree", style="new.Treeview")
        for spellname in self.sorts_values.keys():
            try:
                root_pic1 = Image.open(os.path.join(self.iconFolder, normaliser(spellname)+".png"))                       # Open the image like this first
                self.spellIcons[spellname] = ImageTk.PhotoImage(root_pic1)      # Then with PhotoImage. NOTE: self.root_pic2 =     and not     root_pic2 =
            except:
                self.spellIcons[spellname] = None
            if self.spellIcons[spellname] is not None:
                self.treevw.insert('', 'end', spellname, text=spellname, image=self.spellIcons[spellname])
            else:
                self.treevw.insert('', 'end', spellname, text=spellname)
        scbVSel = ttk.Scrollbar(self.frameTw,
                                orient=tk.VERTICAL,
                                command=self.treevw.yview)
        self.treevw.configure(yscrollcommand=scbVSel.set)
        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        scbVSel.grid(row=0, column=1, sticky=tk.NS)
        default_spellname = ""
        if self.sorts_values:
            default_spellname = list(self.sorts_values.keys())[0]
        self.editFrameUI(default_spellname)
        self.paned.add(self.frameTw)
        self.paned.add(self.editframe)
        self.paned.pack(fill=tk.BOTH, expand=1)
        addSortButton = ttk.Button(self.frameTw, text="Ajouter un sort", command=self.addSort)
        addSortButton.grid(row=1, column=0, sticky=tk.S)
        self.frameTw.rowconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.frameTw.columnconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.treevw.bind("<<TreeviewSelect>>", self.onTreeviewSelect)

    def addSort(self, event=None):
        sortDialog = ChildDialogNouveauSort(self.fenetre)
        self.fenetre.wait_window(sortDialog.app)
        if sortDialog.rvalue is not None:
            self.sorts_values[sortDialog.rvalue] = {}
            self.treevw.insert("", "end", sortDialog.rvalue, text=sortDialog.rvalue)
       
        
        

    def onTreeviewSelect(self, _event=None):
        """Called when a line is selected on the treeview
        Open the selected object view on the view frame.
        Args:
            _event: not used but mandatory
        """
        selection = self.treevw.selection()
        if len(selection) == 1:
            item = selection[0]
            self.openSpell(item)

    def openSpell(self, spellname):
        self.lastOpenSpell = spellname
        spell = self.sorts_values.get(spellname, {"desc":""})
        self.imgLbl.configure(image=self.spellIcons.get(spellname))
        self.titleLbl.configure(text=spellname)
        self.descLbl.configure(text=spell.get("desc", ""))
        self.debutCombatValue.set(spell.get("debutCombat", False))
        self.lancableParJoueurValue.set(spell.get("lancableParJoueur", True))
        lastLevel = 0
        for i in range(1, 4):
            self.levelNotebook.tab(i-1, text=str("N/A"))
            if str(i) not in spell.keys():
                spellAtLevel= {"Autres":{}, "level":"1"}
            else:
                spellAtLevel = spell[str(i)]
            self.paSpinboxs[str(i)].delete(0, "end")
            self.paSpinboxs[str(i)].insert(0, int(spellAtLevel.get("PA", 0)))
            self.poMaxSpinboxs[str(i)].delete(0, "end")
            self.poMaxSpinboxs[str(i)].insert(0, int(spellAtLevel.get("PO_max", 0)))
            self.poMinSpinboxs[str(i)].delete(0, "end")
            self.poMinSpinboxs[str(i)].insert(0, int(spellAtLevel.get("PO_min", 0)))
            self.poModValues[str(i)].set(1 if spellAtLevel["Autres"].get("Portée modifiable", "Non") == "Oui" else 0)
            zone = Zones.TypeZone.factory(spellAtLevel["Autres"].get("Zone d'effet", ""), spell.get("desc", ""))
            tailleZone = zone.zonePO
            typeZone = zone.__class__.__name__.replace("TypeZone", '')
            listOfEffect = {}
            for children in self.normalEffectTables[str(i)].get_children():
                self.normalEffectTables[str(i)].delete(children)
            for children in self.criticalEffectTables[str(i)].get_children():
                self.criticalEffectTables[str(i)].delete(children)
            for effect_i, effect_infos in enumerate(spellAtLevel.get("Effets", [])):
                craftedEffect = Effet.effectFactory(effect_infos, tailleZone=tailleZone, typeZone=typeZone, desc=spell.get("desc", ""), nomSort=spellname)
                listOfEffect[str(effect_i)] = craftedEffect
                self.normalEffectTables[str(i)].insert('', 'end', str(effect_i), text=str(craftedEffect))
            self.normalEffectTables[str(i)].effectsValues = listOfEffect
            listOfEffect = {}
            for effect_i, effect_infos in enumerate(spellAtLevel.get("EffetsCritiques", [])):
                craftedEffect = Effet.effectFactory(effect_infos, tailleZone=tailleZone, typeZone=typeZone, desc=spell.get("desc", ""), nomSort=spellname)
                listOfEffect[str(effect_i)] = craftedEffect
                self.criticalEffectTables[str(i)].insert('', 'end', str(effect_i), text=str(craftedEffect))
            self.criticalEffectTables[str(i)].effectsValues = listOfEffect
            self.chaineValues[str(i)].set(1 if spellAtLevel["Autres"].get("Chaîné", "Oui") == "Oui" else 0) # N'existe pas sur le site officiel
            self.ldvValues[str(i)].set(1 if spellAtLevel["Autres"].get("Ligne de vue", "Oui") == "Oui" else 0)
            if spellAtLevel["Autres"].get("Lancer en diagonale", "Non") == "Oui": # N'existe pas sur le site officiel
                self.typeLancerComboboxs[str(i)].set("diagonale")
            elif spellAtLevel["Autres"].get("Lancer en ligne", "Non") == "Oui":
                self.typeLancerComboboxs[str(i)].set("ligne")
            else:
                if "diagonale" in spell.get("desc", ""):
                    self.typeLancerComboboxs[str(i)].set("diagonale")
                else:
                    self.typeLancerComboboxs[str(i)].set("cercle")
            self.nbTourEntreDeuxLancerSpinboxs[str(i)].delete(0,"end")
            self.nbTourEntreDeuxLancerSpinboxs[str(i)].insert(0, int(spellAtLevel["Autres"].get("Nb. de tours entre deux lancers", "0")))
            self.nbLanceTourParJoueurSpinboxs[str(i)].delete(0,"end")
            self.nbLanceTourParJoueurSpinboxs[str(i)].insert(0, int(spellAtLevel["Autres"].get("Nb. de lancers par tour par joueur", "1")))
            self.nbLanceTourSpinboxs[str(i)].delete(0,"end")
            self.nbLanceTourSpinboxs[str(i)].insert(0, int(spellAtLevel["Autres"].get("Nb. de lancers par tour", "1")))
            self.probaCritSpinboxs[str(i)].delete(0,"end")
            self.probaCritSpinboxs[str(i)].insert(0, int(spellAtLevel["Autres"].get("Probabilit\u00e9 de coup critique", "0%")[:-1]))
            try:
                if lastLevel < int(spellAtLevel.get("level", "1")):
                    self.levelNotebook.tab(i-1, text=" "+str(spellAtLevel.get("level", "1")+" "), state="normal")
                    lastLevel = int(spellAtLevel.get("level", "1"))
            except ValueError:
                pass

        self.levelNotebook.select(0)

    def main(self):
        pass

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python3 editeur_sorts_gui.py <json downloaded file> <json outfile> <icon folder>")
        sys.exit(1)
    filename = sys.argv[1]
    outfilename = sys.argv[2]
    icon_folder = sys.argv[3]
    values = {}
    try:
        with open(filename, "r") as f:
            values = json.loads(f.read())
    except FileNotFoundError:
        pass
    fenetre_tk = tk.Tk()
    page = OpeningPage(fenetre_tk, outfilename, values, icon_folder)
    fenetre_tk.mainloop()