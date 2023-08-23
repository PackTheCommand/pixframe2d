from .scriptAPI import playGround
class pyManager:
    def __init__(self,path,render_loop,playerId):
        self.path = path
        self.playground=None

        api = API()
        self.api=api
        api.Player = playerId

        api.VERSION = "S1.B.0"

    def setLEVconstants(self,uuid_to_id,objects,):
        self.api.Objects=objects
        self.api.uuidTO_EL_ID=uuid_to_id
    def Import(self):


        imp=__import__(self.path)
        imp.Script(self.api)


    def start(self):
        self.Import()


class API:
    def __init__(self):
        self.Player:int=None
        self.Objects=[]
        self.VERSION=None
        self.uuidTO_EL_ID=None

    def getIDbyUUID(self,uuid):
        if uuid in self.uuidTO_EL_ID:
            return self.uuidTO_EL_ID[uuid]
