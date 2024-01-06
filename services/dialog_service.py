import json
import math

import pygame

from textwrap import wrap



class fade:
    IN=0
    OUT=1



limgs=None
loading_index=0

def draw_percent_circle(screen, center, radius, procent, color, start_angle=0):
    total_value = 100


    if procent>=100:
        procent=100
        color=(76, 185, 68)
    angle_per_value = 360 / total_value

    current_angle = start_angle

    i, value = 0,procent
    angle = value * angle_per_value


    # Calculate the points of the pie slice
    points = []
    num_points = int(angle) + 2
    for j in range(num_points):

        #outer_point
        angle_rad = math.radians(current_angle + (j / (num_points - 1)) * angle)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))
        #iner point
    for j in range(num_points):
        angle_rad = math.radians(current_angle + (j / (num_points - 1)) * angle)
        x = center[0] + radius//9*8 * math.cos(angle_rad)
        y = center[1] + radius//9*8*math.sin(angle_rad)
        points.append((x, y))

    for j in range(num_points).__reversed__():

        #outer_point
        angle_rad = math.radians(current_angle + (j / (num_points - 1)) * angle)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))




    pygame.draw.polygon(screen, color, points)
    current_angle += angle


def getloadingImg(surf:pygame.surface.Surface,procent):
    global loading_index


    draw_percent_circle(surf, (surf.get_width()-100, surf.get_height()-100), 20, procent, (255, 255, 255))
    return surf

loading_progress=0


def rounded_polygon(start, end, text, font, screen, outline_margin=2):
    # Define colors
    Forground = (255, 255, 255)
    BackgroundC = (0, 0, 0, 128)

    # Define points for polygon

    # Draw polygon

    pygame.draw.rect(screen, BackgroundC,
                     pygame.rect.Rect(start[0], start[1], end[0] - start[0], end[1] - start[1]), border_radius=20)
    om = outline_margin
    pygame.draw.rect(screen, Forground,
                     pygame.rect.Rect( start[0]+ om, start[1] + om, end[0] - start[0] - om * 2,
                                      end[1] - start[1] - om * 2), 1,
                     border_radius=20)

    # Draw text
    # pygame.draw.polygon(screen, BLACK, points2, outline_width)
    text_surface = font.render(text, True, Forground)
    #print("width",text_surface.get_width())

    pygame.draw.rect(screen, BackgroundC,(start[0]+10,start[1]-20,text_surface.get_width()+
                                        15,text_surface.get_height()+10),border_radius=10,)

    screen.blit(text_surface, (start[0] + 20, start[1]-10 ))

class BackgoundModeFlags:

    STORY=0
    GAME=1
line_ofset = 0
max_row=0

class DialogService:
    def draw_alpha_circle(self,screen, alpha_value, screen_width, screen_height):
        global loading_progress
        # Clear the screen
        if alpha_value>255:
            alpha_value=255

        # Calculate circle position
        circle_x = screen_width // 2
        circle_y = screen_height // 2

        # Create a circle surface


        circle_surface = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA, )

        if self.FLAG_BACKGROUND_MODE == BackgoundModeFlags.STORY:

            pygame.draw.circle(circle_surface, (0, 0, 0, alpha_value),(screen_width//2,screen_height//2),(screen_width//2)*alpha_value)
            self.loading_screen_img.set_alpha(alpha_value)

            circle_surface.blit(self.loading_screen_img, (circle_x - 100, circle_y - 100))




        getloadingImg(circle_surface, int(loading_progress))

        # Blit the circle surface onto the main screen
        screen.blit(circle_surface, (0, 0))  # ,special_flags=pygame.BLEND_RGBA_ADD)

    curantService=None
    def __init__(self, renderloop,kt=None):
        self.text_popuop_efect_index =0
        global limgs
        self.keytrans=kt

        self.currant_text_group_len=0
        self.renderloop = renderloop
        DialogService.curantService=self
        self.curdialog=None
        self.fade_in=0
        self.FLAG_BACKGROUND_MODE=BackgoundModeFlags.STORY


        self.loading_screen_img=pygame.transform.scale(pygame.image.load("imgs/loading_icon.png"),(200,200))
        self.dialog_endet=False
        self.fade_in_or_out=fade.OUT
        """self.box=pygame.transform.scale(pygame.image.load("imgs/dialog_box.png"),(self.renderloop.screen_width,(self.renderloop.screen_height//4)))
        """
        self.dialog_index = -1
        self.store= {"text":[], "img":None,"box":None,"text_source":None}
        self.font=font = pygame.font.Font(None, 30)
        self.source_font=pygame.font.Font(None, 40)


    def while_dialog(self,key_inputs,screen:pygame.surface.Surface,mouse_input):
        global loading_progress
        max_lines_on_screen=4
        print("dindex=",self.dialog_index)

        skip_spaceKey=False
        global line_ofset,max_row
        if not (self.dialog_endet):
            if pygame.K_SPACE in key_inputs:
                lentext = len(self.store["text"])
                if (self.text_popuop_efect_index <= lentext):
                    self.text_popuop_efect_index = lentext + 1
                    skip_spaceKey=True





        self.draw_alpha_circle(screen, self.fade_in, self.renderloop.screen_width, self.renderloop.screen_height)
        loading_progress +=1
        #print("loading...",loading_progress,)
        if self.FLAG_BACKGROUND_MODE == BackgoundModeFlags.STORY:

            if not (self.fade_in <= 0):
                #(self.fade_in)

                if self.fade_in_or_out==fade.OUT:
                    self.fade_in+=3


                    #print(loading_progress)
                    if self.fade_in>=350:
                        self.fade_in-=2
                        self.renderloop.togleSchadows(False)




                    self.fade_in_or_out=fade.IN
                return
            if self.fade_in != 0:

                self.fade_in -= 2
            else:
                self.renderloop.pause_gameplay_level_engene = True

            if not self.dialog_endet:
                if (not skip_spaceKey)&(pygame.K_SPACE in key_inputs):

                    if self.dialog_index >= len(self.curdialog):

                        self.dialog_endet = True

                        self.fade_in = 4

                        return
                    else:
                        self.ren_new_dialog_part(screen)
                        self.dialog_index += 1
            else:
                if self.fade_in != 0:
                    #print(self.fade_in)

                    if self.fade_in_or_out == fade.OUT:
                        self.fade_in += 2
                        if self.fade_in >= 350:
                            self.fade_in -= 2
                            self.fade_in_or_out = fade.IN
                        return
                self.renderloop.pause_gameplay_level_engene = False
                if not (self.fade_in <= 0):

                    self.fade_in -= 2
                else:
                    self.renderloop.in_dialog = False
                    self.renderloop.togleSchadows(True)
        else:
            if not self.dialog_endet:



                if (not skip_spaceKey)&(pygame.K_SPACE in key_inputs):


                    if self.dialog_index >= len(self.curdialog):

                        self.dialog_endet = True

                        self.fade_in = 4

                        return
                    else:






                        self.ren_new_dialog_part(screen)
                        self.dialog_index += 1
                        line_ofset=0
                        max_row=0
                        self.text_popuop_efect_index = 0

                for e in mouse_input:
                    if e.button == 4:

                        if line_ofset>0:
                            line_ofset-=1
                    elif e.button == 5:
                        if line_ofset<max_row:
                            line_ofset += 1


            else:

                self.renderloop.pause_gameplay_level_engene = False

                self.renderloop.in_dialog = False
                self.renderloop.togleSchadows(True)

        if self.FLAG_BACKGROUND_MODE == BackgoundModeFlags.STORY:
            if self.store["img"]!=None:

                screen.blit(self.store["img"],(0,0))

        text_source = "Unknown"
        if self.store["text_source"]!=None:
            text_source=self.store["text_source"]
        p1,p2=self.renderloop.screen_width//8, (self.renderloop.screen_height//4)*3-60

        rounded_polygon((p1,p2),(p1*7,self.renderloop.screen_height-40),text_source,self.source_font,screen)











        if self.store["text"]!=[]:
            self.currant_text_group_len=len(self.store["text"])
            #print("t",self.store["text"])
            #line breaking
            spaceofset = -1
            max_width = self.renderloop.screen_width//12*7
            wi = 0
            last_space_a = 0

            nl = []
            for n, text in enumerate(self.store["text"]):

                if text == "space":

                    last_space_a = n

                    wi+=10
                    if wi >= max_width:
                        nl.append( "break")

                        wi = 0
                        continue
                    else:
                        nl.append(text)
                        continue

                wi += text.get_width()
                if wi > max_width:
                    nl[last_space_a] =  "break"

                    wi = 0


                nl.append(text)

            #text rendering
            lastwidth=0

            row=0
            if self.text_popuop_efect_index<= len(self.store["text"]):
                self.text_popuop_efect_index+=0.5
            print("ti",self.text_popuop_efect_index)
            for n,text in enumerate(nl):
                print(n)
                if n>self.text_popuop_efect_index:
                    break
                #print(row)

                if text=="space":
                    lastwidth+=10

                    continue
                elif text=="break":
                    row+=1
                    lastwidth=0
                    continue



                if line_ofset<=row<max_lines_on_screen-line_ofset:
                    screen.blit(text, (self.renderloop.screen_width//6+lastwidth, (self.renderloop.screen_height//4)*3+50*(row-line_ofset)-10))


                lastwidth+=text.get_width()
                if row > max_row:
                    max_row += 1

                if (row > max_row)&(row > line_ofset):
                    line_ofset += 1



            #screen.blit(self.store["text_source"], (self.renderloop.screen_width//6-40, (self.renderloop.screen_height//4)*3-50))







    def ren_new_dialog_part(self, screen=None, max_chars=40):
        """ self.box = pygame.transform.scale(pygame.image.load("imgs/dialog_box.png"),
                                          (self.renderloop.screen_width, (self.renderloop.screen_height // 4)))"""


        it=self.curdialog[self.dialog_index]
        print("it",it)
        if it.get("img")!=None:
            self.store["img"]=pygame.transform.scale(pygame.image.load(it["img"].replace("$levdir",self.renderloop.level.path[:-1])),(self.renderloop.screen_width,self.renderloop.screen_height))
        self.store["text"]=[]
        if it.get("text")!=None:
            col = (255, 255, 255)
            toglecol=""
            for i in it["text"].split(" "):

                if i.startswith("*"):
                    i=i[1:]
                    toglecol="imp"
                    col=(245, 85, 54)

                if i.endswith("*"):

                    i = i[:-1]






                for e in i:


                    self.store["text"].append(self.font.render(e,True,col,))
                self.store["text"].append("space")

                if i.endswith("*"):
                    toglecol=""
                    i=i[:-1]
                    col=(255, 255, 255)

        if it.get("text_source")!=None:

            self.store["text_source"]=it["text_source"]



    def run_dialog(self,file):
        global loading_progress
        loading_progress = 0
        self.FLAG_BACKGROUND_MODE=BackgoundModeFlags.STORY
        file=file.replace("$levdir",self.renderloop.level.path[:-1])
        self.fade_in_or_out=fade.OUT
        self.dialog_endet=False
        self.fade_in=4

        with open(file, "r") as f:
            self.curdialog = json.load(f)
        self.renderloop.in_dialog=True
        self.dialog_index = 0



        self.ren_new_dialog_part(self.renderloop.screen)

    def run_dialog_in_game(self,file):
        global loading_progress
        loading_progress = 0
        self.FLAG_BACKGROUND_MODE = BackgoundModeFlags.GAME
        file = file.replace("$levdir", self.renderloop.level.path[:-1])
        self.fade_in_or_out = fade.OUT
        self.dialog_endet = False
        self.fade_in = 4

        with open(file, "r") as f:
            self.curdialog = json.load(f)
        self.renderloop.in_dialog = True
        self.dialog_index = 0
