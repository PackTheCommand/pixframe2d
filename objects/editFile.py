from .material import Material


class EditFile:

    def __init__(self):
        self.Materials=[]


    def addMaterial(self,material):
        if type(material)==Material:
            self.Materials.append(material)
        elif type(material)==dict:
            m=Material(material)
            self.Materials.append(m)
        elif type(material)==str:
            m=Material(file=material)
            self.Materials.append(m)

        else:
            print("Error: Material is not of type Material")



