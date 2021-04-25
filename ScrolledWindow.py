from tkinter.ttk import Frame, Scrollbar
from tkinter import Canvas

class ScrolledWindow(Frame):
    """
    1. Master widget gets scrollbars and a canvas. Scrollbars are connected 
    to canvas scrollregion.

    2. self.scrollwindow is created and inserted into canvas

    Usage Guideline:
    Assign any widgets as children of <ScrolledWindow instance>.scrollwindow
    to get them inserted into canvas

    __init__(self, parent, canv_w = 400, canv_h = 400, *args, **kwargs)
    docstring:
    Parent = master of scrolled window
    canv_w - width of canvas
    canv_h - height of canvas

    """


    def __init__(self, parent, *args, **kwargs):
        """Parent = master of scrolled window
        canv_w - width of canvas
        canv_h - height of canvas

       """
        super().__init__(parent, *args, **kwargs)
        self.parent = parent
        self.canv_w  = kwargs.get("width", 10)
        self.canv_h  = kwargs.get("height", 10)
        # creating a scrollbars
        self.yscrlbr = Scrollbar(self.parent)
        self.yscrlbr.grid(column = 1, row = 0, sticky = 'ns')         
        # creating a canvas
        self.canv = Canvas(self.parent)
        self.canv.config(relief = 'flat',
                         width = self.canv_w,
                         heigh = self.canv_h, bd = 2)
        # placing a canvas into frame
        self.canv.grid(column = 0, row = 0, sticky = 'nsew')
        # accociating scrollbar comands to canvas scroling
        self.yscrlbr.config(command = self.canv.yview)

        # creating a frame to inserto to canvas
        self.scrollwindow = Frame(self.parent)

        self.canv.create_window(0, 0, window = self.scrollwindow, anchor = 'nw')

        self.canv.config(yscrollcommand = self.yscrlbr.set,
                         scrollregion = (0, 0, self.canv_w, self.canv_h))

        self.yscrlbr.lift(self.scrollwindow)        
        self.scrollwindow.bind('<Configure>', self._configure_window)  
        self.scrollwindow.bind('<Enter>', self._bound_to_mousewheel)
        self.scrollwindow.bind('<Leave>', self._unbound_to_mousewheel)

        return

    def _bound_to_mousewheel(self, event):
        self.canv.bind_all("<MouseWheel>", self._on_mousewheel)   

    def _unbound_to_mousewheel(self, event):
        self.canv.unbind_all("<MouseWheel>") 

    def _on_mousewheel(self, event):
        self.canv.yview_scroll(int(-1*(event.delta/120)), "units")  

    def _configure_window(self, event):
        # update the scrollbars to match the size of the inner frame
        size = (self.scrollwindow.winfo_reqwidth(), self.scrollwindow.winfo_reqheight())
        try:
            self.canv.config(scrollregion='0 0 %s %s' % size)
        except:
            return
        if self.scrollwindow.winfo_reqwidth() != self.canv.winfo_width():
            # update the canvas's width to fit the inner frame
            self.canv.config(width = min(self.scrollwindow.winfo_reqwidth(), self.canv_w))
        s_h = self.scrollwindow.winfo_reqheight()
        if s_h != self.canv.winfo_height():
            # update the canvas's width to fit the inner frame
            self.canv.config(height = min(s_h, self.canv_h))
