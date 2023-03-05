import numpy as np
from numpy.linalg import norm
from numpy import cos, sin


class Util:
    DIRECTION_X = np.array([1, 0, 0])
    DIRECTION_Y = np.array([0, 1, 0])
    DIRECTION_Z = np.array([0, 0, 1])
    WORLD_ORIGIN = np.zeros(3)

    @classmethod
    def rotated_row_vectors(cls, R, vectors):
        """rotate all vectors in the array of (row) vectors"""
        return (R @ vectors.T).T

    # reference: https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    @classmethod
    def quaternion_rotation_matrix(cls, axis, degree):
        """Converts axis and degree to rotation matrix"""
        rad = np.radians(degree)
        axis = axis / norm(axis)
        w = np.cos(rad / 2)
        x, y, z = axis * np.sin(rad / 2)
        s = 2.0
        rot_matrix = np.array([
            [1 - s * (y * y + z * z), s * (x * y - z * w), s * (x * z + y * w)],
            [s * (x * y + z * w), 1 - s * (x * x + z * z), s * (y * z - x * w)],
            [s * (x * z - y * w), s * (y * z + x * w), 1 - s * (x * x + y * y)]
        ])
        return rot_matrix

    # reference: https://en.wikipedia.org/wiki/Rotation_matrix
    @classmethod
    def __euler_rotation_matrix(cls, degree_x, degree_y, degree_z):
        """Converts rotation angles in degree to a rotation matrix"""
        alpha, beta, gamma = np.radians(degree_x), np.radians(degree_y), np.radians(degree_z)
        ca, sa = cos(alpha), sin(alpha)
        cb, sb = cos(beta), sin(beta)
        cg, sg = cos(gamma), sin(gamma)
        return np.array([
            [cb * cg, sa * sb * cg - ca * sg, ca * sb * cg + sa * sg],
            [cb * sg, sa * sb * sg + ca * cg, ca * sb * sg - sa * cg],
            [-sb, sa * cb, ca * cb]
        ])
