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
        self.vertices = parsed['vertices']  # array of 3d vertex vectors in obj's local coordinates, e.g. [p0, p1, ...]
        self.faces = parsed['faces']        # list of list of vertex vectors indices, e.g. [[idx_p0, idx_p1, idx_p2], ...]
        self.faces_color = parsed['faces_color']    # list of string, same length as self.faces

    def faces_local(self):
        """return array of array of vertices vectors"""
        return self.vertices[self.faces]
