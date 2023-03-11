import numpy as np
from base_object import BaseObject
from util import Util
from PIL import Image
import os


class MeshObject(BaseObject):
    def __init__(self, vertices=np.empty(0), faces=np.empty(0), faces_color=np.empty(0), file_path=None):
        super().__init__()

        if file_path:
            self.__init_obj_from_file(file_path)
        else:
            # indices will be converted to 0-indexed
            self.vertices = vertices    # array of 3d points, where points are in local coordinates, e.g. [p0, p1 ...]
            self.faces = faces          # array of point indices array, e.g. [[0, 1, 2], [1, 2, 3, 5], ...]
            self.faces_color = faces_color

    def rotate(self, axis, degree):
        R = Util.quaternion_rotation_matrix(axis, degree)
        self._rotate_basis(R)
        self.vertices = Util.rotated_row_vectors(R, self.vertices)

    def __init_obj_from_file(self, file_path):
        parsed = self.__parse_obj_file(file_path)
        self.vertices = parsed['vertices']
        self.faces = parsed['faces']
        self.faces_color = parsed['faces_color']    # same length as self.faces

    def __parse_obj_file(self, file_path):
        vertices, faces, faces_color = [], [], []
        vts, vns = [], []
        material = None
        current_dir = os.path.dirname(os.path.abspath(file_path))
        with open(file_path, 'r') as f:
            curr_mat = None   # material name
            for line in f.read().splitlines():
                if line.startswith('mtllib '):
                    material_file_path = os.path.join(current_dir, line.split(' ')[1])
                    material = self.__parse_mtl_file(material_file_path)
                elif line.startswith('usemtl '):
                    curr_mat = line.split(' ')[1]
                elif line.startswith('vn '):
                    vns.append(list(map(float, line.split(' ')[1:])))
                elif line.startswith('vt '):
                    vts.append(list(map(float, line.split(' ')[1:])))
                elif line.startswith('v '):
                    vertices.append(list(map(float, line.split(' ')[1:])))
                elif line.startswith('f '):
                    temp_v, temp_vt, temp_vn = [], [], []
                    for s in line.split(' ')[1:]:
                        vi, ti, ni = s.split('/')   # format: vertex_index/texture_index/normal_index
                        temp_v.append(int(vi) - 1)  # original obj file is 1-indexed
                        if ti:
                            temp_vt.append(int(ti) - 1)
                        # temp_vn.append(ni)
                    faces.append(temp_v)
                    if material and vts and temp_vt:
                        faces_color.append(
                            Util.average_rgb_color(
                                [self.__get_color_at_point(material[curr_mat]['image'], vts[idx]) for idx in temp_vt]
                            )
                        )

        return {
            'vertices': np.array(vertices), # np array
            'faces': np.array(faces),       # np array
            'faces_color': faces_color      # list of string
        }

    def __get_color_at_point(self, image: Image, coord) -> str:
        x, y = coord
        """x, y are normalized coordinates (between 0 and 1), return RGB color tuple"""
        width, height = image.size
        return image.getpixel((x * width, y * height))

    def __parse_mtl_file(self, file_path) -> dict:
        current_dir = os.path.dirname(os.path.abspath(file_path))
        res = {}    # material name -> info dict
        with open(file_path, 'r') as f:
            curr_mat = ''
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
                    k, fp = line.split(' ')
                    res[curr_mat]['map'] = k[4:]
                    res[curr_mat]['image'] = Image.open(os.path.join(current_dir, fp)).convert("RGB")
                elif line.startswith('illum '):
                    res[curr_mat]['illum'] = int(line.split(' ')[1])
                elif line.startswith('Ka ') or line.startswith('Kd ') or line.startswith('Ks '):
                    line_arr = line.split(' ')
                    res[curr_mat][line_arr[0]] = np.array(list(map(float, line_arr[1:])))
        return res