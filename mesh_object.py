import numpy as np
from base_object import BaseObject
from util import Util


class MeshObject(BaseObject):
    def __init__(self, vertices=np.empty(0), faces=np.empty(0), faces_color=np.empty(0), file_path=None):
        super().__init__()

        if file_path:
            self.__init_obj_from_file(file_path)
        else:
            # indices will be converted to 0-indexed
            self.vertices = vertices    # array of 3d points, where points are in local coordinates, e.g. [p0, p1 ...]
            self.faces = faces          # array of point indices array, e.g. [[0, 1, 2], [1, 2, 3, 5], ...]
            self.faces_color = faces_color

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)
        self.vertices = Util.rotated_row_vectors(R, self.vertices)

    def __init_obj_from_file(self, file_path):
        parsed = Util.parse_obj_file(file_path)
        self.vertices = parsed['vertices']
        self.faces = parsed['faces']
        self.faces_color = parsed['faces_color']    # same length as self.faces
