import tkinter as tk
from mesh_object import MeshObject
from camera import Camera


test_object1 = MeshObject(file_path='user/obj/chr_knight.obj')
test_object2 = MeshObject(file_path='user/obj/3x3x3.obj')


class GUI:
    WINDOW_SIZE = (900, 600)  # width, height

    def __init__(self):
        self.__window = tk.Tk()
        self.__window.minsize(*self.WINDOW_SIZE)
        self.__window.maxsize(*self.WINDOW_SIZE)

        # storage
        self.__objects = [test_object1]

        # main camera
        self.__main_camera = Camera(self.__window)
        self.__main_camera.get_canvas().grid(column=0, row=0)

        # events
        self.__init_events()

        # start the program
        self.__start()

    def __update_display(self):
        self.__main_camera.render(self.__objects)
        self.__window.after(100, self.__update_display)

    def __start(self):
        self.__update_display()
        self.__window.mainloop()

    def __init_events(self):
        self.__window.bind('<KeyPress-Up>', lambda x: self.__objects[0].rotate(self.__objects[0].x_direction(), 1))
        self.__window.bind('<KeyPress-Down>', lambda x: self.__objects[0].rotate(self.__objects[0].x_direction(), -1))
        self.__window.bind('<KeyPress-Left>', lambda x: self.__objects[0].rotate(self.__objects[0].z_direction(), 1))
        self.__window.bind('<KeyPress-Right>', lambda x: self.__objects[0].rotate(self.__objects[0].z_direction(), -1))
        self.__window.bind('<KeyPress-w>', lambda x: self.__objects[0].move(self.__objects[0].y_direction()))
        self.__window.bind('<KeyPress-s>', lambda x: self.__objects[0].move(-self.__objects[0].y_direction()))
        self.__window.bind('<KeyPress-a>', lambda x: self.__objects[0].move(-self.__objects[0].x_direction()))
        self.__window.bind('<KeyPress-d>', lambda x: self.__objects[0].move(self.__objects[0].x_direction()))
