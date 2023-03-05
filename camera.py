import numpy as np
from util import *


class Camera:
    def __init__(self):
        self.position = LOCAL_ORIGIN

        # direction vectors
        self.direction_x = DIRECTION_X
        self.direction_y = DIRECTION_Y
        self.direction_z = DIRECTION_Z
