import numpy as np
from base_object import BaseObject
from util import Util


class MeshObject(BaseObject):
    def __init__(self, file_path):
        super().__init__()
        self.__init_from_obj_file(file_path)

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)
        self.vertices = Util.rotated_row_vectors(R, self.vertices)

    def __init_from_obj_file(self, file_path):
        parsed = Util.parse_obj_file(file_path)
        self.vertices = parsed['vertices']  # array of 3d points, where points are in local coordinates, e.g. [p0, p1 ...]
        self.faces = parsed['faces']        # array of point indices array, e.g. [[0, 1, 2], [1, 2, 3, 5], ...]
        self.faces_color = parsed['faces_color']    # array of string, same length as self.faces
        self.faces_normal = parsed['faces_normal']  # array of face arrays of normal vectors, same length as self.faces