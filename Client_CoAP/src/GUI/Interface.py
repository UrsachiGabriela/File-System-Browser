import tkinter as tk
from doctest import master
from tkinter import ttk, W
from tkinter.messagebox import showinfo

import top as top
from PIL import Image, Image, ImageTk
from tkinter.ttk import Combobox
from src.CoAP.commands import *
from src.CoAP.CoAPclient import q

# root window
root = tk.Tk()
root.geometry("600x900")
root.resizable(False, False)
root.title('Browser FS CoAP')

name= tk.StringVar()
name1= tk.StringVar()
name2= tk.StringVar()
name3= tk.StringVar()
name4= tk.StringVar()
rename= tk.StringVar()
name5= tk.StringVar()
path1= tk.StringVar()
name6= tk.StringVar()
name7= tk.StringVar()
path2= tk.StringVar()
def ERROR():
    """ callback when the search button is clicked
    """
    msg = f'Eroare la comunicarea cu server-ul!'
    showinfo(
        title='Information',
        message=msg
    )

def create_dir_clicked():
    """ callback when the create_dir button is clicked
    """
    cmd=createCommand(name.get(),'folder')
    cmd.mType=TYPE_CON_MSG
    q.put(cmd)
    msg = f'Se creeaza directorul {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )

def create_file_clicked():
    """ callback when the create_file button is clicked
    """
    cmd=createCommand(name.get(),'file')
    cmd.mType=TYPE_CON_MSG
    q.put(cmd)
    msg = f'Se creeaza fisierul {name1.get()}!'
    showinfo(
        title='Information',
        message=msg
    )

def save_clicked():
    """ callback when the save button is clicked
    """
    msg = f'Se salveaza continutul fisierului {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )

def delete_clicked():
    """ callback when the delete button is clicked
    """
    msg = f'Se realizeaza stergerea fisierului/directorului {name3.get()}!'
    showinfo(
        title='Information',
        message=msg
    )
def rename_clicked():
    """ callback when the rename button is clicked
    """
    msg = f'Se realizeaza redenumirea fisierului/directorului {name4.get()}!'
    showinfo(
        title='Information',
        message=msg
    )
def move_clicked():
    """ callback when the move button is clicked
    """
    msg = f'Se realizeaza mutarea fisierului/directorului {name.get()}!'
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
def dir_back_clicked():
    """ callback when the dir_back button is clicked
    """
    msg = f'Se navigheaza spre directorul anterior lui {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )
def search_clicked():
    """ callback when the search button is clicked
    """
    msg = f'Se realizeaza cautarea fisierului/directorului {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )

def openNewWindow():

    # Toplevel object which will
    # be treated as a new window
    newWindow = tk.Toplevel(master)

    # sets the title
    newWindow.title("Opened File Content")

    # sets the geometry
    newWindow.geometry("400x350")

    T = tk.Text(newWindow, height = 18, width = 52)

    # A Label widget to show in toplevel
    l = tk.Label(newWindow, text = name2.get())
    l.config(font =("Courier", 14))
    content = """Aici se va afisa continutul fisieruluuuuuui"""
    # Create an Save button.
    b2 = tk.Button(newWindow, text = "Save")#trebuie adaugata comanda la Save
    l.pack()
    T.pack()
    b2.pack()
    T.insert(tk.END, content)

def Create_Interface():
    # Browser frame
    browser = ttk.Frame(root)
    browser.pack(padx=10, pady=0, fill='x', expand=True, side= tk.LEFT)

    #create_dir button
    name_label = ttk.Label(browser, text="Directory Name:")
    name_label.pack(fill='x', expand=True,padx=1, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    create_dir_button = ttk.Button(browser, text="Create_dir", command=create_dir_clicked)
    create_dir_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # create_file button
    name_label = ttk.Label(browser, text="File Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name1)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    create_file_button = ttk.Button(browser, text="Create_file", command=create_file_clicked)
    create_file_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # open button
    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name2)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    open_button = ttk.Button(browser, text="Open", command=openNewWindow)
    open_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # save button
    #save_button = ttk.Button(browser, text="Save", command=save_clicked)
    #save_button.pack(fill='x', expand=True, pady=10)

    # delete button
    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name3)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    delete_button = ttk.Button(browser, text="Delete", command=delete_clicked)
    delete_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # rename button
    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name4)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()

    name_label = ttk.Label(browser, text="New Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=rename)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    rename_button = ttk.Button(browser, text="Rename", command=rename_clicked)
    rename_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # move button

    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name5)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()

    name_label = ttk.Label(browser, text="Path:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=path1)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()

    move_button = ttk.Button(browser, text="Move", command=move_clicked)
    move_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # cd button
    #cd_button = ttk.Button(browser, text="Cd(Navigate)", command=cd_clicked)
    #cd_button.pack(fill='x', expand=True, pady=10)

    # dir_back button
    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name6)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    dir_back_button = ttk.Button(browser, text="Dir_back", command=dir_back_clicked)
    dir_back_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    # search button

    name_label = ttk.Label(browser, text="File/Directory Name:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=name7)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()

    name_label = ttk.Label(browser, text="Path:")
    name_label.pack(fill='x', expand=True, pady=1,side= tk.TOP)

    name_entry = ttk.Entry(browser, textvariable=path2)
    name_entry.pack(fill='x', expand=True, pady=1,side= tk.TOP)
    name_entry.focus()
    search_button = ttk.Button(browser, text="Search", command=search_clicked)
    search_button.pack(fill='x', expand=True, pady=1,side= tk.TOP)
Create_Interface()
root.mainloop()