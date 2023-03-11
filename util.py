import os
import numpy as np
from numpy.linalg import norm
from numpy import cos, sin
from PIL import Image


def normalize(v):
    """Normalize a 3d vector v."""
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm

def reflect(v, n):
    """Compute the reflection vector of a vector v around a normal vector n."""
    return v - 2 * np.dot(v, n) * n


class Util:
    DIRECTION_X = np.array([1, 0, 0])
    DIRECTION_Y = np.array([0, 1, 0])
    DIRECTION_Z = np.array([0, 0, 1])
    WORLD_ORIGIN = np.zeros(3)

    La = np.array([1.0, 0.5, 0.0])  # bright orange ambient color
    Ld = np.array([1.0, 1.0, 0.5])  # bright yellow diffuse color
    Ls = np.array([1.0, 1.0, 1.0])  # white specular color

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
    def euler_rotation_matrix(cls, degree_x, degree_y, degree_z):
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

    @classmethod
    def parse_obj_file(cls, file_path):
        vertices, normals, faces, faces_color, faces_vertex_normal = [], [], [], [], []
        vts = []
        material = None
        current_dir = os.path.dirname(os.path.abspath(file_path))
        with open(file_path, 'r') as f:
            curr_mat = None   # material name
            for line in f.read().splitlines():
                if line.startswith('mtllib '):
                    material_file_path = os.path.join(current_dir, line.split(' ')[1])
                    material = cls.parse_mtl_file(material_file_path)
                elif line.startswith('usemtl '):
                    curr_mat = line.split(' ')[1]
                elif line.startswith('vn '):
                    normals.append(list(map(float, line.split(' ')[1:])))
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
                        temp_vn.append(int(ni) - 1)
                    faces.append(temp_v)
                    faces_vertex_normal.append(temp_vn)
                    if material and vts and temp_vt:
                        faces_color.append(
                            Util.average_rgb_color(
                                [cls.get_color_at_point(material[curr_mat]['image'], vts[idx]) for idx in temp_vt]
                            )
                        )
        return {
            'vertices': np.array(vertices),
            'normals': np.array(normals),
            'faces': faces,                 # list of list of vertex coordinate indices
            'faces_color': faces_color,     # list of RGB color string
            'faces_vertex_normal': faces_vertex_normal  # list of list of vertex normal indices
        }

    @classmethod
    def parse_mtl_file(cls, file_path) -> dict:
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

    @classmethod
    def get_color_at_point(cls, image: Image, coord) -> str:
        """x, y are normalized coordinates (between 0 and 1), return RGB color tuple"""
        x, y = coord
        width, height = image.size
        return image.getpixel((x * width, y * height))

    @classmethod
    def rendered_face_color(cls, ambient_color, diffuse_color, specular_color, shininess,
                            ambient_light, diffuse_light, specular_light,
                            face_normal, light_normal, light_vector, view_vector):
        return ambient_color * ambient_light + \
        diffuse_color * diffuse_light * (max(np.dot(light_normal, light_vector), 0.0)) + \
        specular_color * specular_light * (max(np.dot(reflect(-light_vector, face_normal), view_vector), 0.0) ** shininess)
