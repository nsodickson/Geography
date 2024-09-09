import json
import tkinter as tk
from tkinter import messagebox
import numpy as np
import random
from PIL import Image, ImageTk

with open("Data/geoBoundariesCGAZ_ADM0.geojson", "r") as f:
    geo_dict = json.load(f)

features = geo_dict["features"]
countries = []
for feature in features:
    countries.append(feature["properties"]["shapeName"])

root = tk.Tk()
root.title("Country Displayer")
screen_width, screen_height = 600, 600
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.grid(row=0, column=0, columnspan=4)

width_var = tk.IntVar(root, 300)
history = [countries[random.randint(0, len(countries) - 1)]]
country_idx = 0
country_var = tk.StringVar(root, history[country_idx])


def drawCountry():
    w = width_var.get()
    country = country_var.get()
    idx = countries.index(country)
    geometry = features[idx]["geometry"]

    canvas.delete("all")
    if geometry["type"] == "Polygon":
        points = np.array(geometry["coordinates"][0]).flatten()
        points[1::2] *= -1  # Reversing y points for coordinate change
        init_w = np.max(points[::2]) - np.min(points[::2])
        init_h = np.max(points[1::2]) - np.min(points[1::2])
        scale = w / init_w
        points[::2] = (points[::2] - np.min(points[::2]) - init_w / 2) * scale + screen_width / 2
        points[1::2] = (points[1::2] - np.min(points[1::2]) - init_h / 2) * scale + screen_height / 2
        canvas.create_polygon(*points, fill="white", outline="black")
    elif geometry["type"] == "MultiPolygon":
        """
        max_val = 0
        max_idx = -1
        for idx, poly in enumerate(geometry["coordinates"]):
            points = np.array(poly[0]).flatten()
            if len(points) > max_val:
                max_val = len(points)
                max_idx = idx
        mainland_points = np.array(geometry["coordinates"][max_idx][0]).flatten()
        """
        mainland_points = np.empty(0)
        for poly in geometry["coordinates"]:
            points = np.array(poly[0]).flatten()
            if len(points) > 100000:
                mainland_points = np.append(mainland_points, np.array(poly[0]).flatten())
        if len(mainland_points) == 0:  # Edge case for small island countries with few points
            for poly in geometry["coordinates"]:
                mainland_points = np.append(mainland_points, np.array(poly[0]).flatten())
        mainland_points[1::2] *= -1  # Reversing y points for coordinate change
        min_x = np.min(mainland_points[::2])
        min_y = np.min(mainland_points[1::2])
        init_w = np.max(mainland_points[::2]) - min_x
        init_h = np.max(mainland_points[1::2]) - min_y
        scale = w / init_w
        for poly in geometry["coordinates"]:
            points = np.array(poly[0]).flatten()
            points[1::2] *= -1  # Reversing y points for coordinate change
            points[::2] = (points[::2] - min_x - init_w / 2) * scale + screen_width / 2
            points[1::2] = (points[1::2] - min_y - init_h / 2) * scale + screen_height / 2
            canvas.create_polygon(*points, fill="white", outline="black")

def onSlide(val):
    width_var.set(int(val))
    drawCountry()

def onSelect(val):
    country_var.set(val)
    drawCountry()

def onClickLeft(val):
    global country_idx
    if country_idx > 0:
        country_idx -= 1
    country_var.set(history[country_idx])
    drawCountry()

def onClickRight(val):
    global country_idx
    country_idx += 1
    if country_idx == len(history):
        test = countries[random.randint(0, len(countries) - 1)]
        while history[-1] == test:
            test = countries[random.randint(0, len(countries) - 1)]
        history.append(test)
    country_var.set(history[country_idx])
    drawCountry()

def revealCountry():
    messagebox.showinfo("Country", country_var.get())

slider = tk.Scale(root, from_=50, to_=500, length=200, command=onSlide, orient=tk.HORIZONTAL)
slider.set(200)
slider.grid(row=1, column=2, pady=5)

"""
with Image.open("Assets/left.png") as left_img:
    left_img = left_img.resize((40, 40))
with Image.open("Assets/right.png") as right_img:
    right_img = right_img.resize((40, 40))
left_img = ImageTk.PhotoImage(left_img)
right_img = ImageTk.PhotoImage(right_img)

buttons = tk.Canvas(root, width=100, height=50)
buttons.grid(row=1, column=1, pady=5)
left = buttons.create_image(0, 5, image=left_img, anchor=tk.NW)
right = buttons.create_image(60, 5, image=right_img, anchor=tk.NW)

buttons.tag_bind(left, "<Button-1>", onClickLeft)
buttons.tag_bind(right, "<Button-1>", onClickRight)

reveal = tk.Button(root, text="Reveal", command=revealCountry)
reveal.grid(row=2, column=1, columnspan=2, pady=5)
"""

dropdown = tk.OptionMenu(root, country_var, *countries, command=onSelect)
dropdown.grid(row=1, column=1, pady=5)

root.mainloop()