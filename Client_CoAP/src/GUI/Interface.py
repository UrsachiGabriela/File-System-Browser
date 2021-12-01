import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo


# root window
root = tk.Tk()
root.geometry("400x520")
root.resizable(False, False)
root.title('Browser FS CoAP')

name= tk.StringVar()

#def create_dir_clicked():
 #   """ callback when the create_dir button is clicked
 #    """
 #   msg = f'Se creeaza directorul {name.get()}!'
 #   showinfo(
 #       title='Information',
 #       message=msg
  #  )
def create_file_clicked():
    """ callback when the create_file button is clicked
    """
    msg = f'Se creeaza fisierul {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )
def open_clicked():
    """ callback when the open button is clicked
    """
    msg = f'Se deschide fisierul {name.get()}!'
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
    msg = f'Se realizeaza stergerea fisierului/directorului {name.get()}!'
    showinfo(
        title='Information',
        message=msg
    )
def rename_clicked():
    """ callback when the rename button is clicked
    """
    msg = f'Se realizeaza redenumirea fisierului/directorului {name.get()}!'
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
# Browser frame
browser = ttk.Frame(root)
browser.pack(padx=20, pady=10, fill='x', expand=True)

# Background
pict= tk.PhotoImage(file='CoAp.png')
picture= tk.Label(browser,image=pict)
picture.place(x=-70,y=-10)

# File/Directory Name
name_label = ttk.Label(browser, text="File/Directory Name:")
name_label.pack(fill='x', expand=True)

name_entry = ttk.Entry(browser, textvariable=name)
name_entry.pack(fill='x', expand=True)
name_entry.focus()

# create_dir button
#create_dir_button = ttk.Button(browser, text="Create_dir", command=create_dir_clicked)
#create_dir_button.pack(fill='x', expand=True, pady=10)

# create_file button
create_file_button = ttk.Button(browser, text="Create_file", command=create_file_clicked)
create_file_button.pack(fill='x', expand=True, pady=10)

# open button
open_button = ttk.Button(browser, text="Open", command=open_clicked)
open_button.pack(fill='x', expand=True, pady=10)

# save button
save_button = ttk.Button(browser, text="Save", command=save_clicked)
save_button.pack(fill='x', expand=True, pady=10)

# delete button
delete_button = ttk.Button(browser, text="Delete", command=delete_clicked)
delete_button.pack(fill='x', expand=True, pady=10)

# rename button
rename_button = ttk.Button(browser, text="Rename", command=rename_clicked)
rename_button.pack(fill='x', expand=True, pady=10)

# move button
move_button = ttk.Button(browser, text="Move", command=move_clicked)
move_button.pack(fill='x', expand=True, pady=10)

# cd button
#cd_button = ttk.Button(browser, text="Cd(Navigate)", command=cd_clicked)
#cd_button.pack(fill='x', expand=True, pady=10)

# dir_back button
dir_back_button = ttk.Button(browser, text="Dir_back", command=dir_back_clicked)
dir_back_button.pack(fill='x', expand=True, pady=10)

# search button
search_button = ttk.Button(browser, text="Search", command=search_clicked)
search_button.pack(fill='x', expand=True, pady=10)

root.mainloop()