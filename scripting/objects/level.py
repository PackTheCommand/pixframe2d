

class Level():
    def __init__(self,render_loop):
        self.objects = []
        self.__render_loop = render_loop
        self.metadatas = []
        self.path:str
        self.objectsUID_to_id={}
        self.nbts={}
    def addLight(self,x,y,radius,color):

        self.__render_loop.addTorch(x,y,radius)
