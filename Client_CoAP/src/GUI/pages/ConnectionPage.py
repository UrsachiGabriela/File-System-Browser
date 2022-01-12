import re
import tkinter as tk
from tkinter import ttk

import socket
from PIL import Image, ImageTk
from itertools import count, cycle


from src.GUI.pages.BasePage import BasePage


class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            try:
                img= Image.open(im)
                frames = []

                try:
                    for i in count(1):
                        frames.append(ImageTk.PhotoImage(img.copy()))
                        img.seek(i)
                except EOFError :
                    pass

                self.frames = cycle(frames)

                try:
                    self.delay = img.info['duration']
                except:
                    self.delay = 100

                if len(frames) == 1:
                    self.config(image=next(self.frames))
                else:
                    self.next_frame()
            except Exception as err:

                print(err)


    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)


class ConnectionPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)



        self.viewer_frame = tk.LabelFrame(self)
        self.viewer_frame.pack(side=tk.BOTTOM, fill=tk.Y, expand=True)


        self.init_gui(self.viewer_frame)


    def init_gui(self,master):
        lbl = ImageLabel(master)
        lbl.pack(side=tk.BOTTOM)
        lbl.load('D:/__FACULTATE/AN_3/Sem1/__PROIECT_RC/RC_P/Client_CoAP/src/GUI/utilities/7Tix.gif')

        #ip

        self.ipEntry = tk.Entry(master)
        self.ipEntry.place(x=50,y=30)
        self.ipEntry.pack()
        #port

        self.portEntry = tk.Entry(master)
        self.portEntry.place(x=200, y=30)
        self.portEntry.pack()

        #ip
        ipLabel = tk.Label(master,text="IP:")
        ipLabel.place(x=20,y=2)

        #port
        portLabel = tk.Label(master,text="PORT:")
        portLabel.place(x=20,y=20)


        button = tk.Button(master, text='Start Connection', width=25,height=2,command=self.on_connect)
        button.place(x=40,y=100)



    def on_connect(self):
        ip=self.ipEntry.get().strip()
        port=self.portEntry.get().strip()


        if str(port)=='' or int(port)<0 or int(port)>65535:
            self.controller.show_message('Invalid PORT')
            return

        if ip=='':
            self.controller.show_message('Invalid IP')
            return

        """
        https://www.geeksforgeeks.org/python-program-to-validate-an-ip-address/
        https://www.regextester.com/99895
        """
        ip_url_regex = "^(http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?[a-z0-9]+([\-\.]{1}[a-z0-9]+)*\.[a-z]{2,5}(:[0-9]{1,5})?(\/.*)?|^((http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
        if not re.search(ip_url_regex, ip)  :
            self.controller.show_message('Invalid IP')
            return

        ip_regex="^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"
        if not re.search(ip_regex,ip):
            ip=socket.gethostbyname(ip)
        print(ip)
        self.controller.connect_to_server(port,ip)



