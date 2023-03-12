import tkinter as tk
from mesh_object import MeshObject
from camera import Camera
import numpy as np


test_object = MeshObject(file_path='user/obj/chr_knight.obj')
test_object.rotate(test_object.x_direction(), np.pi / 2)

class GUI:
    WINDOW_SIZE = (900, 600)  # width, height

    def __init__(self):
        self.__window = tk.Tk()
        self.__window.minsize(*self.WINDOW_SIZE)
        self.__window.maxsize(*self.WINDOW_SIZE)

        # storage
        self.__objects = [test_object]

        # main camera
        self.__main_camera = Camera(self.__window)
        self.__main_camera.get_canvas().grid(column=0, row=0)

        self.__init_events()

        # start the program
        self.__start()

    def __update_display(self):
        self.__main_camera.render(self.__objects)
        self.__window.after(100, self.__update_display)

    def __start(self):
        self.__update_display()
        self.__window.mainloop()

    def __init_events(self):
        self.__window.bind_all('<Button-1>', self.__focus_handler)
        self.__window.bind_all('<Button-3>', self.__focus_handler)

    def __focus_handler(self, event):
        widget = event.widget
        widget.focus_get()
        widget.focus_set()
