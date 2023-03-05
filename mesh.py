import numpy as np


# storing vertices as array of points, where points are in local coordinates, e.g. [p0, p1 ...]
# storing faces as array of set of point indices, e.g. [[i_p0, i_p1, i_p2], [i_p1, i_p2, i_p4, i_p5], ...]
class Mesh:
    @classmethod
    def load_from_file(cls, rel_path):
        pass

    @classmethod
    def save_to_file(cls, rel_path):
        pass

    def __init__(self, vertices=np.array([]), faces=np.array([])):
        self.vertices = vertices
        self.faces = faces
