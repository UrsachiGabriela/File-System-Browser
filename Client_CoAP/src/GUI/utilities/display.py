import tkinter as tk
from tkinter import ttk, font as tkfont


class DisplayFrame(tk.Frame):
    def __init__(self, master, tree_columns, row_color=True, cnf={}, **kw):
        tk.Frame.__init__(self, master, cnf=cnf, **kw)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.row_color = row_color
        self.odd = False
        self.init(tree_columns)

    def init(self, tree_columns):
        font = tkfont.Font(family='Helvetica', size=10, weight="bold")
        self.tree = ttk.Treeview(master=self, columns=tree_columns, show='headings', selectmode='extended')
        vsb = ttk.Scrollbar(self, orient='vertical', command=self.tree.yview)
        hsb = ttk.Scrollbar(self, orient='horizontal', command=self.tree.xview)
        vsb.grid(column=1, row=0, sticky='ns', in_=self)
        hsb.grid(column=0, row=1, sticky='ew', in_=self)
        self.tree.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        self.tree.grid(column=0, row=0, sticky='nsew', in_=self)
        self.tree.tag_configure('oddrow', font=font)
        self.tree.tag_configure('evenrow', font=font)
        for col in tree_columns:
            self.tree.heading(col, text=col, anchor='w', command=lambda c=col: self.sort_by(self.tree, c, 0))
            self.tree.column(col, width=tkfont.Font().measure(col.title()),  stretch=True)


        self.fix_treeview_color()

    def fix_treeview_color(self):
        def fixed_map(option):
            return [elm for elm in style.map('Treeview', query_opt=option) if
                    elm[:2] != ('!disabled', '!selected')]

        font = tkfont.Font(family='Helvetica', size=5, weight="bold")
        style = ttk.Style()
        style.map('Treeview', foreground=fixed_map('foreground'),
                  background=fixed_map('background'))
        style.configure("Treeview.Heading", foreground='black', font=font)




    def sort_by(self, tree: ttk.Treeview, col, descending):

        data = [(tree.set(child, col), child) for child in tree.get_children('')]
        data.sort(reverse=descending)
        num = 'Even'
        for indx, item in enumerate(data):
            tree.move(item[1], '', indx)

            if bool(self.row_color) is True:
                if num == 'Even':
                    tree.item(item[1], tags=('evenrow',))
                    num = 'Odd'
                elif num == 'Odd':
                    tree.item(item[1], tags=('oddrow',))
                    num = 'Even'
            else:
                pass
        if self.row_color is True:
            tree.tag_configure('evenrow', background='#FFF')
            tree.tag_configure('oddrow', background='#EAECEE')
        else:
            pass

        tree.heading(col, command=lambda col=col: self.sort_by(tree, col, int(not descending)))

    def insert(self, *args, **kwargs):
        if self.odd:
            tag = 'oddrow'
        else:
            tag = 'evenrow'
        self.odd = not self.odd

        result = self.tree.insert(tags=(tag,), *args, **kwargs)

        if self.row_color:
            self.tree.tag_configure('evenrow', background='#FFF')
            self.tree.tag_configure('oddrow', background='#EAECEE')
        return result

    def clear_display(self):
        self.tree.delete(*self.tree.get_children())
