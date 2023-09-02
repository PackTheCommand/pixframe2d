import pygame
import math

def draw_percent_circle(screen, center, radius, procent, color, start_angle=0):
    total_value = sum(segment_values)
    angle_per_value = 360 / total_value

    current_angle = start_angle

    i, value = 0,procent
    angle = value * angle_per_value


    # Calculate the points of the pie slice
    points = [center]
    num_points = int(angle) + 2
    for j in range(num_points):
        angle_rad = math.radians(current_angle + (j / (num_points - 1)) * angle)
        x = center[0] + radius * math.cos(angle_rad)
        y = center[1] + radius * math.sin(angle_rad)
        points.append((x, y))


    pygame.draw.polygon(screen, color, points)
    current_angle += angle

    pygame.display.flip()

# Example usage:
pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

segment_values = [10,90]
colors = [(255, 255, 0),(0,0,0)]

draw_percent_circle(screen, (200, 200), 100, segment_values, colors)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()