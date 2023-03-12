import numpy as np
import tkinter as tk

from typing import List, Tuple

from util import Util
from base_object import BaseObject
from mesh_object import MeshObject


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

    def __y_sort_faces(self, obj: MeshObject) -> Tuple[List[np.array], List[str]]:
        """sort faces in camera coordinates in decreasing order in y direction"""
        face_vertices = obj.faces_local()
        # sort faces in cam coordinate in y direction (forward direction of camera)
        y_in_cam_coord = face_vertices[:,:,1] + (obj.position[1] - self.position[1])
        sorted_face_indices = np.argsort(np.mean(-y_in_cam_coord, axis=1))
        sorted_faces = face_vertices[sorted_face_indices].tolist()
        sorted_colors = [obj.faces_color[i] for i in sorted_face_indices]
        return sorted_faces, sorted_colors

    def __object_face_list_to_render(self, obj: MeshObject) -> Tuple[List[list], List[str]]:
        """return array of screen-coordinated faces[face_on_screen, ...] from a mesh object"""
        face_list, color_list = self.__y_sort_faces(obj)
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
