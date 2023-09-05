import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
GLASS_COLOR = (135, 206, 235)  # Light Blue

# Initialize Pygame window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Glass Break Effect")

clock = pygame.time.Clock()
running = True

# Create a list to store glass pieces

glass_pieces = []

vars=[i for i in range(10,40)]
def create_glass_piece(x, y, size):
    """Create a glass piece as a Rect object."""
    l=random.choices(vars,k=3)


    return (pygame.Rect(x, y, size, size),(l[0],l[1],l[2]))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Create a glass piece at a random position and size
    s=pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
    x = random.randint(0, SCREEN_WIDTH)
    y = random.randint(0, SCREEN_HEIGHT)
    size = random.randint(20, 40)
    glass_piece = create_glass_piece(x, y, size)
    glass_pieces.append(glass_piece)

    screen.fill(GLASS_COLOR)

    # Draw and animate glass pieces
    for piece in glass_pieces:

        pygame.draw.rect(s, piece[1], piece[0],border_radius=size)  # White color for glass pieces
        piece[0].x += random.randint(-1, 1)  # Move glass pieces randomly
        piece[0].y += random.randint(-1, 1)

    screen.blit(s, (0, 0),special_flags=pygame.BLEND_ADD)

    pygame.display.flip()
    clock.tick(30)  # Adjust the frame rate as needed
    if len(glass_pieces) > 100:
        glass_pieces.pop(0)

pygame.quit()