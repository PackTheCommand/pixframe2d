from random import randint

import pygame

from .baseShader import Shader

def grab(display,x, y, w, h):
    "Grab a part of the screen"
    # get the dimension of the surface
    rect = pygame.Rect(x, y, w, h)
    # copy the part of the screen
    sub = display.subsurface(rect)
    # create another surface with dimensions
    # This is done to unlock the screen surface
    screenshot = pygame.Surface((w, h))
    screenshot.blit(sub, (0, 0))
    return screenshot

class ScreenshakeShader(Shader):
    def __init__(self,effectlen=120,ofset_range_x=(-10,10),ofset_range_y=(-10,10),effectpause=10):
        self.effectlen=effectlen

        self.ofset_range_x=ofset_range_x
        self.ofset_range_y=ofset_range_y
        self.counter=0
        self.random_ofsets=[]
        super().__init__()
        self.effectpause=effectpause





    def apply(self,display:pygame.display):
        try:

            w=display.get_width()
            h=display.get_height()

            if self.effectpause<self.counter<self.effectlen:
                keep_render=True
            else:
                keep_render=False
                if self.counter>=self.effectlen:

                    self.counter=0



            self.counter+=1
            if keep_render:

                screenrect=grab(display,0,0,w,h)
                ofset_x = randint(self.ofset_range_x[0],self.ofset_range_x[1])
                ofset_y = randint(self.ofset_range_y[0],self.ofset_range_y[1])



                display.blit(screenrect,(ofset_x,ofset_y))
        except Exception as e:
            print(e)
            self.counter = 0
            pass




