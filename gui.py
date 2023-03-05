import numpy as np
import tkinter as tk
from mesh_object import MeshObject
from camera import Camera
from util import Util

# test_object = MeshObject(vertices=np.array(
#     [[1, 1, 1],
#      [1, 1, -1],
#      [1, -1, 1],
#      [1, -1, -1],
#      [-1, 1, 1],
#      [-1, 1, -1],
#      [-1, -1, 1],
#      [-1, -1, -1]]
# ))

test_object = MeshObject(file_path='user/obj/chr_knight.obj')

test_object.rotate(Util.DIRECTION_X, 45)
test_object.rotate(Util.DIRECTION_Y, 30)

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

        # events
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
        self.__window.bind('<KeyPress-Up>', lambda x: self.__objects[0].rotate(Util.DIRECTION_Y, 1))
        self.__window.bind('<KeyPress-Left>', lambda x: self.__objects[0].rotate(Util.DIRECTION_Z, 1))
        self.__window.bind('<KeyPress-Right>', lambda x: self.__objects[0].rotate(Util.DIRECTION_Z, -1))
        self.__window.bind('<KeyPress-Down>', lambda x: self.__objects[0].rotate(Util.DIRECTION_Y, -1))
        self.__window.bind('<KeyPress-a>', lambda x: self.__objects[0].move(-Util.DIRECTION_Y))
        self.__window.bind('<KeyPress-d>', lambda x: self.__objects[0].move(Util.DIRECTION_Y))
        self.__window.bind('<KeyPress-w>', lambda x: self.__objects[0].move(Util.DIRECTION_X))
        self.__window.bind('<KeyPress-s>', lambda x: self.__objects[0].move(-Util.DIRECTION_X))
