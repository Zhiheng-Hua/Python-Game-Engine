import os
import numpy as np
from numpy import array
from util import Util, normalize
from mesh_object import MeshObject


test_base_dir = os.path.dirname(os.path.abspath(__file__))


DIRECTION_X = array([1, 0, 0])
DIRECTION_Y = array([0, 1, 0])
DIRECTION_Z = array([0, 0, 1])

def rotated(v, axis, rad):
    R = Util.quaternion_rotation_matrix(axis, rad)
    return R @ v

def test_mesh_obj_transformation():
    obj = MeshObject(os.path.join(test_base_dir, 'test_files', 'chr_knight.obj'))
    obj.speed = 1

    obj.move(obj.y_direction())
    exp_pos = np.array([0, 1, 0])
    assert np.allclose(obj.position, exp_pos)

    obj.rotate(obj.z_direction(), np.radians(30))
    exp_x_dir = rotated(DIRECTION_X, DIRECTION_Z, np.radians(30))
    exp_y_dir = rotated(DIRECTION_Y, DIRECTION_Z, np.radians(30))
    exp_z_dir = DIRECTION_Z
    assert np.allclose(obj.x_direction(), exp_x_dir)
    assert np.allclose(obj.y_direction(), exp_y_dir)
    assert np.allclose(obj.z_direction(), exp_z_dir)

    obj.move(obj.y_direction())
    exp_pos = exp_pos + array([-0.5, np.sqrt(3)/2, 0])
    assert np.allclose(obj.position, exp_pos)

    obj.rotate(obj.x_direction(), np.radians(60))
    exp_y_dir = rotated(exp_y_dir, exp_x_dir, np.radians(60))
    exp_z_dir = rotated(exp_z_dir, exp_x_dir, np.radians(60))
    assert np.allclose(obj.x_direction(), exp_x_dir)
    assert np.allclose(obj.y_direction(), exp_y_dir)
    assert np.allclose(obj.z_direction(), exp_z_dir)

    obj.move(obj.y_direction())
    exp_pos = exp_pos + exp_y_dir
    assert np.allclose(obj.position, exp_pos)
