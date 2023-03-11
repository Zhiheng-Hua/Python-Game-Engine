import numpy as np
import tkinter as tk

from typing import List, Tuple

from util import Util
from base_object import BaseObject
from mesh_object import MeshObject

from PIL import Image, ImageTk


class Camera(BaseObject):
    CANVAS_SIZE = (700, 500)
    GRID_SCALE = 100
    DEFAULT_FOCAL_LENGTH = 20
    DEFAULT_CAMERA_POSITION = np.array([0, -20, 0])

    def __init__(self, root_window: tk.Tk, position=None):
        super().__init__(position if position else self.DEFAULT_CAMERA_POSITION)

        self.__window = root_window
        self.__canvas = tk.Canvas(self.__window, bg="lightgrey", width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.__focal_length = self.DEFAULT_FOCAL_LENGTH
        self.__window_origin = np.array(self.CANVAS_SIZE) / 2

    def render(self, objects):
        self.__canvas.delete("all")
        for obj in objects:
            faces, colors = self.__object_face_list_to_render(obj)
            for point_list, color in zip(faces, colors):
                self.__draw_face(point_list, color)

    def __filter_faces(self, obj: MeshObject) -> Tuple[List[np.array], List[str]]:
        """filter faces to exclude back-facing faces, return list of faces in object's 3d coordinate system"""
        face_list, color_list = [], []
        face_vertices = obj.faces_local()
        for idx, vertex_normals in enumerate(obj.face_normals_local()):
            f_normal = np.mean(vertex_normals, axis=0)
            if np.dot(self.y_direction(), f_normal) < 0:    # face toward each other
                face_list.append(face_vertices[idx])
                color_list.append(obj.faces_color[idx])
        return face_list, color_list

    def __object_face_list_to_render(self, obj: MeshObject) -> Tuple[List[list], List[str]]:
        """return array of screen-coordinated faces[face_on_screen, ...] from a mesh object"""
        face_list, color_list = self.__filter_faces(obj)
        # convert faces in face_list to screen coordinate
        res_faces = []
        for face_vertices in face_list:
            temp = []
            for x, y, z in Util.rotated_row_vectors(self.basis.T, obj.position + face_vertices - self.position):
                if y <= 0:
                    return ([], [])
                temp.append([x / y, -z / y])
            face_on_screen = np.array(temp) * self.GRID_SCALE * self.__focal_length + self.__window_origin
            res_faces.append(face_on_screen.ravel().tolist())
        return res_faces, color_list

    def __draw_face(self, point_list: list, color: str):
        self.__canvas.create_polygon(point_list, fill=color, outline='black', width=1)

    def get_canvas(self):
        return self.__canvas
