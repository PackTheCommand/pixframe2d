class Player:
    def __init__(self,renderloop,player_id):
        self.__renderloop = renderloop
        self.player_id = player_id
        pass

    def getPlayer(self):
        self.__renderloop.getXY(self.player_id)
        print("Player at 12,12")


    def setPlayer(self,x,y):
        self.__renderloop.moveto(self.player_id)
        print("Player at 12,12")

    def movePlayer(self,x,y):
        playerx,playery=self.__renderloop.getXY(self.player_id)
        self.__renderloop.moveto(self.player_id,playerx+x,playery+y)

class Objects:
    def __init__(self,renderloop,schared_level_store):
        self.__renderloop = renderloop
        self.schared_level = schared_level_store


    def getObjects(self):
        return self.schared_level

    def setObject(self,uuid,x,y):
        self.__renderloop.moveto(uuid,x,y)

    def moveObject(self,uuid,x,y):
        objectx,objecty=self.__renderloop.getXY(uuid)
        self.__renderloop.moveto(self.schared_level,objectx+x,objecty+y)

    def delObject(self,uuid):
        self.__renderloop.removeElement(uuid)

    def addTextObject(self,uuid,x,y):

