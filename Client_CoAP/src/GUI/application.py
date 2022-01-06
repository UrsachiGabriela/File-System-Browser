import tkinter as tk

from src.GUI.pages.FSbrowserPage import FSBrowserPage
from src.GUI.pages.ConnectionPage import ConnectionPage


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        tk.Tk.wm_title(self,"CoAP CLIENT")


        self.container=tk.Frame(self,bg='gray97')
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames={}
        for F in (ConnectionPage,FSBrowserPage):
            page_name=F.__name__
            frame=F(parent=self.container,controller=self)
            self.frames[page_name]=frame
            frame.grid(row=0, column=0, sticky="nesw")
        self.show_frame('ConnectionPage')


    def show_frame(self , name):
        frame=self.frames[name]
        frame.init_gui()
        frame.tkraise()