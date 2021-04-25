import tkinter as tk
import tkinter.ttk as ttk
import os
import json

class ChildDialogChooseSpell:
    """
   Ouvre une fenetre pour chercher un sort externe
    """
    def __init__(self, parent, persoVw):
        """
        
        Args:
            parent: a vue tkinter parent pour créer cette fenetre
            persoVw: la vue d'un personnage.
        """
        self.app = tk.Toplevel(parent)
        appFrame = ttk.Frame(self.app)
        self.app.resizable(False, False)
        self.rvalue = None
        self.parent = parent
        lbl = ttk.Label(appFrame, text="Sort/Item cherché:")
        lbl.grid(row=0, column=0)
        self.ent_sortCherche = ttk.Entry(appFrame, width="50")
        self.ent_sortCherche.grid(row=0, column=1)
        self.ent_sortCherche.bind("<Return>", self.cherche)
        btnSearch = ttk.Button(appFrame, text="Cherche", command=self.cherche)
        btnSearch.grid(row=0, column=2)
        tvFrame = ttk.Frame(appFrame)
        self.treevw = ttk.Treeview(tvFrame)
        scrollbarV = ttk.Scrollbar(tvFrame,
                                orient=tk.VERTICAL,
                                command=self.treevw.yview)
        self.treevw.configure(yscrollcommand=scrollbarV.set)
        self.treevw.grid(row=0, column=0, sticky=tk.NSEW)
        scrollbarV.grid(row=0, column=1, sticky=tk.NS)
        tvFrame.grid(row=1,column = 1)
        tvFrame.rowconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        tvFrame.columnconfigure(0, weight=1) # Weight 1 sur un layout grid, sans ça le composant ne changera pas de taille en cas de resize
        self.ok_button = ttk.Button(appFrame, text="OK", command=self.onOk)
        self.ok_button.grid(row=2,column = 1)
        appFrame.pack(ipady=10, ipadx=10)
        try:
            self.app.wait_visibility()
            self.app.transient(parent)
            self.app.grab_set()
        except tk.TclError:
            pass

    def cherche(self, event=None):
        nomSortCherche = self.ent_sortCherche.get()
        current_path = os.path.dirname(os.path.abspath(__file__))
        sorts_path = os.path.join(current_path, "Sorts")
        sort_files = os.listdir(sorts_path)
        self.matches = []
        for sort_file in sort_files:
            if sort_file.endswith(".json"):
                with open(os.path.join(sorts_path, sort_file), "r") as f:
                    sorts = json.loads(f.read())
                    for sort_name in list(sorts.keys()):
                        if nomSortCherche.lower() in sort_name.lower():
                            self.matches.append(tuple((sort_file, sort_name)))
        self.treevw.delete(*self.treevw.get_children())
        for sort_file, sort in self.matches:
            var = tk.IntVar()
            var.set(0)
            filename = os.path.splitext(os.path.basename(sort_file))[0]
            self.treevw.insert('', "end", filename+"::"+sort, text=filename+"::"+sort)

    def onOk(self):
        """
        Called when the user clicked the validation button. Set the rvalue attributes to the value selected and close the window.
        """
        # send the data to the parent
        curItem = self.treevw.focus()
        self.rvalue = self.treevw.item(curItem)["text"]
        self.app.destroy()