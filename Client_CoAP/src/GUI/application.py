import queue
import threading
import tkinter as tk
from tkinter.messagebox import showinfo
from tkinter import messagebox

from src.CoAP.CoAPclient import CoAPclient
from src.CoAP.commands import createCommand, openCommand
from src.GUI.pages.FSbrowserPage import FSBrowserPage
from src.GUI.pages.ConnectionPage import ConnectionPage


class Application(tk.Tk):

    def __init__(self):
        super().__init__()
        tk.Tk.wm_title(self,"CoAP CLIENT")


        self.message_queue=queue.Queue()
        self.client=None
        self.resizable(False,False)
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
        frame.tkraise()

    def connect_to_server(self,serverPort:int,serverIP:str):

        self.show_frame('FSBrowserPage')
        self.resizable(True,True)
        self.init_client(serverPort,serverIP)
        self.client_thread=threading.Thread(target=lambda: self.run_client())
        self.client_thread.start()

    def init_client(self,serverPort:int,serverIP:str):
        self.client=CoAPclient(10001,serverPort,serverIP,self,self.message_queue) #initializare client CoAP
        self.client.running=True


    def run_client(self):
        self.client.run()


    def add_cmd(self,cmd):
        self.message_queue.put(cmd)



    def show_message(self,text):
        showinfo(
            title='Information',
            message=text
        )

    def destroy(self):
        if self.client:
            self.client.running=False
        super().destroy()





