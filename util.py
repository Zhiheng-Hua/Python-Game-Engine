import numpy as np
from numpy.linalg import norm
from numpy import cos, sin


class Util:
    DIRECTION_X = np.array([1, 0, 0])
    DIRECTION_Y = np.array([0, 1, 0])
    DIRECTION_Z = np.array([0, 0, 1])
    WORLD_ORIGIN = np.zeros(3)

    @classmethod
    def rotate_vector(cls, axis, degree, v):
        """Rotates a vector around given axis"""
        rad = np.radians(degree)
        axis = axis / norm(axis)
        qw = np.cos(rad / 2)
        qx, qy, qz = axis * np.sin(rad / 2)
        q = np.array([qw, qx, qy, qz])
        rot_matrix = cls.__quaternion_rotation_matrix(q)
        return np.dot(rot_matrix, v)

    # reference: https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
    @classmethod
    def __quaternion_rotation_matrix(cls, q):
        """Converts a quaternion to a rotation matrix"""
        w, x, y, z = q
        n = norm(q)
        s = 2.0 / (n * n)
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