import numpy as np
from util import Util


class BaseObject:
    def __init__(self, position=Util.WORLD_ORIGIN):
        self.position = position    # position in world system
        self.basis = np.array([Util.DIRECTION_X, Util.DIRECTION_Y, Util.DIRECTION_Z])   # direction in world system
        self.speed = 1

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)

    def move(self, direction):
        """direction vector is in world coordinate system"""
        self.position = self.position + direction * self.speed

    def x_direction(self):
        """x direction in world system"""
        return self.basis[0]

    def y_direction(self):
        """y direction in world system"""
        return self.basis[1]

    def z_direction(self):
        """z direction in world system"""
        return self.basis[2]

    # this can be used by children class to handle rotation
    def _rotate_basis(self, R):
        self.basis = Util.rotated_row_vectors(R, self.basis)
