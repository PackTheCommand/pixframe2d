import json
import threading

import scripting.objects.objectCol
from scripting.objects.level import Level
from audio import sound


INTERACTION_RADIUS=50

with open("leveldata/levels.json") as f:
    all_level_overview_json = json.load(f)

import pygame

from engene import GameRenderLoop, SCHADOW_STATE
from ui_elements import Button

import movable_objects


def title_screen(render_loop):
    def clear_content():
        nonlocal render_loop
        render_loop.clearMenu()

    def save_and_close():
        # Implement your save logic here
        pass

    def check_button_click():
        pass
        """print("Check button clicked")
        print("Checkbox 1:", checkbox1.is_checked())
        print("Checkbox 2:", checkbox2.is_checked())
        print("Input Text:", input_text.get_text())"""

    # checkbox1 = Checkbox(render_loop, 100, 200, width=20, height=20, label="Option 1")
    def play():
        # print("klicked")
        render_loop.hides([play, load, quit, title,creadits])
        level_select_screen()

    def cred():
        # print("klicked")
        render_loop.hides([play, load, quit, title, creadits])
        display_Credits()

    xline1 = SCREEN_WIDTH / 2 - 100

    title = render_loop.addText("My Game", xline1-40, 100, 90, )

    def quit():
        pygame.quit()
        quit()



    play = Button(render_loop, xline1, 200, width=200, height=50, text="Play", click_function=play, font_size=35)

    load = Button(render_loop, xline1, 280, width=200, height=50, text="Load", click_function=quit, font_size=35)

    quit = Button(render_loop, xline1, 360, width=200, height=50, text="Quit", click_function=None, font_size=35)

    creadits = Button(render_loop, 0, 0, width=80, height=20, text="Creadits", click_function=cred, font_size=25)
    """checkbox2 = Checkbox(render_loop, 100, 230, width=20, height=20, label="Option 2")

    input_text = TextInput(render_loop, 100, 300, width=200, height=40, placeholder="Enter text here")

    check_button = Button(render_loop, 320, 310, width=60, height=40, text="Check", click_function=check_button_click)

    clear_button = Button(render_loop, 20, 20, width=120, height=40, text="Clear Content", click_function=clear_content)
    save_button = Button(render_loop, 650, 550, width=120, height=40, text="Save and Close",
                         click_function=save_and_close)"""
def playsound(sound):

    threading.Thread(target=sound.play).start()
def loopsound(sound):

    threading.Thread(target=sound.play,args=(-1,)).start()

def display_Credits():
    def return_to_titlescreen():


        for i in credits_screen_store:

            render_loop.removeElement(i)
        render_loop.hides([B])
        title_screen(render_loop)
    def on_key(pressed_keys, mouseButtons_pressed,_):

        y = 0
        for event in mouseButtons_pressed:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button)
                if event.button == 4:
                    y += 100
                elif event.button == 5:
                    y -= 100
                if (y >= 0) & (render_loop.map_ofset_y - 100 <= 0):
                    render_loop.map_ofset_y += y
                elif (y < 0):
                    render_loop.map_ofset_y += y
                print(render_loop.map_ofset_y)
                break

    render_loop.keypressfunction = on_key
    credits_screen_store = []
    x=50
    with open("credits.txt") as f:
        for n, i in enumerate(f.readlines()):
            i = i[:-1]
            if i.startswith("#"):
                i=i[1:]
                t = render_loop.addText(i, x, 150 + 20 * n, 30, uses_map_offset=True)
            else:
                t = render_loop.addText(i, x, 150 + 20 * n, 20, uses_map_offset=True)
            credits_screen_store.append(t)


    B=Button(render_loop,0,0,60,30,"Menu",return_to_titlescreen)


    t = render_loop.addText("Credits", x - 30, 50, 50, uses_map_offset=True)
    credits_screen_store.append(t)









level=None

def level_select_screen():



    def load_levl(lev_file_path):

        print("selected", lev_file_path)

        for i in level_select_store:
            render_loop.clearClickListener(i)
            render_loop.removeElement(i)
        startGame(lev_file_path)

    x = 100

    def on_key(pressed_keys, mouseButtons_pressed,_):

        y = 0


        """<Event(1025-MouseButtonDown {'pos': (206, 393), 'button': 4, 'touch': False, 'window': None})>"""
        for event in mouseButtons_pressed:
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.button)
                if event.button == 4:
                    y += 100
                elif event.button == 5:
                    y -= 100
                if (y >= 0) & (render_loop.map_ofset_y - 100 <= 0):
                    render_loop.map_ofset_y += y
                elif (y < 0):
                    render_loop.map_ofset_y += y
                print(render_loop.map_ofset_y)
                break

    render_loop.keypressfunction = on_key
    level_select_store = []
    t = render_loop.addImage("imgs/level_select_bg.png", 0, 0, uses_map_offset=False)
    level_select_store.append(t)
    for n, i in enumerate(all_level_overview_json):
        t = render_loop.addText(f"{n+1}. "+i["name"], x, 150 + 50 * n, 30, uses_map_offset=True)
        render_loop.addClickListener(t, lambda ln=i["file"]: load_levl(ln))
        level_select_store.append(t)

    t = render_loop.addImage("imgs/level_select.png", 0, 0, uses_map_offset=False)
    level_select_store.append(t)
    t = render_loop.addText("Select a Level", x - 30, 50, 50, uses_map_offset=False)
    level_select_store.append(t)




SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000



def updateHeightWidth(w,h):
    global SCREEN_WIDTH,SCREEN_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = w,h

render_loop = GameRenderLoop(SCREEN_WIDTH, SCREEN_HEIGHT)


# render_loop.startuplogo()
def onclick():
    pass


"""def startGame():
    global level,s
    i,l=level_map.openLevel(1,render_loop)
    level=l
    imgbg=render_loop.addImage(i,0,0)
    player = render_loop.addImage("imgs/player.png", 0,0)
    s=render_loop.getSurface(player)
    s.get_width()
    s.get_height()

    l.setposition(220,30)
    l.on_move=lambda x,y:render_loop.moveto(player,x,y)


space_jump=False
space_tick=0"""

globalStore={}
def get_collisions(main_surface, main_id, other_surfaces):
    collisions = []
    mr = main_surface.get_rect()
    mr.topleft = render_loop.getXY(main_id)
    for n, other_surface in enumerate(other_surfaces):
        id = other_surfaces[other_surface]

        r = other_surface.get_rect()
        r.topleft = render_loop.getXY(id)

        if mr.colliderect(r):
            collisions.append(other_surface)

    return collisions


def check_if_collisions(main_surface, player_new_x, player_new_y, other_surfaces):
    mr = main_surface.get_rect()
    mr.topleft = player_new_x, player_new_y
    for n, other_surface in enumerate(other_surfaces):
        id = other_surfaces[other_surface]

        r = other_surface.get_rect()
        r.topleft = render_loop.getXY(id)

        if mr.colliderect(r):
            return True
    return False

musicBG_tile,musicBG_author="",""


player = None
daeth_areas = []
currant_game_file = ""
backgroundMusic=None
player_animation=None

level_store_uid_to_Elementid={}

# (x,y,width,height,KeyName)
keyPressInteractions=[]
levelOBJ=None
scriptsManagers= {}
from audio import definebgMusic
from scripting import scriptManager
def startGame(path_uuid=None):
    global player, player_surf, currant_game_file,backgroundMusic,musicBG_tile,musicBG_author,player_animation,level_store_uid_to_Elementid,levelOBJ,scriptsManagers
    render_loop.pauseMenu=pase_to_engene_pause_func
    levelOBJ = Level(render_loop)
    render_loop.level=levelOBJ
    if path_uuid == None:
        path_uuid = currant_game_file
    currant_game_file = path_uuid

    render_loop.togleSchadows(SCHADOW_STATE.ON)


    start_x, start_y = 100, 100
    render_loop.keypressfunction = handle_keypress
    player,player_animation = render_loop.addAnimatedImage("imgs/animations/player.anime", start_x, start_y, True)
    print("player", player)

    player_surf = render_loop.getSurface(player)

    with open(path_uuid + "level.levdat") as f:

        level = json.load(f)


    scripts=level["scripts"]
    print(scripts)



    scriptsManagers= {}
    for script in scripts:
        if script["path"].split(".")[-1]=="py":
            pass
            #scriptsManagers.append(scriptManager.pyManager(script["path"],path_uuid+"/scripts",render_loop,player))
        elif  script["path"].split(".")[-1]=="lua":
            name=script["path"][::-1].split(".",1)[1][::-1]
            scriptsManagers[name]=scriptManager.lua_Importer(name+".lua",path_uuid+"/scripts",render_loop,player,{"stop_sound":pauseAll})


    def genLevel(level,):
        global level_store_uid_to_Elementid
        global colidebles, level_store


        level_store = []
        colidebles = {}

        lowerable=[]
        for e in level:
            if e["type"] == "object":

                i = render_loop.addImageFixedWidth(e["texture"], e["x"], e["y"], e["width"], e["height"])
                if "o-layer" in e:
                    if e["o-layer"]=="back":
                        lowerable.append(i)
                if e["collision"]:
                    colidebles[render_loop.getSurface(i)] = i

                level_store.append(i)
                level_store_uid_to_Elementid[e["uuid"]]=i

                if "nbt" in e:
                    if "interact" in e["nbt"]:
                        interact_type=e["nbt"]["interact"]["sptype"]
                        if (interact_type=="Interactive")|(interact_type=="OneTime-Interact"):
                            keyPressInteractions.append((e["x"], e["y"],e["x"]+e["width"],e["y"]+e["height"],interact_type,e["nbt"]["interact"]["trigger"],e["nbt"]["interact"]["function"],e["uuid"]))

                    levelOBJ.nbts[e["uuid"]]=e["nbt"]
            elif e["type"] == "spawn":
                render_loop.moveto(player, e["x"], e["y"])
            elif e["type"] == "bg_image":
                i = render_loop.addImageFixedWidth(e["texture"], 0,0,1920,1080
                                                   , uses_map_offset=False)
                render_loop.addSchadowIgnore(i)
                render_loop.lower(i)
                level_store += [i]

            elif e["type"] == "death_area":

                daeth_areas.append((
                    e["x"], e["y"],
                    e["width"], e["height"]

                ))

            elif e["type"] == "light":
                print("addedLight")

                render_loop.addTorch(e["x"], e["y"],100)
            elif e["type"] == "level_finisch":

                finisch_areas.append((
                    e["x"], e["y"],
                    e["width"], e["height"]

                ))
        for e in lowerable:
            render_loop.lower(e)
        return colidebles

    ll = genLevel(level["elements"])

    levelOBJ.objectsUID_to_id=level_store_uid_to_Elementid
    levelOBJ.objects=level_store
    levelOBJ.path=path_uuid


    level_metadata=level["level-metadata"]

    if level_metadata["bg-music"]:
        print("bg_music_defined")
        musicBG_tile,musicBG_author=definebgMusic(level_metadata["bg-music"], )
    backgroundMusic = sound.bg_music
    loopsound(sound.bg_music)
    render_loop.after(200, display_musicInfo)
    #display_musicInfo()




    movable_objects.clear_animation_list()
    render_loop.clear_scedue()
    for path_uuid in level["path-metadata"]:
        path_meta=level["path-metadata"][path_uuid]

        if not path_meta:
            continue
        print("path_meta",path_meta)
        print("path", path_uuid, path_meta["data"])
        if path_meta["type"]=="moveline":

            if "bound_to" in path_meta["data"]:

                path_data=[p for p in level["paths"] if p[1] == path_uuid]

                print("path_data",path_data)
                bound_to=path_meta["data"]["bound_to"]
                print(path_meta)
                if len(path_data)>0:
                    anima=movable_objects.PathFollowAnimation(path_data[0][0],1*path_meta["speed"],True,renderloop=render_loop)
                    print("addet animation")
                    movable_objects.addAnimatedObject(render_loop, level_store_uid_to_Elementid[bound_to], anima)

    for script in scriptsManagers:
        mygame.scripting.objects.objectCol.Objects.uuid_to_id=level_store_uid_to_Elementid
        #script.setLEVconstants(level_store_uid_to_Elementid,level_store)
        scriptsManagers[script].start(levelOBJ)


    render_loop.set_scedue(movable_objects.run_animation)



bg_music_indicator=None

bg_music_info_components={}

def display_musicInfo():
    global backgroundMusic,bg_music_indicator

    rx,ry=80,80
    if backgroundMusic:
        title,author=musicBG_tile[:14]+"..",musicBG_author[:18]+".."

        title_x,title_y=108, SCREEN_HEIGHT  +8
        artist_x,artist_y=118, SCREEN_HEIGHT  + 34

        a = render_loop.addImage("imgs/song_info_bg.png", 40, SCREEN_HEIGHT , 0.5, 0.5, uses_map_offset=False)
        title = render_loop.addText(title, title_x,title_y, font_size=26, )
        artist = render_loop.addText(author,artist_x,artist_y , font_size=22, )
        render_loop.addSchadowIgnore(a)
        render_loop.addSchadowIgnore(artist)
        render_loop.addSchadowIgnore(title)

    circle=0
    direction=-1
    def slide_in_slide_out():
        global bg_music_indicator
        nonlocal direction, circle



        if (circle>=220)&(direction==-1):

            direction=1

        if (circle<80):

            render_loop.moveto(a,40,SCREEN_HEIGHT-circle)
            render_loop.moveto(title, title_x , title_y- circle)
            render_loop.moveto(artist, artist_x , artist_y - circle)

        circle-=direction
        if circle<=-1:
            render_loop.removes([a,title,artist])
            bg_music_indicator=None
            return 3
    bg_music_indicator=[a,title,artist]

    render_loop.set_scedue(slide_in_slide_out)





def move(xp,sprint=False):
    global player_surf, colidebles

    if xp:

        x, y = render_loop.getXY(player)
        w = player_surf.get_width()
        h = player_surf.get_height()

        if sprint:
            ms = 8 * xp
        else:
            ms = 4 * xp
        if x > 0:
            a, b = not check_if_collisions(player_surf, x + ms, y, colidebles), \
                not check_if_collisions(player_surf, x + ms, y, colidebles)
            print(a, b)
            if (a & b):
                render_loop.moveto(player, x + ms, y)
            player_animation.loop("walk",5)
        else:

            a, b = not check_if_collisions(player_surf, x + ms + w, y, colidebles), \
                not check_if_collisions(player_surf, x + ms + w, y, colidebles)
            print(a, b)
            if (a & b):
                render_loop.moveto(player, x + xp, y)


def fall_down(yp):
    x, y = render_loop.getXY(player)
    render_loop.moveto(player, x, y + yp)


fall_acelaration = 5

jumping = False
falling = False
jumpacseleration = 5


def jump_s():
    global jumping, jumpacseleration, falling

    if not jumping:
        return

    jumpacseleration -= 0.1
    x, y = render_loop.getXY(player)
    w = player_surf.get_width()
    h = player_surf.get_height()
    ji = int(jumpacseleration)
    a = check_if_collisions(player_surf, x, y + 2 * ji-10, colidebles)

    if (a):
        print(a)
        print("end-0")
        jumping = False
        falling = True
        return
    render_loop.moveto(player, x, y - 2 * ji)
    if jumpacseleration < 2:
        print("end-1")
        jumping = False
        falling = True
def pushUp():





    x, y = render_loop.getXY(player)


    a = check_if_collisions(player_surf, x, y, colidebles)

    if (a):

        render_loop.moveto(player, x, y -2)


def calculate_map_correction(screen_width, screen_height, margin_x, margin_y, player_x, player_y):
    # Calculate the bounds of the playable area within the screen
    min_x = margin_x
    max_x = screen_width - margin_x
    min_y = margin_y
    max_y = screen_height - margin_y

    # Check if the player is outside the bounds
    correction_x = 0
    correction_y = 0

    if player_x < min_x:
        correction_x = min_x - player_x
    elif player_x > max_x:
        correction_x = max_x - player_x

    if player_y < min_y:
        correction_y = min_y - player_y
    elif player_y > max_y:
        correction_y = max_y - player_y

    return correction_x, -correction_y


def gravity():
    global fall_acelaration, falling
    if jumping:
        print("jumping")
        return

    if fall_acelaration < 8:
        fall_acelaration += 0.2
    x, y = render_loop.getXY(player)
    w = player_surf.get_width()
    h = player_surf.get_height()
    fi = int(fall_acelaration)
    # print(h,w)
    a1 = not check_if_collisions(player_surf, x, y + 2, colidebles)

    a = not check_if_collisions(player_surf, x, y + 2 * fi , colidebles)

    # print("a",a,"b",b)
    if not (a1):
        falling = False
        fall_acelaration = 5
        return
    else:

        falling = True

    if (a):
        fall_down(2 * fi)


    else:

        fall_acelaration /= 2
        print(fall_acelaration)
        print("divide")


#
debug_elements = []


def on_debub_ON(tr):
    global debug_elements

    if tr:
        for i in debug_elements:
            render_loop.removeElement(i)

        debug_infos = [
            f"Player pos-raw {render_loop.getXY(player)}",
            f"World_offset {render_loop.map_ofset_x} : {render_loop.map_ofset_y}",

        ]
        debug_elements.clear()

        for n, text in enumerate(debug_infos):
            debug_elements.append(render_loop.addText(text, 0, 30 * n, 25, (255, 0, 0)))
    else:
        for i in debug_elements:
            render_loop.removeElement(i)


# [(600, 650, 650, 700), (650, 650, 700, 700), (600, 700, 650, 750), (650, 700, 700, 750), (600, 750, 650, 800), (650, 750, 700, 800)] 600 500
def rect_rect_collision(playerrect, x2, y2, width2, height2):
    rect2 = pygame.Rect(x2, y2, width2, height2)
    return playerrect.colliderect(rect2)


finisch_areas = []


def check_finisch_areas(px, py):
    global daeth_areas, tm, tm2, finisch_areas

    ps = player_surf.get_rect()

    ps.topleft = px, py

    for a in finisch_areas:
        if rect_rect_collision(ps, a[0], a[1], a[2], a[3]):
            return True
    return False


def check_death_areas(px, py):
    global daeth_areas, tm, tm2

    ps = player_surf.get_rect()

    ps.topleft = px, py

    for a in daeth_areas:
        if rect_rect_collision(ps, a[0], a[1], a[2], a[3]):
            return True
    return False


# [(600, 650, 650, 700), (650, 650, 700, 700), (600, 700, 650, 750), (650, 700, 700, 750), (600, 750, 650, 800), (650, 750, 700, 800)] 616 742

def death_Menu():
    pauseAll()
    death_titel = render_loop.addText("You died", 310, 100, 80, (255, 30, 30), uses_map_offset=False)

    def replay():
        pauseAll()
        # print("klicked")
        render_loop.hides([play, quit, levsel])
        render_loop.removeElement(death_titel)

        startGame(None)

    def play_select_level():
        pauseAll()
        # print("klicked")
        render_loop.removeElement(death_titel)
        render_loop.hides([play, quit, levsel])
        level_select_screen()

    play = Button(render_loop, 320, 200, width=200, height=50, text="Play Again", click_function=replay, font_size=35)

    levsel = Button(render_loop, 320, 260, width=200, height=50, text="Level Selection",
                    click_function=play_select_level, font_size=35)

    def quit():
        pauseAll()
        render_loop.running = False

    quit = Button(render_loop, 320, 320, width=200, height=50, text="Quit", click_function=quit, font_size=35)


def finisch_Menu():
    death_titel = render_loop.addText("Finished Level", 260, 100, 80, (30, 255, 100), uses_map_offset=False)

    def replay():
        # print("klicked")
        pauseAll()

        render_loop.hides([play, quit, levsel])
        render_loop.removeElement(death_titel)
        startGame(None)

    def select_title_screen():
        # print("klicked")
        pauseAll()
        clearLevel()

        render_loop.removeElement(death_titel)
        render_loop.removes([play, quit, levsel])
        title_screen(render_loop)

    play = Button(render_loop, 320, 200, width=200, height=50, text="Play Again", click_function=replay, font_size=35)

    levsel = Button(render_loop, 320, 260, width=200, height=50, text="Level Selection",
                    click_function=select_title_screen, font_size=35)

    def quit():
        pauseAll()

        render_loop.running = False

    quit = Button(render_loop, 320, 320, width=200, height=50, text="Quit", click_function=quit, font_size=35)

from audio import pauseAll


def clearLevel():
    global level_store, daeth_areas, player, player_surf, jumping, falling, finisch_areas,bg_music_indicator
    render_loop.keypressfunction = None
    for i in level_store:
        render_loop.removeElement(i)

    level_store = []
    daeth_areas = []
    finisch_areas = []
    render_loop.togleSchadows(SCHADOW_STATE.OFF)
    render_loop.no_schadow_elements=[]
    render_loop.removeElement(player)
    player, player_surf = None, None
    jumping = False

    falling = False
    if bg_music_indicator:
        render_loop.removes(bg_music_indicator)
        bg_music_indicator = None

    render_loop.map_ofset_x, render_loop.map_ofset_y = 0, 0

    pauseAll()
def on_death():
    clearLevel()

    playsound(sound.death_sound)
    death_Menu()


def on_finisch():
    global level_store, daeth_areas, player, player_surf, jumping, falling, finisch_areas
    render_loop.keypressfunction = None
    for i in level_store:
        render_loop.removeElement(i)

    level_store = []
    daeth_areas = []
    finisch_areas = []
    render_loop.removeElement(player)
    player, player_surf = None, None
    jumping = False

    falling = False

    render_loop.map_ofset_x, render_loop.map_ofset_y = 0, 0
    finisch_Menu()

in_pause_menu=False
escape_pressing=False

def display_pause_menu():
    render_loop.set_pause_ANY_CUTSENE_DIALOG(True)

    pause_titel = render_loop.addText("Game Paused", 40, 30, 80, (131, 201, 244), uses_map_offset=False)
    render_loop.addSchadowIgnore(pause_titel)
    def replay():
        global in_pause_menu
        # print("klicked")
        pauseAll()

        render_loop.removes([play, quitb, levsel,pause_titel])
        in_pause_menu=False
        clearLevel()
        render_loop.after(100,lambda :startGame(None))


    def play_select_level():
        global in_pause_menu
        in_pause_menu = False
        # print("klicked")
        pauseAll()


        render_loop.removes([play, quitb, levsel,pause_titel])
        clearLevel()
        startGame()
        level_select_screen()

    play = Button(render_loop, 100, 200, width=200, height=50, text="Restart", click_function=replay, font_size=35)

    levsel = Button(render_loop, 100, 260, width=200, height=50, text="Back To Title",
                    click_function=play_select_level, font_size=35)

    def quit():
        pauseAll()

        render_loop.running = False

    quitb = Button(render_loop, 100, 320, width=200, height=50, text="Quit", click_function=quit, font_size=35)
    def pause_end(e):
        render_loop.removes(e)
        render_loop.set_pause_ANY_CUTSENE_DIALOG(False)



        return display_pause_menu
    return lambda p=play,q=quitb,lev=levsel,pt=pause_titel,:pause_end([p,q,lev,pt])
hide_display_pause_function=None


keyConfig={
    "Button-Interact_Main":(pygame.K_q,"Q"),
    "Button-Interact_Second":(pygame.K_e,"E"),
}

last_interact_id=None
last_interact_Kname=""
interactdisplay_store={"text":None,"image":None}
def displayInteractPreview(name,objectid):
    global last_interact_Kname,last_interact_id

    if not objectid:
        if interactdisplay_store["text"]:
            render_loop.removeElement(interactdisplay_store["text"])
            render_loop.removeElement(interactdisplay_store["image"])
            interactdisplay_store["text"]=None
            interactdisplay_store["image"]=None
            last_interact_id=None
            last_interact_Kname=""
        return

    if objectid!=last_interact_id:



        x,y=render_loop.getXY(objectid)


        last_interact_Kname=name
        last_interact_id=objectid
        i=render_loop.addImage("imgs/press_button.png",x+10,y-20,uses_map_offset=True)
        t=render_loop.addText(keyConfig[name][1],x+17,y-16,25,(215, 78, 9),uses_map_offset=True)
        render_loop.addSchadowIgnore(t)
        render_loop.addSchadowIgnore(i)
        interactdisplay_store["image"]=i
        interactdisplay_store["text"]=t




def check_interaction(px,py,pressedKeys):
    global player, player_surf, jumping, falling, escape_pressing, in_pause_menu
    #format (estart,estart,eend,eend ,triger,function,uuid)
    """(e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"], e["nbt"]["interact"], e["nbt"]["interact"]["trigger"],
     e["nbt"]["interact"]["function"], e["uuid"])"""
    def doInteractFunc(func_name):

        file,func=func_name.split(".",1)
        func=func.split(";",1)[0]  #security mesure to prevent script injection
        if file in scriptsManagers:
            scriptsManagers[file].runtime.eval(func)


    if not in_pause_menu:
        is_interactable=None
        for inter in keyPressInteractions.copy():
            e_x_start, e_y_start, e_x_end, e_y_end,type, trigger, function, uuid = inter

            if keyConfig.get(trigger,"NO_KEY")[0] in  pressedKeys:

                if (-INTERACTION_RADIUS+e_x_start<px+25<INTERACTION_RADIUS+e_x_end) and (-INTERACTION_RADIUS+e_y_start<py+25<INTERACTION_RADIUS+e_y_end):
                    print("interacts")
                    if type=="OneTime-Interact":

                        keyPressInteractions.remove(inter)
                    if function:
                        doInteractFunc(function)
            else:
                if (-INTERACTION_RADIUS + e_x_start < px + 25 < INTERACTION_RADIUS + e_x_end) and (
                        -INTERACTION_RADIUS + e_y_start < py + 25 < INTERACTION_RADIUS + e_y_end):
                    is_interactable=(trigger,uuid)


        if is_interactable:
            trigger,uuid=is_interactable
            displayInteractPreview(trigger, level_store_uid_to_Elementid[uuid])
        else:
            displayInteractPreview(None,None)

    pass


def pase_to_engene_pause_func():
    if in_pause_menu:
        render_loop.set_pause_ANY_CUTSENE_DIALOG(True)
        render_loop.pauseMenuFunc = display_pause_menu()
    else:
        render_loop.set_pause_ANY_CUTSENE_DIALOG(False)
        render_loop.pauseMenuFunc=render_loop.pauseMenuFunc()


def handle_keypress(pressed_keys, mouseButtons_pressed,triger_once):
    global player, jumping, jumpacseleration,escape_pressing,in_pause_menu,hide_display_pause_function
    """Function runs on every tick """

    if not player:
        return

    x, y,sprinting = 0, 0,False

    """if pygame.K_w in pressed_keys:
        y-=1"""

    """if pygame.K_s in pressed_keys:
        y+=1"""
    """if (pygame.K_ESCAPE in triger_once):

        in_pause_menu= not in_pause_menu

        if in_pause_menu:
            render_loop.set_pause_ANY_CUTSENE_DIALOG(True)
            hide_display_pause_function=display_pause_menu()
        else:
            render_loop.set_pause_ANY_CUTSENE_DIALOG(False)
            hide_display_pause_function()"""




    if (not in_pause_menu)|(not render_loop.REQUEST_STATUS_IN_NOT_GAME_MODE()):
        if pygame.K_a in pressed_keys:
            x -= 1
        if pygame.K_d in pressed_keys:
            x += 1


        if pygame.K_w in pressed_keys:
            player_animation.play("attack")

        if pygame.K_s in pressed_keys:
            sprinting=True

        if pygame.K_SPACE in pressed_keys:
            if not jumping:
                if falling:
                    print("fall")
                    jumping = False
                else:
                    print("jump")
                    jumpacseleration = 4.4
                    jumping = True
                    playsound(sound.jump_sound)
        pushUp()
        gravity()
        jump_s()
        BOUNCE_AREA_X = SCREEN_WIDTH // 2.4
        BAUCE_AREA_Y = SCREEN_HEIGHT // 3


        move(x,sprinting)
        px, py = render_loop.getXY(player)
        c1, c2 = calculate_map_correction(SCREEN_WIDTH, SCREEN_HEIGHT, BOUNCE_AREA_X,BAUCE_AREA_Y ,px + render_loop.map_ofset_x,
                                          py + render_loop.map_ofset_y)
        # print(render_loop.getXY(player),)
        a1 = check_if_collisions(player_surf, x, y + 6, colidebles)
        if a1:
            move(player,px,py+4 )

        render_loop.mod_map_ofset(-c1, c2)
        # print(check_death_areas(px,py),daeth_areas)


        check_interaction(px,py,pressed_keys)

        if (check_finisch_areas(px, py)):
            print("finisch !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!S")
            on_finisch()
            return

        if (check_death_areas(px, py)):
            print("death")
            on_death()
            return



player, colidebles, player_surf, level_store = None, None, None, None
"""level,s=None,None

b=Button(render_loop,50,50,100,40,"halihalo",onclick())"""
title_screen(render_loop)

render_loop.debug_interface_function = on_debub_ON
render_loop.togleSchadows(SCHADOW_STATE.OFF)
# display_start_screen(render_loop)
render_loop.run(updateHeightWidth)
