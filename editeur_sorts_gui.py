import tkinter as tk
import tkinter.ttk as ttk
import sys
import json
from PIL import Image, ImageTk
import os
from importlib import import_module
from dofus_sorts_downloader import normaliser
from Effets.Effet import Effet, ChildDialogEffect
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
        self.effectsValues = {}
        self.effectsCritValues = {}
        self.normalEffectTables = {}
        self.criticalEffectTables = {}
        self.typeLancerComboboxs = {}
        self.probaCritSpinboxs = {}
        self.nbLanceTourSpinboxs = {}
        self.nbLanceTourParJoueurSpinboxs = {}
        self.nbTourEntreDeuxLancerSpinboxs = {}
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
            self.normalEffectTables[str(i)] = ttk.Treeview(effectsFrame)
            self.normalEffectTables[str(i)].heading("#0", text="Effets normaux:")
            self.normalEffectTables[str(i)].grid(row=0, column=0, sticky=tk.NSEW, padx=5, pady=5)
            self.normalEffectTables[str(i)].bind("<Double-1>", self.onNormalEffectDoubleClick)
            self.normalEffectTables[str(i)].bind("<Delete>", self.onNormalEffectDelete)
            self.normalEffectTables[str(i)].bind("<Alt-Up>", self.onNormalEffectUp)
            self.normalEffectTables[str(i)].bind("<Alt-Down>", self.onNormalEffectDown)
            self.normalEffectTables[str(i)].bind("<Delete>", self.onNormalEffectDelete)
            buttonsEffectFrame = ttk.Frame(effectsFrame)
            normalToCritButton = ttk.Button(buttonsEffectFrame, text=">>", command=lambda:self.normalToCrit())
            normalToCritButton.pack()
            precLvlImportButton = ttk.Button(buttonsEffectFrame, text="<<Lvl-1", command=lambda: self.importFromPrecLevel())
            precLvlImportButton.pack()
            buttonsEffectFrame.grid(row=0, column=1, padx=5, pady=5)
            self.criticalEffectTables[str(i)] = ttk.Treeview(effectsFrame)
            self.criticalEffectTables[str(i)].heading("#0", text="Effets critiques:")
            self.criticalEffectTables[str(i)].grid(row=0, column=2, sticky=tk.NSEW, padx=5, pady=5)
            self.criticalEffectTables[str(i)].bind("<Double-1>", self.onCriticalEffectDoubleClick)
            self.criticalEffectTables[str(i)].bind("<Delete>", self.onCriticalEffectDelete)
            self.criticalEffectTables[str(i)].bind("<Alt-Up>", self.onCriticalEffectUp)
            self.criticalEffectTables[str(i)].bind("<Alt-Down>", self.onCriticalEffectDown)
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
            
            subCaracsFrame.pack(side="top", fill=tk.BOTH, padx=10, pady=5)
            levelFrame.pack(fill=tk.BOTH, padx=10, pady=5)
            self.levelNotebook.add(levelFrame, text="  "+"lvl"+" ")
            
        self.levelNotebook.pack(side="top", fill=tk.BOTH, expand="yes")
        okButton = ttk.Button(self.editframe, text="Appliquer", command=lambda: self.saveSpell())
        okButton.pack(anchor="center", side="bottom")
        self.editframe.pack(fill=tk.BOTH)
        if spellname != "":
            self.openSpell(spellname)

    def normalToCrit(self):
        lvl = self.levelNotebook.index(self.levelNotebook.select())+1
        children = self.criticalEffectTables[str(lvl)].get_children()
        for child in children:
            self.criticalEffectTables[str(lvl)].delete(child)
        self.effectsCritValues[str(lvl)].clear()
        effetDict = self.effectsValues[str(lvl)]
        for key, val in effetDict.items():
            self.effectsCritValues[str(lvl)][key] = deepcopy(val)
            self.criticalEffectTables[str(lvl)].insert('', 'end', str(lvl)+'|'+str(key), text=str(self.effectsCritValues[str(lvl)][key]))
    
    def importFromPrecLevel(self):
        precLvl = self.levelNotebook.index(self.levelNotebook.select())
        if precLvl == 0:
            return
        currentLvl = self.levelNotebook.index(self.levelNotebook.select())+1
        children = self.normalEffectTables[str(currentLvl)].get_children()
        for child in children:
            self.normalEffectTables[str(currentLvl)].delete(child)
        self.effectsValues[str(currentLvl)].clear()
        effetDict = self.effectsValues[str(precLvl)]
        for key, val in effetDict.items():
            self.effectsValues[str(currentLvl)][key] = deepcopy(val)
            self.normalEffectTables[str(currentLvl)].insert('', 'end', str(currentLvl)+'|'+str(key), text=str(self.effectsValues[str(currentLvl)][key]))
    
    def onCriticalEffectUp(self, event):
        treeview = event.widget
        selected = treeview.selection()[0]
        currentIndice = 0
        children = treeview.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice != 0:
            item_moved = selected
            moved_by_side_effect = children[currentIndice-1]
            self.effectsCritValues = self.swapTreeviewItem(treeview, item_moved, moved_by_side_effect, self.effectsCritValues)
        return "break"

    def onCriticalEffectDown(self, event):
        treeview = event.widget
        selected = treeview.selection()[0]
        len_max = len(treeview.get_children())
        currentIndice = len_max-1
        children = treeview.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice < len_max-1:
            item_moved = selected
            moved_by_side_effect = children[currentIndice+1]
            self.effectsCritValues = self.swapTreeviewItem(treeview, item_moved, moved_by_side_effect, self.effectsCritValues)
        return "break"

    def onNormalEffectUp(self, event):
        treeview = event.widget
        selected = treeview.selection()[0]
        currentIndice = 0
        children = treeview.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice != 0:
            item_moved = selected
            moved_by_side_effect = children[currentIndice-1]
            self.effectsValues= self.swapTreeviewItem(treeview, item_moved, moved_by_side_effect, self.effectsValues)
        return "break"

    def onNormalEffectDown(self, event):
        treeview = event.widget
        selected = treeview.selection()[0]
        len_max = len(treeview.get_children())
        currentIndice = len_max-1
        children = treeview.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice < len_max-1:
            item_moved = selected
            moved_by_side_effect = children[currentIndice+1]
            self.effectsValues = self.swapTreeviewItem(treeview, item_moved, moved_by_side_effect, self.effectsValues)
        return "break"
    
    def swapTreeviewItem(self, treeview, item_moved, moved_by_side_effect, values):
        parts_moved = item_moved.split('|')
        lvl_moved = parts_moved[0]
        index_moved = parts_moved[1]
        parts_moved_side_effect = moved_by_side_effect.split('|')
        lvl_moved_side_effect = parts_moved_side_effect[0]
        index_moved_side_effect = parts_moved_side_effect[1]
        save = values[str(lvl_moved_side_effect)][str(index_moved_side_effect)]
        values[str(lvl_moved_side_effect)][str(index_moved_side_effect)] = values[str(lvl_moved)][str(index_moved)]
        values[str(lvl_moved)][str(index_moved)] = save
        treeview.item(item_moved, text=str(values[str(lvl_moved)][str(index_moved)]))
        treeview.item(moved_by_side_effect, text=str(values[str(lvl_moved_side_effect)][str(index_moved_side_effect)]))
        treeview.selection_set(moved_by_side_effect)
        return values
    
    def onNormalEffectDoubleClick(self, event):
        treeview = event.widget
        item = treeview.identify('item', event.x, event.y)
        if item == "":
            lvl = self.levelNotebook.index(self.levelNotebook.select())+1
            parts = str(max([int(x) for x in self.effectsValues[str(lvl)].keys()]+[0])+1)
            effect = self.openEffectModifyWindow()
            if effect is not None:
                self.effectsValues[str(lvl)][parts] = effect
                treeview.insert('', 'end', str(lvl)+"|"+parts, text=str(effect))
        else:
            parts = item.split('|')
            lvl = parts[0]
            index = parts[1]

            effect = self.effectsValues[lvl][index]
            effect = self.openEffectModifyWindow(effect)
            if effect is not None:
                self.effectsValues[lvl][index] = effect
                treeview.item(item, text=str(self.effectsValues[lvl][index]))
   
    def onCriticalEffectDoubleClick(self, event):
        treeview = event.widget
        item = treeview.identify('item', event.x, event.y)
        if item == "":
            lvl = self.levelNotebook.index(self.levelNotebook.select())+1
            parts = str(max([int(x) for x in self.effectsCritValues[str(lvl)].keys()])+1)
            effect = self.openEffectModifyWindow()
            if effect is not None:
                self.effectsCritValues[str(lvl)][parts] = effect
                treeview.insert('', 'end', str(lvl)+"|"+parts, text=str(effect))
        else:
            parts = item.split('|')
            lvl = parts[0]
            index = parts[1]
            effect = self.effectsCritValues[lvl][index]
            effect = self.openEffectModifyWindow(effect)
            if effect is not None:
                self.effectsCritValues[lvl][index] = effect
                treeview.item(item, text=str(effect))
    
    def onNormalEffectDelete(self, event):
        treeview = event.widget
        item = treeview.identify('item', event.x, event.y)
        parts = item.split('|')
        lvl = parts[0]
        index = parts[1]
        del self.effectsValues[lvl][index]
        treeview.delete(item)

    def onCriticalEffectDelete(self, event):
        treeview = event.widget
        item = treeview.identify('item', event.x, event.y)
        parts = item.split('|')
        lvl = parts[0]
        index = parts[1]
        del self.effectsCritValues[lvl][index]
        treeview.delete(item)

    def openEffectModifyWindow(self, effect=None):
        effectDialog = ChildDialogEffect(self.fenetre, effect)
        self.fenetre.wait_window(effectDialog.app)
        return effectDialog.rvalue

    def saveSpell(self):
        spellname = self.lastOpenSpell
        spell = self.sorts_values[spellname]
        spell["desc"] = self.descLbl.cget("text")
        for i in range(1, 4):
            if str(i) not in spell.keys():
                continue
            else:
                spellAtLevel = spell[str(i)]
            spellAtLevel["level"] = self.levelNotebook.tab(i-1, option="text")
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
            for effectsValue in self.effectsValues[str(i)].values():
                if effectsValue is not None:
                    spellAtLevel["Effets"].append(effectsValue.getAllInfos())
            spellAtLevel["EffetsCritiques"] = []
            for effectsValue in self.effectsCritValues[str(i)].values():
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
            root_pic1 = Image.open(os.path.join(self.iconFolder, normaliser(spellname)+".png"))                       # Open the image like this first
            self.spellIcons[spellname] = ImageTk.PhotoImage(root_pic1)      # Then with PhotoImage. NOTE: self.root_pic2 =     and not     root_pic2 =
            self.treevw.insert('', 'end', spellname, text=spellname, image=self.spellIcons[spellname])
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
        lastLevel = 0
        for i in range(1,4):
            self.levelNotebook.tab(i-1, text=str("N/A"), state="disabled")
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
                self.normalEffectTables[str(i)].insert('', 'end', str(i)+'|'+str(effect_i), text=str(craftedEffect))
            self.effectsValues[str(i)] = listOfEffect
            listOfEffect = {}
            for effect_i, effect_infos in enumerate(spellAtLevel.get("EffetsCritiques", [])):
                craftedEffect = Effet.effectFactory(effect_infos, tailleZone=tailleZone, typeZone=typeZone, desc=spell.get("desc", ""), nomSort=spellname)
                listOfEffect[str(effect_i)] = craftedEffect
                self.criticalEffectTables[str(i)].insert('', 'end', str(i)+'|'+str(effect_i), text=str(craftedEffect))
            self.effectsCritValues[str(i)] = listOfEffect
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