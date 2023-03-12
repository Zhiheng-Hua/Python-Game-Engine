import os
import numpy as np
from mesh_object import MeshObject


test_base_dir = os.path.dirname(os.path.abspath(__file__))


def test_mesh_obj_move():
    obj = MeshObject(os.path.join(test_base_dir, 'test_files', 'chr_knight.obj'))
    obj.move(obj.y_direction())
    obj.rotate(obj.z_direction(), np.radians(30))
    obj.move(obj.y_direction())
    assert(np.allclose(obj.position, np.array([-0.5, np.sqrt(3)/2 + 1, 0])))

