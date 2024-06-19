import tkinter as tk

def test(event):
    print(event.x)

root = tk.Tk()
root.title("Test Window")
screen_width, screen_height = 800, 800
canvas = tk.Canvas(root, width=screen_width, height=screen_height, bg="black")
canvas.bind("<Button-1>", test)
canvas.pack()

root.mainloop()