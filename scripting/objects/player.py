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
