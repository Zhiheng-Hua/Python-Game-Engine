import numpy as np
import tkinter as tk
from base_object import BaseObject
from mesh import Mesh


DEFAULT_FOCAL_LENGTH = 20
INITIAL_DISTANCE_TO_WORLD_ORIGIN = 1000
GUI_INITIAL_WORLD_POSITION = np.array([-100, 0, 0])
WINDOW_SIZE = (700, 500)    # width, height
CANVAS_SIZE = (700, 500)

GRID_SCALE = 100

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
    def __init__(self):
        self.__position = GUI_INITIAL_WORLD_POSITION
        self.__window = tk.Tk()
        self.__focal_length = DEFAULT_FOCAL_LENGTH
        self.__window_origin = np.array(WINDOW_SIZE) / 2

        # storage
        self.__objects = [test_object]

        self.__init_window()

    def __init_window(self):
        self.__window.minsize(*WINDOW_SIZE)
        self.__window.maxsize(*WINDOW_SIZE)

        # create canvas
        self.__canvas = tk.Canvas(self.__window, bg="white", width=CANVAS_SIZE[0], height=CANVAS_SIZE[1])
        self.__canvas.grid(column=0, row=0)

    def __render(self):
        for obj in self.__objects:
            pos = obj.position
            for v in obj.mesh.vertices:
                x, y, z = pos + v - self.__position
                ry, rz = self.__focal_length / x * np.array([y, z])
                self.__draw_vertex(ry, rz)


    def __draw_vertex(self, y, z):
        x, y = np.array([y, -z]) * GRID_SCALE + self.__window_origin
        self.__canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="black")

    def start(self):
        self.__render()
        self.__window.mainloop()
