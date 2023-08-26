



class Particle:
    def __init__(self,renderloop,at_object_id):
        self.element = at_object_id

    def tick(self):
        pass

    def update(self):
        x,y=self.renderloop.get_XY(self.element)
        self.tick(x,y)


    def stop(self):
        pass