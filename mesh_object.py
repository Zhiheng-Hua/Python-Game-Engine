import numpy as np
from base_object import BaseObject
from util import Util


# storing vertices as array of points, where points are in local coordinates, e.g. [p0, p1 ...]
# storing faces as array of set of point indices, e.g. [[i_p0, i_p1, i_p2], [i_p1, i_p2, i_p4, i_p5], ...]
class MeshObject(BaseObject):
    def __init__(self, vertices=np.array([]), faces=np.array([]), file_path=None):
        super().__init__()

        if file_path:
            self.__init_obj_from_file(file_path)
        else:
            self.vertices = vertices
            self.faces = faces

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
                    faces.append([list(map(int, s.split('/'))) for s in line.split(' ')[1:]])
        self.vertices = np.array(vertices)
        self.faces = np.array(faces)
