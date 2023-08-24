import tkinter as tk
from tkinter import ttk

class ObjectPropertiesMenu:
    def __init__(self, root, data_dict, ret_function):
        self.root = root


        self.data_dict = data_dict
        self.ret_function = ret_function

        self.type_var = tk.StringVar(value=data_dict.get("sptype", ""))
        self.triger_var = tk.StringVar(value=data_dict.get("trigger", ""))
        self.function_var = tk.StringVar(value=data_dict.get("function", ""))




        self.trigers=["Button-Interact_Main","Button-Interact_Second","Collision-BoxCollide","Collision-Box-HOVER","NONE","Action-Attack"]
        self.special_types=["Interactive","Destroy","None"]

        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.root.tk_setPalette(background="#2E2E2E", foreground="white", activeBackground="#4E4E4E",
                                activeForeground="white")



    def setup_ui(self):
        save_button = ttk.Button(self.root, text="✖",width=2, command=lambda :self.save_and_close(False), style="Dark.TButton")
        save_button.pack(side="top",anchor="ne")

        type_label = ttk.Label(self.root, text="Select Object Type", foreground="white", background="#2E2E2E")
        type_label.pack()

        type_combobox = ttk.Combobox(self.root, textvariable=self.type_var, values=self.special_types)
        type_combobox.pack()

        InteractTriger_label = ttk.Label(self.root, text="Select Trigger (If interaction)", foreground="white", background="#2E2E2E")
        InteractTriger_label.pack()

        InteractTriger_Box = ttk.Combobox(self.root, textvariable=self.triger_var, values=self.trigers)
        InteractTriger_Box.pack()

        fuction_label = ttk.Label(self.root, text="Function (IF interaction)", foreground="white", background="#2E2E2E")
        fuction_label.pack()

        func_entry = ttk.Entry(self.root, textvariable=self.function_var, style="Dark.TEntry")
        func_entry.pack()

        save_button = ttk.Button(self.root, text="Save", command=self.save_and_close, style="Dark.TButton")
        save_button.pack()


    def save_and_close(self,save=True):
        self.data_dict["sptype"] = self.type_var.get()
        self.data_dict["trigger"] = self.triger_var.get()
        self.data_dict["function"] = self.function_var.get()
        """
        self.data_dict["color"] = self.color_var.get()
        self.data_dict["type"] = self.type_var.get()
        self.data_dict["speed"] = round(self.speed_var.get(),3)"""

        self.ret_function(self.data_dict, save)

