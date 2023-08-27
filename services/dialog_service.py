import json

import pygame

from textwrap import wrap



class fade:
    IN=0
    OUT=1

class DialogService:
    def draw_alpha_circle(self,screen, alpha_value, screen_width, screen_height):
        # Clear the screen
        if alpha_value>255:
            alpha_value=255

        # Calculate circle position
        circle_x = screen_width // 2
        circle_y = screen_height // 2

        # Create a circle surface
        circle_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, )
        pygame.draw.rect(circle_surface, (0, 0, 0, alpha_value), (0, 0, screen_width, screen_height))
        self.loading_screen_img.set_alpha(alpha_value)
        circle_surface.blit(self.loading_screen_img, (circle_x-100, circle_y-100))


        # Blit the circle surface onto the main screen
        screen.blit(circle_surface, (0, 0))  # ,special_flags=pygame.BLEND_RGBA_ADD)

    curantService=None
    def __init__(self, renderloop):
        self.renderloop = renderloop
        DialogService.curantService=self
        self.curdialog=None
        self.fade_in=0

        self.loading_screen_img=pygame.transform.scale(pygame.image.load("imgs/loading_icon.png"),(200,200))
        self.dialog_endet=False
        self.fade_in_or_out=fade.OUT
        self.box=pygame.transform.scale(pygame.image.load("imgs/dialog_box.png"),(self.renderloop.screen_width,(self.renderloop.screen_height//4)))
        self.dialog_index = -1
        self.store= {"text":[], "img":None,"box":None,"text_source":None}
        self.font=font = pygame.font.Font(None, 50)
        self.source_font=pygame.font.Font(None, 60)
    def while_dialog(self,key_inputs,screen:pygame.surface.Surface):
        if not (self.fade_in <= 0):
            print(self.fade_in)
            self.draw_alpha_circle(screen,self.fade_in,self.renderloop.screen_width,self.renderloop.screen_height)

            if self.fade_in_or_out==fade.OUT:
                self.fade_in+=3
                if self.fade_in>=350:
                    self.fade_in-=2


                    self.fade_in_or_out=fade.IN
                return





        if self.store["img"]!=None:

            screen.blit(self.store["img"],(0,0))
        screen.blit(self.box, (0, (self.renderloop.screen_height//4)*3-60))
        if self.store["text"]!=[]:
            for n,text in enumerate(self.store["text"]):
                screen.blit(text, (self.renderloop.screen_width//6, (self.renderloop.screen_height//4)*3+50*n))
        if self.store["text_source"]!=None:
            screen.blit(self.store["text_source"], (self.renderloop.screen_width//6-40, (self.renderloop.screen_height//4)*3-50))

        if self.fade_in!=0:
            self.draw_alpha_circle(screen, self.fade_in, self.renderloop.screen_width, self.renderloop.screen_height)
            self.fade_in -= 2
        else:
            self.renderloop.pause_gameplay_level_engene=True

        if not self.dialog_endet:
            if pygame.K_SPACE in key_inputs:

                if self.dialog_index>=len(self.curdialog):

                    self.dialog_endet=True

                    self.fade_in=4

                    return
                else:
                    self.ren_new_dialog_part(screen)
                    self.dialog_index += 1
        else:
            if self.fade_in != 0:
                print(self.fade_in)
                self.draw_alpha_circle(screen, self.fade_in, self.renderloop.screen_width, self.renderloop.screen_height)

                if self.fade_in_or_out == fade.OUT:
                    self.fade_in += 2
                    if self.fade_in >= 350:
                        self.fade_in-=2
                        self.fade_in_or_out = fade.IN
                    return
            self.renderloop.pause_gameplay_level_engene = False
            if not (self.fade_in <= 0):
                self.draw_alpha_circle(screen, self.fade_in, self.renderloop.screen_width, self.renderloop.screen_height)
                self.fade_in -= 2
            else:
                self.renderloop.in_dialog = False
                self.renderloop.togleSchadows(True)




    def ren_new_dialog_part(self, screen=None, max_chars=40):
        self.box = pygame.transform.scale(pygame.image.load("imgs/dialog_box.png"),
                                          (self.renderloop.screen_width, (self.renderloop.screen_height // 4)))

        print("index",self.dialog_index)
        it=self.curdialog[self.dialog_index]
        if it.get("img")!=None:
            self.store["img"]=pygame.transform.scale(pygame.image.load(it["img"].replace("$levdir",self.renderloop.level.path[:-1])),(self.renderloop.screen_width,self.renderloop.screen_height))
        self.store["text"]=[]
        if it.get("text")!=None:

            
            for i in wrap(it["text"],max_chars):
                self.store["text"].append(self.font.render(i,True,(255,255,255),))

        if it.get("text_source")!=None:
            f=self.source_font.render(it["text_source"],True,(255,255,255),)
            self.store["text_source"]=f



    def run_dialog(self,file):
        file=file.replace("$levdir",self.renderloop.level.path[:-1])
        self.fade_in_or_out=fade.OUT
        self.dialog_endet=False
        self.fade_in=4

        with open(file, "r") as f:
            self.curdialog = json.load(f)
        self.renderloop.in_dialog=True
        self.dialog_index = 0
        self.renderloop.togleSchadows(False)


        self.ren_new_dialog_part(self.renderloop.screen)


