import importlib.util

import lupa

import scripting.objects.objectCol
import scripting.objects.player
from scripting.objects.api import API


class pyManager:
    def __init__(self,name,path,render_loop,playerId):
        self.name = name
        self.path = path
        self.playground=None

        api = API(render_loop)
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


def restricted_lua_environment():
    lua = lupa.LuaRuntime(unpack_returned_tuples=True,)

    # Remove functions related to file I/O
    lua.globals().open = None
    lua.globals().io = None

    return lua

class lua_Importer:
    def __init__(self,name,path,render_loop,playerId,importantArtibutes=None):
        with open(path+"/"+name, "r", encoding="utf-8") as f:
            self.contents=f.read()


        self.runtime=None
        api = API(render_loop)
        self.api = api
        api.stopSound=importantArtibutes["stop_sound"]
        api.Player = scripting.objects.player.Player(render_loop, playerId)
        api.Objects = scripting.objects.objectCol.Objects(render_loop, )
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