import numpy as np
import tkinter as tk
from tkinter import messagebox
from math import sin, cos, radians

# Define the 3D mesh object
vertices = np.array([
    [-1, -1, -1],
    [-1, 1, -1],
    [1, 1, -1],
    [1, -1, -1],
    [-1, -1, 1],
    [-1, 1, 1],
    [1, 1, 1],
    [1, -1, 1]
])

faces = np.array([
    [0, 1, 2, 3],
    [0, 1, 5, 4],
    [1, 2, 6, 5],
    [2, 3, 7, 6],
    [3, 0, 4, 7],
    [4, 5, 6, 7]
])

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.master.geometry("800x600")
        self.master.title("3D Mesh Object Viewer")
        self.init_camera()
        self.init_canvas()
        self.init_object()
        self.bind_events()
        self.render()

    def init_camera(self):
        self.camera = np.array([0, 0, -5])  # Camera position
        self.theta = 0  # Camera rotation around y-axis
        self.phi = 0  # Camera rotation around x-axis

    def init_canvas(self):
        self.canvas = tk.Canvas(self.master, bg="white")
        self.canvas.pack(fill="both", expand=True)

    def init_object(self):
        self.object_vertices = vertices.copy()
        self.object_faces = faces.copy()

    def bind_events(self):
        self.canvas.bind("<Button-1>", self.start_drag)
        self.canvas.bind("<B1-Motion>", self.drag)
        self.canvas.bind("<Button-2>", self.start_rotate)
        self.canvas.bind("<B2-Motion>", self.rotate)

    def start_drag(self, event):
        self.dragging = True
        self.last_x = event.x
        self.last_y = event.y

    def drag(self, event):
        if self.dragging:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.camera[0] += dx / 50
            self.camera[1] -= dy / 50
            self.last_x = event.x
            self.last_y = event.y
            self.render()

    def start_rotate(self, event):
        self.rotating = True
        self.last_x = event.x
        self.last_y = event.y

    def rotate(self, event):
        if self.rotating:
            dx = event.x - self.last_x
            dy = event.y - self.last_y
            self.theta += dx / 100
            self.phi -= dy / 100
            self.phi = max(-np.pi / 2, min(self.phi, np.pi / 2))
            self.last_x = event.x
            self.last_y = event.y
            self.render()

    def render(self):
        # Calculate the rotation matrix based on theta and phi
        cos_theta = cos(radians(self.theta))
        sin_theta = sin(radians(self.theta))
        cos_phi = cos(radians(self.phi))
        sin_phi = sin(radians(self.phi))
        rotation_matrix = np.array([
            [cos_theta, 0, -sin_theta],
            [sin_theta * sin_phi, cos_phi, cos_theta * sin_phi],
            [sin_theta * cos_phi, -sin_phi, cos_theta * cos_phi]
        ])

        # Calculate the transformed vertices
        transformed_vertices = np.dot(self.object_vertices, rotation_matrix)
        transformed_vertices -= self.camera
        transformed_vertices = np.dot(transformed_vertices, np.array([
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]))  # Invert y-axis to match tkinter coordinates

        # Sort the faces by distance from camera
        face_centers = np.mean(transformed_vertices[self.object_faces], axis=1)
        distances = np.linalg.norm(face_centers - self.camera, axis=1)
        sorted_faces = np.argsort(distances)[::-1]

        # Clear the canvas and draw the sorted faces
        self.canvas.delete("all")
        for face_index in sorted_faces:
            face = self.object_faces[face_index]
            points = []
            for vertex_index in face:
                x, y, z = transformed_vertices[vertex_index]
                if z > 0:
                    # Project the 3D point onto the 2D canvas
                    scale = 200 / z
                    x2d = x * scale + self.canvas.winfo_width() / 2
                    y2d = y * scale + self.canvas.winfo_height() / 2
                    points.append(x2d)
                    points.append(y2d)
            if len(points) > 2:
                self.canvas.create_polygon(points, fill="gray")

    def run(self):
        self.master.mainloop()


if __name__ == "__main__":
    app = Application(tk.Tk())
    app.run()

