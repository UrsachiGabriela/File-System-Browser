import tkinter as tk
from tkinter import *

class Window():
    def __init__(self):
        self.window = Tk()
        self.window.wm_title('Browser FS CoAP')
        self.fFrame = Frame(self.window, height=960, width=1024)

app= Window()
app.window.mainloop()