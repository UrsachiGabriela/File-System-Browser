import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo

from src.CoAP.commands import createCommand
from src.CoAP.constants import TYPE_CON_MSG, TYPE_NON_CON_MSG
from src.GUI.pages.BasePage import BasePage
from src.GUI.utilities.display import DisplayFrame


class FSBrowserPage(BasePage):
    def __init__(self, parent, controller):
        super().__init__(parent, controller)


        self.viewer_frame = tk.LabelFrame(self)
        self.viewer_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.viewer_frame.grid_columnconfigure(0, weight=1)
        self.viewer_frame.grid_columnconfigure(1, weight=1)

        self.init_gui(self.viewer_frame)

        self.current_path='\\'
        self.current_items=[]

    def init_gui(self,master):
        # Browser frame


        self.buttons_frame = tk.Frame(master)
        self.buttons_frame.pack(padx=10, pady=0, fill='x', expand=True, side= tk.LEFT)

        #create_dir button
        name_label = ttk.Label(self.buttons_frame, text="Directory Name:")
        name_label.pack(fill='x', expand=True,padx=1, pady=1,side= tk.TOP)


        self.new_dir_name_entry = ttk.Entry(self.buttons_frame)
        self.new_dir_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_dir_name_entry.focus()
        self.create_dir_button = ttk.Button(self.buttons_frame, text="Create_dir", command=self.create_dir_clicked)
        self.create_dir_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # create_file button
        name_label = ttk.Label(self.buttons_frame, text="File Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_file_name_entry = ttk.Entry(self.buttons_frame)
        self.new_file_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_file_name_entry.focus()
        self.create_file_button = ttk.Button(self.buttons_frame, text="Create_file", command=self.create_file_clicked)
        self.create_file_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # open button
        name_label = ttk.Label(self.buttons_frame, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.opened_item_name_entry = ttk.Entry(self.buttons_frame)
        self.opened_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.opened_item_name_entry.focus()
        self.open_button = ttk.Button(self.buttons_frame, text="Open", command=self.openNewWindow)
        self.open_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # save button
        #save_button = ttk.Button(browser, text="Save", command=save_clicked)
        #save_button.pack(fill='x', expand=True, pady=10)

        # delete button
        name_label = ttk.Label(self.buttons_frame, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.deleted_item_name_entry = ttk.Entry(self.buttons_frame)
        self.deleted_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.deleted_item_name_entry.focus()
        self.delete_button = ttk.Button(self.buttons_frame, text="Delete", command=self.delete_clicked)
        self.delete_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # rename button
        name_label = ttk.Label(self.buttons_frame, text="Old Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.renamed_item_name_entry = ttk.Entry(self.buttons_frame)
        self.renamed_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.renamed_item_name_entry.focus()

        name_label = ttk.Label(self.buttons_frame, text="New Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_name_entry = ttk.Entry(self.buttons_frame)
        self.new_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_name_entry.focus()

        self.rename_button = ttk.Button(self.buttons_frame, text="Rename", command=self.rename_clicked)
        self.rename_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # move button

        name_label = ttk.Label(self.buttons_frame, text="File/Directory Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.moved_item_name_entry = ttk.Entry(self.buttons_frame)
        self.moved_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.moved_item_name_entry.focus()

        name_label = ttk.Label(self.buttons_frame, text="Path:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.new_path_name_entry = ttk.Entry(self.buttons_frame)
        self.new_path_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.new_path_name_entry.focus()

        self.move_button = ttk.Button(self.buttons_frame, text="Move", command=self.move_clicked)
        self.move_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)


        # dir_back button

        dir_back_button = ttk.Button(self.buttons_frame, text="Dir_back", command=self.dir_back_clicked)
        dir_back_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        # search button

        name_label = ttk.Label(self.buttons_frame, text="Target Name:")
        name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

        self.searched_item_name_entry = ttk.Entry(self.buttons_frame)
        self.searched_item_name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
        self.searched_item_name_entry.focus()

        self.search_button = ttk.Button(self.buttons_frame, text="Search", command=self.search_clicked)
        self.search_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)


        self.isConfirmable=tk.IntVar()
        self.isConfirmable.set(1)
        portLabel = tk.Label(master,text="The message is:")
        portLabel.place(x=20,y=20)
        portLabel.pack(side=tk.LEFT)
        r1=tk.Radiobutton(master, text="CON", variable=self.isConfirmable,value=0,command=self.on_confirmation_select)
        r2=tk.Radiobutton(master, text="NCON", variable=self.isConfirmable,value=1,command=self.on_confirmation_select)
        r1.place(x=100,y=50)
        r2.place(x=180, y=50)
        r1.pack(side=tk.TOP)
        r2.pack(side=tk.TOP)

        print(self.isConfirmable.get())

        column_name=['Item Name']
        self.display_frame = DisplayFrame(master,column_name)
        self.display_frame.pack(padx=10, pady=0, fill='both', expand=True, side= tk.RIGHT)




    def on_confirmation_select(self):
        if self.isConfirmable.get()==0:
            return TYPE_CON_MSG
        else:
            return TYPE_NON_CON_MSG

    def on_create_dir_response(self,name,status):
        if status != 'existed':
            self.current_items.append(name)
            self.display_current_items()


    def on_create_file_response(self,name,status):
        if status != 'exists':
            self.current_items.append(name)
            self.display_current_items()

    def display_current_items(self):
        self.display_frame.clear_display()
        for item in self.current_items:
            self.display_frame.insert('', 'end', values=item)

    def create_dir_clicked(self):
        """ callback when the create_dir button is clicked
        """
        dir_path=self.current_path+self.new_dir_name_entry.get().strip()
        cmd=createCommand(dir_path,'folder',call_fct=lambda status :self.on_create_dir_response(self.new_dir_name_entry.get().strip(),status))
        cmd.mType=self.on_confirmation_select()
        self.controller.add_cmd(cmd)



    def create_file_clicked(self):
        """ callback when the create_file button is clicked
        """
        file_path=self.current_path+self.new_file_name_entry.get().strip()
        cmd=createCommand(file_path,'file',call_fct=lambda status:self.on_create_file_response(self.new_file_name_entry.get().strip(),status))
        cmd.mType=self.on_confirmation_select()
        self.controller.add_cmd(cmd)






    def save_clicked(self):
        """ callback when the save button is clicked
        """
        msg = f'Se salveaza continutul fisierului !'
        showinfo(
            title='Information',
            message=msg
        )

    def delete_clicked(self):
        """ callback when the delete button is clicked
        """
        msg = f'Se realizeaza stergerea fisierului/directorului {self.deleted_item_name_entry.get().strip()}!'
        showinfo(
            title='Information',
            message=msg
        )
    def rename_clicked(self):
        """ callback when the rename button is clicked
        """
        msg = f'Se realizeaza redenumirea fisierului/directorului {self.renamed_item_name_entry.get().strip()}!'
        showinfo(
            title='Information',
            message=msg
        )
    def move_clicked(self):
        """ callback when the move button is clicked
        """
        msg = f'Se realizeaza mutarea fisierului/directorului {self.moved_item_name_entry.get().strip()}!'
        showinfo(
            title='Information',
            message=msg
        )

        #def cd_clicked():
        #   """ callback when the cd button is clicked
        #   """
        #   msg = f'Se navigheaza spre directorul {name.get()}!'
        #   showinfo(
        #     message=msg
        # )
    def dir_back_clicked(self):
        """ callback when the dir_back button is clicked
        """
        msg = f'Se navigheaza spre directorul anterior lui {self.current_path}!'
        showinfo(
            title='Information',
            message=msg
        )
    def search_clicked(self):
        """ callback when the search button is clicked
        """
        msg = f'Se realizeaza cautarea fisierului/directorului {self.searched_item_name_entry.get().strip()}!'
        showinfo(
            title='Information',
            message=msg
        )

    def openNewWindow(self):
        pass
    #
    #     # Toplevel object which will
    #     # be treated as a new window
    #     newWindow = tk.Toplevel(master)
    #
    #     # sets the title
    #     newWindow.title("Opened File Content")
    #
    #     # sets the geometry
    #     newWindow.geometry("400x350")
    #
    #     T = tk.Text(newWindow, height = 18, width = 52)
    #
    #     # A Label widget to show in toplevel
    #     l = tk.Label(newWindow, text = name2.get())
    #     l.config(font =("Courier", 14))
    #     content = """Aici se va afisa continutul fisieruluuuuuui"""
    #     # Create an Save button.
    #     b2 = tk.Button(newWindow, text = "Save")#trebuie adaugata comanda la Save
    #     l.pack()
    #     T.pack()
    #     b2.pack()
    #     T.insert(tk.END, content)