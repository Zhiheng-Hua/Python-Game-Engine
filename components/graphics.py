import tkinter as tk
from tkinter import ttk

from camera import Camera
from store import Store


class Graphics(tk.Frame):
    def __init__(self, root: tk.Tk, store: Store, **kwargs):
        super().__init__(root, **kwargs)
        self.__store = store
        self.__cameras = [Camera(self, self.__store)]

        self.__curr_camera_index = 0

    def cameras(self):
        return self.__cameras

    def add_camera(self):
        self.__cameras.append(Camera(self, self.__store))

    def curr_camera(self) -> Camera:
        return self.__cameras[self.__curr_camera_index]
