import tkinter as tk
from tkinter import ttk

class EditWindow:
    def __init__(self, root, data_dict, ret_function):
        self.root = root


        self.data_dict = data_dict
        self.ret_function = ret_function

        self.name_var = tk.StringVar(value=data_dict.get("name", ""))
        self.color_var = tk.StringVar(value=data_dict.get("color", ""))
        self.speed_var = tk.DoubleVar(value=data_dict.get("speed", 1.0))  # Default speed is 1.0

        self.type_var = tk.StringVar(value=data_dict.get("type", ""))
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.root.tk_setPalette(background="#2E2E2E", foreground="white", activeBackground="#4E4E4E",
                                activeForeground="white")

        """style = ttk.Style()
        style.theme_use("")
        style.map("Custom.TEntry",
                  background=[("active", "#2E2E2E"), ("!active", "#333333"), ("disabled", "#444444")],
                  fieldbackground=[("active", "#2E2E2E"), ("!active", "#333333"), ("disabled", "#444444")],
                  foreground=[("active", "red"), ("!active", "red"), ("disabled", "#666666")],
                  selectbackground=[("active", "#4E4E4E"), ("!active", "#3E3E3E"), ("disabled", "#555555")],
                  selectforeground=[("active", "red"), ("!active", "white"), ("disabled", "#888888")])

        style.map("Dark.TCheckbutton", background=[("active", "#2E2E2E"), ("!active", "#2E2E2E")],
                  foreground=[("active", "white"), ("!active", "white")])

        style.configure("Dark.TEntry", bordercolor="#444444")
        style.configure("Dark.TCheckbutton", bordercolor="#2E2E2E")"""


    def setup_ui(self):
        save_button = ttk.Button(self.root, text="✖",width=2, command=lambda :self.save_and_close(False), style="Dark.TButton")
        save_button.pack(side="top",anchor="ne")


        name_label = ttk.Label(self.root, text="Name:", foreground="white", background="#2E2E2E")
        name_label.pack()

        name_entry = ttk.Entry(self.root, textvariable=self.name_var, style="Dark.TEntry")
        name_entry.pack()

        color_label_frame = tk.LabelFrame(self.root, text="Color", background="#2E2E2E", foreground="white")
        color_label_frame.pack()

        color_entry = ttk.Entry(color_label_frame, textvariable=self.color_var, style="Dark.TEntry")
        color_entry.pack()

        type_label = ttk.Label(self.root, text="Select Binding:", foreground="white", background="#2E2E2E")
        type_label.pack()

        type_combobox = ttk.Combobox(self.root, textvariable=self.type_var, values=['moveline', 'actionline', 'None'])
        type_combobox.pack()

        speed_label = ttk.Label(self.root, text="Animation Speed:", foreground="white", background="#2E2E2E")
        speed_label.pack()

        speed_slider_frame = ttk.Frame(self.root)
        speed_slider_frame.pack()

        speed_label = ttk.Label(speed_slider_frame, text="0.1", foreground="white", background="#2E2E2E")
        speed_label.pack(side="top")

        def update_speed_label(self, value):

            speed_label.configure(text=str(round(float(value),2)))

        speed_slider = ttk.Scale(speed_slider_frame, from_=0.1, to=10.0, variable=self.speed_var, orient="horizontal",
                                 length=200, command=lambda e:update_speed_label(self, e))
        speed_slider.pack(side="bottom")


        """check_var = tk.BooleanVar()
        check_button = ttk.Checkbutton(self.root, text="Enable", variable=check_var, style="Dark.TCheckbutton")
        check_button.pack()"""

        save_button = ttk.Button(self.root, text="Save", command=self.save_and_close, style="Dark.TButton")
        save_button.pack()


    def save_and_close(self,save=True):
        self.data_dict["name"] = self.name_var.get()
        self.data_dict["color"] = self.color_var.get()
        self.data_dict["type"] = self.type_var.get()
        self.data_dict["speed"] = round(self.speed_var.get(),3)

        self.ret_function(self.data_dict, save)

