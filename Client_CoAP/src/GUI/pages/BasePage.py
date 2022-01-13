import tkinter as tk
from tkinter import font as tkfont
import abc
from tkinter.messagebox import showinfo

class BasePage(tk.Frame):
    """
        Pentru implementarea interfetei , s-au utilizat 2 pagini cu functionalitati diferite
        (conexiune , respectiv browser propriu-zis) , care mostenesc o clasa de baza ce pune la
        dispozitie anumite aspecte comune (aplicatia de legatura intre front-end si back-end ,
        respectiv titlul paginilor )
    """

    def __init__(self,parent,controller):
        tk.Frame.__init__(self,parent,bg=parent['bg'])
        self.controller=controller
        self.parent=parent

        self.init_title()



    def init_title(self):
        title_font=tkfont.Font(family='Helvetica',size=20,weight='bold')
        title_color='black'

        title_frame=tk.Frame(master=self,bg=self.parent['bg'])
        title_frame.pack(side=tk.TOP,fill=tk.X)

        title_frame.grid_columnconfigure(0,weight=1)
        tk.Label(master=title_frame,text='File System Browser',font=title_font,fg=title_color,bg=title_frame['bg']).grid(row=0, column=0, sticky='nesw')



    @abc.abstractmethod
    def init_gui(self,master):
        """
            Functie abstracta, implementata in clasele descendent, in functie de elementele afisate.
        """
        pass



