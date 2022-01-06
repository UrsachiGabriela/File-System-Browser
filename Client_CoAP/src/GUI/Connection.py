import tkinter as tk
from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(tk.Label):
    """
    A Label that displays images, and plays them if they are gifs
    :im: A PIL Image instance or a string filename
    """
    def load(self, im):
        if isinstance(im, str):
            im = Image.open(im)
        frames = []

        try:
            for i in count(1):
                frames.append(ImageTk.PhotoImage(im.copy()))
                im.seek(i)
        except EOFError:
            pass
        self.frames = cycle(frames)

        try:
            self.delay = im.info['duration']
        except:
            self.delay = 100

        if len(frames) == 1:
            self.config(image=next(self.frames))
        else:
            self.next_frame()

    def unload(self):
        self.config(image=None)
        self.frames = None

    def next_frame(self):
        if self.frames:
            self.config(image=next(self.frames))
            self.after(self.delay, self.next_frame)

root = tk.Tk()
root.geometry("260x260")
root.resizable(False, False)
root.title('Connection')
lbl = ImageLabel(root)
lbl.pack(side=tk.BOTTOM)
lbl.load('7Tix.gif')

#ip
ipContent = tk.StringVar()
ipEntry = tk.Entry(root,textvariable=ipContent)
ipEntry.place(x=50,y=30)
ipEntry.pack()
#port
portContent = tk.StringVar()
portEntry = tk.Entry(root, textvariable=portContent)
portEntry.place(x=200, y=30)
portEntry.pack()

#ip
ipLabel = tk.Label(root,text="IP:")
ipLabel.place(x=20,y=2)

#port
portLabel = tk.Label(root,text="PORT:")
portLabel.place(x=20,y=20)
v0=tk.IntVar()
v0.set(1)
portLabel = tk.Label(root,text="The message is:")
portLabel.place(x=20,y=20)
portLabel.pack(side=tk.LEFT)
r1=tk.Radiobutton(root, text="CON", variable=v0,value=1)
r2=tk.Radiobutton(root, text="NCON", variable=v0,value=2)
r1.place(x=100,y=50)
r2.place(x=180, y=50)
r1.pack(side=tk.TOP)
r2.pack(side=tk.TOP)
button = tk.Button(root, text='Start Connection', width=25)
button.pack()


root.mainloop()