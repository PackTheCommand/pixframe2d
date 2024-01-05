from .material import Material


class EditFile:

    def __init__(self):
        self.Materials=[]
        self.material_snapp_map = {}
        self.all_canvas_ids_map = {}

    def addItem(self,sx,sy,item_id,material:Material):
        self.all_canvas_ids_map[item_id]=(sx,sy)
        print("added item",item_id,"at",sx,sy)
        self.material_snapp_map[material.getUNIQE()][(sx,sy)]=item_id

    def removeItem(self,item):
        if item in self.all_canvas_ids_map:
            sx,sy=self.all_canvas_ids_map[item]
            self.all_canvas_ids_map.pop(item)
            self.material_snapp_map.pop((sx, sy))


        print("removed item",(sx,sy))
    def addMaterial(self,path,material_file):

        if type(material_file)==str:
            m=Material(file=material_file,path=path)
            self.Materials.append(m)
            self.material_snapp_map[m.getUNIQE()]={}
            print("added material",m.getUNIQE())
            return m

        else:
            print("Error: Material is not of type Material")

    def getMaterilaAtXY(self,m:Material,x,y):
        return self.material_snapp_map[m.getUNIQE()].get((x,y),None)

        pass



