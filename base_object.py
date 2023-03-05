import numpy as np
from mesh import Mesh
from camera import Camera
from util import *


class BaseObject:
    def __init__(self, mesh: Mesh):
        self.position = WORLD_ORIGIN   # world position vector
        self.mesh = mesh

        # direction vectors
        self.__direction_x = DIRECTION_X
        self.__direction_y = DIRECTION_Y
        self.__direction_z = DIRECTION_Z


    """
    public methods
    """
    # rotating around the world x, y, z axis
    def euler_rotate(self, degree_x, degree_y, degree_z):
        R = rotation_matrix(degree_x, degree_y, degree_z)
        self.__update_direction_vectors(R)
        self.__update_mesh(R)

    """
    helper functions
    """
    def __update_direction_vectors(self, R):
        self.__direction_x = np.matmul(R, self.__direction_x)
        self.__direction_y = np.matmul(R, self.__direction_y)
        self.__direction_z = np.matmul(R, self.__direction_z)

    def __update_mesh(self, R):
        for i in range(len(self.mesh.vertices)):
            self.mesh.vertices[i] = np.matmul(R, self.mesh.vertices[i])
