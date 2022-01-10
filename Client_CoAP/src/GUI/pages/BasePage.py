import tkinter as tk
from tkinter import font as tkfont
import abc
from tkinter.messagebox import showinfo

class BasePage(tk.Frame):
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
        pass



