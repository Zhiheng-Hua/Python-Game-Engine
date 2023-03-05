import numpy as np
from base_object import BaseObject
from util import Util


# storing vertices as array of points, where points are in local coordinates, e.g. [p0, p1 ...]
# storing faces as array of set of point indices, e.g. [[i_p0, i_p1, i_p2], [i_p1, i_p2, i_p4, i_p5], ...]
class MeshObject(BaseObject):
    def __init__(self, vertices=np.array([]), faces=np.array([])):
        super().__init__()
        self.vertices = vertices
        self.faces = faces

    def rotate(self, axis, degree):
        self._rotate_basis(axis, degree)
        self.vertices = [Util.rotate_vector(axis, degree, v) for v in self.vertices]