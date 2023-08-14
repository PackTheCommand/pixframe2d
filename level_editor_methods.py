import json
import os
import random
import tkinter
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from PIL import ImageDraw


def __add_corners(im, rad):
    circle = Image.new('L', (rad * 2, rad * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, rad * 2 - 1, rad * 2 - 1), fill=255)
    alpha = Image.new('L', im.size, 255)
    w, h = im.size
    alpha.paste(circle.crop((0, 0, rad, rad)), (0, 0))
    alpha.paste(circle.crop((0, rad, rad, rad * 2)), (0, h - rad))
    alpha.paste(circle.crop((rad, 0, rad * 2, rad)), (w - rad, 0))
    alpha.paste(circle.crop((rad, rad, rad * 2, rad * 2)), (w - rad, h - rad))
    im.putalpha(alpha)
    return im


StatikImage = []


def createImage(path, x, y, nsa=False, name="", unknown="resources/unknown_plg.png", cornerRadius=None):
    global StatikImage

    try:
        photo = Image.open(path)
        if cornerRadius:
            photo = __add_corners(im=photo, rad=cornerRadius)
        if not name:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=path + f"{x}_{y}")
        else:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=name + f"{x}_{y}")
        if not nsa:
            StatikImage += [i]
        return i
    except FileNotFoundError:
        print("missing:", path)
        photo = Image.open(unknown)
        if not name:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=unknown + f"_{x}_{y}")
        else:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=unknown + f"{x}_{y}")
        if not nsa:
            StatikImage += [i]
        return i

def returnScrollFrame(master):
    canvas = tk.Canvas(master, width=200, bg='#333440', highlightthickness=0,)


    scrollbar = ttk.Scrollbar(master=master, command=canvas.yview, )
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas.pack(side=tk.RIGHT, fill=tk.BOTH,expand=True)

    canvas.configure(yscrollcommand=scrollbar.set)

    # Create a frame inside the canvas for the scrollable content
    inner_frame = tk.Frame(canvas, bg='#333440')
    canvas.create_window((0, 0), window=inner_frame, anchor="nw",)
    return inner_frame
def save_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.asksaveasfilename(defaultextension=".levdat", filetypes=[("Level Data Files", "*.levdat")])

    return file_path


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("Level Data Files", "*.levdat")])

    if file_path:
        return file_path
        print("Selected file:", file_path)
        # Add your code here to handle the selected file
    return None


def get_files_in_folder(folder_path):
    files = []

    try:
        # Get a list of all items in the folder
        items = os.listdir(folder_path)

        # Filter out only the files (not directories)
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

    except OSError as e:
        print("Error:", e)

    return files