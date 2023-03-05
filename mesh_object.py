import numpy as np
from base_object import BaseObject
from util import Util


class MeshObject(BaseObject):
    def __init__(self, vertices=np.empty(0), faces=np.empty(0), file_path=None):
        super().__init__()

        if file_path:
            self.__init_obj_from_file(file_path)
        else:
            self.vertices = vertices    # array of points, where points are in local coordinates, e.g. [p0, p1 ...]
            self.faces = faces          # array of point indices array, e.g. [[i_p0, i_p1, i_p2], [i_p1, i_p2, i_p4, i_p5], ...]

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)
        self.vertices = Util.rotated_row_vectors(R, self.vertices)

    def __init_obj_from_file(self, file_path):
        vertices = []
        faces = []
        with open(file_path, "r") as f:
            for line in f.read().splitlines():
                if line.startswith('v '):
                    vertices.append(list(map(float, line.split(' ')[1:])))
                elif line.startswith('f '):
                    temp_v, temp_t, temp_n = [], [], []
                    for s in line.split(' ')[1:]:
                        vi, ti, ni = map(int, s.split('/')) # format: vertex_index/texture_index/normal_index
                        temp_v.append(vi)
                    faces.append(temp_v)
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
