import numpy as np
import tkinter as tk


class Camera:
    CANVAS_SIZE = (700, 500)
    GRID_SCALE = 100

    DEFAULT_FOCAL_LENGTH = 20
    DEFAULT_CAMERA_POSITION = np.array([-100, 10, 10])

    def __init__(self, root_window: tk.Tk):
        self.__window = root_window
        self.__canvas = tk.Canvas(self.__window, bg="white", width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])

        self.__position = self.DEFAULT_CAMERA_POSITION
        self.__focal_length = self.DEFAULT_FOCAL_LENGTH
        self.__window_origin = np.array(self.CANVAS_SIZE) / 2

    def render_objects(self, objects):
        for obj in objects:
            pos = obj.position
            for v in obj.mesh.vertices:
                x, y, z = pos + v - self.__position
                ry, rz = self.__focal_length / x * np.array([y, z])
                self.__draw_vertex(ry, rz)

    def __draw_vertex(self, y, z):
        x, y = np.array([y, -z]) * self.GRID_SCALE + self.__window_origin
        self.__canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="black")

    def show(self):
        self.__canvas.grid(column=0, row=0)
