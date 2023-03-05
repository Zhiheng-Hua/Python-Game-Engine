import numpy as np
from util import Util


class BaseObject:
    def __init__(self, position=Util.WORLD_ORIGIN):
        self.position = position
        self.basis = np.array([Util.DIRECTION_X, Util.DIRECTION_Y, Util.DIRECTION_Z])
        self.speed = 2

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)

    def move(self, direction):
        """direction vector is in local coordinate system"""
        self.position = self.position + direction * self.speed

    def x_direction(self):
        return self.basis[0]

    def y_direction(self):
        return self.basis[1]

    def z_direction(self):
        return self.basis[2]

    # this can be used by children class to handle rotation
    def _rotate_basis(self, R):
        self.basis = Util.rotated_row_vectors(R, self.basis)

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