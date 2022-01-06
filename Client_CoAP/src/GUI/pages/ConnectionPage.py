import tkinter as tk
from tkinter import ttk

from src.GUI.pages.BasePage import BasePage


class ConnectionPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)

        bg_color='light blue'
        self.viewer_frame = tk.LabelFrame(self, bg=bg_color)
        self.init_gui(self.viewer_frame)


    def init_gui(self,master):
        pass



    ###functiile pt fiecare buton