import tkinter as tk
import numpy as np

from mesh_object import MeshObject
from camera import Camera
from store import Store


test_object = MeshObject(file_path='user/obj/chr_knight.obj')
test_object.rotate(test_object.x_direction(), np.pi / 2)

class GUI:
    WINDOW_SIZE = (900, 600)  # width, height

    def __init__(self):
        self.__window = tk.Tk()
        self.__window.minsize(*self.WINDOW_SIZE)
        self.__window.maxsize(*self.WINDOW_SIZE)

        self.__init_store()

        # main camera
        self.__main_camera = Camera(self.__window, self.__store)

        self.__init_events()

        # start the program
        self.__start()

    def __init_store(self):
        store = Store()
        store.add_game_object(test_object)
        self.__store = store

    def __start(self):
        self.__main_camera.show()
        self.__window.mainloop()

    def __init_events(self):
        self.__window.bind_all('<Button-1>', self.__focus_handler)
        self.__window.bind_all('<Button-3>', self.__focus_handler)

    def __focus_handler(self, event):
        widget = event.widget
        widget.focus_get()
        widget.focus_set()
