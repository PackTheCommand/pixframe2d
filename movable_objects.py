class PathFollowAnimation:
    def __init__(self, points, step_width, loop=False):
        self.points = points
        self.step_width = step_width
        self.loop = loop
        self.current_index = 0
        self.current_position = self.points[0]
        self.target_position = self.points[1]
        self.forward = True  # Indicates if animation is moving forward or backward

    def move(self):
        if self.current_index >= len(self.points) - 1:
            if self.loop:
                self.current_index = 0 if self.forward else len(self.points) - 1
                self.target_position = self.points[1] if self.forward else self.points[-2]
                self.forward = not self.forward
            else:
                return None  # Animation finished

        direction = (
            self.target_position[0] - self.current_position[0],
            self.target_position[1] - self.current_position[1]
        )

        magnitude = (direction[0] ** 2 + direction[1] ** 2) ** 0.5

        if magnitude <= self.step_width:
            self.current_index += 1
            self.current_position = self.target_position
            if self.current_index < len(self.points) - 1:
                self.target_position = self.points[self.current_index + 1]
        else:
            direction = (direction[0] / magnitude, direction[1] / magnitude)
            self.current_position = (
                self.current_position[0] + direction[0] * self.step_width,
                self.current_position[1] + direction[1] * self.step_width
            )

        return self.current_position

class Animated_block:
    def __init__(self,renderloop,elementid,Animation:PathFollowAnimation):

        self.x,self.y=renderloop.getXY(elementid)
        self.renderloop=renderloop
        self.elementid = elementid
        self.Animation=Animation

    def move(self):
        mx,my=self.Animation.move()
        print(mx,my)


        self.renderloop.moveto(self.elementid,mx,my)



def run_animation():
    #print("r",animated_blocks)

    for block in animated_blocks:

        block.move()

animated_blocks=[]

def clear_animation_list():
    global animated_blocks
    animated_blocks=[]



def addAnimatedObject(renderloop,elementid,Animation:PathFollowAnimation):
    global animated_blocks
    animated_blocks+=[Animated_block(renderloop,elementid,Animation)]





