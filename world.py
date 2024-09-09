import tkinter as tk
import numpy as np
import json

with open("Data/geoBoundariesCGAZ_ADM0.geojson", "r") as f:
    geo_dict = json.load(f)

features = geo_dict["features"]

root = tk.Tk()
root.title("Country Displayer")
screen_width, screen_height = 1200, 800
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.pack()

scale_var = tk.IntVar(root, 3)

def draw(scale, center_x, center_y):
    all_points = np.empty(0)
    for country in features:
        geometry = country["geometry"]
        if geometry["type"] == "MultiPolygon":
            for poly in geometry["coordinates"]:
                all_points = np.append(all_points, np.array(poly[0]).flatten())
        else:
            all_points = np.append(all_points, np.array(geometry["coordinates"][0]).flatten())
    all_points[1::2] *= -1  # Reversing y points for coordinate change
    min_x = np.min(all_points[::2])
    min_y = np.min(all_points[1::2])
    w = np.max(all_points[::2]) - min_x
    h = np.max(all_points[1::2]) - min_y

    for country in features:
        geometry = country["geometry"]
        if geometry["type"] == "MultiPolygon":
            for poly in geometry["coordinates"]:
                points = np.array(poly[0]).flatten()
                points[1::2] *= -1  # Reversing y points for coordinate change
                points[::2] = (points[::2] - min_x - w / 2) * scale + center_x
                points[1::2] = (points[1::2] - min_y - h / 2) * scale + center_y
                canvas.create_polygon(*points, fill="white", outline="black")
        else:
            points = np.array(geometry["coordinates"][0]).flatten()
            points[1::2] *= -1  # Reversing y points for coordinate change
            points[::2] = (points[::2] - min_x - w / 2) * scale + center_x
            points[1::2] = (points[1::2] - min_y - h / 2) * scale + center_y
            canvas.create_polygon(*points, fill="white", outline="black")

"""
def zoomIn(event):
    scale_var.set(scale_var.get() + 1)
    draw(scale_var.get(), event.x, event.y)

def reset():
    draw(scale_var.get(), screen_width / 2, screen_height / 2)

reset()
canvas.bind("<Button-1>", zoomIn)
canvas.bind("<space>", lambda event: reset)
"""

draw(scale_var.get(), screen_width / 2, screen_height / 2)
root.mainloop()