import random

import pygame
glass_pieces = []

vars=[i for i in range(10,40)]
def create_glass_piece(x, y, size):
    """Create a glass piece as a Rect object."""
    l=random.choices(vars,k=3)


    return (pygame.Rect(x, y, size, size),(l[0],l[1],l[2]))
tick=0
def screen_bubbeling(screen:pygame.display):
    global tick


    SCREEN_WIDTH, SCREEN_HEIGHT = screen.get_size()

    glass_pieces = []
    s=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    if tick ==10:
        tick=0
        x = random.randint(0, SCREEN_WIDTH)
        y = random.randint(0, SCREEN_HEIGHT)
        size = random.randint(20, 40)
        glass_piece = create_glass_piece(x, y, size)
        glass_pieces.append(glass_piece)
    tick+=1


    # Draw and animate glass pieces
    for piece in glass_pieces:
        size = random.randint(20, 40)

        pygame.draw.rect(s, piece[1], piece[0],border_radius=size)  # White color for glass pieces
        if tick % 60 == 0:
            piece[0].x += random.randint(-1, 1)  # Move glass pieces randomly
            piece[0].y += random.randint(-1, 1)

    screen.blit(s, (0, 0),)


    if len(glass_pieces) > 200:
        glass_pieces.pop(0)