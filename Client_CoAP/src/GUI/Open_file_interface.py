import tkinter as tk
import Interface


# root window
root = tk.Tk()
root.geometry("400x350")
root.resizable(False, False)
root.title('Opened File Content')


# Create text widget and specify size.
T = tk.Text(root, height = 18, width = 52)

# Create label

l = tk.Label(root, text = Interface.name.get())
l.config(font =("Courier", 14))

content = """Aici se va afisa continutul fisieruluuuuuui"""

# Create an Exit button.
b2 = tk.Button(root, text = "Exit", command = root.destroy)

l.pack()
T.pack()
b2.pack()


T.insert(tk.END, content)

tk.mainloop()