class Texture:

    def __init__(self, filename,path,type,collision,folder):
        self.filename = filename
        self.name = filename

        self.path = path
        self.type = type
        self.collision = collision
        self.folder = folder

    def to_json(self):
        return {
            "filename":self.filename,
            "path":self.path,
            "type":self.type,
            "collision":self.collision,
            "folder":self.folder,

        }




