import pygame
import random

# Initialize Pygame
pygame.init()

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fireworks Particle Effect")

# Colors
WHITE = (255, 255, 255)
COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255)]


class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.size = random.randint(2, 6)
        self.speed_x = random.uniform(-1, 1)
        self.speed_y = random.uniform(-1, -3)

    def update(self):
        self.speed_y += 0.1
        self.x += self.speed_x
        self.y += self.speed_y

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)


particles = []

# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if pygame.mouse.get_pressed()[0]:
        particles.append(Particle(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], random.choice(COLORS)))

    screen.fill(WHITE)

    for particle in particles:
        particle.update()
        particle.draw()

    particles = [particle for particle in particles if particle.y < screen_height]

    pygame.display.flip()
    pygame.time.delay(10)

pygame.quit()
