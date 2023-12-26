from .material import Material


class EditFile:

    def __init__(self):
        self.Materials=[]


    def addMaterial(self,path,material_file):

        if type(material_file)==str:
            m=Material(file=material_file,path=path)
            self.Materials.append(m)
            print("added material",m.getUNIQE())
            return m

        else:
            print("Error: Material is not of type Material")



