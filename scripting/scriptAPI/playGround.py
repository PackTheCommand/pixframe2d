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
    def __init__(self,renderloop):
        self.__renderloop = renderloop
        self.uuid_to_id = {}



    def setObject(self,uuid,x,y):
        self.__renderloop.moveto(uuid,x,y)

    def moveObject(self,uuid,x,y):
        id=self.uuid_to_id.get(uuid)
        objectx,objecty=self.__renderloop.getXY(id)
        self.__renderloop.moveto(id,objectx+x,objecty+y)

    def delObject(self,uuid):
        id=self.uuid_to_id.get(uuid)
        self.__renderloop.removeElement(id)

    def addTextObject(self,uuid,x,y):
        pass

