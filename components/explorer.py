import tkinter as tk
from tkinter import ttk

class Explorer():
    def __init__(self, master):
        self.__tree = ttk.Treeview(master)
        self.__tree.heading("#0", text="Game Objects", anchor='w')
        self.__tree.column("#0", stretch=True)

        self.__init_menu()
        self.__init_events()

    def __init_menu(self):
        self.__menu = tk.Menu(self.__tree, tearoff=0)     # right click menu

        self.__delete_confirm = tk.Menu(self.__menu, tearoff=0)
        self.__menu.add_command(label='New', command=self.__menu_new_ctl)
        self.__menu.add_cascade(label='Delete', menu=self.__delete_confirm)
        self.__delete_confirm.add_command(label='Delete', command=self.__menu_delete_ctl)

    def __menu_new_ctl(self):
        parent = self.__tree.selection()[0] if self.__tree.selection() else ''
        inserted = self.__tree.insert(parent, "end", text='New File')
        self.__tree.item(parent, open=True)

    def __menu_delete_ctl(self):
        while s := self.__tree.selection():
            self.__tree.delete(s[0])

    def __right_click_ctl(self, event):
        item_clicked = self.__tree.identify_row(event.y)
        if item_clicked == '':
            for item in self.__tree.selection():
                self.__tree.selection_remove(item)

    def __left_click_ctl(self, event):
        # control focus and selection on left click
        item_clicked = self.__tree.identify_row(event.y)
        if item_clicked == '' or item_clicked not in self.__tree.selection():
            for item in self.__tree.selection():
                self.__tree.selection_remove(item)
            self.__tree.selection_add(item_clicked)
            self.__tree.focus(item_clicked)

        self.__menu.entryconfig(0, state='normal' if len(self.__tree.selection()) <= 1 else 'disabled')    # New
        self.__menu.entryconfig(1, state='normal' if self.__tree.selection() else 'disabled')              # Delete
        self.__menu.post(event.x_root, event.y_root)

    def __init_events(self):
        self.__tree.bind('<Button-1>', self.__right_click_ctl)
        self.__tree.bind('<Button-3>', self.__left_click_ctl)

    def get_tree(self):
        return self.__tree
