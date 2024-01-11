
from .player import Player
from .objectCol import Objects
from .level import Level

from services.dialog_service import DialogService

class API:
    def __init__(self,renderloop):
        self.__renderloop = renderloop
        self.Player:Player
        self.Objects:Objects
        self.level:Level
        self.stopSound:any
        self.VERSION:str

        self.levpath:str

        self.uuidTO_EL_ID:dict

    def innit_shader(self,refer,name,*args,**kwargs):
        self.__renderloop.createShader(refer,name,*args,**kwargs)
    def engageShader(self,refer):

        self.__renderloop.engageShader(refer)
    def disengageActiveShader(self):
        self.__renderloop.disengageShaders()


    def playCutScene(self,file):
        print(self.__renderloop)
        self.stopSound()
        self.__renderloop.playCutScene(file.replace("$levdir",self.level.path))


    def playDialog(self,file,excludeObjects=True):
        self.stopSound()
        if excludeObjects:
            self.__renderloop.dialog_service.run_dialog(file)
        else:
            self.__renderloop.dialog_service.run_dialog_in_game(file)
    def getIDbyUUID(self,uuid):
        if uuid in self.uuidTO_EL_ID:
            return self.uuidTO_EL_ID[uuid]


    def uuids_getObject_where_NBT(self,datatag):

        nbts=self.level.nbts
        return [nbt for nbt in nbts if datatag in nbts[nbt]]


    def ids_getObject_where_NBT(self,datatag):
        nbts = self.level.nbts
        return [self.uuidTO_EL_ID[uuid] for uuid in nbts if datatag in nbts[uuid]]
