import pygame

pygame.init()

def addSound(name):
    return pygame.mixer.Sound("sounds/"+name)


def pauseAll():
    sound.jump_sound.fadeout(1)
    sound.jump_sound.stop()
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



