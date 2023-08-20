import os
import tkinter.messagebox

import pygame
from mutagen import File as mutangenFile

pygame.init()

def addSound(name):
    if name.startswith("/sounds"):
        return pygame.mixer.Sound( name[1:])

    return pygame.mixer.Sound("sounds/"+name)


def extract_metadata(audio_file_path):
    p = os.getcwd().replace("\\", "/")
    if not audio_file_path.startswith(p):
        audio_file_path = p + audio_file_path
    audio = mutangenFile(audio_file_path, easy=True)

    if audio:
        title = audio.get("title", "Unknown Title")
        artist = audio.get("artist", "Unknown Artist")
        album = audio.get("album", "Unknown Album")

        print("dsaöükldfkpsoa",title,title[0]=="")
        if title[0]=="":
            title[0]="Unknown Title"
        if artist[0]=="":
            artist[0]="Unknown Artist"



        return {
            "title": title[0],
            "artist": artist[0],
            "album": album[0]
        }
    else:
        return None


def definebgMusic(path:str):
    global bgMusicName,bgMusic_by




    meta=extract_metadata(path)

    name,by="",""
    if meta is not None:
        name=meta["title"]
        print("red")
        by=meta["artist"]

    bgMusicName[0]=name
    bgMusic_by[0]=by
    print("dsadsadsaDSADSADSA",bgMusicName[0],bgMusic_by[0])
    sound.bg_music.stop()
    sound.bg_music=addSound(path)
    sound.bg_music.set_volume(0.09)
    return name,by


bgMusicName=[""]
bgMusic_by=[""]


def getMusic_Info():

    return bgMusicName[0],bgMusic_by[0]

def pauseAll():
    sound.jump_sound.fadeout(1)
    sound.jump_sound.stop()
    sound.bg_music.stop()


    sound.music_communicate.fadeout(1)
    sound.music_communicate.stop()
    sound.death_sound.fadeout(1)
    sound.death_sound.stop()




class sound:
    jump_sound=addSound("jump.mp3")
    jump_sound.set_volume(0.09)

    death_sound = addSound("death.mp3")
    death_sound.set_volume(0.2)


    music_communicate=addSound("communicate_soundtrack.ogg")
    music_communicate.set_volume(0.09)

    bg_music=addSound("communicate_soundtrack.ogg")



