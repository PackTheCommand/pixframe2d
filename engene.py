import math
import os
import random
import threading
import time

import pygame
import sys

from pygame import KEYDOWN, KEYUP, BLEND_RGBA_MULT

from mygame.objects.animation import Animation

import json

def get_files_in_folder(folder_path):
    files = []

    try:
        # Get a list of all items in the folder
        items = os.listdir(folder_path)

        # Filter out only the files (not directories)
        files = [item for item in items if os.path.isfile(os.path.join(folder_path, item))]

    except OSError as e:
        print("Error:", e)

    return files
class GameRenderLoop:
    def __init__(self, width, height):
        self.lights =[]
        self.shadow_store = {}
        self.shadow_textures = {}
        self.no_schadow_elements = []
        self.display_debug = False

        self.screen_width, self.screen_height=width,height
        pygame.init()
        self.width = width
        self.map_ofset_x,self.map_ofset_y=0,0
        self.height = height
        self.screen = pygame.display.set_mode((width, height),vsync=1)
        self.clock = pygame.time.Clock()
        self.schadow_intensity=(100,100,100)
        self.elements = {}
        self.animation_colections = {}
        self.keypressfunction=None
        self.light_templade=pygame.image.load("imgs/ShadowMaps/1.png")
        self.light_templade_coise_colect=[]
        for i in get_files_in_folder("imgs/ShadowMaps/"):
            self.light_templade_coise_colect+=[pygame.image.load("imgs/ShadowMaps/"+i)]
        self.event_listeners = {}
        self.element_click_listeners = {}  # Store click listeners by element ID
        self.hidden_elements = {}  # Set to store hidden element IDs
        self.font_cache = {}  # Cache font interfaces for different sizes
        self.scedue_queue = []
        self.debug_interface_function=None
        self.menu_elements=[]


        self.scheduled_events = []

    def addSchadowIgnore(self,id):
        self.no_schadow_elements.append(id)

    def after(self, duration, function):
        scheduled_time = pygame.time.get_ticks() + duration
        self.scheduled_events.append((scheduled_time, function))

    def process_scheduled_events(self):
        current_time = pygame.time.get_ticks()
        events_to_remove = []

        for scheduled_time, function in self.scheduled_events:
            if current_time >= scheduled_time:
                function()
                events_to_remove.append((scheduled_time, function))

        for event in events_to_remove:
            self.scheduled_events.remove(event)

    def genId(self):
        r=random.randint(1,99999999)
        while (r in self.elements.keys()) or (r in self.elements.keys()):
            r = random.randint(1, 99999999)
        return r

    def addEventListener(self, event_type, event_function):
        if event_type not in self.event_listeners:
            self.event_listeners[event_type] = []
        self.event_listeners[event_type].append(event_function)

    def removeEventListeners(self, listener):
        for event_type, event_functions in self.event_listeners.items():
            self.event_listeners[event_type] = [func for func in event_functions if func != listener]

    def startuplogo(renderloop):
        logo_image = pygame.image.load("imgs/company_logo.png")
        logo_width, logo_height = logo_image.get_size()
        logo_x = (renderloop.width - logo_width) // 2
        logo_y = (renderloop.height - logo_height) // 2

        fade_in_time = 1000  # milliseconds
        fade_out_time = 1000  # milliseconds

        for alpha in range(0, 255):
            logo_image.set_alpha(alpha)
            renderloop.screen.fill((0, 0, 0))
            renderloop.screen.blit(logo_image, (logo_x, logo_y))
            pygame.display.flip()
            pygame.time.wait(fade_in_time // 255)

        pygame.time.wait(1000)

        for alpha in range(255, 0, -1):
            logo_image.set_alpha(alpha)
            renderloop.screen.fill((0, 0, 0))
            renderloop.screen.blit(logo_image, (logo_x, logo_y))
            pygame.display.flip()
            pygame.time.wait(fade_out_time // 255)

        renderloop.elements = [element for element in renderloop.elements if element[1] != logo_image]
        pygame.time.wait(1000)

    def hide(self, element_id):

        print(element_id in self.elements)
        if element_id in self.elements:
            self.hidden_elements[element_id]=self.elements.pop(element_id)

    def hides(self,element_ids:list):
        for id in element_ids:

            if not (type(id)==int):

                id.__hide__()
                continue
            self.hide(id)
    def removes(self,element_ids:list):
        for id in element_ids:
            print(id)

            if not (type(id)==int):


                self.removes(id.__remove__())
                continue
            self.removeElement(id)
    def getSurface(self, element_id)->pygame.Surface|None:

        if element_id in self.elements:
            element, _, _,_=self.elements[element_id]


            if isinstance(element, pygame.Surface):
                return element
            if isinstance(element, Animation):
                return element.getSurface()
            elif isinstance(element, pygame.font.Font):
                return element.render("", True, (0, 0, 0))
            else:
                raise ValueError("Unsupported element type"+str(element))


        return None
    def moveto(self,id,x,y):
        #print("move")
        if id in self.elements:
            e,ox,oy,umo=self.elements[id]
            self.elements[id]=(e,x,y,umo)
        elif id in self.hidden_elements:
            e,ox,oy,umo=self.elements[id]
            self.elements[id]=(e,x,y,umo)


    def getXY(self,id):
        if id in self.elements:
            e,ox,oy,umo=self.elements[id]
            """if umo:
                return ox+self.map_ofset_x, oy+self.map_ofset_y"""
            return ox,oy
        elif id in self.hidden_elements:
            e,ox,oy,umo=self.elements[id]
            """ if umo:
                return ox+self.map_ofset_x, oy+self.map_ofset_y"""
            return ox,oy
        return None,None

    def lift(self,element_id):

        if element_id in self.elements:
            e=self.elements.pop(element_id)
            self.elements[element_id]=e

    def lower(self,element_id):

        if element_id in self.elements:
            e = self.elements.pop(element_id)
            self.elements = {element_id: e, **self.elements}


    def scedueCall(self):


        i=0
        while (i<len(self.scedue_queue)):
            try:
                r=self.scedue_queue[i]()

                if r==3:
                    self.scedue_queue.pop(i)
                else:
                    i+=1
            except IndexError:
                self.scedue_queue.pop(i)

    def set_scedue(self,func):
        print("addet",func)
        self.scedue_queue+=[func]

    def clear_scedue(self):
        self.scedue_queue=[]
    def show(self, element_id):
        if element_id in self.hidden_elements:
            if element_id in self.hidden_elements:
                self.elements[element_id] = self.hidden_elements.pop(element_id)

    def addAnimatedImage(self,path, x, y,  scale_x=1.0, scale_y=1.0,uses_map_offset=True):

        with open(path) as f:
            animation = json.load(f) #{"frames":[{"path":str}],"speed":1.0,"subanimations":{}}
            #todo Implement Subanimations
        l = []
        shadow_images=[]
        for i in animation["frames"]:
            path=i["path"]


            image = pygame.image.load("imgs/"+path)
            image = pygame.transform.scale(image, (int(image.get_width() * scale_x), int(image.get_height() * scale_y)))
            shadow_images+=[self.craete_manual_shadow_image(image)]
            l+=[image]
        d={}
        sub_shadows={}
        for subani in animation["subanimations"]:
            d[subani]=[]
            sub_shadows[subani]=[]
            for frame in animation["subanimations"][subani]["frames"]:
                image = pygame.image.load("imgs/"+frame["path"])
                image = pygame.transform.scale(image, (int(image.get_width() * scale_x), int(image.get_height() * scale_y)))
                d[subani] +=[image]
                sub_shadows[subani] +=[self.craete_manual_shadow_image(image)]
        element_id = self.genId()
        animationObj=Animation(l,animation["speed"],d,element_id,shadow_images,sub_shadows)
        self.animation_colections[element_id]=animationObj
        self.elements[element_id]=( animationObj, x, y,uses_map_offset)
        return element_id,animationObj
    def addImage(self, path, x, y, scale_x=1.0, scale_y=1.0,uses_map_offset=True):
        image = pygame.image.load(path)
        image = pygame.transform.scale(image, (int(image.get_width() * scale_x), int(image.get_height() * scale_y)))
        element_id = self.genId()
        self.shadow_textures[element_id] = self.modify_translucent_areas(image, self.schadow_intensity)

        self.elements[element_id]=( image, x, y,uses_map_offset)
        return element_id

    def modify_translucent_areas(self,image, color):
        """If an image doesnt work in the shadow"""
        color=self.schadow_intensity
        # Create a copy of the image to modify
        modified_image = image.convert()
        tr=False
        hasTranclucensi=False
        for x in range(modified_image.get_width()):
            for y in range(modified_image.get_height()):
                tr=True

                pixel_color = modified_image.get_at((x, y))
                mg=60
                # Check if the pixel is fully translucent
                if (pixel_color.r<=mg and pixel_color.g<=mg and pixel_color.b<=mg):
                    # Set color to white if translucent, else set the provided color
                    hasTranclucensi=True
                    modified_image.set_at((x, y), (255,255,255,255))

                else:
                    modified_image.set_at((x, y),(*color,255) )
        """if not hasTranclucensi:
            

            modified_image.fill((255,0,0))"""

        print(modified_image.get_size())
        return modified_image

    def addTorch(self,x,y,width,flickering_light=True):
        self.lights+=[(x,y,width,flickering_light)]


    def addImageFixedWidth(self, path, x, y, width,height,uses_map_offset=True):
        
        
        
        image = pygame.image.load(path)

        image = pygame.transform.scale(image, (width, height))
        
        
        
        element_id = self.genId()
        if path not in self.shadow_store:
            st=self.modify_translucent_areas(image, self.schadow_intensity)
            self.shadow_textures[element_id]=st
            self.shadow_store[path]=st
        else:
            self.shadow_textures[element_id]=self.shadow_store[path]

        self.elements[element_id]=( image, x, y,uses_map_offset)
        #print(image,element_id)
        return element_id
    def craete_manual_shadow_image(self,image):
        return self.modify_translucent_areas(image, self.schadow_intensity)

    def addText(self, text, x, y, font_size=36, color=(255, 255, 255),uses_map_offset=False):
        if font_size not in self.font_cache:
            font = pygame.font.Font(None, font_size)
            self.font_cache[font_size] = font
        else:
            font = self.font_cache[font_size]

        text_surface = font.render(text, True, color)
        element_id = self.genId()
        self.elements[element_id]=( text_surface, x, y,uses_map_offset)
        return element_id

    def addClickListener(self, element_id, click_function):
        event_id = len(self.element_click_listeners) + 1
        if element_id not in self.element_click_listeners:
            self.element_click_listeners[element_id] = []
        self.element_click_listeners[element_id].append((event_id, click_function))
        return event_id
    
    


    def removeClickListener(self, event_id):
        """

        :param event_id:
        :return:
        """
        for element_id, listeners in self.element_click_listeners.items():
            self.element_click_listeners[element_id] = [(eid, fn) for eid, fn in listeners if eid != event_id]

    def clearClickListener(self,element_id):
        if element_id in self.element_click_listeners:
            self.element_click_listeners.pop(element_id)

    def setClickListenerDisabled(self, element_id, disabled):
        if element_id in self.element_click_listeners:
            for event_id, _ in self.element_click_listeners[element_id]:
                if disabled:
                    pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
                else:
                    pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)

    def quit(self):
        self.running = False
        pygame.quit()
    def mod_map_ofset(self,xp,yp):
        self.map_ofset_x-=xp
        self.map_ofset_y-=yp
    def removeElement(self, element_id):
        if element_id in self.elements:
            if element_id in self.shadow_textures:
                self.shadow_textures.pop(element_id)

            self.elements.pop(element_id)
        elif element_id in self.hidden_elements:
            if element_id in self.shadow_textures:
                self.shadow_textures.pop(element_id)
            self.hidden_elements.pop(element_id)

    def createShadowMap(self):
        #polygon_points = []
        s=pygame.Surface((self.screen_width,self.screen_height))
        s.fill((255,255,255))


        def text(text,x,y):
            font = pygame.font.Font(None, 16)  # You can replace None with a font file path

            # Set the text you want to render


            # Render the text onto the surface
            text_render = font.render(text, True, (255, 255, 255))  # Text color: white

            # Define the position where you want to render the text on the surface
            text_position = (x,y)

            # Blit (copy) the rendered text onto the surface
            s.blit(text_render, text_position)



        for n,obj_id in enumerate(self.elements.copy()):
            if obj_id in self.no_schadow_elements:

                continue


            if obj_id not  in self.elements:
                continue
            x, y = self.getXY(obj_id)



            o_type=self.elements[obj_id][0]
            if isinstance(o_type,Animation):

                obj_id=o_type.getRenderLoopId()
                if self.getUsesMapOfset(obj_id):
                    x, y = self.map_ofset_x + x, self.map_ofset_y + y
                if not ((-100 < x - 50 < self.width) & (-100 < y - 50 < self.height)):
                    continue
                if obj_id in self.shadow_textures:
                    s.blit(o_type.getShadow_img(), (x, y))
                    continue
                continue

            if self.getUsesMapOfset(obj_id):
                x,y=self.map_ofset_x+x,self.map_ofset_y+y
            if not ((-100<x-50<self.width)&(-100<y-50<self.height)):
                continue
            if obj_id in self.shadow_textures:


                s.blit(self.shadow_textures[obj_id],(x,y))
                """text(str(obj_id),x+10,y+10)"""
                continue

            """text("s-ERROR", x + 10, y + 10)"""

            surf=self.getSurface(obj_id)

        for n,light in enumerate(self.lights):
            x,y,w,flickers=light[0],light[1],light[2],light[3]
            x, y = self.map_ofset_x + x, self.map_ofset_y + y
            if not ((-100 < x - 50 < self.width) & (-100 < y - 50 < self.height)):

                continue
            lightLayer=self.light_templade
            """if flickers:
                lightLayer=random.choices(self.light_templade_coise_colect)[0]
            """

            s.blit(pygame.transform.scale(lightLayer,(w*2,w*2)),(x-w-25,y-w-25))
            #pygame.draw.circle(s, (255,255,255,255),(x-w-25,y-w-25),w)





        # Create a surface to draw the polygon
        #polygon_surface = pygame.Surface((max_x - min_x, max_y - min_y), pygame.SRCALPHA)

        #c=pygame.draw.rect(s,(100,100,100), (0,0,self.screen_width,self.screen_height))

        s.set_colorkey((0,0,0))
        return s

    def distance(s,point1, point2):
        return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

    def raycasting_shadow_polygons(self,surface, light_source, obstacles):


        for ray_angle in range(0, 360, 5):
            ray_direction = pygame.math.Vector2(math.cos(math.radians(ray_angle)), math.sin(math.radians(ray_angle)))
            intersections = []

            for obstacle in obstacles:
                for point in obstacle:
                    to_point = pygame.math.Vector2(point[0] - light_source[0], point[1] - light_source[1])
                    angle_diff = ray_direction.angle_to(to_point)

                    if abs(angle_diff) < 45:
                        intersections.append(point)

            if intersections:
                intersections.sort(key=lambda point: self.distance(light_source, point))
                pygame.draw.polygon(surface, self.SHADOW_COLOR, intersections)
    def getUsesMapOfset(self,id):
        if id in self.elements:
            return self.elements[id][3]
    def run(self):
        self.running = True
        def scedue():

            while self.running:

                self.scedueCall()

                time.sleep(0.01)
        threading.Thread(target=scedue).start()
        pressed_keys = set()
        self.togled_debug=False

        while self.running:

            mouseButtons_pressed = []
            presse_triger_once=[]
            self.process_scheduled_events()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == KEYDOWN:
                    presse_triger_once+=[event.key]

                    if event.key == pygame.K_F1:

                        self.display_debug=not self.display_debug


                    pressed_keys.add(event.key)
                elif event.type == KEYUP:

                    pressed_keys.discard(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouseButtons_pressed+=[event]
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    print(event)
                    if event.button==1:
                        for element_id in list(self.elements.keys()):

                            if element_id in self.elements:
                                element, x, y,uses_map_ofset = self.elements[element_id]
                                if x <= mouse_x <= x + element.get_width() and y <= mouse_y <= y + element.get_height():
                                    #print(element_id , self.element_click_listeners)
                                    if element_id in self.element_click_listeners:
                                        for _, click_function in self.element_click_listeners[element_id]:
                                            click_function()


                elif event.type in self.event_listeners:
                    for event_function in self.event_listeners[event.type]:
                        event_function(event)

            #self.screen.fill((0, 0, 0))  # Fill the screen with black
            if self.keypressfunction:
                self.keypressfunction(pressed_keys,mouseButtons_pressed,presse_triger_once)



            for element_id in self.elements.copy() :
                if element_id not in self.elements:
                    continue
                #print(element_id)
                #print(self.elements[element_id],element_id)
                element, x, y,uses_map_ofset = self.elements[element_id]
                if isinstance(element, pygame.Surface):
                    if uses_map_ofset:
                        self.screen.blit(element, (self.map_ofset_x+x, self.map_ofset_y+y))


                    else:

                        self.screen.blit(element, (x,y))
                elif isinstance(element, Animation):

                    element=element.getImage()
                    if uses_map_ofset:
                        self.screen.blit(element, (self.map_ofset_x + x, self.map_ofset_y + y))


                    else:

                        self.screen.blit(element, (x, y))

            if self.debug_interface_function:

                if (self.display_debug):

                    self.debug_interface_function(True)
                else:
                    self.debug_interface_function(False)

            if self.flagXL_SCHADOW_FILTER:
                shadow_map = self.createShadowMap()
                self.screen.blit(shadow_map,(0,0),special_flags=BLEND_RGBA_MULT)
            self.clock.tick(60)


            pygame.display.flip()  # Update the display
              # Limit to 60 FPS
            self.screen.fill((0, 0, 0))
        pygame.quit()
        sys.exit()

    def togleSchadows(self, param):
        self.flagXL_SCHADOW_FILTER=param
        pass

class SCHADOW_STATE:
    ON=True
    OFF=False

if __name__ == "__main__":
    render_loop = GameRenderLoop(800, 600)

    render_loop.run()