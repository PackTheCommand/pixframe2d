import time



import tkinter as tk

import tkinter as tk

class PathfindingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Pathfinding Example")

        self.canvas = tk.Canvas(root, width=400, height=400, bg="white")
        self.canvas.pack()

        self.pathstore = []
        self.points = []
        self.current_path = []

        self.pathfinding_mode = False
        self.toggle_button = tk.Button(root, text="Toggle Pathfinding Mode", command=self.toggle_mode)
        self.toggle_button.pack()

        self.toggle_visibility_button = tk.Button(root, text="Toggle Visibility", command=self.toggle_visibility)
        self.toggle_visibility_button.pack()

        self.canvas.bind("<Button-1>", self.canvas_click)
        self.root.bind("<Return>", self.end_path)
        def pr(e):
            print(self.pathstore)

        self.root.bind("<e>",pr)

    def toggle_mode(self):
        self.pathfinding_mode = not self.pathfinding_mode
        if self.pathfinding_mode:
            self.toggle_button.config(text="Exit Pathfinding Mode")
            self.current_path = []
        else:
            self.toggle_button.config(text="Toggle Pathfinding Mode")
            if self.current_path:
                self.pathstore.append(self.current_path)
                self.current_path = []
            self.draw_paths()

    def canvas_click(self, event):
        if self.pathfinding_mode:
            x, y = event.x, event.y
            self.points.append((x, y))
            self.current_path.append((x, y))
            self.canvas.create_oval(x - 3, y - 3, x + 3, y + 3, fill="red", tags=["paths","temp_paths"])
            if len(self.current_path) > 1:
                self.canvas.create_line(self.current_path[-2], self.current_path[-1], fill="blue", tags=["paths","temp_paths"])

    def end_path(self, event):
        if self.pathfinding_mode and len(self.current_path) > 1:
            self.pathstore.append(self.current_path)
            self.current_path = []
            self.draw_paths()

    def draw_paths(self):
        self.canvas.delete("temp_paths")
        for path in self.pathstore:
            for i in range(len(path) - 1):
                self.canvas.create_line(path[i], path[i + 1], fill="green", tags=["paths","o"],)
                self.canvas.create_oval(path[i][0] - 3, path[i][1] - 3, path[i][0] + 3, path[i][1] + 3, fill="green", tags=["paths"])
            self.canvas.create_oval(path[-1][0] - 3, path[-1][1] - 3, path[-1][0] + 3, path[-1][1] + 3, fill="red", tags=["paths"])

    def toggle_visibility(self):
        current_visibility = self.canvas.itemcget("paths", "state")
        new_visibility = "normal" if current_visibility == "hidden" else "hidden"
        #self.canvas.tag_raise("paths")
        self.canvas.itemconfigure("paths", state=new_visibility)


if __name__ == "__main__":
    root = tk.Tk()
    app = PathfindingApp(root)
    root.mainloop()



exit()
import tkinter as tk



def on_configure(event):
    # Update the scroll region when the canvas size changes
    canvas.configure(scrollregion=canvas.bbox("all"))

root = tk.Tk()
root.title("Scrollable Frame Example")

# Create a canvas widget to hold the scrollable content
canvas = tk.Canvas(root)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar and link it to the canvas
scrollbar = tk.Scrollbar(root, command=canvas.yview)
scrollbar.pack(side=tk.LEFT, fill=tk.Y)
canvas.configure(yscrollcommand=scrollbar.set)

# Create a frame inside the canvas for the scrollable content
inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Configure the canvas to adjust scroll region when resized
inner_frame.bind("<Configure>", on_configure)

# Place some widgets inside the inner frame
for i in range(20):
    label = tk.Label(inner_frame, text=f"Label {i}")
    label.pack(padx=10, pady=5)

root.mainloop()
















exit()
import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Set up display
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Shadow Polygons with Raycasting")

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SHADOW_COLOR = (0, 0, 0, 150)
import vector_shading
# Function to calculate distance between two points
def distance(point1, point2):
    return math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)

# Function to cast rays from the light source and determine shadow polygons
def raycasting_shadow_polygons(surface, light_source, obstacles):


    for ray_angle in range(0, 360, 10):



        ray_directiona,ray_directionb = pygame.math.Vector2(math.cos(math.radians(ray_angle)), math.sin(math.radians(ray_angle)))

        la,lb=light_source

        ray_direction=(int(ray_directiona*1000),int(ray_directionb*1000))

        #pygame.draw.line(surface,(255,0,0),light_source,ray_direction)
        v1=vector_shading.collision_detection(ray_direction, obstacles[0],light_source)
        if v1:
            print(v1)




        """intersections = []"""

        """for obstacle in obstacles:
            if len(obstacle) >= 3:
                obstacle_points = []
                for x, y in obstacle:
                    to_point = pygame.math.Vector2(x - light_source[0], y - light_source[1])
                    angle_diff = ray_direction.angle_to(to_point)

                    if abs(angle_diff) < 45:
                        obstacle_points.append((x, y))

                if len(obstacle_points) >= 3:
                    intersections.extend(obstacle_points)

        if intersections:
            intersections.sort(key=lambda point: distance(light_source, point))
            pygame.draw.polygon(surface, SHADOW_COLOR, intersections)"""

# Main function
def main():
    obstacles = [
        [(300, 200), (500, 200), (500, 400), (300, 400)],  # Example obstacle
    ]
    light_source = (200, 300)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False


        raycasting_shadow_polygons(screen, light_source, obstacles)
        pygame.draw.circle(screen,(50,50,255),light_source,6)
        pygame.draw.polygon(screen, (50, 50, 255), obstacles[0])

        pygame.display.flip()
        screen.fill(WHITE)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()