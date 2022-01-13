import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from src.CoAP.commands import createCommand, openCommand, deleteCommand, renameCommand, moveCommand, detailsCommand, \
    searchCommand
from src.CoAP.constants import TYPE_CON_MSG, TYPE_NON_CON_MSG
from src.GUI.pages.BasePage import BasePage
from src.GUI.pages.FileContentPage import FileContentPage
from src.GUI.utilities.display import DisplayFrame


class FSBrowserPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        self.viewer_frame = tk.LabelFrame(self)
        self.viewer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.viewer_frame.grid_columnconfigure(0, weight=1)
        self.viewer_frame.grid_columnconfigure(1, weight=1)
        self.init_gui(self.viewer_frame)

        self.current_path=''
        self.current_items=[]

    def init_gui(self,master):

        # Browser frame1
        self.buttons_frame1 = tk.Frame(master)
        self.buttons_frame1.pack(padx=10, pady=0, fill='x', expand=True, side= tk.LEFT)

        #details button
        name_label = ttk.Label(self.buttons_frame1, text="Item Name:")
        name_label.pack(fill='x', expand=True,padx=1, pady=1,side= tk.TOP)


        self.detailed_item_name_entry = ttk.Entry(self.buttons_frame1)
        self.detailed_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.detailed_item_name_entry.focus()
        self.details_button = ttk.Button(self.buttons_frame1, text="Details", command=self.details_clicked)
        self.details_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        #create_dir button
        name_label = ttk.Label(self.buttons_frame1, text="Directory Name:")
        name_label.pack(fill='x', expand=True,padx=1, pady=1,side= tk.TOP)


        self.new_dir_name_entry = ttk.Entry(self.buttons_frame1)
        self.new_dir_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_dir_name_entry.focus()
        self.create_dir_button = ttk.Button(self.buttons_frame1, text="Create_dir", command=self.create_dir_clicked)
        self.create_dir_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # create_file button
        name_label = ttk.Label(self.buttons_frame1, text="File Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_file_name_entry = ttk.Entry(self.buttons_frame1)
        self.new_file_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_file_name_entry.focus()
        self.create_file_button = ttk.Button(self.buttons_frame1, text="Create_file", command=self.create_file_clicked)
        self.create_file_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # open button
        name_label = ttk.Label(self.buttons_frame1, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.opened_item_name_entry = ttk.Entry(self.buttons_frame1)
        self.opened_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.opened_item_name_entry.focus()
        self.open_button = ttk.Button(self.buttons_frame1, text="Open", command=self.open_clicked)
        self.open_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)



        # delete button
        name_label = ttk.Label(self.buttons_frame1, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.deleted_item_name_entry = ttk.Entry(self.buttons_frame1)
        self.deleted_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.deleted_item_name_entry.focus()
        self.delete_button = ttk.Button(self.buttons_frame1, text="Delete", command=self.delete_clicked)
        self.delete_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)


        self.buttons_frame2 = tk.Frame(master)
        self.buttons_frame2.pack(padx=10, pady=0, fill='x', expand=True, side= tk.RIGHT)

        # rename button
        name_label = ttk.Label(self.buttons_frame2, text="Old Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.renamed_item_name_entry = ttk.Entry(self.buttons_frame2)
        self.renamed_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.renamed_item_name_entry.focus()

        name_label = ttk.Label(self.buttons_frame2, text="New Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_name_entry = ttk.Entry(self.buttons_frame2)
        self.new_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_name_entry.focus()

        self.rename_button = ttk.Button(self.buttons_frame2, text="Rename", command=self.rename_clicked)
        self.rename_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)


        # move button
        name_label = ttk.Label(self.buttons_frame2, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.moved_item_name_entry = ttk.Entry(self.buttons_frame2)
        self.moved_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.moved_item_name_entry.focus()

        name_label = ttk.Label(self.buttons_frame2, text="Path:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_path_name_entry = ttk.Entry(self.buttons_frame2)
        self.new_path_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_path_name_entry.focus()

        self.move_button = ttk.Button(self.buttons_frame2, text="Move", command=self.move_clicked)
        self.move_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # search button

        name_label = ttk.Label(self.buttons_frame2, text="Target Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.searched_item_name_entry = ttk.Entry(self.buttons_frame2)
        self.searched_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.searched_item_name_entry.focus()

        self.search_button = ttk.Button(self.buttons_frame2, text="Search", command=self.search_clicked)
        self.search_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # cd button
        name_label = ttk.Label(self.buttons_frame2, text="CD:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.go_to_item_name_entry = ttk.Entry(self.buttons_frame2)
        self.go_to_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.go_to_item_name_entry.focus()

        self.cd_button = ttk.Button(self.buttons_frame2, text="CD", command=self.cd_clicked)
        self.cd_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # dir_back button

        dir_back_button = ttk.Button(self.buttons_frame2, text="Dir_back", command=self.dir_back_clicked)
        dir_back_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)




        self.isConfirmable=tk.IntVar()
        self.isConfirmable.set(1)
        portLabel = tk.Label(master,text="The message is:")
        portLabel.place(x=150,y=20)
        portLabel.pack(side=tk.TOP)
        r1=tk.Radiobutton(master, text="CON", variable=self.isConfirmable,value=0,command=self.on_confirmation_select)
        r2=tk.Radiobutton(master, text="NCON", variable=self.isConfirmable,value=1,command=self.on_confirmation_select)
        r1.place(x=100,y=50)
        r2.place(x=180, y=50)
        r1.pack(side=tk.TOP)
        r2.pack(side=tk.TOP)




        column_name=['Item Name','Current Path']
        self.display_frame = DisplayFrame(master,column_name)
        self.display_frame.pack(padx=10, pady=0, fill='both', expand=True, side= tk.RIGHT)

        self.refresh_button=tk.Button(self.display_frame,text='REFRESH',command=self.refresh_clicked)
        self.refresh_button.grid()





    def on_confirmation_select(self):
        if self.isConfirmable.get()==0:
            return TYPE_CON_MSG
        else:
            return TYPE_NON_CON_MSG

    # functii de callback la primirea raspunsurilor aferente comenzilor transmise #########################
    def on_create_dir_response(self,name):
        self.current_items.append(name)
        self.display_current_items()


    def on_create_file_response(self,name):
        self.current_items.append(name)
        self.display_current_items()

    def open_item(self,content,type:str):
        if type=='file':
            self.open_file_response(content)
        elif type=='folder':
            self.open_dir_response(content)

    def open_file_response(self,content):
        head, tail = os.path.split(self.opened_path)
        self.current_path=head
        #print(self.current_path + '     ---->file')
        FileContentPage(self,content)
        self.display_current_items()

    def open_dir_response(self,content):
        self.current_items=[]
        for item in content:
            self.current_items.append(item)
        self.current_path=self.opened_path
        self.display_current_items()

    def delete_item_response(self,deleted_path):
        head, tail = os.path.split(deleted_path)
        for item in self.current_items:
            if item == tail:
                self.current_items.remove(item)
                self.display_current_items()
                return


    def rename_item_response(self,new_name):
        head, tail = os.path.split(self.renamed_path)
        for item in self.current_items:
            if item == tail:
                self.current_items.remove(item)
                self.current_items.append(new_name)
                self.display_current_items()
                return


    def move_item_response(self):
        head, tail = os.path.split(self.moved_path)
        for item in self.current_items:
            if item == tail:
                self.current_items.remove(item)
                self.display_current_items()
                return

    def on_details_response(self,response):
        msg_to_show=f'PATH : {response["path"]}\n ' \
                    f'TYPE : {response["type"]}\n '

        if response["type"] == 'file':
            msg_to_show += f'SIZE : {response["size"]}\n'
        else:
            msg_to_show += f'DIR_CONTENTS : {response["dir_contents"]}'

        self.controller.show_message(msg_to_show)

    def search_item_response(self,response):

        msg_to_show=''
        for item in response:
            msg_to_show+= f'Name : {item["name"]}\t Type : {item["type"]}\t Path : {item["path"]} \n'
        self.controller.show_message(msg_to_show)

    ####################################################################################################

    def display_current_items(self):
        self.display_frame.clear_display()
        for item in self.current_items:
            row=[item,self.current_path]
            self.display_frame.insert('', 'end', values=row)


    def details_clicked(self):
        if self.current_path.endswith('/'):
            detailed_path=f'{self.current_path}{self.detailed_item_name_entry.get().strip()}'
        else:
            detailed_path=f'{self.current_path}/{self.detailed_item_name_entry.get().strip()}'

        cmd=detailsCommand(detailed_path,call_fct=lambda response:self.on_details_response(response))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)


    def cd_clicked(self):
        go_to_path=self.go_to_item_name_entry.get().strip()
        if  go_to_path[0] == '/':
            self.opened_path=go_to_path
        else:
            self.opened_path='/'+go_to_path



        cmd=openCommand(self.opened_path,call_fct=lambda content,item_type: self.open_item(content,item_type))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)


    def create_dir_clicked(self):
        if self.current_path.endswith('/'):
            new_dir_path=f'{self.current_path}{self.new_dir_name_entry.get().strip()}'
        else:
            new_dir_path=f'{self.current_path}/{self.new_dir_name_entry.get().strip()}'

        cmd=createCommand(new_dir_path,'folder',call_fct=lambda :self.on_create_dir_response(self.new_dir_name_entry.get().strip()))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)



    def create_file_clicked(self):
        if self.current_path.endswith('/'):
            new_file_path=f'{self.current_path}{self.new_file_name_entry.get().strip()}'
        else:
            new_file_path=f'{self.current_path}/{self.new_file_name_entry.get().strip()}'
        cmd=createCommand(new_file_path,'file',call_fct=lambda :self.on_create_file_response(self.new_file_name_entry.get().strip()))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)


    def open_clicked(self):
        if self.current_path.endswith('/'):
            self.opened_path=f'{self.current_path}{self.opened_item_name_entry.get().strip()}'
        else:
            self.opened_path=f'{self.current_path}/{self.opened_item_name_entry.get().strip()}'
        cmd=openCommand(self.opened_path,call_fct=lambda content,item_type: self.open_item(content,item_type))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)



    def refresh_clicked(self):
        if self.current_path.endswith('/'):
            self.opened_path=f'{self.current_path}'
        else:
            self.opened_path=f'{self.current_path}/'
        cmd=openCommand(self.opened_path,call_fct=lambda content,item_type: self.open_item(content,item_type))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)

    def delete_clicked(self):
        if self.current_path.endswith('/'):
            self.deleted_path=f'{self.current_path}{self.deleted_item_name_entry.get().strip()}'
        else:
            self.deleted_path=f'{self.current_path}/{self.deleted_item_name_entry.get().strip()}'
        cmd=deleteCommand(self.deleted_path,call_fct=lambda : self.delete_item_response(self.deleted_path))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)

    def rename_clicked(self):
        if self.current_path.endswith('/'):
            self.renamed_path=f'{self.current_path}{self.renamed_item_name_entry.get().strip()}'
        else:
            self.renamed_path=f'{self.current_path}/{self.renamed_item_name_entry.get().strip()}'
        new_name=self.new_name_entry.get().strip()
        cmd=renameCommand(self.renamed_path,new_name,call_fct=lambda : self.rename_item_response(new_name))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)


    def move_clicked(self):
        if self.current_path.endswith('/'):
            self.moved_path=f'{self.current_path}{self.moved_item_name_entry.get().strip()}'
        else:
            self.moved_path=f'{self.current_path}/{self.moved_item_name_entry.get().strip()}'

        #calea absoluta
        self.new_path=self.new_path_name_entry.get().strip() + self.moved_path


        cmd=moveCommand(self.moved_path,self.new_path,call_fct=lambda : self.move_item_response())
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)


    def dir_back_clicked(self):
        head, tail = os.path.split(self.current_path)
        self.opened_path=head
        cmd=openCommand(self.opened_path,call_fct=lambda content,item_type: self.open_item(content,item_type))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)

    def search_clicked(self):
        searched_path='/'
        target_name=self.searched_item_name_entry.get().strip()
        cmd=searchCommand(searched_path,target_name,call_fct=lambda response: self.search_item_response(response))
        cmd.mType=self.on_confirmation_select()
        self.send_cmd(cmd)



    def send_cmd(self,cmd):
        """
            Se trimite catre aplicatia controller comanda generata.

            :param cmd: comanda generata din interfata
        """
        self.controller.add_cmd(cmd)


