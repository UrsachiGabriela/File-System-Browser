import tkinter as tk

# Toplevel object which will
# be treated as a new window
from src.CoAP.commands import saveCommand


class FileContentPage(tk.Toplevel):

    def __init__(self,master,file_content):
        super().__init__()
        self.geometry("400x350")
        self.resizable(False,False)
        self.master=master
        self.file_content=file_content
        self.init_gui()


    def init_gui(self):
        self.viewer_frame=tk.Frame(master=self)
        self.viewer_frame.place(anchor='nw')


        self.current_content=tk.Text(self.viewer_frame,height = 18, width = 52)
        self.current_content.insert(tk.END,self.file_content)
        self.current_content.pack()

        self.save_button=tk.Button(self.viewer_frame,text='Save',command=self.save_clicked)
        self.save_button.pack()

    def save_clicked(self):
        content=self.current_content.get('1.0', tk.END)
        cmd=saveCommand(self.master.opened_path,content)
        self.master.send_cmd(cmd)
