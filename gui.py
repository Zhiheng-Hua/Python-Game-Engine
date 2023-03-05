import numpy as np
import tkinter as tk
from base_object import BaseObject
from mesh import Mesh
from camera import Camera

test_object = BaseObject(Mesh(vertices=np.array(
    [[1, 1, 1],
     [1, 1, -1],
     [1, -1, 1],
     [1, -1, -1],
     [-1, 1, 1],
     [-1, 1, -1],
     [-1, -1, 1],
     [-1, -1, -1]]
)))

class GUI:
    WINDOW_SIZE = (700, 500)  # width, height

    def __init__(self):
        self.__window = tk.Tk()
        self.__window.minsize(*self.WINDOW_SIZE)
        self.__window.maxsize(*self.WINDOW_SIZE)

        # storage
        self.__objects = [test_object]

        # main camera
        self.__main_camera = Camera(self.__window)
        self.__main_camera.show()

    def __render(self):
        self.__main_camera.render_objects(self.__objects)

    def root_window(self):
        return self.__window

    def start(self):
        self.__render()
        self.__window.mainloop()
