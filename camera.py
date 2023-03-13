import numpy as np
import tkinter as tk

from typing import List, Tuple

from util import Util
from base_object import BaseObject
from mesh_object import MeshObject
from store import Store


class Camera(BaseObject):
    CANVAS_SIZE = (700, 500)
    GRID_SCALE = 100
    DEFAULT_FOCAL_LENGTH = 10
    DEFAULT_CAMERA_POSITION = np.array([0, -10, 0])
    HORIZONTAL_RAD_CHANGE_PER_PIXEL = 2/3 * np.pi / CANVAS_SIZE[0]
    VERTICAL_RAD_CHANGE_PER_PIXEL = 2/3 * np.pi / CANVAS_SIZE[1]

    def __init__(self, master, store: Store, position=DEFAULT_CAMERA_POSITION):
        super().__init__(position)

        self.__store = store
        self.__canvas = tk.Canvas(master, bg="lightgrey", width=self.CANVAS_SIZE[0], height=self.CANVAS_SIZE[1])
        self.__focal_length = self.DEFAULT_FOCAL_LENGTH
        self.__window_origin = np.array(self.CANVAS_SIZE) / 2

        self.__is_showing = False

        self.__init_cam_control()

    def render(self):
        self.__canvas.delete("all")
        for obj in self.__store.game_objects():
            faces, colors = self.__project_object_to_screen(obj)
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

    def __project_object_to_screen(self, obj: MeshObject) -> Tuple[List[list], List[str]]:
        """return array of screen-coordinated faces[face_on_screen, ...], color list from a mesh object"""
        face_list, color_list = self.__y_sort_faces(obj)
        # convert faces in face_list to screen coordinate
        res_faces = []
        for face_vertices in face_list:
            temp = []
            for x, y, z in Util.rotated_row_vectors(self.basis, obj.position - self.position + face_vertices):
                if y <= 0:
                    return ([], [])
                temp.append([x / y, -z / y])
            face_on_screen = self.GRID_SCALE * self.__focal_length * np.array(temp) + self.__window_origin
            res_faces.append(face_on_screen.tolist())
        return res_faces, color_list

    def __draw_face(self, point_list: list, color: str):
        self.__canvas.create_polygon(point_list, fill=color, outline='black', width=1)

    def get_canvas(self):
        return self.__canvas

    def __init_cam_control(self):
        self.__mouse_x = 0
        self.__mouse_y = 0

        self.__canvas.bind('<Button-3>', self.__left_click_ctl)
        self.__canvas.bind('<B3-Motion>', self.__left_drag_ctl)
        self.__canvas.bind('<KeyPress-w>', lambda e: self.move(self.y_direction()))
        self.__canvas.bind('<KeyPress-s>', lambda e: self.move(-self.y_direction()))
        self.__canvas.bind('<KeyPress-a>', lambda e: self.move(-self.x_direction()))
        self.__canvas.bind('<KeyPress-d>', lambda e: self.move(self.x_direction()))

    def __left_click_ctl(self, event):
        self.__mouse_x = event.x
        self.__mouse_y = event.y

    def __left_drag_ctl(self, event):
        x, y = event.x, event.y
        horizontal_rad_change = (self.__mouse_x - x) * self.HORIZONTAL_RAD_CHANGE_PER_PIXEL
        vertical_rad_change = (self.__mouse_y - y) * self.VERTICAL_RAD_CHANGE_PER_PIXEL
        self.rotate(Util.DIRECTION_Z, horizontal_rad_change)
        self.rotate(self.x_direction(), vertical_rad_change)
        self.__mouse_x = x
        self.__mouse_y = y

    def show(self):
        self.__canvas.pack(fill=tk.BOTH, expand=True)
        self.__is_showing = True
        self.__update_display()

    def hide(self):
        self.__canvas.pack_forget()
        self.__is_showing = False

    def __update_display(self):
        if self.__is_showing:
            self.render()
            self.__canvas.after(100, self.__update_display)
