import json

from PIL import Image, ImageTk

list=[]
preview_show = Image.open("imgs/img-tools/material_overlay.png").resize((25,25),Image.NEAREST)
list.append(preview_show)

class Material:
    def __init__(self, info=None,file=None,path=None):
        if file:
            with  open(path+file, "r") as f:
                info = json.load(f)
        map=self.split_texture(path+info["map"])

        self.info = info
        self.map = map
        self.category = info["category"]
        self.n = map["n"]
        self.s = map["s"]
        self.w = map["w"]
        self.e = map["e"]
        self.nw = map["nw"]
        self.ne = map["ne"]
        self.sw = map["sw"]
        self.uniquename = info["uniqueName"]
        self.se = map["se"]
        self.preview=None

    from PIL import Image

    def gPreview(self,x,y):
        return self.generatePreview(x,y)
    def generatePreview(self,x,y):
        if self.preview:
            return self.preview

        prev = self.map[self.info["preview"]].convert("RGBA")
        print(prev,preview_show.convert("RGBA"))

        i=Image.alpha_composite(prev.resize((x,y),Image.NEAREST), preview_show)
        self.preview=ImageTk.PhotoImage(i)
        return self.preview

    def split_texture(self,filename):
        # Load the PNG image
        image = Image.open(filename)

        # Get the dimensions of the image
        width, height = image.size

        # Ensure the image is at least 3x3 pixels in size
        if width < 3 or height < 3:
            raise ValueError("Image dimensions must be at least 3x3 pixels")

        # Define the 3x3 grid coordinates
        grid_coordinates = [
            ((0, 0), (width // 3, height // 3)),  # NW
            ((width // 3, 0), (2 * (width // 3), height // 3)),  # N
            ((2 * (width // 3), 0), (width, height // 3)),  # NE
            ((0, height // 3), (width // 3, 2 * (height // 3))),  # W
            ((width // 3, height // 3), (2 * (width // 3), 2 * (height // 3))),  # Center
            ((2 * (width // 3), height // 3), (width, 2 * (height // 3))),  # E
            ((0, 2 * (height // 3)), (width // 3, height)),  # SW
            ((width // 3, 2 * (height // 3)), (2 * (width // 3), height)),  # S
            ((2 * (width // 3), 2 * (height // 3)), (width, height))  # SE
        ]

        # Create a dictionary to store the subtextures
        subtextures = {}

        # Iterate through the grid coordinates and extract the subtextures
        for direction, (start, end) in zip(['nw', 'n', 'ne', 'w', 'center', 'e', 'sw', 's', 'se'], grid_coordinates):
            subtexture = image.crop((*start, *end))
            subtextures[direction] = subtexture

        return subtextures

    def getUNIQE(self):
        return self.uniquename


    def to_json(self):
        return {
            "uniqueName":self.uniquename,
            "collection":{
                "se":self.se,
                "sw":self.sw,
                "nw":self.nw,
                "ne":self.ne,
                "n":self.n,
                "w":self.w,
                "e":self.e,
                "s":self.s,

            }
        }
