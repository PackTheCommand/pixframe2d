import pygame
import sys
import math

pygame.init()

# Set up display
width, height = 800, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Gradient Circle")

# Colors
background_color = (10,10,10)

# Circle parameters
center = (width // 2, height // 2)
max_radius = 200
num_circles = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Clear the screen
    screen.fill(background_color)
    s=pygame.Surface((width,height))
    # Draw gradient circles
    for i in range(num_circles):
        radius = int(max_radius * i / num_circles)
        alpha = int(255 * (1 - i / num_circles))
        circle_color = (alpha, alpha, alpha,255)
        pygame.draw.circle(s, circle_color, center, radius)
    screen.blit(s, (0, 0),special_flags=pygame.BLEND_RGBA_MULT)
    pygame.display.flip()

pygame.quit()
sys.exit()
