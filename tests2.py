import random
import string
import tkinter as tk

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Example")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.object_pathstore = []
        self.path_labels = []  # Store path label data (names)
        self.path_metadata = {}
        self.pathpoints = []
        self.points = []
        self.grid_spacing=50
        self.current_path = []

        self.pathInfo_overviewList_frame = tk.Frame(root)
        self.pathInfo_overviewList_frame.pack(side="right", padx=10, pady=10)

        self.path_entries = []
        self.pathfinding_mode = False
        self.toggle_pathEdit_on_button = tk.Button(root, text="Toggle Pathfinding Mode", command=self.toggle_path_craete_mode)
        self.toggle_pathEdit_on_button.pack()

        self.toggle_visibility_button = tk.Button(root, text="Toggle Visibility", command=self.toggle_object_path_visibility)
        self.toggle_visibility_button.pack()

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.preview_point = None

        # Bind the motion event to the canvas
        self.canvas.bind("<Motion>", self.update_preview)

        def pr(e):
            print(self.object_pathstore)

        self.root.bind("<e>",pr)

    def update_preview(self, event):
        if self.pathfinding_mode:
            if self.preview_point:
                self.canvas.delete(self.preview_point)
            x, y = event.x, event.y
            snapped_x = (x // self.grid_spacing) * self.grid_spacing+25
            snapped_y = (y // self.grid_spacing) * self.grid_spacing+25
            self.preview_point = self.canvas.create_oval(snapped_x - 4, snapped_y - 4, snapped_x + 4, snapped_y + 4,
                                                         fill="gray", tags="temp_paths")

    def toggle_path_craete_mode(self):
        self.pathfinding_mode = not self.pathfinding_mode
        if self.pathfinding_mode:
            self.toggle_pathEdit_on_button.config(text="Exit Pathfinding Mode")
            self.current_path = []
        else:
            self.toggle_pathEdit_on_button.config(text="Toggle Pathfinding Mode")
            if self.current_path:
                id = self.gen_path_id()

                self.path_metadata[id] = {"name": "New Path", "data": {}}
                self.object_pathstore.append((self.current_path, id))
                self.current_path = []
            self.draw_object_paths()

    def canvas_click(self, event):
        if self.pathfinding_mode:
            x, y = event.x, event.y
            snapped_x = (x // self.grid_spacing) * self.grid_spacing+25
            snapped_y = (y // self.grid_spacing) * self.grid_spacing+25
            self.points.append((snapped_x, snapped_y))
            self.current_path.append((snapped_x, snapped_y))
            self.canvas.create_oval(snapped_x - 3, snapped_y - 3, snapped_x + 3, snapped_y + 3, fill="red", tags=["paths", "temp_paths"])
            if len(self.current_path) > 1:
                self.canvas.create_line(self.current_path[-2], self.current_path[-1], fill="blue", tags=["paths", "temp_paths"])


    def gen_path_id(self):
        return ''.join(random.choices(["1","2","3","4","5","6","7","8","9","a","b","c","d","e"], k=5))
    def draw_object_paths(self):
        self.canvas.delete("temp_paths")
        self.canvas.delete("paths")
        for path,id in self.object_pathstore:

            for i in range(len(path) - 1):
                self.canvas.create_line(path[i], path[i + 1], fill="green", tags=["paths","o"],)
                self.canvas.create_oval(path[i][0] - 3, path[i][1] - 3, path[i][0] + 3, path[i][1] + 3, fill="green", tags=["paths"])
            self.canvas.create_oval(path[-1][0] - 3, path[-1][1] - 3, path[-1][0] + 3, path[-1][1] + 3, fill="red", tags=["paths"])

        for entry in self.path_entries:
            entry.destroy()
        self.path_entries = []

        # Create path entries in the list frame
        for index, path_pac in enumerate(self.object_pathstore):
            path, id=path_pac
            path_entry = tk.Frame(self.pathInfo_overviewList_frame, bg="white")
            print(path)
            print(self.path_labels)

            path_entry.pack(fill="x")

            number_label = tk.Label(path_entry, text=f"{index + 1}.", width=3, anchor="w")
            number_label.pack(side="left")

            name_label = tk.Label(path_entry, text=self.path_metadata[id]["name"], width=15, anchor="w")
            name_label.pack(side="left")

            edit_button = tk.Button(path_entry, text="Edit", command=lambda i=index: self.edit_object_path_metadata(id))
            edit_button.pack(side="right")

            remove_button = tk.Button(path_entry, text="❌", command=lambda i=index: self.remove_object_path(i))
            remove_button.pack(side="right")

            self.path_entries.append(path_entry)

    def edit_object_path_metadata(self, id):
        edit_window = tk.Toplevel(self.root)
        edit_window.title("Edit Path")

        new_name_label = tk.Label(edit_window, text="New Name:")
        new_name_label.pack()

        new_name_entry = tk.Entry(edit_window)
        new_name_entry.pack()

        save_button = tk.Button(edit_window, text="Save",
                                command=lambda: self.path_save_edited_metadata(id, new_name_entry.get(), edit_window))
        save_button.pack()

    def path_save_edited_metadata(self, id, new_name, edit_window):

        self.path_metadata[id]["name"]=new_name

        self.draw_object_paths()
        edit_window.destroy()

    def remove_object_path(self, index):
        if 0 <= index < len(self.object_pathstore):
            path,id=self.object_pathstore.pop(index)
            self.path_metadata.pop(id)
            self.draw_object_paths()
    def toggle_object_path_visibility(self):
        current_visibility = self.canvas.itemcget("paths", "state")
        new_visibility = "normal" if current_visibility == "hidden" else "hidden"
        #self.canvas.tag_raise("paths")
        self.canvas.itemconfigure("paths", state=new_visibility)


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()

