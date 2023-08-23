import os
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import filedialog
class PermissionWindow:
    def __init__(self, parent, permissions, update_function):
        self.window = tk.Toplevel(parent)
        self.window.title("Set Permissions")

        self.permissions = permissions
        self.update_function = update_function

        self.permission_vars = []
        names= {"Read":"file.read", "Write":"file.write", "Allow-Unlimited-imports":"scripts.all_import"}

        for permission in names:
            var = tk.BooleanVar(value=names[permission] in self.permissions)
            self.permission_vars.append(var)
            checkbox = ttk.Checkbutton(self.window, text=permission, variable=var)
            checkbox.pack(side="top", anchor="w")

        save_button = ttk.Button(self.window, text="Save Permissions", command=self.save_permissions)
        save_button.pack(side="top")

    def save_permissions(self):
        names = {"Read Files": "file.read", "Write Files": "file.write", "Allow-Unlimited-imports": "scripts.all_import"}

        new_permissions = []
        for i, var in enumerate(self.permission_vars):
            if var.get():
                new_permissions.append(list(names.values())[i])

        self.update_function(new_permissions)
        self.window.destroy()

class UIWindow:
    def __init__(self, root):
        self.root = root


        self.entries = []

        self.scroll_frame = ttk.Frame(root)
        self.scroll_frame.pack(side="top", fill="both", expand=True)

        self.canvas = tk.Canvas(self.scroll_frame,width=200)
        self.canvas.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.scroll_frame, command=self.canvas.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.add_button = ttk.Button(root, text="Add Entry", command=self.add_entry)
        self.add_button.pack(side="top")
        self.frame = ttk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor="nw",width=186)




        self.save_button = ttk.Button(root, text="Save Entries", command=self.save_entries)
        self.save_button.pack(side="bottom")

    def add_entry(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python and Lua Files", "*.py *.lua")])
        print("se",os.getcwd())
        file_path=file_path.replace("\\","/").replace(os.getcwd().replace("\\","/"),"")
        print(file_path)
        if file_path:

            entry = {"name": file_path.split("/")[-1], "path": file_path, "permissions": []}
            self.entries.append(entry)
            self.display_entries()
    def renewEntrys(self,new):
        self.entries=new
        self.display_entries()

    def remove_entry(self, index):
        self.entries.pop(index)
        self.display_entries()

    def set_permissions(self, index):
        entry = self.entries[index]
        PermissionWindow(self.root, entry["permissions"], lambda new_permissions: self.update_permissions(index, new_permissions))

    def update_permissions(self, index, new_permissions):
        self.entries[index]["permissions"] = new_permissions
        self.display_entries()

    def display_entries(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

        for index, entry in enumerate(self.entries):
            frame = tk.Frame(self.frame,highlightcolor="green",highlightthickness=1,highlightbackground="green")
            frame.pack(fill="x", expand=True)

            file_label = ttk.Label(frame, text="📄")
            file_label.pack(side="left")

            name_label = ttk.Label(frame, text=entry["name"])
            name_label.pack(side="left",)

            remove_button = tk.Button(frame, text="🗑️", command=lambda i=index: self.remove_entry(i),relief="flat")
            remove_button.pack(side="right")

            permission_button = tk.Button(frame, text="🔒", command=lambda i=index: self.set_permissions(i),relief="flat")
            permission_button.pack(side="right")

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def save_entries(self):
        for entry in self.entries:
            print(entry)