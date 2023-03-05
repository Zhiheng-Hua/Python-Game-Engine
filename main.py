import tkinter as tk
import numpy as np
from gui import GUI


# window = tk.Tk()
#
# window.geometry('300x400')
#
# canvas = tk.Canvas(window, bg="white", width=700, height=500)
# canvas.grid(column=0, row=0)
#
# canvas.create_rectangle(30, 0, 100, 100, fill="blue")
#
# window.mainloop()

# # create a new tkinter window
# root = tk.Tk()
# root.title("Polygon Drawing Example")
# # create a new canvas to draw on
# canvas = tk.Canvas(root, width=500, height=500)
# canvas.pack()
# # define the points of the polygon
# points = np.array([[100, 100], [200, 100], [150, 200]]).tolist()
# # draw the polygon on the canvas
# canvas.create_polygon(points, fill='red', outline='black', width=2)
# # start the main tkinter event loop
# root.mainloop()

GUI()
