import pygame
from PIL import Image
from pygame import USEREVENT
from engene import GameRenderLoop

class Level:
    def __init__(self, image_path,render_loop:GameRenderLoop):
        self.image = Image.open(image_path).convert('1')  # Convert image to black and white
        self.width, self.height = self.image.size
        self.player_x = 0
        self.render_loop = render_loop
        self.player_y = 0
        self.jumping=False
        self.faling=False
        self.on_move=None
        self.map_data = self._create_map()

    def _create_map(self):
        map_data = []
        for y in range(self.height):
            row = []
            for x in range(self.width):
                pixel = self.image.getpixel((x, y))

                if pixel == 100:  # Red pixel
                    self.player_x = 1+x
                    self.player_y = 1+y
                    row.append(0)
                elif pixel == 255:  # White pixel
                    row.append(0)
                else:
                    row.append(1)
            map_data.append(row)
        return map_data

    def addCom(self,func):
        self.on_move=func

    def check_corner(self,new_x,new_y,base_x,base_y):


        if self.map_data[new_y][new_x] == 0:

            return True,True
        elif self.map_data[new_y][base_x] == 0:

            return False,True

        elif self.map_data[base_y][new_x] == 0:

            return True,False
        else:
            return False,False


    def fall(self):
        rise = 0

        print("fall-err",self.jumping,self.faling)
        if self.jumping|self.faling:
            return

        repeat = False
        self.faling=True

        acselaration = 1
        def falltime():
            print("fallfsdfsdafdsafdsafdsa")
            nonlocal rise,acselaration,repeat


            if (rise >= 0):
                rise += 1
                if acselaration < 4:
                    acselaration += 0.7

                _, yt = self.move(0, 1, 50, 50, int(2 * acselaration))
                if not yt:
                    if repeat:
                        self.faling=False
                        return
                    else:
                        repeat=True
                        if acselaration<1:
                            self.faling = False
                            return
                        acselaration=acselaration//2
                else:
                    repeat=False


            self.render_loop.after(10, falltime)

        self.render_loop.after(10, falltime)

        pass

    def jump(self, jump_height=40, jump_speed=2):


        if self.faling:
            return
        rise=10
        down=False
        self.jumping=True
        def jumptime():
            nonlocal rise,down
            acselaration=1.7
            print("djklasdk")

            if (not down)&(rise>=0):
                rise-=1
                if acselaration>0.9:
                    acselaration-=0.1
                _,yt=self.move(0,-1,50,50,int(1*acselaration))
                if not yt:
                    down=True
            elif down:
                rise+=1
                if acselaration<3:
                    acselaration+=0.44

                _, yt = self.move(0, 1, 50, 50, int(1*acselaration))
                if not yt:
                    self.jumping=False
                    return
            elif not(rise>=0):
                down=True
            self.render_loop.after(10, jumptime)


        self.render_loop.after(10,jumptime)

        pass

    def move(self, px, py,player_width,player_height,speed=2):
        try:
            px,py=px*speed,py*speed
            new_x = self.player_x + px
            new_y = self.player_y + py



            if 0 < new_x < self.width and 0 < new_y < self.height:
                #print(self.player_x,self.player_y,px,py,self.height,player_width)



                xm,ym=True,True
                print(player_width,"###",new_x+player_width,new_y,self.map_data[300][30])

                c4x, c4y = self.check_corner(new_x + player_width, new_y + player_height,self.player_x+player_width, self.player_y+player_height)
                c2x,c2y=self.check_corner(new_x+player_width,new_y,self.player_x+player_width, self.player_y)

                #print(new_x,new_y,new_x+player_width, new_y+player_height,self.map_data[new_y][new_x],"\r")

                c1x, c1y = self.check_corner(new_x, new_y,self.player_x,self.player_y)
                c3x,c3y=self.check_corner(new_x, new_y+player_height,self.player_x,self.player_y+player_height)

                #print(c4y)

                if not (c1x&c2x&c3x&c4x):
                    xm=False

                if not (c1y&c2y&c3y&c4y):
                    ym=False

                print("x",(self.map_data[self.player_y+player_height+20][self.player_x] == 0)&(self.map_data[self.player_y+player_height+20][self.player_y+player_width] == 0))
                if ((self.map_data[self.player_y+player_height+20][self.player_x] == 0)&(self.map_data[self.player_y+player_height+20][self.player_y+player_width] == 0)):
                    self.fall()
                if (xm&ym):
                    self.player_x = new_x
                    self.player_y = new_y
                    self.on_move(self.player_x, new_y)
                    return True,True
                elif ((not xm)&ym):
                    self.player_y = new_y
                    self.on_move(self.player_x, new_y)
                    return False,True
                elif (  xm&(not ym)):
                    self.player_x = new_x
                    self.on_move(self.player_x, new_y)
                    return True,False
                return False,False



            return False,False
        except IndexError:
            print("Fall out of world!")
            return  False,False
    def get_position(self):
        return self.player_x, self.player_y

    def setposition(self,x,y):
        self.player_x=x
        self.player_y=y



def openLevel(num,renderloop):
    path=f"leveldata/{1}/"
    l=Level(path+"map.move.png",renderloop)
    l.setposition(250,30)
    print(l.get_position())
    return path+"map.png",l


