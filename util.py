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

    @classmethod
    def hex_to_rgb(cls, hex_code):
        """hex_code: color string of format #RRGGBB"""
        r = int(hex_code[1:3], 16)
        g = int(hex_code[3:5], 16)
        b = int(hex_code[5:7], 16)
        return (r, g, b)

    @classmethod
    def rgb_to_hex(cls, rgb_tuple):
        r_hex = hex(rgb_tuple[0])[2:].zfill(2)
        g_hex = hex(rgb_tuple[1])[2:].zfill(2)
        b_hex = hex(rgb_tuple[2])[2:].zfill(2)
        return f"#{r_hex}{g_hex}{b_hex}"

    @classmethod
    def average_hex_color(cls, color_list):
        """input list of #RRGGBB color string, output avg color string"""
        n = len(color_list)
        rs, gs, bs = 0, 0, 0
        for color in color_list:
            r, g, b = cls.hex_to_rgb(color)
            rs += r
            gs += g
            bs += b
        avg_rgb = (round(rs / n), round(gs / n), round(bs / n))
        return cls.rgb_to_hex(avg_rgb)

    @classmethod
    def average_rgb_color(cls, color_list):
        """input list of rgb color tuple, output avg color string"""
        n = len(color_list)
        rs, gs, bs = 0, 0, 0
        for r, g, b in color_list:
            rs += r
            gs += g
            bs += b
        avg_rgb = (round(rs / n), round(gs / n), round(bs / n))
        return cls.rgb_to_hex(avg_rgb)
