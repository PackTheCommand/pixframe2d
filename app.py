import json
import math
import threading
import time

import scripting.objects.objectCol
from scripting.objects.level import Level
from audio import sound
import lib_coop.models as multiplayerModels

MULTIPLAYER_CLIENT:multiplayerModels.Client=None

I_AM_HOST=False


DISPLAY_STARTUP_LOGO=True

flags={"multiplayer":False}

def enableFlag(id):
    flags[id]=True

def disableFlag(id):
    flags[id]=False


import random
from tkinter import messagebox

def genuserid():


    return ''.join(random.choices(["1","2","3", "4", "5","6","7","8","9","0","a","b","c","d","e","f"], k=10))


def genEntityId():
    return '#en-'.join(random.choices(["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "a", "b", "c", "d", "e", "f"], k=10))

def moveMultiplayersOutOfWay():
    for player in OtherPlayers:
        render_loop.moveto(OtherPlayers[player][0],-300,-300)
        render_loop.moveto(OtherPlayers[player][2], -300, -300)
player_id_to_name={}
def clientListenData_IN(head,body):
    global KillPositionUpdateFlag
    if head=="sync_update":
        #print("sync_update")

        match body["update-type"]:

            case "join_level":
                resetMulty_players()
                render_loop.hides(blist)
                startGame(body["level-name"])
                pass
            case "leave_level":

                pass
            case "player-pos-update":
                if not player_is_in_deathScreen:
                    pos=body["pos"].split(":")
                    updateMultyPlayerposition(body["player-id"],int(pos[0]),int(pos[1]))

                pass
            case "player-join-world":
                #AddNewPlayerToLevel(body["player-id"],)
                if  body["player-id"]==randomuid:
                    print("I joined the world")
                print("Player joined World",body["player-id"])
                player_id_to_name[body["player-id"]]=body["player-name"]
                pass
            case "ask_player_spawn":
                sendCliendSelfJoinWorld()
            case "back-to-title":
                KillPositionUpdateFlag=True
                resetMulty_players()
                multiplayer_executeBackToTitle()
            case "lua-function-call":
                executeLuaFunctionCall(body["function-name"])
            case "player-animation-start":

                updateMultyPlayerAnimation(body["player-id"],body["animation-name"])
            case "player-animation-loop":
                updateMultyPlayerAnimation(body["player-id"],body["animation-name"],True,body["rep"])
    elif head =="player-action":
        match body["action"]:
            case "attack":
                print("Recived Attack")
                if not player_is_in_deathScreen:
                    checkPlayerRecivesDamage(body["pos"],body["radius"],body["pow"])

        pass


class HealthBar:

    heathBarItems=[]
    HeathBar_items_bg=[]
    last_heath_since_update=0


    @staticmethod
    def addHeathBarItem():
        l=len(HealthBar.heathBarItems)
        item=render_loop.addImage("imgs/health_icon.png",10+40*l,20,uses_map_offset=False,noShadow=True)
        HealthBar.heathBarItems.append(item)

    @staticmethod
    def addDeathHaertBarItem():
        global play
        l=len(HealthBar.heathBarItems)
        item=render_loop.addImage("imgs/death_health_icon.png",10+40*l,20,uses_map_offset=False,noShadow=True)
        HealthBar.HeathBar_items_bg.append(item)
    @staticmethod
    def removeHeathBarItem():
        l=len(HealthBar.heathBarItems)
        item=render_loop.removeElement(HealthBar.heathBarItems.pop(Health))

    @staticmethod
    def removeHeathBarItems():
        render_loop.removes(HealthBar.heathBarItems)
        HealthBar.heathBarItems.clear()
        render_loop.removes(HealthBar.HeathBar_items_bg)
        HealthBar.HeathBar_items_bg.clear()



def playerDealDamage(amount):
    global Health
    Health-=amount
    for i in range(0,amount):
        HealthBar.removeHeathBarItem()
    if Health<=0:
        on_death()

def checkPlayerRecivesDamage(pos, radius, amount):
    playerPos=render_loop.getXY(player)
    if is_point_in_radius(playerPos[0],playerPos[1],pos[0],pos[1],radius):
        print("Player recives damage")
        playerDealDamage(amount)
        return
    print("Nodamage",pos,radius,amount,playerPos)


def is_point_in_radius(x1, y1, x2, y2, radius):
    """
    Check if a point (x1, y1) is within the specified radius around another point (x2, y2).

    Parameters:
    - x1, y1: Coordinates of the point to check.
    - x2, y2: Coordinates of the center point.
    - radius: The radius around the center point.

    Returns:
    - True if the point is within the radius, False otherwise.
    """
    distance = math.sqrt((x1 - x2)**2 + (y1 - y2)**2)
    return distance <= radius

class PARMS:
    """Values of time are given in ticks"""
    attack_cooldown=30
    player_attack_radius_def=100
    player_attack_pow_def=1


class Cooldowns:
    attack_cooldown=PARMS.attack_cooldown

def Scedued_Coldowns():
    global Cooldowns


    if Cooldowns.attack_cooldown>=-1:
        Cooldowns.attack_cooldown-=1

    pass

def ACTION_ATTACK(pos, radius,power):
    global MULTIPLAYER_CLIENT


    if flags["multiplayer"]:
        print("sending attack")



        MULTIPLAYER_CLIENT.send_data("player-action",{"action":"attack","pos":pos,"radius":radius,"pow":power})


    #todo: implement atack Enimy-AI
    pass

def command_send_executeLuaFunctionCall(func_name):
    global MULTIPLAYER_CLIENT

    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"lua-function-call","function-name":func_name})

    pass
def updateMultyPlayerAnimation(player_id,animationName,loop=False,times_if_Loop=0):
    global OtherPlayers
    #todo: implement Animation Execution
    if not loop:
        OtherPlayers[player_id][1].play(animationName)
        return
    OtherPlayers[player_id][1].loop(animationName)

    pass

KillPositionUpdateFlag=False



def sendClientPositionUpdate(x,y):
    global MULTIPLAYER_CLIENT
    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"player-pos-update","pos":f"{x}:{y}","player-id":randomuid})
def sendCliendSelfJoinWorld():
    global MULTIPLAYER_CLIENT

    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"player-join-world","player-id":randomuid,"player-name":"#pn-"+randomuid})

def command_send_backToTitle():
    global MULTIPLAYER_CLIENT

    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"back-to-title"})
    pass
def requestClientsSpawnSignal():
    global MULTIPLAYER_CLIENT

    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"ask_player_spawn"})

def updateMultyPlayerposition(uuid,new_x,new_y):
    if uuid in OtherPlayers.keys():
        #print(OtherPlayers[uuid])
        render_loop.moveto(OtherPlayers[uuid][0],new_x,new_y)
        render_loop.moveto(OtherPlayers[uuid][2],new_x+25,new_y-20)
        #print("updated pos")
        return
    AddNewPlayerToLevel(uuid,"")
    #print("unregistered_player",uuid)

def sendIFMultiplayerAnimation(name):
    global MULTIPLAYER_CLIENT
    if not flags["multiplayer"]:
        return

    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"player-animation-start","player-id":randomuid,"animation-name":name})
def sendIFMultiplayerAnimation_loop(name,times):
    global MULTIPLAYER_CLIENT
    if not flags["multiplayer"]:
        return
    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"player-animation-loop","player-id":randomuid,"animation-name":name,"rep":times})


def Multiplayer_selectLevel(level_name):
    global MULTIPLAYER_CLIENT

    if not I_AM_HOST:
        return False
    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"join_level","level-name":level_name})
    return True

def Multiplayer_syncPosition(playerPosition:(10,10)):
    global MULTIPLAYER_CLIENT


    MULTIPLAYER_CLIENT.send_data("sync_update",{"update-type":"player-pos-update","pos":playerPosition})
    return True

import pygame
randomuid=genuserid()

def display_message():
    tk=messagebox.showinfo("User ID",randomuid)


threading.Thread(target=display_message).start()


INTERACTION_RADIUS=50

with open("leveldata/levels.json") as f:
    all_level_overview_json = json.load(f)

import pygame

from engene import GameRenderLoop, SCHADOW_STATE,ViewPoints
from ui_elements import Button

import movable_objects


backupKeypressfunc=None
def keyOptions():
    global backupKeypressfunc,blist
    blist=[]





    def changekey(uid):
        render_loop.removes(blist)
        key_text=render_loop.addText("Please press a key", SCREEN_WIDTH/2-100, 100, 30, (30, 255, 100), uses_map_offset=False,)
        key_text2 = render_loop.addText("Courant selected: : "+uid, SCREEN_WIDTH / 2 - 180, 140, 30, (30, 255, 100),
                                       uses_map_offset=False )

        def listenkey(key:set,s,x):
            if len(key)==1:
                k=key.pop()

                if k==pygame.K_ESCAPE:
                    render_loop.keypressfunction=backupKeypressfunc
                    render_loop.removes([key_text,key_text2])
                    keyOptions()
                    return
                keyConfig[uid]=(k,pygame.key.name(k))
                with open("keyconfig.json","w") as f:
                    json.dump(keyConfig,f)

                render_loop.keypressfunction=backupKeypressfunc

                render_loop.removes([key_text,key_text2])
                keyOptions()


        backupKeypressfunc=render_loop.keypressfunction
        render_loop.keypressfunction=listenkey

        #print(uid)
    blist.append(render_loop.addText("Key Config", SCREEN_WIDTH/2-50, 10, font_size=40))
    def returnToTitle():
        render_loop.removes(blist)
        title_screen(render_loop)

    blist.append(Button(render_loop,0,0,20,30,"<",click_function=returnToTitle,font_size=36))

    for n,option in enumerate(keyConfig):

        blist.append(Button(render_loop, SCREEN_WIDTH/2-60, 60+34*n, width=200, height=30, text=f"{option } : {keyConfig[option][1]}", click_function=lambda keyuid=option:  changekey(keyuid), font_size=20))
def removeMultiplayer():
    global MULTIPLAYER_CLIENT,I_AM_HOST
    if not flags["multiplayer"]:
        return


    MULTIPLAYER_CLIENT.disconnect()
    MULTIPLAYER_CLIENT=None
    I_AM_HOST=False
    flags["multiplayer"]=False
    render_loop.removes(blist)
    title_screen(render_loop)
    pass

def createGameclient():
    global MULTIPLAYER_CLIENT
    enableFlag("multiplayer")
    c = multiplayerModels.Client(*multiplayerModels.standartdarta,username=randomuid)
    MULTIPLAYER_CLIENT = c
    render_loop.addText("Joining game...", 10, 10, 30, (30, 255, 100),)
    c.receveFunction=clientListenData_IN
    c.connect()
    render_loop.addText("Fatal Error Conection lost ", 10, 10, 30, (255,0,0),)


from effectShaders import destructionIlusion,Screenshake

def ShaderTestMenu():
    global blist
    blist=[]
    shaderlist={"Destruction (Glitch) Shader":destructionIlusion.DestrucktionShader(),"Screen-shake Shader":Screenshake.ScreenshakeShader(),"No Shader":None}
    def changeShader(keyuid):
        if keyuid==None:
            render_loop.disengageShaders()
        else:
            render_loop.engageShader(shaderlist[keyuid])
        render_loop.removes(blist)
        ShowOptions()



    def returnToTitle():
        render_loop.removes(blist)
        title_screen(render_loop)

    blist.append(Button(render_loop, 0, 0, 20, 30, "<", click_function=returnToTitle, font_size=36))

    blist.append(render_loop.addText("Shader Config", SCREEN_WIDTH / 2 - 50, 10, font_size=40))

    for n,otp in enumerate(shaderlist):
        buttonsize=len(otp)*10
        blist.append(Button(render_loop, SCREEN_WIDTH / 2 -buttonsize/2, 60+34*n, width=buttonsize, height=30, text=f"{otp }", click_function=lambda keyuid=otp:  changeShader(keyuid),))


    pass



def ShowOptions():
    global blist
    #blist=[]

    def openKeyOptions():
        render_loop.hides(blist)

        keyOptions()

    def openShaderOptions():
        render_loop.hides(blist)
        ShaderTestMenu()
    def returnToTitle():
        render_loop.hides(blist)
        title_screen(render_loop)

    blist.append(Button(render_loop, 0, 0, 20, 30, "<", click_function=returnToTitle, font_size=36))
    blist.append(Button(render_loop, SCREEN_WIDTH / 2 - 60, 60, width=200, height=30, text="Key Config", click_function=openKeyOptions, font_size=20))
    blist.append(Button(render_loop, SCREEN_WIDTH / 2 - 60, 94, width=200, height=30, text="Shaders",
                        click_function=openShaderOptions, font_size=20))

    pass


def showMultiplayerMenu():
    bs=[]
    def returnToTitle():
        render_loop.removes(bs)
        title_screen(render_loop)


    def host_game():
        def gamehost():
            global I_AM_HOST

            I_AM_HOST = True
            render_loop.addText("Hosting game...", 10, 10, 30, (30, 255, 100),)


            def server():
                try:
                    multiplayerModels.beHost()
                except Exception as e:
                    #print(e)
                    render_loop.addText("Fatal Error Server error ", 10, 10, 30, (255,0,0),)

            threading.Thread(target=server).start()


            threading.Thread(target=createGameclient).start()
            returnToTitle()



        threading.Thread(target=gamehost()).start()

        pass

    def join_game():

        threading.Thread(target=createGameclient).start()
        returnToTitle()


        pass


    bs.append(Button(render_loop, 0, 0, 20, 30, "<", click_function=returnToTitle, font_size=36))

    B=Button(render_loop, SCREEN_WIDTH/2-60, 60, width=200, height=30, text="Host", click_function=host_game, font_size=20)

    bs.append(B)

    B=Button(render_loop, SCREEN_WIDTH/2-60, 120, width=200, height=30, text="Join Game", click_function=join_game,font_size=20)

    bs.append(B)


blist=[]
def title_screen(render_loop):
    global blist
    def clear_content():
        nonlocal render_loop
        render_loop.clearMenu()



    def play_func():
        # print("klicked")
        render_loop.hides(blist)
        level_select_screen()

    def cred():
        # print("klicked")
        render_loop.hides(blist)
        display_Credits()

    xline1 = SCREEN_WIDTH / 2 - 100

    title = render_loop.addText("PixFrame2D", xline1-40, 100, 90, )

    def quit():
        pygame.quit()
        quit()

    def showOptions():
        #print("Hide Options")
        render_loop.hides(blist)
        ShowOptions()

    def showMultiplay():
        render_loop.hides(blist)
        showMultiplayerMenu()



    play=None
    if (not flags["multiplayer"])|(I_AM_HOST):
        play = Button(render_loop, xline1, 200, width=200, height=50, text="Play", click_function=play_func, font_size=35)

    load = Button(render_loop, xline1, 280, width=200, height=50, text="Load", click_function=None, font_size=35)

    quit = Button(render_loop, xline1, 360, width=200, height=50, text="Quit", click_function=quit, font_size=35)

    creadits = Button(render_loop, 0, 0, width=80, height=20, text="Creadits", click_function=cred, font_size=25)

    options= Button(render_loop, SCREEN_WIDTH-80, 0, width=80, height=20, text="Options", click_function=showOptions, font_size=25)


    multiplayer = Button(render_loop, SCREEN_WIDTH - 100, 40, width=100, height=20, text="Multiplayer", click_function=showMultiplay,
                     font_size=25)

    blist=[play,load,quit,title,creadits,options,multiplayer]
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
                #print(event.button)
                if event.button == 4:
                    y += 100
                elif event.button == 5:
                    y -= 100
                if (y >= 0) & (render_loop.map_ofset_y - 100 <= 0):
                    render_loop.map_ofset_y += y
                elif (y < 0):
                    render_loop.map_ofset_y += y
                #(render_loop.map_ofset_y)
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
        Multiplayer_selectLevel(lev_file_path)

        #print("selected", lev_file_path)

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
                #print(event.button)
                if event.button == 4:
                    y += 100
                elif event.button == 5:
                    y -= 100
                if (y >= 0) & (render_loop.map_ofset_y - 100 <= 0):
                    render_loop.map_ofset_y += y
                elif (y < 0):
                    render_loop.map_ofset_y += y
                #print(render_loop.map_ofset_y)
                break

    render_loop.keypressfunction = on_key
    level_select_store = []


    row,colum=0,0
    lev_g_size_x=240

    for n, i in enumerate(all_level_overview_json):

        l=render_loop.addImage("imgs/levelimg.png",x+lev_g_size_x*colum, 150 + 190*row, uses_map_offset=True)
        level_select_store.append(l)
        try:

            level_select_store.append( render_loop.addImage(i["file"]+"preview.png",x+lev_g_size_x*colum+8, 150 + 190*row+8, uses_map_offset=True))
        except Exception as e:

            pass
        t = render_loop.addText(f"{n+1}. "+i["name"], 20+x+lev_g_size_x*colum, 285 + 190*row, 30, uses_map_offset=True)

        colum+=1
        if colum>2:
            colum=0
            row+=1

        render_loop.addClickListener(t, lambda ln=i["file"]: load_levl(ln))
        level_select_store.append(t)

    t = render_loop.addImageFixedWidth("imgs/level_select.png",0,0, render_loop.screen_width ,100, uses_map_offset=False)
    level_select_store.append(t)
    t = render_loop.addText("Select a Level", x - 30, 50, 50, uses_map_offset=False)
    level_select_store.append(t)




SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 1000



def updateHeightWidth(w,h):
    global SCREEN_WIDTH,SCREEN_HEIGHT
    SCREEN_WIDTH, SCREEN_HEIGHT = w,h

render_loop = GameRenderLoop(SCREEN_WIDTH, SCREEN_HEIGHT)


StartupDoneFlag=False
def sratup():
    global StartupDoneFlag
    if DISPLAY_STARTUP_LOGO:
        render_loop.startuplogo()
    StartupDoneFlag=True
threading.Thread(target=sratup()).start()

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



def checkForPlayerColideDamage(px,py):
    try:
        for i in DamageAreas:
            #(i,amount,radius)
            if player:
                posx,posy=render_loop.getXY(i[0])
            checkPlayerRecivesDamage((posx+i[3][0],posy+i[3][1]),i[2],i[1])
    except Exception:
        pass

def resetDamageAreas():
    global DamageAreas
    DamageAreas=[]
    #print("DamageAreas",DamageAreas)
    #print("DamageAreas",DamageAreas)


DamageAreas=[]

def startGame(path_uuid=None):
    global player, player_surf, currant_game_file,backgroundMusic,musicBG_tile,musicBG_author,player_animation,level_store_uid_to_Elementid,levelOBJ,scriptsManagers,player_is_in_deathScreen,Health
    print("Game Started")
    start_t=time.time()
    player_is_in_deathScreen=False
    Health=Max_Health

    render_loop.pauseMenu=pase_to_engene_pause_func
    levelOBJ = Level(render_loop)
    render_loop.level=levelOBJ
    if path_uuid == None:
        path_uuid = currant_game_file
    currant_game_file = path_uuid

    render_loop.togleSchadows(SCHADOW_STATE.ON)


    start_x, start_y = 100, 100

    player,player_animation = render_loop.addAnimatedImage("imgs/animations/player.anime", start_x, start_y, True)
    #print("player", player)

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

                    elif "damage" in e["nbt"]:
                        amount=e["nbt"]["damage"]["amount"]
                        radius=e["nbt"]["damage"]["radius"]
                        ofset_area=e["nbt"]["damage"]["ofset_area"]
                        DamageAreas.append((i,amount,radius,ofset_area))


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
        scripting.objects.objectCol.Objects.uuid_to_id=level_store_uid_to_Elementid
        #script.setLEVconstants(level_store_uid_to_Elementid,level_store)
        scriptsManagers[script].start(levelOBJ)


    render_loop.set_scedue(movable_objects.run_animation)

    #start gamephysics
    render_loop.keypressfunction = handle_keypress
    if flags["multiplayer"]:

        EnablePlayerPositionUpdate()
        if I_AM_HOST:
            requestClientsSpawnSignal()
    for i in range(0,Max_Health):
        HealthBar.addDeathHaertBarItem()
        HealthBar.addHeathBarItem()
    print("load time: ",time.time()-start_t)





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
    global player_surf, colidebles,player_facing_x

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
            sendIFMultiplayerAnimation_loop("walk",5)
        else:

            a, b = not check_if_collisions(player_surf, x + ms + w, y, colidebles), \
                not check_if_collisions(player_surf, x + ms + w, y, colidebles)
            print(a, b)
            if (a & b):
                if x>0:
                    player_facing_x=1
                else:
                    player_facing_x=-1
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
        #print(a)
        #print("end-0")
        jumping = False
        falling = True
        return
    render_loop.moveto(player, x, y - 2 * ji)
    if jumpacseleration < 2:
        #print("end-1")
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
        #print(fall_acelaration)
        #print("divide")


#
debug_elements = []
import os, psutil
process = psutil.Process()

def convert_bytes_to_megabytes_or_kilobytes(byte_size):
    if byte_size >= 10 * 1024 * 1024:  # If at least 10 MB
        result = byte_size / (1024 * 1024)
        unit = "MB"
    elif byte_size >= 10 * 1024:  # If at least 10 KB
        result = byte_size / 1024
        unit = "KB"
    else:
        result = byte_size
        unit = "bytes"
    return f"{result:.2f} {unit}"

def cpu_thread():
    global CPU_usage
    while True:
        CPU_usage = psutil.cpu_percent(interval=1)
        time.sleep(1)
threading.Thread(target=cpu_thread).start()



CPU_usage=0.0


def on_debub_ON(tr):
    global debug_elements

    if tr:
        for i in debug_elements:
            render_loop.removeElement(i)

        debug_infos = [
            f"Player pos-raw: {render_loop.getXY(player)}",
            f"World_offset: {render_loop.map_ofset_x} : {render_loop.map_ofset_y}",
            f"Memory usage: {convert_bytes_to_megabytes_or_kilobytes(process.memory_info().rss)}",
            f"Total Memory : {convert_bytes_to_megabytes_or_kilobytes(process.memory_info().vms)}",
            f"CPU Usage : {CPU_usage}s%",
            f"Active Shaders {render_loop.info_only_engagedShaderName}s%",
            f"Heath : {Health}",
            f"Multiplayer : Active?:{flags['multiplayer']}; host?{I_AM_HOST}",

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

def replay():
    pauseAll()
    # print("klicked")
    render_loop.hides(blist)
    HealthBar.removeHeathBarItems()
    resetDamageAreas()

    startGame(None)

def death_Menu():
    global blist
    blist=[]
    pauseAll()
    death_titel = render_loop.addText("You died", 310, 100, 80, (255, 30, 30), uses_map_offset=False)



    def play_select_level():
        pauseAll()
        # print("klicked")

        render_loop.hides(blist)
        level_select_screen()

    play = Button(render_loop, 320, 200, width=200, height=50, text="Play Again", click_function=replay, font_size=35)

    levsel = Button(render_loop, 320, 260, width=200, height=50, text="Level Selection",
                    click_function=play_select_level, font_size=35)

    def quit():
        pauseAll()
        render_loop.running = False

    quit = Button(render_loop, 320, 320, width=200, height=50, text="Quit", click_function=quit, font_size=35)

    blist=[play, quit, levsel,death_titel]
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
        resetDamageAreas()

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


def resetHeath():
    global Health
    Health =Max_Health
Max_Health=4
Health=Max_Health

def clearLevel():
    global level_store, daeth_areas, player, player_surf, jumping, falling, finisch_areas,bg_music_indicator
    render_loop.keypressfunction = None
    for i in level_store:
        render_loop.removeElement(i)

    level_store = []
    daeth_areas = []
    finisch_areas = []
    render_loop.clearLightning()
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
    global player_is_in_deathScreen
    clearLevel()
    player_is_in_deathScreen = True
    moveMultiplayersOutOfWay()
    playsound(sound.death_sound)

    HealthBar.removeHeathBarItems()
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
backtoTitleFunction_for_currantlevel=None

def multiplayer_executeBackToTitle():#
    global in_pause_menu
    # print("klicked")
    cleanup_all()

    title_screen(render_loop)




def cleanup_all():
    global in_pause_menu
    render_loop.game_is_paused = False
    # print("klicked")
    pauseAll()

    render_loop.removes(blist)
    in_pause_menu = False
    clearLevel()
def display_pause_menu():
    global blist
    blist=[]
    render_loop.set_pause_ANY_CUTSENE_DIALOG(True)

    pause_titel = render_loop.addText("Game Paused", 40, 30, 80, (131, 201, 244), uses_map_offset=False)
    render_loop.addSchadowIgnore(pause_titel)
    def replay():
        cleanup_all()
        render_loop.after(100,lambda :startGame(None))


    def play_select_level():
        global in_pause_menu

        if flags["multiplayer"]:
            command_send_backToTitle()
        HealthBar.removeHeathBarItems()

        cleanup_all()


        title_screen(render_loop)


    play = Button(render_loop, 100, 200, width=200, height=50, text="Restart", click_function=replay, font_size=35)

    levsel=None

    if (not flags["multiplayer"])|(I_AM_HOST):

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
    blist = [play, quitb, levsel, pause_titel]
    return lambda p=play,q=quitb,lev=levsel,pt=pause_titel,:pause_end([p,q,lev,pt])
hide_display_pause_function=None

with open("keyconfig.json","r") as f:
    keyConfig=json.load(f)
"""keyConfig={
    "Button-Interact_Main":(pygame.K_q,"Q"),
    "Button-Interact_Second":(pygame.K_e,"E"),
}"""

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




def executeLuaFunctionCall(func_name):
    file, func = func_name.split(".", 1)
    func = func.split(";", 1)[0]  # security mesure to prevent script injection
    if file in scriptsManagers:
        scriptsManagers[file].runtime.eval(func)
    if flags["multiplayer"]:
        command_send_executeLuaFunctionCall(func_name)

def check_interaction(px,py,pressedKeys):
    global player, player_surf, jumping, falling, escape_pressing, in_pause_menu
    #format (estart,estart,eend,eend ,triger,function,uuid)
    """(e["x"], e["y"], e["x"] + e["width"], e["y"] + e["height"], e["nbt"]["interact"], e["nbt"]["interact"]["trigger"],
     e["nbt"]["interact"]["function"], e["uuid"])"""





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
                        executeLuaFunctionCall(function)
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
    global in_pause_menu

    in_pause_menu = not in_pause_menu
    if in_pause_menu:
        render_loop.game_is_paused = True
        render_loop.set_pause_ANY_CUTSENE_DIALOG(True)
        render_loop.pauseMenuFunc = display_pause_menu()
    else:
        render_loop.set_pause_ANY_CUTSENE_DIALOG(False)
        render_loop.game_is_paused = False

        render_loop.pauseMenuFunc=render_loop.pauseMenuFunc()


def getKeyHandle(keyid):
    if keyid in keyConfig:
        return keyConfig[keyid][0]
    return 0



def resetMulty_players():
    global OtherPlayers,players_to_add
    for id in OtherPlayers:

        render_loop.removeElement(OtherPlayers[id][0])

    OtherPlayers = {}

    players_to_add = []

OtherPlayers= {}

players_to_add=[]

def AddNewPlayerToLevel(uid,model="model",playerName="???"):
    global players_to_add
    players_to_add+=[(uid,model,playerName)]


def playerPosUpdateThread():
    global player,KillPositionUpdateFlag
    while not KillPositionUpdateFlag:
        try:

            if player:
                px,py=render_loop.getXY(player)
                if flags.get("multiplayer", False):
                    #print(px,py)
                    sendClientPositionUpdate(px, py)
        except Exception as e:
            print("Data send Error")
        time.sleep(0.020)


    KillPositionUpdateFlag=False

def EnablePlayerPositionUpdate():

    threading.Thread(target=playerPosUpdateThread).start()
player_facing_x=1
player_is_in_deathScreen=False
def handle_keypress(pressed_keys, mouseButtons_pressed,triger_once):
    global player, jumping, jumpacseleration,escape_pressing,in_pause_menu,hide_display_pause_function,OtherPlayers,players_to_add
    """Function runs on every tick """

    if not player:
        return
    if len(players_to_add)>0:
        if not player_is_in_deathScreen:
            other_player_uid,m,name=players_to_add.pop(0)

            OtherPlayers[other_player_uid] = (*render_loop.addAnimatedImage("imgs/animations/player.anime", -10000,-10000, True),render_loop.addText(player_id_to_name.get(other_player_uid,"@"+other_player_uid), -10000, -10000, 20, (255, 255, 255), True))


    Scedued_Coldowns()
    px, py = render_loop.getXY(player)
    checkForPlayerColideDamage(px,py)
    if player_is_in_deathScreen:
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


        if getKeyHandle("gc-attac-primary") in pressed_keys:

            if Cooldowns.attack_cooldown<=0:
                print("attacking")
                player_animation.play("attack")
                sendIFMultiplayerAnimation("attack")
                Cooldowns.attack_cooldown=PARMS.attack_cooldown
                if player_facing_x<0:

                    ACTION_ATTACK((px-25,py),PARMS.player_attack_radius_def,PARMS.player_attack_pow_def)
                else:
                    ACTION_ATTACK((px+50,py),PARMS.player_attack_radius_def,PARMS.player_attack_pow_def)
            else:
                print("Attac cooldown active")

        if getKeyHandle("Button-Sprint") in pressed_keys:
            sprinting=True

        if getKeyHandle("gc-control-jump") in pressed_keys:
            if not jumping:
                if falling:
                    #print("fall")
                    jumping = False
                else:
                    #print("jump")
                    jumpacseleration = 4.4
                    jumping = True
                    playsound(sound.jump_sound)
        pushUp()


        if render_loop.viewpoint==ViewPoints.sideview:
            if not render_loop.game_is_paused:
                gravity()
                jump_s()
        BOUNCE_AREA_X = SCREEN_WIDTH // 2.4
        BAUCE_AREA_Y = SCREEN_HEIGHT // 3

        if not render_loop.game_is_paused:
            move(x,sprinting)
        px, py = render_loop.getXY(player)






        c1, c2 = calculate_map_correction(SCREEN_WIDTH, SCREEN_HEIGHT, BOUNCE_AREA_X,BAUCE_AREA_Y ,px + render_loop.map_ofset_x,
                                          py + render_loop.map_ofset_y)
        # print(render_loop.getXY(player),)
        a1 = check_if_collisions(player_surf, x, y + 6, colidebles)
        if a1:
            if not render_loop.game_is_paused:
                move(player,px,py+4 )

        if not render_loop.game_is_paused:
            render_loop.mod_map_ofset(-c1, c2)
        # print(check_death_areas(px,py),daeth_areas)

        if not render_loop.game_is_paused:
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

pygame.display.set_caption(randomuid)

""" build procedure """


render_loop.addText("Dev Version ",10,70,30,(255,0,0))

while not StartupDoneFlag:
    time.sleep(0.1)

render_loop.run(updateHeightWidth)