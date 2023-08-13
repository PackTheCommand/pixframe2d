import json
import os
import tkinter
import tkinter as tk
from tkinter import filedialog, ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
from PIL import ImageDraw

G_WIDTH=800
G_HEIGHT=600


BLOCK_SIZE=50
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
StatikImage=[]
def createImage(path, x, y,nsa=False,name="",unknown="resources/unknown_plg.png",cornerRadius=None):
    global StatikImage


    try:
        photo = Image.open(path)
        if cornerRadius:
            photo=__add_corners(im=photo,rad=cornerRadius)
        if not name:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=path+f"{x}_{y}")
        else:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=name+f"{x}_{y}")
        if not nsa:
            StatikImage += [i]
        return i
    except FileNotFoundError:
        print("missing:",path)
        photo = Image.open(unknown)
        if not name:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=unknown+f"_{x}_{y}")
        else:
            i = ImageTk.PhotoImage(photo.resize((x, y)), name=unknown+f"{x}_{y}")
        if not nsa:
            StatikImage += [i]
        return i
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
import ui_code
class CanvasApp:
    def __init__(self, root):
        self.b = None
        self.selected_index = None
        self.bg_image_path = ""
        self.grid_size = 50
        self.protected_elements = []
        self.root = root
        self.root.title("Level Editor")
        self.ofset_x = 0
        self.ofset_y = 0
        self.grid_ofset=0
        self.save_path=None
        self.displayimage=None
        self.curant_object_data={}
        self.root.configure(bg='#333440')
        self.left_Frame=tk.Frame(root,bg='#333440')
        self.left_Frame.pack(side="left",fill="both",expand=True)
        self.right_Frame = tk.Frame(root,bg='#333440')
        self.right_Frame.pack(side="right", fill="y")
        can_tool_frame=tk.Frame(self.left_Frame,bg='#333440')
        can_tool_frame.pack(expand=True,fill="both")
        toolFrame = tk.Frame(can_tool_frame,bg='#333440')
        toolFrame.pack(side="left",anchor="ne")
        self.canvas = tk.Canvas(can_tool_frame, bg='black')
        self.canvas.pack(fill=tk.BOTH, expand=True,side="left")
        self.create_cordnateSystem()
        self.bg_image = None  # Variable to store the background image




        self.canvas.bind("<Button-1>", self.canvas_left_click)
        self.canvas.bind("<Button-3>", self.canvas_right_click)
        self.canvas.bind("<Button-2>", self.canvas_middle_click)

        self.texture_buttons_frame = tk.Frame(self.left_Frame, bg='#333440')
        self.texture_buttons_frame.pack(side=tk.RIGHT, fill=tk.Y)

        #self.texture_listbox = tk.Listbox(self.right_Frame, bg='#333440', fg='white', selectbackground='gray',width=30,font=tkfont.Font(size=12,family="Bahnschrift"))

        #self.texture_listbox.bind("<<ListboxSelect>>", self.texture_selected)


        self.canvas.bind("<Configure>",self.updatebg)



        f= tk.Frame(self.right_Frame, bg='#333440')
        f.pack(side=tk.TOP,anchor="nw")


        self.fill_mode = False
        self.fill_start_x = 0
        self.fill_start_y = 0


        self.fill_button = tk.Button(toolFrame, text="🪣", command=self.toggle_fill_mode, bg='#444654', fg='white',font=tkfont.Font(size=12,weight="bold"),relief="flat")
        self.fill_button.pack(side=tk.TOP,anchor="n")

        self.rubber_mode = False
        self.rubber_area_id = None

        self.rubber_button = tk.Button(toolFrame, text="🧽", command=self.toggle_rubber_mode, bg='#444654',font=tkfont.Font(size=12,weight="bold"),relief="flat",
                                       fg='white')
        self.rubber_button.pack(side=tk.TOP,anchor="n")

        root.bind("<Escape>", self.stop_fill)


        #self.texture_listbox.pack(side=tk.TOP, fill="y",expand=True)


        self.save_button = tk.Button(self.left_Frame, text="Save", command=self.save_elements, bg='#444654', fg='white')


        self.root.bind("<Control-s>",lambda e:self.save_elements())
        self.root.bind("<Control-l>", lambda e: self.load_elements())
        self.root.bind("<Control-Shift-b>", lambda e: self.select_bg_image())
        self.root.bind("<Control-Shift-s>", lambda e: self.save_elements(True))
        self.root.bind("<f>", lambda e: self.toggle_fill_mode())
        self.root.bind("<r>", lambda e: self.toggle_rubber_mode())
        self.save_button.pack(side=tk.BOTTOM, fill=tk.X)

        # Initialize data
        self.images = []
        self.texture_data = [
            {"name": "🎯 Spawnpoint", "path": "imgs/spawnpoint.png", "type": "spawn","collision":False},
            {"name": "💀 Death-Area", "path": "imgs/death_area.png", "type": "death_area","collision":False}
        ]
        self.texture_data += [
            {"name": "🖼 " + file.split(".", 1)[0], "path": "imgs/blocks/" + file, "type": "object","collision":True}
            for file in get_files_in_folder("imgs/blocks/")
        ]
        self.texture_data += [
            {"name": "✿ " + file.split(".", 1)[0], "path": "imgs/decoration/" + file, "type": "object","collision":False}
            for file in get_files_in_folder("imgs/decoration/")
        ]
        self.texture_data.append({"name": "🏁 Finisch", "path": "imgs/finisch.png", "type": "level_finisch","collision":False},)

        self.current_texture = None
        self.current_obj_type=None
        self.elements = []

        # can
        canvas = tk.Canvas(self.right_Frame,width=200,bg='#333440',highlightthickness=0)
        #canvas.pack(side=tk.LEFT, fill=tk.BOTH)

        # Create a scrollbar and link it to the canvas
        style = ttk.Style()
        style.theme_use("clam")  # Use the "clam" theme for a dark-themed look
        style.configure("TScrollbar",
                        background='#333440',
                        troughcolor="#76818E",
                        gripcount=0,
                        darkcolor='#444654',
                        lightcolor='#444654',
                        bordercolor='#444654')
        scrollbar = ttk.Scrollbar(master=self.right_Frame, command=canvas.yview,)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas.pack(side=tk.RIGHT, fill=tk.BOTH)

        canvas.configure(yscrollcommand=scrollbar.set)

        # Create a frame inside the canvas for the scrollable content
        inner_frame = tk.Frame(canvas,bg='#333440')
        canvas.create_window((0, 0), window=inner_frame, anchor="nw")

        # Configure the canvas to adjust scroll region when resized
        def on_configure(event):
            # Update the scroll region when the canvas size changes
            canvas.configure(scrollregion=canvas.bbox("all"))

        inner_frame.bind("<Configure>", on_configure)


        #can


        self.texture_buttons_frame = inner_frame

        #self.texture_buttons_frame.pack(side=tk.TOP, fill=tk.BOTH)

        #self.populate_texture_listbox()
        self.create_texture_buttons()
        self.load_button = tk.Button(self.left_Frame, text="Load", command=self.load_elements, bg='#444654', fg='white')
        self.load_button.pack(side=tk.BOTTOM, fill=tk.X)

        self.select_bg_button = tk.Button(self.left_Frame, text="Select Background Image", command=self.select_bg_image,
                                          bg='#444654', fg='white')
        self.select_bg_button.pack(side=tk.BOTTOM, fill=tk.X)


    def create_texture_buttons(self, parent):
        for index, texture in enumerate(self.texture_data):
            row = index // 3
            col = index % 3

            texture_frame = tk.Frame(parent, bg='#333440')
            texture_frame.grid(row=row, column=col, padx=5, pady=5)

            image = tk.PhotoImage(file=texture["path"])
            image_label = tk.Label(texture_frame, image=image, bg='#333440')
            image_label.image = image
            image_label.pack()

            name_label = tk.Label(texture_frame, text=texture["name"], bg='#333440', fg='white')
            name_label.pack()


    def create_texture_buttons(self):
        last_texture =None
        t=None
        for index, texture in enumerate(self.texture_data):
            row = index // 2
            t=texture
            col = index % 2

            texture_frame = tk.Frame(self.texture_buttons_frame, bg='#333440')
            texture_frame.grid(row=row, column=col, padx=5, pady=5)


            def selectItem(texture_frame,texture,namelabel):
                texture=self.texture_data[texture]
                nonlocal last_texture
                if self.curant_object_data == texture: return
                if last_texture:
                    last_texture[0].configure(bg="#333440")
                    last_texture[1].configure(bg="#333440")
                texture_frame.configure(bg="green")
                namelabel.configure(bg="green")
                last_texture=(texture_frame,namelabel)
                print(texture)
                self.current_obj_type=texture["type"]
                print(texture["type"])

                self.curant_object_data=texture
                self.current_texture=texture["path"]

            image = createImage(texture["path"],25,25,name=texture["path"].split("/")[-1])
            image_label = tk.Label(texture_frame, image=image, bg='#333440')

            image_label.image = image
            image_label.pack()
            pr=texture["name"]

            if len(texture["name"])>15:
                pr=pr[:12]+"..."

            name_label = tk.Label(texture_frame, text=pr, bg='#333440', fg='white',width=12,anchor="w")
            name_label.bind("<Button-1>",lambda e,te=texture_frame,tex=index,nl=name_label:selectItem(te,tex,nl))

            image_label.bind("<Button-1>",
                             lambda e, te=texture_frame, tex=index, nl=name_label: selectItem(te, tex, nl))
            texture_frame.bind("<Button-1>",
                             lambda e, te=texture_frame, tex=index, nl=name_label: selectItem(te,tex,nl))

            name_label.pack()
    def updatebg(self,e):
        if self.bg_image_path:
            if self.b in self.protected_elements:
                self.protected_elements.remove(self.b)

            self.canvas.delete(self.b)
            StatikImage.remove(self.bg_image)
            w=self.canvas.winfo_width()
            fac=w/G_WIDTH

            h=G_HEIGHT*fac
            if h<0:
                h=-h
            print(w,h,G_WIDTH,fac)

            self.bg_image = createImage(self.bg_image_path, int(w),int(h), name="background_image")

            self.b = self.canvas.create_image(0, h//2-self.canvas.winfo_height(), anchor=tk.NW, image=self.bg_image, tags="background")
            self.protected_elements += [self.b]
            self.canvas.lower(self.b)
    def select_bg_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif")])
        if file_path:
            self.bg_image_path=file_path
            self.bg_image = createImage(file_path,G_WIDTH,G_HEIGHT,name="background_image")
            self.b=self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image, tags="background")
            self.protected_elements+= [self.b]
            self.canvas.tag_lower("background")  # Move background to the bottom

    def load_elements(self):
        ask = open_file_dialog()
        if not ask:
            return
        self.canvas.delete("all")  # Clear canvas before loading new elements
        self.protected_elements = []
        self.create_cordnateSystem()

        with open(ask) as f:
            elem=json.load(f)
        self.root.title("Editing - "+ask.split("/")[-1])
        self.save_path=ask


        self.elements=[]
        for n,element in enumerate(elem):
            if element["type"]=="bg_image":

                self.bg_image_path = element["texture"]

                self.bg_image = createImage(element["texture"], G_WIDTH, G_HEIGHT,name=element["texture"].split("/")[-1])
                self.b = self.canvas.create_image(0, 0, anchor=tk.NW, image=self.bg_image, tags="background")

                self.protected_elements += [self.b]
                self.canvas.tag_lower("background")  # Move background to the bottom
                self.updatebg("")
                continue
            image = createImage(element["texture"],50,50,name=element["texture"].split("/")[-1])
            image_width, image_height = image.width(), image.height()


            id=self.canvas.create_image(element["x"],element["y"], image=image, tags=["#movable"],anchor="nw")
            element["id"]=id
            self.elements+=[element]
        self.canvas.tag_raise("coordinate_labels")#, "coordinate_labels")


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
            self.rubber_button.configure(bg = '#444654',)
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

    def stop_rubber(self):
        self.canvas.delete(self.rubber_area_id)
        self.canvas.unbind("<B1-Motion>")





    def create_cordnateSystem(self):
        canvas_width = 500
        canvas_height = 500

        a=self.canvas.create_line(0, -canvas_height*2 , 0, canvas_height*2 , tags=["coordinate_labels","#movable"],fill="white")

        b=self.canvas.create_line(-canvas_width*2, 0, canvas_width*2, 0, tags=["coordinate_labels","#movable"],fill="white")




        b1 = self.canvas.create_line(canvas_width * 2+6, -canvas_height * 2, -canvas_width * 2, -canvas_height * 2,
                                    tags="coordinate_lines", fill="white")


        b2 = self.canvas.create_line(-canvas_width * 2, canvas_height * 2, canvas_width * 2, canvas_height * 2,
                                     tags=["coordinate_labels","#movable"], fill="white")
        b3 = self.canvas.create_line(-canvas_width * 2, -canvas_height * 2, -canvas_width * 2, canvas_height * 2
                                    , tags=["coordinate_labels","#movable"], fill="white")
        b4 = self.canvas.create_line(canvas_width * 2, -canvas_height * 2, canvas_width * 2, canvas_height * 2
                                    , tags=["coordinate_labels","#movable"], fill="white")

        for i in range(-canvas_width*2+50,canvas_width*2,50):
            if i!=0:
                self.protected_elements.append(self.canvas.create_text(i, 10, text=f"{i}", tags=["coordinate_labels","#movable"],fill="white"))

            else:
                self.protected_elements.append(self.canvas.create_text(i+6, 8, text=f"{i}",  tags=["coordinate_labels","#movable"], fill="white"))

        for i in range(-canvas_width*2+50,canvas_width*2,50):
            if i!=0:
                self.protected_elements.append(self.canvas.create_text(10, i, text=f"{i}", tags=["coordinate_labels","#movable"],fill="white"))

        self.protected_elements+=[a,b,b1,b2,b3,b4]

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
        self.ofset_x+=dx
        self.ofset_y += dy

        self.canvas.move("#movable", dx, dy)

    """self.images+=[new_image]"""

    def canvas_left_click(self, event):
        if self.current_texture:
            print(self.current_obj_type)
            x, y = event.x, event.y

            snapped_x = round((x-25 - self.ofset_x) / self.grid_size) * self.grid_size + self.ofset_x
            snapped_y = round((y-25 - self.ofset_y) / self.grid_size) * self.grid_size + self.ofset_y

            """ snapped_x = (x + grid_offset_x) // self.grid_size * self.grid_size
            snapped_y = (y + grid_offset_y) // self.grid_size * self.grid_size"""

            """grid_offset_x = self.grid_size-(self.ofset_x%self.grid_size)
            grid_offset_y = self.grid_size-(self.ofset_y%self.grid_size)

            snapped_x = ((x+grid_offset_x)//self.grid_size)*self.grid_size
            snapped_y = ((y+grid_offset_y)//self.grid_size)*self.grid_size"""

            #print(snapped_x+grid_offset_x)
            print(snapped_x,x)

            image = createImage(self.current_texture,50,50,name=self.current_texture.split("/")[-1])
            image_width, image_height = image.width(), image.height()
            #new_image = image.subsample(2)  # Half the size
            #self.images += [new_image]
            element = self.canvas.create_image(snapped_x, snapped_y, image=image,tags=["#movable"],anchor="nw")
            self.elements.append({
                "id": element,
                "type": self.current_obj_type,
                "texture": self.current_texture,
                "x": snapped_x - self.ofset_x, "y": snapped_y - self.ofset_y,
                "collision": self.curant_object_data["collision"],
                "width": BLOCK_SIZE , "height": BLOCK_SIZE,
                "tags": []
            })
            self.canvas.tag_raise("coordinate_labels")

    def canvas_right_click(self, event):
        selected_element = self.canvas.find_closest(event.x, event.y)
        if selected_element[0] in self.protected_elements:
            return
        if selected_element:
            self.canvas.delete(selected_element)
            print(self.elements)
            self.elements = [element for element in self.elements if element["id"] != selected_element[0]]
            if hasattr(self, 'selected_element') and self.selected_element == selected_element[0]:
                self.selected_label.config(text="Selected: None")


    def canvas_middle_click(self, event):
        print("fdsfdsfsda")
        self.prev_x = event.x
        self.prev_y = event.y
        self.canvas.bind("<B2-Motion>", self.move_element)
        self.canvas.bind("<ButtonRelease-2>", self.stop_move_element)

    def stop_move_element(self, event):
        self.canvas.unbind("<B1-Motion>")
        self.canvas.unbind("<ButtonRelease-2>")
    def save_elements(self,force=False):
        print("Saved elements:")


        if ((not self.save_path)|force):
            sf=save_file_dialog()
        else:
            sf=self.save_path
        if not sf:
            return
        self.save_path = sf
        self.root.title("Editing - " + sf.split("/")[-1])
        with open(sf,"w") as f:
            if self.bg_image:
                print([{"type": "bg_image","texture":self.bg_image_path}]+self.elements)
                json.dump([{"type": "bg_image","texture":self.bg_image_path}]+self.elements,f)
            else:
                json.dump(self.elements, f)

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
        self.fill_area_id= self.canvas.create_rectangle(0, 0, 0, 0, outline="#92BDA3",width=2, tags="fill_area")

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


            if snapped_x2<snapped_x1:
                snapped_x2,snapped_x1=snapped_x1,snapped_x2

            if snapped_y2<snapped_y1:
                snapped_y2,snapped_y1=snapped_y1,snapped_y2


            print(snapped_x1, snapped_y1, snapped_x2,snapped_y2,self.current_texture)

            if self.current_texture:


                for iy in range(snapped_y1,snapped_y2,50):
                    for ix in range(snapped_x1,snapped_x2,50):
                        if self.current_texture:
                            snapped_x,snapped_y = ix,iy



                            image=createImage(self.current_texture,50,50,name=self.current_texture)
                            image_width, image_height = image.width(), image.height()


                            element = self.canvas.create_image(snapped_x, snapped_y, image=image, tags=["#movable"],
                                                               anchor="nw")
                            self.elements.append({
                                "id": element,
                                "type": self.current_obj_type,
                                "texture": self.current_texture,
                                "x": snapped_x - self.ofset_x, "y": snapped_y - self.ofset_y,
                                "collision": self.curant_object_data["collision"],
                                "width": image_width , "height": image_height ,
                                "tags": []
                            })
                self.canvas.tag_raise("coordinate_labels")#, "coordinate_labels")

class fake_event():
    def __init__(self, x,y):
        self.x,self.y=x,y
root = tk.Tk()
app = CanvasApp(root)
root.mainloop()