import numpy as np
from base_object import BaseObject
from util import Util
from PIL import Image
import pywavefront


class MeshObject(BaseObject):
    def __init__(self, vertices=np.empty(0), faces=np.empty(0), file_path=None):
        super().__init__()

        if file_path:
            self.__init_obj_from_file(file_path)
        else:
            self.vertices = vertices    # array of points, where points are in local coordinates, e.g. [p0, p1 ...]
            self.faces = faces          # array of point indices array, e.g. [[i_p0, i_p1, i_p2], [i_p1, i_p2, i_p4, i_p5], ...]

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)
        self.vertices = Util.rotated_row_vectors(R, self.vertices)

    def __init_obj_from_file(self, file_path):
        parsed = self.__parse_obj_file(file_path)
        self.vertices = np.array(parsed['vertices'])
        self.faces = np.array(parsed['faces'])

    def __parse_obj_file(self, file_path):
        vertices = []
        faces = []
        material_file_path = ''   # material path
        material = {}
        vt = []
        with open(file_path, 'r') as f:
            curr_mat = ''   # material name
            for line in f.read().splitlines():
                if line.startswith('mtllib '):
                    material_file_path = line.split(' ')[1]
                    material = self.__parse_mtl_file(material_file_path)
                elif line.startswith('usemtl '):
                    curr_mat = line.split(' ')[1]
                elif line.startswith('v '):
                    vertices.append(list(map(float, line.split(' ')[1:])))
                elif line.startswith('f '):
                    v, t, n = [], [], []
                    for s in line.split(' ')[1:]:
                        vi, ti, ni = map(int, s.split('/'))  # format: vertex_index/texture_index/normal_index
                        v.append(vi)
                        t.append(ni)
                        n.append(ni)
                    faces.append(v)
                elif line.startswith('vt '):
                    vt.append(list(map(float, line.split(' ')[1:])))

        return {
            'vertices': vertices,
            'faces': faces,
            'material': material
        }

    def __get_color_at_point(self, image: Image, x, y) -> str:
        """x, y are normalized coordinates (between 0 and 1), return RGB color str"""
        width, height = image.size
        return "#%02x%02x%02x" % image.getpixel((x * width, y * height))

    def __parse_mtl_file(self, file_path):
        res = {}
        with open(file_path, 'r') as f:
            curr_mat = ''   # material name
            for line in f.read().splitlines():
                if line.startswith('newmtl '):
                    curr_mat = line.split(' ')[1]
                    res[curr_mat] = {
                        'illum': 0,
                        'map': '',
                        'image': None,
                        'Ka': np.zeros(3),
                        'Kd': np.zeros(3),
                        'Ks': np.zeros(3),
                        'Ns': 0.0
                    }
                elif line.startswith('map_'):
                    k, fp = line.split(' ')[0]
                    res[curr_mat]['map'] = k[4:]
                    res[curr_mat]['image'] = Image.open(fp).convert("RGB")
                elif line.startswith('illum '):
                    res[curr_mat]['illum'] = int(line.split(' ')[1])
                else:
                    k, v = line.split(' ')
                    res[curr_mat][k] = np.array(list(map(float, v[1:])))
        return res