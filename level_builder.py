import json
import os
import random
import re
import tkinter
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from PIL import ImageDraw

from mygame.interfaces.editWindow import EditWindow
import interfaces.script_overview_menu as script_overview_menu

G_WIDTH = 800
G_HEIGHT = 600

BLOCK_SIZE = 50

from level_editor_methods import *

import ui_code

from interfaces.objectPropertiesMenu import ObjectPropertiesMenu

folders = {"main": {"deco": {}, "blocks": {}, "actions": {},"materials":{} }}


def addSubfolder(path: str, name: str):
    p = ["main"] + path.split("/")
    cr = folders
    while len(p) > 0:
        print(cr)
        cr = cr[p.pop(0)]

    print(cr)

    cr[name] = {}


"""import sv_ttk"""  # to slow


class CanvasApp:
    def __init__(self, root):
        self.object_orinetation_level = "front"  # "front" or "back"
        self.select_object_path_bind_mode = False

        self.tempANY_store = None
        self.preview_point = None
        self.loaded_from_file=False

        # sv_ttk.set_theme("dark")

        self.b = None
        self.selected_index = None
        self.bg_image_path = ""
        self.grid_size = 50
        self.grid_spacing = 50
        self.protected_elements = []
        self.root = root
        self.root.title("Level Editor")
        self.ofset_x = 0
        self.ofset_y = 0
        self.path_grid_mode = "free"  # 'free' or 'grid'
        self.grid_ofset = 0
        self.save_path = None
        self.displayimage = None
        self.curant_object_data = {}
        self.fill_mode = False
        self.fill_start_x = 0
        self.fill_start_y = 0
        self.curant_scripts = []

        self.rubber_mode = False
        self.rubber_area_id = None
        self.level_matadata = {"name": "", "dificulty": 1.0, "bg-music": ""}

        self.current_texture = None
        self.current_obj_type = None
        self.elements = []

        self.uids = set()
        # path data

        self.object_pathstore = []
        self.path_labels = []  # Store path label data (names)
        self.path_metadata = {}
        self.pathpoints = []
        self.path_position_offset = {"$curant": []}
        self.current_path = []

        self.path_entries = []
        self.pathfinding_mode = False

        self.root.configure(bg='#333440')

        self.left_Frame = ttk.Frame(root, )  # bg='#333440')
        self.left_Frame.pack(side="left", fill="both", expand=True)
        self.right_Frame = ttk.Frame(root, )  # bg='#333440')
        self.right_Frame.pack(side="right", fill="y")
        top_bar = ttk.Frame(self.left_Frame, )  # bg='#333440')
        top_bar.pack(fill="y", side="top", anchor="nw")
        top_frame = ttk.LabelFrame(top_bar, labelanchor="w")
        top_frame.pack(side="left", anchor="nw")
        can_tool_frame = ttk.Frame(self.left_Frame, )  # bg='#333440')
        can_tool_frame.pack(expand=True, fill="both")
        toolFrame = ttk.Frame(can_tool_frame, )  # bg='#333440')
        toolFrame.pack(side="left", anchor="ne")

        self.canvas = tk.Canvas(can_tool_frame, borderwidth=1, highlightbackground="gray", highlightthickness=1,
                                highlightcolor="gray")
        self.canvas.pack(fill=tk.BOTH, expand=True, side="left")
        self.create_cordnateSystem()
        self.bg_image = None  # Variable to store the background image

        self.canvas.bind("<Button-1>", self.canvas_left_click)
        self.canvas.bind("<Button-3>", self.canvas_right_click)
        self.canvas.bind("<Button-2>", self.canvas_middle_click)

        self.texture_buttons_frame = ttk.Frame(self.left_Frame, )  # bg='#333440')
        self.texture_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)

        self.canvas.bind("<Configure>", self.updatebg)

        f = ttk.Frame(self.right_Frame, )  # bg='#333440')
        f.pack(side=tk.TOP, anchor="nw")

        self.fill_button = tk.Button(toolFrame, text="🪣", command=self.toggle_fill_mode, bg='#444654', fg='white',
                                     font=tkfont.Font(size=12, weight="bold"), relief="flat")
        self.fill_button.pack(side=tk.TOP, anchor="n")

        self.rubber_button = tk.Button(toolFrame, text="🧽", command=self.toggle_rubber_mode, bg='#444654',
                                       font=tkfont.Font(size=12, weight="bold"), relief="flat", fg='white')
        self.rubber_button.pack(side=tk.TOP, anchor="n")

        root.bind("<Escape>", self.stop_fill)

        self.root.bind("<Control-s>", lambda e: self.save_elements())
        self.root.bind("<Control-l>", lambda e: self.load_elements())
        self.root.bind("<Control-Shift-b>", lambda e: self.select_bg_image())
        self.root.bind("<Control-Shift-s>", lambda e: self.save_elements(True))
        self.root.bind("<f>", lambda e: self.toggle_fill_mode())
        self.root.bind("<r>", lambda e: self.toggle_rubber_mode())

        self.root.bind("<q>", lambda e: self.toggle_path_craete_mode())

        #

        self.canvas.bind("<Motion>", self.update_preview)

        # Initialize data
        self.images = []

        self.texture_data = [
            {"name": "🎯 Spawnpoint", "path": "imgs/spawnpoint.png", "type": "spawn", "collision": False,
             "folder": "actions/"},
            {"name": "💀 Death-Area", "path": "imgs/death_area.png", "type": "death_area", "collision": False,
             "folder": "actions/"},
            {"name": " Light", "path": "imgs/light.png", "type": "light", "collision": False,
             "folder": "actions/"}
        ]

       """ self.texture_data += [
            {"name": "🖼 " + file.split(".", 1)[0], "path": "imgs/blocks/" + file,"collection":{}, "type": "object", "collision": True,
             "folder": "blocks/","material_unique":""}
            for file in get_files_in_folder("imgs/blocks/")
        ]"""

        self.texture_data += [
            {"name": "🖼 " + file.split(".", 1)[0], "path": "imgs/blocks/" + file, "type": "object", "collision": True,
             "folder": "blocks/"}
            for file in get_files_in_folder("imgs/blocks/")
        ]

        for folder in get_folders_in_folder("imgs/blocks/"):
            addSubfolder("blocks", folder)
            for file in get_files_in_folder("imgs/blocks/" + folder):
                self.texture_data += [
                    {"name": "🖼 " + file.split(".", 1)[0], "path": "imgs/blocks/" + folder + "/" + file,
                     "type": "object",
                     "collision": True, "folder": "blocks/" + folder + "/"}
                ]

        self.texture_data += [
            {"name": "✿ " + file.split(".", 1)[0], "path": "imgs/decoration/" + file, "type": "object",
             "folder": "deco/",
             "collision": False}
            for file in get_files_in_folder("imgs/decoration/")
        ]

        for folder in get_folders_in_folder("imgs/decoration/"):
            addSubfolder("blocks", folder)
            for file in get_files_in_folder("imgs/decoration/" + folder):
                self.texture_data += [
                    {"name": "✿ " + file.split(".", 1)[0], "path": "imgs/decoration/" + folder + "/" + file,
                     "type": "object",
                     "collision": True, "folder": "deco/" + folder + "/"}
                ]

        self.texture_data.append(
            {"name": "🏁 Finisch", "path": "imgs/finisch.png", "type": "level_finisch", "collision": False,
             "folder": "actions/"})

        root.tk.call("source", "ttk_theme/azure.tcl")
        root.tk.call("set_theme", "dark")

        editor_tabs_book = ttk.Notebook(self.right_Frame, width=210)
        editor_tabs_book.pack(side="top", fill="both", expand=True)
        self.editor_tabs_book = editor_tabs_book
        # tab 1

        general_setingsTab = ttk.Frame(editor_tabs_book)
        import interfaces.general_level_setings_menu as glsm

        self.general_setings_menu = glsm.GeneralLevelSetings_Window(general_setingsTab, self.level_matadata,
                                                                    lambda _, e: ())

        tab1 = ttk.Frame(editor_tabs_book)

        tap_paths = ttk.Frame(editor_tabs_book, )  # bg="#444654")

        # can
        fr2 = ttk.LabelFrame(tab1, text="path")
        fr2.pack(fill="x")

        scripts_frame = ttk.Frame(editor_tabs_book)

        self.folder_nav_back_button = tk.Button(fr2, text="ᐊ", width=1, font=tkfont.Font(size=10), relief="flat")
        self.folder_nav_back_button.pack(side=tk.LEFT)

        self.elements_path_area_label = tk.Label(fr2, text="/fvdsdf", anchor="nw")
        self.elements_path_area_label.pack(fill=tk.BOTH, side="left")

        canvas = tk.Canvas(tab1, width=200, bg='#333440', highlightthickness=0)

        editor_tabs_book.add(tab1, text="Elements",
                             image=createImage("imgs/editor/editor_element_tab.png", 16, 16, name="elements_tab_icon"))

        editor_tabs_book.add(tap_paths, text="Elements",
                             image=createImage("imgs/editor/editor_paths_tab.png", 16, 16, name="path_tab_icon"))

        editor_tabs_book.add(general_setingsTab, text="Lev Settings",
                             image=createImage("imgs/editor/level_setings.png", 16, 16,
                                               name="general_lev_setings_tab_icon"))

        editor_tabs_book.add(scripts_frame, text="Scripts",
                             image=createImage("imgs/editor/scripts_tab.png", 16, 16, name="scripts_tab_icon"))

        scrollbar = ttk.Scrollbar(master=tab1, command=canvas.yview, )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(fill=tk.BOTH, expand=True)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas for the scrollable content
        inner_frame = ttk.Frame(canvas, )  # bg='#333440')
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Configure the canvas to adjust scroll region when resized
        def on_configure(event):
            # Update the scroll region when the canvas size changes
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)

        # can

        self.texture_buttons_frame = inner_frame

        # self.texture_buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        # self.populate_texture_listbox()
        self.create_texture_buttons()
        self.save_button = tk.Button(top_frame, text="Save",
                                     command=self.save_elements, bg='#343540', fg='white', relief="flat")
        self.save_button.pack(side=tk.LEFT, )

        self.load_button = tk.Button(top_frame, text="Load", command=self.load_elements, bg='#444654', fg='white',
                                     relief="flat")
        self.load_button.pack(side=tk.LEFT, )
        self.select_bg_button = tk.Button(top_frame, text="Select Background Image", command=self.select_bg_image,
                                          relief="flat", bg='#343540', fg='white')
        self.select_bg_button.pack(side=tk.LEFT)

        back_front_controllFrame = ttk.LabelFrame(top_bar, text="", labelanchor="w")
        back_front_controllFrame.pack(side="left")

        def toback():
            self.send_to_front_button.configure(bg='#343540')
            self.object_orinetation_level = "back"
            self.send_to_back_button.configure(bg='#87D68D')

        def tofront():
            self.send_to_back_button.configure(bg='#343540')
            self.object_orinetation_level = "front"
            self.send_to_front_button.configure(bg='#87D68D')

        self.send_to_back_button = tk.Button(back_front_controllFrame,
                                             image=createImage("imgs/editor/to_back.png", 16, 16), command=toback,
                                             relief="flat", bg='#343540', fg='white')
        self.send_to_back_button.pack(side=tk.LEFT)

        self.send_to_front_button = tk.Button(back_front_controllFrame,
                                              image=createImage("imgs/editor/to_front.png", 16, 16),
                                              command=tofront,
                                              relief="flat", bg='#87D68D', fg='white')
        self.send_to_front_button.pack(side=tk.LEFT)

        self.scriptWIN = script_overview_menu.UIWindow(scripts_frame,self)

        checked_state = tk.BooleanVar()
        checked_state.set(True)

        grid_enabled_state = tk.BooleanVar()

        def on_grid_en_disable_click():
            if grid_enabled_state.get():
                self.path_grid_mode = "grid"
                # self.canvas.tag_raise("paths")
            else:
                self.path_grid_mode = "free"

        def on_checkbox_click():
            if checked_state.get():
                new_visibility = "normal"
                # self.canvas.tag_raise("paths")
            else:
                new_visibility = "hidden"

            self.canvas.itemconfigure("paths", state=new_visibility)

        checkboxes_frame = ttk.LabelFrame(tap_paths, text="Options")
        checkboxes_frame.pack(fill="x", anchor="ne")

        checkbox = ttk.Checkbutton(checkboxes_frame, text="Show Paths", variable=checked_state,
                                   command=on_checkbox_click)

        checkbox.pack(anchor="nw", pady=(4, 4), padx=(10, 0), side="left")
        checkbox_use_grid_for_paths = ttk.Checkbutton(checkboxes_frame, text="Use Grid", variable=grid_enabled_state,
                                                      command=on_grid_en_disable_click)

        checkbox_use_grid_for_paths.pack(anchor="nw", pady=(4, 4), padx=(0, 10), side="right")

        self.toggle_pathEdit_on_button = ttk.Button(tap_paths, text="+ Create New path",
                                                    command=self.toggle_path_craete_mode, )
        self.toggle_pathEdit_on_button.pack(anchor="nw", pady=(4, 4), padx=(10, 0))

        self.buttons = {}

        bindPath_button = ttk.Button(tap_paths, text="Bind Path", command=self.but_path_bind_mode)

        self.buttons["bindPath_button"] = bindPath_button
        bindPath_button.pack()

        f, scrollCan = returnScrollFrame(tap_paths, 500)
        r = ttk.LabelFrame(f, text="Courant Paths", )  # font=tkfont.Font(size=10))
        r.pack()
        self.pathInfo_overviewList_frame = r

        last_height = 0
        """def updateScrollList(e):
            nonlocal last_height
            if last_height!=e.height:
                last_height=e.height
                scrollCan.configure(height=e.height-400)

        tap_paths.bind("<Configure>",updateScrollList)"""

        # Configure the canvas to adjust scroll region when resized
        def on_configure(event):
            # Update the scroll region when the canvas size changes
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)

        L = ttk.Label(self.pathInfo_overviewList_frame, text="No Paths Created yet", )  # bg='#333440', fg="white")
        L.pack()
        self.path_entries += [L]
        self.pathInfo_overviewList_frame.pack(padx=10, pady=10, fill="both")

        """self.toggle_visibility_button =ttk.Button(tap_paths, text="Toggle Visibility",
                                                  command=self.toggle_object_path_visibility)
        self.toggle_visibility_button.pack()"""

    def but_path_bind_mode(self):
        if self.select_object_path_bind_mode == 0:
            self.buttons["bindPath_button"].configure(text="Exit binding")
            self.select_object_path_bind_mode = 1
        else:
            self.buttons["bindPath_button"].configure(text="Bind Path")
            self.select_object_path_bind_mode = 0

    def setPathAsBind(self, uid):
        if self.select_object_path_bind_mode == 1:
            self.path_to_bind = uid
            self.select_object_path_bind_mode = 2

    # path methods
    def toggle_path_craete_mode(self):
        self.pathfinding_mode = not self.pathfinding_mode
        if self.pathfinding_mode:
            self.toggle_pathEdit_on_button.config(text="Save Path")
            self.current_path = []
        else:
            self.toggle_pathEdit_on_button.config(text="+ Create New Path")
            if self.current_path:
                if len(self.current_path) >= 2:
                    id = self.gen_uuid()

                    self.path_metadata[id] = {"name": "New Path", "data": {}, "color": "#0FA3B1", "type": "moveline",
                                              "speed": 1.0}
                    self.object_pathstore.append((self.current_path, id))
                    self.path_position_offset[id] = self.path_position_offset["$curant"]
                    self.path_position_offset["$curant"] = []

                    self.current_path = []
                self.draw_object_paths()

    def gen_uuid(self):

        while True:
            uid = ''.join(random.choices(["1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e"], k=5))
            if uid not in self.uids:
                self.uids.add(uid)
                return uid

    def draw_object_paths(self):
        self.canvas.delete("temp_paths")
        self.canvas.delete("paths")

        def path_add_object_ofset():
            paths = []
            for n, points_pack in enumerate(self.object_pathstore):
                points, id = points_pack
                paths.append([[], id])
                for n2, p in enumerate(points):
                    paths[n][0] += [(p[0] + self.ofset_x, p[1] + self.ofset_y)]
            return paths

        for path, id in path_add_object_ofset():

            metadata = self.path_metadata[id]

            self.canvas.create_line(path[0], path[0 + 1], fill=metadata["color"], tags=["paths", "#movable"])

            self.canvas.create_oval(path[0][0] - 4, path[0][1] - 4, path[0][0] + 4, path[0][1] + 4, fill="yellow",
                                    tags=["paths", "#movable"])

            for i in range(1, len(path) - 1):
                self.canvas.create_line(path[i], path[i + 1], fill=metadata["color"], tags=["paths", "#movable"], )
                self.canvas.create_oval(path[i][0] - 4, path[i][1] - 4, path[i][0] + 4, path[i][1] + 4, fill="#B5E2FA",
                                        tags=["paths", "#movable"])
            self.canvas.create_oval(path[-1][0] - 4, path[-1][1] - 4, path[-1][0] + 4, path[-1][1] + 4, fill="red",
                                    tags=["paths", "#movable"])

        for entry in self.path_entries:
            entry.destroy()

        self.path_entries = []

        # Create path entries in the list frame
        for index, path_pac in enumerate(self.object_pathstore):
            path, id = path_pac
            path_entry = ttk.Frame(self.pathInfo_overviewList_frame, )  # '#333440')
            print(path)
            print(self.path_labels)
            """
                    ,bg='#444654',fg="white"
                    ,bg='#333440',fg="white"


                    """

            path_entry.pack(fill="x")
            if "bound_to" in self.path_metadata[id]["data"]:
                print(self.elements)
                e = [element for element in self.elements if
                     element["uuid"] == self.path_metadata[id]["data"]["bound_to"]]
                print(e)
                print("b", self.path_metadata[id]["data"]["bound_to"])
                if (e):
                    number_label = ttk.Label(path_entry, text=f"⛓️", width=3,
                                             anchor="w", )  # bg='#444654', fg="white")
                else:
                    number_label = ttk.Label(path_entry, text=f"{index + 1}.", width=3,
                                             anchor="w", )  # bg='#444654', fg="white")
                    self.path_metadata[id]["data"].pop("bound_to")
                    print("removed")
            else:

                number_label = ttk.Label(path_entry, text=f"{index + 1}.", width=3,
                                         anchor="w", )  # bg='#444654', fg="white")
            number_label.pack(side="left")

            name_label = ttk.Label(path_entry, text=self.path_metadata[id]["name"], width=15,
                                   anchor="w", )  # bg='#444654',
            # fg="white")
            name_label.pack(side="left")
            name_label.bind("<Button-1>", lambda e, uid=id: self.setPathAsBind(uid))

            edit_button = tk.Button(path_entry, text="✎", width=1,
                                    command=lambda i=index, idd=id: self.edit_object_path_metadata(idd),
                                    bg='#444654', fg="white", relief="flat")
            edit_button.pack(side="right")

            remove_button = tk.Button(path_entry, text="❌", width=1, command=lambda i=index: self.remove_object_path(i),
                                      bg='#444654', fg="white", relief="flat")
            remove_button.pack(side="right", padx=(0, 1))

            self.path_entries.append(path_entry)

    def edit_object_path_metadata(self, id):
        data_dict = self.path_metadata[id]
        f = ttk.Frame(self.editor_tabs_book)

        self.last_tab = self.editor_tabs_book.index(tkinter.CURRENT)

        i = self.editor_tabs_book.add(f, text="Elements",
                                      image=createImage("imgs/editor/element_edit.png", 16, 16,
                                                        name="edit_element_section_icon"))

        self.editor_tabs_book.select(f)

        edit_window = EditWindow(f, data_dict.copy(),
                                 lambda data, save, idv=id, ti=f: self.path_save_edited_metadata(idv, data, ti, save))

    def path_save_edited_metadata(self, id, data, tab_id, save_changes):
        self.editor_tabs_book.forget(tab_id)

        self.editor_tabs_book.select(self.last_tab)

        def is_valid_color_hex(input_string):
            pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
            return bool(pattern.match(input_string))

        self.path_metadata[id]["name"] = data["name"]
        color = data["color"]
        v = is_valid_color_hex(color)
        if v:
            self.path_metadata[id]["color"] = color
        self.path_metadata[id]["type"] = data["type"]
        self.path_metadata[id]["speed"] = data["speed"]

        self.draw_object_paths()

    def update_preview(self, event):
        if self.pathfinding_mode:
            if self.preview_point:
                self.canvas.delete(self.preview_point)
            x, y = event.x, event.y
            if (self.path_grid_mode == "grid"):
                x = (x // self.grid_spacing) * self.grid_spacing + 25
                y = (y // self.grid_spacing) * self.grid_spacing + 25
            self.preview_point = self.canvas.create_oval(x - 4, y - 4, x + 4, y + 4,
                                                         fill="gray", tags="temp_paths")

    def remove_object_path(self, index):
        if 0 <= index < len(self.object_pathstore):
            path, id = self.object_pathstore.pop(index)
            self.path_metadata.pop(id)
            if id in self.path_position_offset:
                self.path_position_offset.pop(id)
            self.draw_object_paths()
        else:
            print(index, len(self.object_pathstore))

    def toggle_object_path_visibility(self):
        current_visibility = self.canvas.itemcget("paths", "state")
        new_visibility = "normal" if current_visibility == "hidden" else "hidden"
        # self.canvas.tag_raise("paths")
        self.canvas.itemconfigure("paths", state=new_visibility)

    def create_texture_buttons(self, parent):
        for index, texture in enumerate(self.texture_data):
            row = index // 3
            col = index % 3

            texture_frame = ttk.Frame(parent, )  # bg='#333440')
            texture_frame.grid(row=row, column=col, padx=5, pady=5)

            image = ttk.PhotoImage(file=texture["path"])
            image_label = ttk.Label(texture_frame, image=image, )  # bg='#333440')
            image_label.image = image
            image_label.pack()

            name_label = ttk.Label(texture_frame, text=texture["name"], )  # bg='#333440', fg='white')
            name_label.pack()

    def new_create_texture_buttons(self, ):

        pass

    def create_texture_buttons(self):
        last_texture = None
        t = None
        row = 0
        element_jard = []
        col = -1
        folder_path = ["main"]

        p = tk.Label(self.texture_buttons_frame, text="Folders", bg='#333440', fg='white')

        def create_folder_button(path, name):
            global folders
            nonlocal element_jard
            texture_frame = tk.Frame(self.texture_buttons_frame, bg='#333440')
            texture_frame.grid(row=row, column=col, padx=5, pady=5)

            def selectItem(path):
                folder_path.append(path)
                load_folder_content()

            image = createImage("imgs/editor/folder.png", 50, 50, name="folder_icon".split("/")[-1])
            image_label = tk.Label(texture_frame, image=image, bg='#333440', width=50, height=25)

            image_label.image = image
            image_label.pack()
            pr = name

            if len(pr) > 15:
                pr = pr[:12] + "..."

            name_label = tk.Label(texture_frame, text=pr, bg='#333440', fg='white', width=12, anchor="n")
            name_label.bind("<Button-1>", lambda e, pat=path: selectItem(pat))

            image_label.bind("<Button-1>", lambda e, pat=path: selectItem(pat))
            texture_frame.bind("<Button-1>",
                               lambda e, pat=path: selectItem(pat))

            name_label.pack(anchor="n", side="top")

            element_jard += [name_label, image_label, texture_frame]

        def navBack():
            nonlocal folder_path
            if len(folder_path) == 1: return
            folder_path.pop()
            load_folder_content()

        self.folder_nav_back_button.configure(command=navBack)

        def load_folder_content():

            nonlocal row, col, element_jard, last_texture
            last_texture = None
            for e in element_jard:
                e.destroy()
            row = 0
            col = -1

            def getCurant_subfolders():
                p = folder_path.copy()
                cd = folders
                print("folders", folders)
                while p:
                    cd = cd[p.pop(0)]
                return cd

            for f in getCurant_subfolders():
                print(f)
                col += 1
                if col >= 2:
                    row += 1
                    col = 0

                create_folder_button(f, f)

            path_str = ""
            for i in folder_path[1::]:
                path_str += i + "/"

            self.elements_path_area_label.configure(text=path_str)
            for index, texture in enumerate(self.texture_data):
                if not texture["path"].endswith(".png"): continue

                print(texture)
                if texture["folder"] != path_str:
                    continue
                col += 1
                if col >= 2:
                    row += 1
                    col = 0

                texture_frame = tk.Frame(self.texture_buttons_frame, bg='#333440')
                texture_frame.grid(row=row, column=col, padx=5, pady=5)

                def selectItem(texture_frame, texture, namelabel):
                    texture = self.texture_data[texture]
                    nonlocal last_texture
                    if self.curant_object_data == texture: return

                    if last_texture:
                        last_texture[0].configure(bg="#333440")
                        last_texture[1].configure(bg="#333440")
                    texture_frame.configure(bg="green")
                    namelabel.configure(bg="green")
                    last_texture = (texture_frame, namelabel)
                    print(texture)
                    self.current_obj_type = texture["type"]
                    print(texture["type"])

                    self.curant_object_data = texture
                    self.current_texture = texture["path"]

                image = createImage(texture["path"], 25, 25, name=texture["path"].split("/")[-1])
                image_label = tk.Label(texture_frame, image=image, bg='#333440')

                image_label.image = image
                image_label.pack()
                pr = texture["name"]

                if len(texture["name"]) > 15:
                    pr = pr[:12] + "..."

                name_label = tk.Label(texture_frame, text=pr, bg='#333440', fg='white', width=12, anchor="w")
                name_label.bind("<Button-1>",
                                lambda e, te=texture_frame, tex=index, nl=name_label: selectItem(te, tex, nl))

                image_label.bind("<Button-1>",
                                 lambda e, te=texture_frame, tex=index, nl=name_label: selectItem(te, tex, nl))
                texture_frame.bind("<Button-1>",
                                   lambda e, te=texture_frame, tex=index, nl=name_label: selectItem(te, tex, nl))

                name_label.pack()
                element_jard += [name_label, image_label, texture_frame]

        load_folder_content()

    def updatebg(self, e):
        if self.bg_image_path:
            if self.b in self.protected_elements:
                self.protected_elements.remove(self.b)

            self.canvas.delete(self.b)
            StatikImage.remove(self.bg_image)
            w = self.canvas.winfo_width()
            fac = w / G_WIDTH

            h = G_HEIGHT * fac
            if h < 0:
                h = -h
            print(w, h, G_WIDTH, fac)

            self.bg_image = createImage(self.bg_image_path, int(w), int(h), name="background_image")

            self.b = self.canvas.create_image(0, h // 2 - self.canvas.winfo_height(), anchor=tk.NW, image=self.bg_image,
                                              tags="background")
            self.protected_elements += [self.b]
            self.canvas.lower(self.b)

    def select_bg_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.bg_image_path = file_path
            self.bg_image = createImage(file_path, G_WIDTH, G_HEIGHT, name="background_image")
            self.b = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image, tags="background")
            self.protected_elements += [self.b]
            self.canvas.tag_lower("background")  # Move background to the bottom

    def load_elements(self, file=None, saveMode=False):
        try:
            if not file:
                ask = ask_dir_dialog()
                if not ask:
                    return
            else:

                ask = file
            self.canvas.delete("all")  # Clear canvas before loading new elements
            self.protected_elements = []
            self.object_pathstore = []
            self.path_metadata = []
            self.create_cordnateSystem()

            with open(ask+"/level.levdat") as f:
                level_json = json.load(f)
            """
            Note Save mode doesnt check all properties of the json file
            """
            if saveMode:
                pr = [[], [], [], {}]
                props = ["elements", "paths", "scripts", "path-metadata"]
                for property in props:
                    if property not in level_json:
                        level_json[property] = pr[props.index(property)]
            self.root.title("Editing - " + ask.split("/")[-1])
            self.save_path = ask

            self.ofset_y, self.ofset_x = 0, 0

            self.elements = []
            elem = level_json["elements"]
            for n, element in enumerate(elem):
                if element["type"] == "bg_image":
                    self.bg_image_path = element["texture"]

                    self.bg_image = createImage(element["texture"], G_WIDTH, G_HEIGHT,
                                                name=element["texture"].split("/")[-1])
                    self.b = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image, tags="background")

                    self.protected_elements += [self.b]
                    self.canvas.tag_lower("background")  # Move background to the bottom
                    self.updatebg("")
                    continue
                if not element.get("uuid"):
                    element["uuid"] = self.gen_uuid()
                image = createImage(element["texture"], 50, 50, name=element["texture"].split("/")[-1])
                image_width, image_height = image.width(), image.height()

                id = self.canvas.create_image(element["x"], element["y"], image=image, tags=["#movable"], anchor="nw")
                element["id"] = id
                self.elements += [element]
            self.canvas.tag_raise("coordinate_labels")  # , "coordinate_labels")
            self.path_metadata = {}

            self.path_position_offset = {"$curant": []}
            self.object_pathstore = level_json["paths"]
            for path, id in self.object_pathstore:
                self.path_position_offset[id] = None

            self.path_metadata = level_json["path-metadata"]
            self.draw_object_paths()

            self.curant_scripts = level_json["scripts"]
            self.scriptWIN.renewEntrys(self.curant_scripts)

            for key in level_json["level-metadata"]:
                self.level_matadata[key] = level_json["level-metadata"][key]
            self.general_setings_menu.updatefunc()
        except Exception as e:
            from tkinter import messagebox
            q = messagebox.askquestion("Error", str(e) + "Retry in Save Mode ?")
            if q == "yes":
                self.load_elements(ask, True)

    def toggle_rubber_mode(self):
        self.rubber_mode = not self.rubber_mode
        if self.rubber_mode:
            if self.fill_mode:
                self.toggle_fill_mode()
            self.rubber_button.configure(bg="#DD1155")
            self.canvas.unbind("<Button-1>")

            self.canvas.bind("<Button-1>", self.start_rubber)
        else:
            self.stop_rubber()
            self.canvas.unbind("<Button-1>")
            self.rubber_button.configure(bg='#444654', )
            self.canvas.bind("<Button-1>", self.canvas_left_click)

    def start_rubber(self, event):
        self.rubber_area_id = self.canvas.create_oval(0, 0, 0, 0, outline="red", tags="rubber_area")
        self.canvas.bind("<B1-Motion>", self.erase_elements)

    def erase_elements(self, event):
        if self.rubber_mode:
            x1, y1 = event.x - 10, event.y - 10
            x2, y2 = event.x + 10, event.y + 10
            elements_to_remove = self.canvas.find_overlapping(x1, y1, x2, y2)
            for element_id in elements_to_remove:
                if element_id in self.protected_elements:
                    continue
                self.canvas.delete(element_id)
                self.elements = [element for element in self.elements if element["id"] != element_id]

                # unbinds paths if there
                id = [element for element in self.path_metadata if
                      self.path_metadata[element]["data"]["bound_to"] == element_id]
                if id:
                    self.path_metadata[id[0]]["data"].pop("bound_to")

    def stop_rubber(self):
        self.canvas.delete(self.rubber_area_id)
        self.canvas.unbind("<B1-Motion>")

    def create_cordnateSystem(self):
        canvas_width = 500
        canvas_height = 500

        a = self.canvas.create_line(0, -canvas_height * 2, 0, canvas_height * 2, tags=["coordinate_labels", "#movable"],
                                    fill="white")

        b = self.canvas.create_line(-canvas_width * 2, 0, canvas_width * 2, 0, tags=["coordinate_labels", "#movable"],
                                    fill="white")

        b1 = self.canvas.create_line(canvas_width * 2 + 6, -canvas_height * 2, -canvas_width * 2, -canvas_height * 2,
                                     tags="coordinate_lines", fill="white")

        b2 = self.canvas.create_line(-canvas_width * 2, canvas_height * 2, canvas_width * 2, canvas_height * 2,
                                     tags=["coordinate_labels", "#movable"], fill="white")
        b3 = self.canvas.create_line(-canvas_width * 2, -canvas_height * 2, -canvas_width * 2, canvas_height * 2
                                     , tags=["coordinate_labels", "#movable"], fill="white")
        b4 = self.canvas.create_line(canvas_width * 2, -canvas_height * 2, canvas_width * 2, canvas_height * 2
                                     , tags=["coordinate_labels", "#movable"], fill="white")

        for i in range(-canvas_width * 2 + 50, canvas_width * 2, 50):
            if i != 0:
                self.protected_elements.append(
                    self.canvas.create_text(i, 10, text=f"{i}", tags=["coordinate_labels", "#movable"], fill="white"))

            else:
                self.protected_elements.append(
                    self.canvas.create_text(i + 6, 8, text=f"{i}", tags=["coordinate_labels", "#movable"],
                                            fill="white"))

        for i in range(-canvas_width * 2 + 50, canvas_width * 2, 50):
            if i != 0:
                self.protected_elements.append(
                    self.canvas.create_text(10, i, text=f"{i}", tags=["coordinate_labels", "#movable"], fill="white"))

        self.protected_elements += [a, b, b1, b2, b3, b4]

    def stop_fill(self, event=None):
        self.fill_mode = False
        self.canvas.delete(self.fill_area_id)
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-1>")

    def move_element(self, event):
        print("move")

        dx = event.x - self.prev_x
        dy = event.y - self.prev_y
        self.prev_x = event.x
        self.prev_y = event.y
        self.ofset_x += dx
        self.ofset_y += dy

        self.canvas.move("#movable", dx, dy)

    """self.images+=[new_image]"""

    def final_bind_element_to_path(self):
        element_uid, can_element_id = self.tempANY_store
        path_uid = self.path_to_bind
        self.path_metadata[path_uid]["data"]["bound_to"] = element_uid
        self.select_object_path_bind_mode = 0
        self.draw_object_paths()
        self.buttons["bindPath_button"].configure(text="Start binding")
        e = [element for element in self.elements if
             element["uuid"] == self.path_metadata[path_uid]["data"]["bound_to"]]
        if e:
            el = e[0]
            op = [path for path in self.object_pathstore if path[1] == path_uid]
            if op:
                p = op[0][0][0]
                print(p)

                point_x, point_y = p[0], p[1]
                o = self.path_position_offset[path_uid]
                if o:

                    map_ofset_x, map_ofset_y = self.ofset_x - o[0][0], self.ofset_y - o[0][1]

                else:

                    map_ofset_x, map_ofset_y = self.ofset_x, self.ofset_y

                box_x, box_y = el["x"] - map_ofset_x, el["y"] - map_ofset_y

                mx, my = box_x + point_x, box_y + point_y
                #
                self.canvas.move(can_element_id, -25 - box_x +  # zurück move nach 0,0
                                 (point_x - map_ofset_x)  # move zum punkt
                                 , -25 - box_y + (point_y - map_ofset_y))

                # self.canvas.move(can_element_id,mx,my)

                el["x"], el["y"] = point_x - 25, point_y - 25

    def canvas_left_click(self, event):

        if self.select_object_path_bind_mode == 2:
            e, can_element_id = self.get_Id_by_Click(event)
            if e:
                self.tempANY_store = e[0]["uuid"], can_element_id
                self.select_object_path_bind_mode = 3
                self.final_bind_element_to_path()





        elif self.pathfinding_mode:
            x, y = event.x, event.y
            if (self.path_grid_mode == "grid"):
                x = (x // self.grid_spacing) * self.grid_spacing + 25
                y = (y // self.grid_spacing) * self.grid_spacing + 25

            # self.pathpoints.append((x, y))

            self.current_path.append((x - self.ofset_x, y - self.ofset_y))
            self.path_position_offset["$curant"] += [(0, 0)]
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", tags=["paths", "temp_paths", "#movable"])
            if len(self.current_path) > 1:
                ox, oy = self.last_ofset
                pa, pb = self.last_point
                print("diference", (self.ofset_x + ox))

                self.canvas.create_line((pa + (self.ofset_x + ox), pb + (self.ofset_y + oy)), (
                self.current_path[-1][0] + self.ofset_x, self.current_path[-1][1] + self.ofset_y), fill="blue",
                                        tags=["paths", "temp_paths", "#movable"])
            self.last_ofset = (-self.ofset_x, -self.ofset_y)
            self.last_point = (x, y)

        elif self.current_texture:
            print(self.current_obj_type)
            x, y = event.x, event.y

            snapped_x = round((x - 25 - self.ofset_x) / self.grid_size) * self.grid_size + self.ofset_x
            snapped_y = round((y - 25 - self.ofset_y) / self.grid_size) * self.grid_size + self.ofset_y

            # print(snapped_x+grid_offset_x)
            print(snapped_x, x)

            image = createImage(self.current_texture, 50, 50, name=self.current_texture.split("/")[-1])
            image_width, image_height = image.width(), image.height()
            # new_image = image.subsample(2)  # Half the size
            # self.images += [new_image]
            element = self.canvas.create_image(snapped_x, snapped_y, image=image, tags=["#movable"], anchor="nw")
            self.elements.append({
                "id": element,
                "type": self.current_obj_type,
                "texture": self.current_texture,
                "x": snapped_x - self.ofset_x, "y": snapped_y - self.ofset_y,
                "collision": self.curant_object_data["collision"],
                "width": BLOCK_SIZE, "height": BLOCK_SIZE,
                "nbt": {},
                "o-layer": self.object_orinetation_level,
                "uuid": self.gen_uuid()
            })
            self.canvas.tag_raise("coordinate_labels")

    def add_temp_side_tab(self) -> ttk.Frame:
        f = ttk.Frame(self.editor_tabs_book)

        self.last_tab = self.editor_tabs_book.index(tkinter.CURRENT)

        i = self.editor_tabs_book.add(f, text="Elements",
                                      image=createImage("imgs/editor/element_edit.png", 16, 16,
                                                        name="edit_element_section_icon2"))
        self.editor_tabs_book.select(f)
        return f

    def canvas_right_click(self, event):
        selected_element = self.canvas.find_closest(event.x, event.y)
        if selected_element[0] in self.protected_elements:
            return

        def open_context_menu(event):
            context_menu = tk.Menu(root, tearoff=0)
            context_menu.add_command(label="Edit Interaction", command=lambda i=selected_element[0]:action_1(i))
            context_menu.add_command(label="Edit plain NBT", command=lambda i=selected_element[0]:action_2(i))
            context_menu.add_separator()
            context_menu.add_command(label="ER_MISSING", command=action_3)

            context_menu.tk_popup(event.x_root, event.y_root)

        def action_1(id):

            def on_done(tab,id, dict, Save):
                self.editor_tabs_book.forget(tab)
                if Save:
                    object_ = [o for o in self.elements if id == id]
                    if object_:
                        if dict["sptype"] == "None":

                            if "interact" in object_[0]["nbt"]:
                                object_[0]["nbt"].pop("interact")

                        else:
                            object_[0]["nbt"]["interact"] = {"sptype": dict["sptype"], "trigger": dict["trigger"],
                                                             "function": dict["function"]}

            nbt = [o for o in self.elements if o["id"] == selected_element[0]][0]["nbt"]
            if not "interact" in nbt:
                action = {"sptype": "None", "trigger": "None", "function": ""}
            else:
                action=nbt["interact"].copy()
            f = self.add_temp_side_tab()

            m = ObjectPropertiesMenu(f, action,
                                     lambda nbt, save,tab=f, i=selected_element[0]: on_done(tab,i, nbt.copy(), save))

            print("Action 1 selected")

        def action_2(id):
            import interfaces.nbt_directEdit
            obj = [o for o in self.elements if o["id"] == id][0]
            if "nbt" in obj:
                nbt_win=interfaces.nbt_directEdit.nbt_directEdit(obj, )

        def action_3():
            print("Action 3 sele")

        open_context_menu(event)

        """if selected_element:
            self.canvas.delete(selected_element)
            print(self.elements)
            self.elements = [element for element in self.elements if element["id"] != selected_element[0]]
            if hasattr(self, 'selected_element') and self.selected_element == selected_element[0]:
                self.selected_label.config(text="Selected: None")"""

    def get_Id_by_Click(self, event):

        selected_element = self.canvas.find_closest(event.x, event.y)
        if selected_element[0] in self.protected_elements:
            return
        if selected_element:
            print(self.elements)
            e = [element for element in self.elements if element["id"] == selected_element[0]]

            return e, selected_element

    def canvas_middle_click(self, event):
        print("fdsfdsfsda")
        self.prev_x = event.x
        self.prev_y = event.y
        self.canvas.bind("<B2-Motion>", self.move_element)
        self.canvas.bind("<ButtonRelease-2>", self.stop_move_element)

    def stop_move_element(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-2>")

    def save_elements(self, force=False):

        print("Saved elements:")




        if ((not self.save_path) | force):

            sf = ask_dir_dialog()
            os.mkdir(sf+"/resources")
            os.mkdir(sf + "/scripts")

        else:
            sf = self.save_path
        if not sf:
            return
        self.save_path = sf
        self.root.title("Editing - " + sf.split("/")[-1])

        pp = self.object_pathstore
        self.loaded_from_file=True
        with open(sf+"/level.levdat", "w") as f:
            if self.bg_image:
                json.dump(
                    {"elements": [{"type": "bg_image", "texture": self.bg_image_path}] + self.elements, "paths": pp,
                     "path-metadata": self.path_metadata, "level-metadata": self.level_matadata,
                     "scripts": self.curant_scripts}, f)
            else:
                json.dump(
                    {"elements": self.elements, "paths": pp,
                     "path-metadata": self.path_metadata, "level-metadata": self.level_matadata,
                     "scripts": self.curant_scripts}, f)

    def toggle_fill_mode(self):
        self.fill_mode = not self.fill_mode
        if self.fill_mode:
            self.fill_button.configure(bg='green')
            if self.rubber_mode:
                self.toggle_rubber_mode()
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.start_fill)
        else:
            self.fill_button.configure(bg='#444654')
            self.canvas.unbind("<Button-1>")
            self.canvas.bind("<Button-1>", self.canvas_left_click)
            self.canvas.unbind("<B1-Motion>")
            self.canvas.unbind("<ButtonRelease-1>")

    def start_fill(self, event):
        self.fill_start_x = event.x
        self.fill_start_y = event.y
        self.fill_area_id = self.canvas.create_rectangle(0, 0, 0, 0, outline="#92BDA3", width=2, tags="fill_area")

        self.canvas.bind("<B1-Motion>", self.draw_fill_area)
        self.canvas.bind("<ButtonRelease-1>", self.end_fill)

    def draw_fill_area(self, event):
        x1, y1 = self.fill_start_x, self.fill_start_y
        x2, y2 = event.x, event.y

        # Calculate grid-aligned coordinates for both points
        snapped_x1 = ((x1 - self.ofset_x) // self.grid_size) * self.grid_size + self.ofset_x
        snapped_y1 = ((y1 - self.ofset_y) // self.grid_size) * self.grid_size + self.ofset_y
        snapped_x2 = ((x2 - self.ofset_x) // self.grid_size) * self.grid_size + self.ofset_x
        snapped_y2 = ((y2 - self.ofset_y) // self.grid_size) * self.grid_size + self.ofset_y

        self.canvas.coords(self.fill_area_id, snapped_x1, snapped_y1, snapped_x2, snapped_y2)

    def end_fill(self, event):
        x1, y1 = self.fill_start_x, self.fill_start_y
        x2, y2 = event.x, event.y
        self.canvas.delete("fill_area")

        # Calculate grid-aligned coordinates
        snapped_x1 = ((x1 - self.ofset_x) // self.grid_size) * self.grid_size + self.ofset_x
        snapped_y1 = ((y1 - self.ofset_y) // self.grid_size) * self.grid_size + self.ofset_y
        snapped_x2 = ((x2 - self.ofset_x) // self.grid_size) * self.grid_size + self.ofset_x
        snapped_y2 = ((y2 - self.ofset_y) // self.grid_size) * self.grid_size + self.ofset_y

        if snapped_x2 < snapped_x1:
            snapped_x2, snapped_x1 = snapped_x1, snapped_x2

        if snapped_y2 < snapped_y1:
            snapped_y2, snapped_y1 = snapped_y1, snapped_y2

        print(snapped_x1, snapped_y1, snapped_x2, snapped_y2, self.current_texture)

        if self.current_texture:

            for iy in range(snapped_y1, snapped_y2, 50):
                for ix in range(snapped_x1, snapped_x2, 50):
                    if self.current_texture:
                        snapped_x, snapped_y = ix, iy

                        image = createImage(self.current_texture, 50, 50, name=self.current_texture)
                        image_width, image_height = image.width(), image.height()

                        element = self.canvas.create_image(snapped_x, snapped_y, image=image, tags=["#movable"],
                                                           anchor="nw")
                        self.elements.append({
                            "id": element,
                            "type": self.current_obj_type,
                            "texture": self.current_texture,
                            "x": snapped_x - self.ofset_x, "y": snapped_y - self.ofset_y,
                            "collision": self.curant_object_data["collision"],
                            "width": image_width, "height": image_height,
                            "tags": [],
                            "uuid": self.gen_uuid()
                        })
            self.canvas.tag_raise("coordinate_labels")  # , "coordinate_labels")


class fake_event():
    def __init__(self, x, y):
        self.x, self.y = x, y


root = tk.Tk()
app = CanvasApp(root)
root.mainloop()
