import tkinter as tk
import numpy as np

from mesh_object import MeshObject
from camera import Camera
from store import Store
from components.explorer import Explorer
from components.graphics import Graphics


test_object = MeshObject(file_path='user/obj/chr_knight.obj')
test_object.rotate(test_object.x_direction(), np.pi / 2)

class App:
    WINDOW_SIZE = (930, 600)  # width, height

    def __init__(self):
        self.__window = tk.Tk()
        self.__window.minsize(*self.WINDOW_SIZE)
        # self.__window.maxsize(*self.WINDOW_SIZE)

        self.__init_store()
        self.__init_layouts()
        self.__init_events()

        # start the program
        self.__start()

    def __init_store(self):
        store = Store()
        store.add_game_object(test_object)
        self.__store = store

    def __start(self):
        # self.__main_camera.show()
        # self.__main_camera.get_canvas().focus_set()
        self.__graphics.curr_camera().show()
        self.__graphics.curr_camera().get_canvas().focus_set()
        self.__window.mainloop()

    def __init_events(self):
        self.__window.bind_all('<Button-1>', self.__focus_handler)
        self.__window.bind_all('<Button-3>', self.__focus_handler)

    def __focus_handler(self, event):
        event.widget.focus_set()

    def __init_layouts(self):
        # self.__main_camera = Camera(self.__window, self.__store)
        self.__graphics = Graphics(self.__window, self.__store)
        self.__graphics.pack(side='left')
        self.__explorer = Explorer(self.__window, self.__store)
        self.__explorer.pack(side='right', fill='y')