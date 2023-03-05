import numpy as np
from util import Util


class BaseObject:
    def __init__(self, position=Util.WORLD_ORIGIN):
        self.position = position
        self.basis = np.array([Util.DIRECTION_X, Util.DIRECTION_Y, Util.DIRECTION_Z])
        self.speed = 2

    def rotate(self, axis, degree):
        self._rotate_basis(axis, degree)

    def move(self, direction):
        """direction vector is in local coordinate system"""
        self.position = self.position + self.basis.T @ (direction * self.speed)

    # this can be used by children class to handle rotation
    def _rotate_basis(self, axis, degree):
        self.basis = np.array([Util.rotate_vector(axis, degree, b) for b in self.basis])

    # """
    # public methods
    # """
    # # rotating around the world x, y, z axis
    # def euler_rotate(self, degree_x, degree_y, degree_z):
    #     R = self.__euler_rotation_matrix(degree_x, degree_y, degree_z)
    #     self.__update_direction_vectors(R)
    #     self.__update_mesh(R)
    #
    # """
    # helper functions
    # """
    # def __update_direction_vectors(self, R):
    #     self.__basis_x = np.matmul(R, self.__basis_x)
    #     self.__basis_y = np.matmul(R, self.__basis_y)
    #     self.__basis_z = np.matmul(R, self.__basis_z)
    #
    # def __update_mesh(self, R):
    #     for i in range(len(self.mesh.vertices)):
    #         self.mesh.vertices[i] = np.matmul(R, self.mesh.vertices[i])


# BaseObject().rotate_x(720)