from tkinter import ttk
from Effets.Effet import ChildDialogEffect, Effet

class EffectsTreeview(ttk.Treeview):
    def __init__(self, frameParent, heading, effects=[]):
        super().__init__(frameParent)
        self.parent = frameParent
        self.heading("#0", text=heading)
        self.effectsValues = {}
        for i, effect in enumerate(effects):
            if effect is not None:
                self.effectsValues[str(i)] = effect
                self.insert('', 'end', str(i), text=str(effect))
        self.bind("<Double-1>", self.onNormalEffectDoubleClick)
        self.bind("<Delete>", self.onNormalEffectDelete)
        self.bind("<Alt-Up>", self.onNormalEffectUp)
        self.bind("<Alt-Down>", self.onNormalEffectDown)
    
    def onNormalEffectUp(self, event):
        selected = self.selection()[0]
        currentIndice = 0
        children = self.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice != 0:
            item_moved = selected
            moved_by_side_effect = children[currentIndice-1]
            self.swapTreeviewItem(item_moved, moved_by_side_effect)
        return "break"

    def onNormalEffectDown(self, event):
        selected = self.selection()[0]
        len_max = len(self.get_children())
        currentIndice = len_max-1
        children = self.get_children()
        for i, child in enumerate(children):
            if child == selected:
                currentIndice = i
                break
        if currentIndice < len_max-1:
            item_moved = selected
            moved_by_side_effect = children[currentIndice+1]
            self.swapTreeviewItem(item_moved, moved_by_side_effect)
        return "break"
    
    def swapTreeviewItem(self, item_moved, moved_by_side_effect):
        index_moved = item_moved
        index_moved_side_effect = moved_by_side_effect
        save = self.effectsValues[str(index_moved_side_effect)]
        self.effectsValues[str(index_moved_side_effect)] = self.effectsValues[str(index_moved)]
        self.effectsValues[str(index_moved)] = save
        self.item(item_moved, text=str(self.effectsValues[str(index_moved)]))
        self.item(moved_by_side_effect, text=str(self.effectsValues[str(index_moved_side_effect)]))
        self.selection_set(moved_by_side_effect)
    
    def onNormalEffectDoubleClick(self, event):
        item = self.identify('item',event.x,event.y)
        if item == "":
            parts = str(max([int(x) for x in self.effectsValues.keys()]+[0])+1)
            effect = self.openEffectModifyWindow()
            if effect is not None:
                self.effectsValues[parts] = effect
                self.insert('', 'end', parts, text=str(effect))
        else:
            effect = self.effectsValues[item]
            effect = self.openEffectModifyWindow(effect)
            if effect is not None:
                self.effectsValues[item] = effect
                self.item(item, text=str(self.effectsValues[item]))
    
    def openEffectModifyWindow(self, effect=None):
        effectDialog = ChildDialogEffect(self.parent, effect)
        self.parent.wait_window(effectDialog.app)
        return effectDialog.rvalue
        
    def onNormalEffectDelete(self, event):
        item = self.identify('item', event.x, event.y)
        del self.effectsValues[item]
        self.delete(item)

    def get(self):
        ret = []
        for effet in self.effectsValues.values():
            ret.append(effet.getAllInfos())
        return ret