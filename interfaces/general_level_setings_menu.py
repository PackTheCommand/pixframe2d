import os
import tkinter as tk
from tkinter import ttk, filedialog


def open_file_dialog():
    root = tk.Tk()
    root.withdraw()  # Hide the main window

    file_path = filedialog.askopenfilename(filetypes=[("WAV", "*.wav"), ("MP3", "*.mp3"),("OGG", "*.ogg"), ("All Files", "*.*")])

    if file_path:
        return file_path

        # Add your code here to handle the selected file
    return None
class GeneralLevelSetings_Window:
    def __init__(self, root, data_dict:{"name":str,"dificulty":str,"bg-music":str}, ret_function):
        self.root = root

        self.updatefunc=None
        self.data_dict = data_dict
        self.ret_function = ret_function

        self.name_var = tk.StringVar(value=data_dict.get("name", ""))

        self.dificulty_var = tk.DoubleVar(value=data_dict.get("dificulty", 1.0))  # Default dificulty is 1.0

        #self.type_var = tk.StringVar(value=data_dict.get("type", ""))
        self.setup_styles()
        self.setup_ui()

    def setup_styles(self):
        self.root.tk_setPalette(background="#2E2E2E", foreground="white", activeBackground="#4E4E4E",
                                activeForeground="white")




    def setup_ui(self):
        save_button = ttk.Button(self.root, text="Save", command=self.save_and_close, style="Dark.TButton")
        save_button.pack(side="top",anchor="ne")
        l = ttk.Label(self.root, text="Level Setings", )

        l.pack()


        name_label = ttk.Label(self.root, text="Name:", foreground="white", background="#2E2E2E")
        name_label.pack()

        name_entry = ttk.Entry(self.root, textvariable=self.name_var, style="Dark.TEntry")
        name_entry.pack()

        f=ttk.LabelFrame(self.root, text="Background Music")

        f.pack(fill="x")

        SoundTrackLabel=ttk.Label(f, text=self.data_dict["bg-music"], foreground="white", background="#2E2E2E",width=12)
        SoundTrackLabel.pack(side="left")



        def setSoundTrack():
            file_path = open_file_dialog()
            ad=os.getcwd().replace("\\","/")
            print(ad)

            if file_path:
                dn=file_path.replace(ad,"")
                if len(dn)>12:
                    dn="..."+dn[-10:]
                SoundTrackLabel.configure(text=dn)

                self.data_dict["bg-music"] = file_path.replace(ad,"")



        soundTrackopenButton=ttk.Button(f, text="📂",width=2, command=setSoundTrack, style="Dark.TButton")
        soundTrackopenButton.pack(side="right")


        dificulty_label = ttk.Label(self.root, text="Level Dificulty:", foreground="white", background="#2E2E2E")
        dificulty_label.pack()

        dificulty_slider_frame = ttk.Frame(self.root)
        dificulty_slider_frame.pack()

        dificulty_label = ttk.Label(dificulty_slider_frame, text=self.data_dict["dificulty"], foreground="white", background="#2E2E2E")
        dificulty_label.pack(side="top")

        def update():

            bgm = self.data_dict["bg-music"]
            if bgm:

                if len(bgm) > 12:
                    bgm = "..." + bgm[-10:]
                SoundTrackLabel.configure(text=bgm)

            name_entry.setvar(self.data_dict.get("name", ""))
            dificulty_slider.set(self.data_dict.get("dificulty", 1.0))
            self.name_var.set(self.data_dict.get("name", ""))
        self.updatefunc=update



        def update_dificulty_label(self, value):

            dificulty_label.configure(text=str(round(float(value),0)))

        dificulty_slider = ttk.Scale(dificulty_slider_frame, from_=1, to=10.0, variable=self.dificulty_var, orient="horizontal",
                                 length=200, command=lambda e:update_dificulty_label(self, e))
        dificulty_slider.pack(side="bottom")


        """check_var = tk.BooleanVar()
        check_button = ttk.Checkbutton(self.root, text="Enable", variable=check_var, style="Dark.TCheckbutton")
        check_button.pack()"""




    def save_and_close(self,save=True):
        self.data_dict["name"] = self.name_var.get()


        self.data_dict["dificulty"] = round(float(self.dificulty_var.get()),0)

        self.ret_function(self.data_dict, save)

