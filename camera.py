import numpy as np
import tkinter as tk

from typing import List

from util import Util
from base_object import BaseObject
from mesh_object import MeshObject


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
            for pl in self.__object_face_list_to_render(obj):
                self.__draw_face(pl)

    def __filter_faces(self, obj: MeshObject) -> List[np.array]:
        """filter faces to exclude back-facing faces, return list of faces in object's 3d coordinate system"""
        res = []
        for face in obj.faces:
            # face vertices in world coordinate
            face_vertices = np.array([obj.vertices[i - 1] for i in face]) + obj.position
            # print(face_vertices)
            f_normal = np.cross(face_vertices[1] - face_vertices[0], face_vertices[2] - face_vertices[1])
            if np.dot(self.y_direction(), f_normal) < 0:    # face toward each other
                res.append(face_vertices)
        return res

    def __object_face_list_to_render(self, obj: MeshObject) -> List[list]:
        """return array of screen-coordinated faces[face_on_screen, ...] from a mesh object"""
        face_list = self.__filter_faces(obj)
        # convert faces in face_list to screen coordinate
        res = []
        for face_vertices in face_list:
            temp = []
            for x, y, z in Util.rotated_row_vectors(self.basis.T, obj.position + face_vertices - self.position):
                if y <= 0:
                    return []
                temp.append([x / y, -z / y])
            face_on_screen = np.array(temp) * self.GRID_SCALE * self.__focal_length + self.__window_origin
            res.append(face_on_screen.ravel().tolist())
        return res

    def __draw_face(self, point_list: list):
        self.__canvas.create_polygon(point_list, fill='blue', outline='black', width=1)

    # def __draw_point(self, point):
    #     x, y = point
    #     self.__canvas.create_rectangle(x - 1, y - 1, x + 1, y + 1, fill="yellow")

    def get_canvas(self):
        return self.__canvas
