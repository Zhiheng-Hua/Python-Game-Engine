import numpy as np
from numpy import cos, sin


WORLD_ORIGIN = np.zeros(3)

WORLD_X_AXIS = np.array([1, 0, 0])
WORLD_Y_AXIS = np.array([0, 1, 0])
WORLD_Z_AXIS = np.array([0, 0, 1])


LOCAL_ORIGIN = np.zeros(3)

# direction vectors in local coordinate
DIRECTION_X = np.array([1, 0, 0])
DIRECTION_Y = np.array([0, 1, 0])
DIRECTION_Z = np.array([0, 0, 1])


# rotation matrices
# reference: https://en.wikipedia.org/wiki/Rotation_matrix
def rotation_matrix(degree_x, degree_y, degree_z):
    alpha, beta, gamma = np.radians(degree_x), np.radians(degree_y), np.radians(degree_z)
    ca, sa = cos(alpha), sin(alpha)
    cb, sb = cos(beta), sin(beta)
    cg, sg = cos(gamma), sin(gamma)
    return np.array([
        [cb * cg, sa * sb * cg - ca * sg, ca * sb * cg + sa * sg],
        [cb * sg, sa * sb *sg + ca * cg, ca * sb * sg - sa * cg],
        [-sb, sa * cb, ca * cb]
    ])

