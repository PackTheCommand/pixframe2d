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

class DestrucktionShader(Shader):
    def __init__(self,effectlen=80,disturptionlen=40,keepdistorption_in_pause=False,distrorption_range=(5,10),fragmentSize=10):
        self.disturptionlen=disturptionlen
        self.effectlen=effectlen
        self.counter=0
        self.random_ofsets=[]
        super().__init__()
        self.keepdistorption_in_pause=keepdistorption_in_pause
        self.distrorption_range=distrorption_range
        self.fragmentSize=fragmentSize



    def apply(self,display:pygame.display):
        try:

            w=display.get_width()
            h=display.get_height()

            if self.disturptionlen<self.counter<self.effectlen:
                keep_render=True
            else:
                keep_render=False
                if self.counter>=self.effectlen:

                    self.counter=0


            screenrects=[]
            self.counter+=1
            if not keep_render:
                self.random_ofsets=[]
            if self.keepdistorption_in_pause | (not keep_render):
                for i in range(0,h,self.fragmentSize):
                    sub=grab(display,0,i,w,self.fragmentSize)
                    screenrects.append(sub)
                    ofset = randint(self.distrorption_range[0], self.distrorption_range[1])
                    if not keep_render:
                        self.random_ofsets.append(ofset)

                pos=True
                display.fill((0, 0, 0))
                for i in range(len(screenrects)):
                    ofset=self.random_ofsets[i]

                    if pos:
                        display.blit(screenrects[i],(ofset,i*self.fragmentSize))
                    else:
                        display.blit(screenrects[i],(-ofset,i*self.fragmentSize))
                    pos=not pos
        except Exception as e:
            print(e)
            self.counter=0
            self.random_ofsets = []
            pass




