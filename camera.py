import numpy as np
import tkinter as tk
from util import Util
from base_object import BaseObject


class Camera(BaseObject):
    CANVAS_SIZE = (700, 500)
    GRID_SCALE = 100
    DEFAULT_FOCAL_LENGTH = 20
    DEFAULT_CAMERA_POSITION = np.array([0, -50, 0])

    def __init__(self, root_window: tk.Tk, position=None):
        super().__init__(position if position else self.DEFAULT_CAMERA_POSITION)

        self.__window = root_window
        self.__canvas = tk.Canvas(self.__window, bg="lightgrey", width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.__focal_length = self.DEFAULT_FOCAL_LENGTH
        self.__window_origin = np.array(self.CANVAS_SIZE) / 2

    def render(self, objects):
        self.__canvas.delete("all")
        for obj in objects:
            for x, y, z in Util.rotated_row_vectors(self.basis.T, obj.position + obj.vertices - self.position):
                if y <= 0:
                    continue
                rx, rz = self.__focal_length / y * np.array([x, z])
                self.__draw_vertex(rx, rz)

    def __draw_faces(self):
        # TODO
        pass

    def __draw_vertex(self, x, z):
        x, y = np.array([x, -z]) * self.GRID_SCALE + self.__window_origin
        self.__canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="black")

    def get_canvas(self):
        return self.__canvas
