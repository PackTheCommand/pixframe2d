import importlib.util
import sys

import lupa

from .scriptAPI import playGround
class pyManager:
    def __init__(self,name,path,render_loop,playerId):
        self.name = name
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


        #sys.path.insert(0,self.path)

        module=__import__("scripts")

        print(module)
        print(module.test)


        exec("module."+self.name+".Script(self.api)")



        return module


    def start(self):
        self.Import()


class API:
    def __init__(self):
        self.Player:object
        self.Objects:object
        self.level:object
        self.VERSION:str
        self.uuidTO_EL_ID:dict

    def getIDbyUUID(self,uuid):
        if uuid in self.uuidTO_EL_ID:
            return self.uuidTO_EL_ID[uuid]


    def uuids_getObject_where_NBT(self,datatag):

        nbts=self.level.nbts
        return [nbt for nbt in nbts if datatag in nbts[nbt]]


    def ids_getObject_where_NBT(self,datatag):
        nbts = self.level.nbts
        return [self.uuidTO_EL_ID[uuid] for uuid in nbts if datatag in nbts[uuid]]





def restricted_lua_environment():
    lua = lupa.LuaRuntime(unpack_returned_tuples=True,)

    # Remove functions related to file I/O
    lua.globals().open = None
    lua.globals().io = None

    return lua

class lua_Importer:
    def __init__(self,name,path,render_loop,playerId):
        with open(path+"/"+name, "r", encoding="utf-8") as f:
            self.contents=f.read()

        plg=playGround
        self.runtime=None
        api = API()
        self.api = api
        api.Player = plg.Player(render_loop,playerId)
        api.Objects = plg.Objects(render_loop,)
        api.VERSION = "S1.B.0"

        pass
    def Import(self,levelOBJ):
        env=restricted_lua_environment()
        self.api.level=levelOBJ
        env.globals().api=self.api
        env.globals().level=levelOBJ
        self.runtime=env

        env.execute(self.contents)



    def start(self,levelOBJ):
        self.Import(levelOBJ)