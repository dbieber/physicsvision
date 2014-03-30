import pygame
from pygame.locals import *
from pygame.color import *
import pymunk
from pymunk import Vec2d


class SimulationDemo:
    def __init__(self):
        self.running = True
        self.drawing = True
        self.w, self.h = 1000,700
        self.screen = pygame.display.set_mode((self.w, self.h))
        self.clock = pygame.time.Clock()

        b = 5 # border

        ### Init pymunk and create space
        self.space = pymunk.Space()
        self.space.gravity = (0.0, 900)
        ### ground
        body = pymunk.Body()
        shape = pymunk.Segment(body, (b, self.h-b), (self.w-b,self.h-b), .0)
        shape.friction = 1.0
        self.space.add(shape)

        body = pymunk.Body()
        shape = pymunk.Segment(body, (b, b), (b,self.h-b), .0)
        shape.friction = 1.0
        self.space.add(shape)

        body = pymunk.Body()
        shape = pymunk.Segment(body, (self.w-b, self.h-b), (self.w-b,b), .0)
        shape.friction = 1.0
        self.space.add(shape)

    def add_contour(self, contour):
        mass = 1

        minx = min(x[0] for x in contour), "minx"
        miny = min(x[1] for x in contour), "miny"
        maxx = max(x[0] for x in contour)
        maxy = max(x[1] for x in contour)

        if minx < 5 or miny < 5:
            return

        if len(contour) <= 2:
            return

        area = pymunk.util.calc_area(contour)
        if area < 0:
            contour = contour[::-1]
            area = -area

        if area <= 10:
            return

        mass = float(area) / 1000.0
        mass = 10

        if mass <= .1:
            return

        position = pymunk.util.calc_center(contour)

        contour = pymunk.util.poly_vectors_around_center(contour)

        moment = pymunk.moment_for_poly(mass, contour)

        if moment <= 100:
            return

        body = pymunk.Body(mass, moment)
        body.position = position

        shape = pymunk.Poly(body, contour)
        shape.friction = .5
        shape.elasticity = 0.85
        shape.collision_type = 1
        self.space.add(body)
        self.space.add(shape)

    def run(self):
        while self.running:
            self.loop()

    def loop(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_p:
                pygame.image.save(self.screen, "simulation.png")
            elif event.type == KEYDOWN and event.key == K_d:
                self.drawing = not self.drawing

        steps = 3
        dt = 1.0/120.0/steps
        for x in range(steps):
            self.space.step(dt)
        if self.drawing:
            self.draw()

        ### Tick clock and update fps in title
        self.clock.tick(30)
        pygame.display.set_caption("fps: " + str(self.clock.get_fps()))

    def draw(self):
        ### Clear the screen
        self.screen.fill(THECOLORS["white"])

        for shape in self.space.shapes:
            if shape.body.is_static:
                body = shape.body
                pv1 = body.position + shape.a.cpvrotate(body.rotation_vector)
                pv2 = body.position + shape.b.cpvrotate(body.rotation_vector)
                pygame.draw.lines(self.screen, THECOLORS["lightgray"], False, [pv1,pv2])
            else:
                if shape.body.is_sleeping:
                    continue
                ps = shape.get_vertices()
                ps.append(ps[0])
                pygame.draw.polygon(self.screen, THECOLORS["lightgray"], ps)
                pygame.draw.polygon(self.screen, THECOLORS["darkgrey"], ps, 1)

        ### All done, lets flip the display
        pygame.display.flip()

def main():
    demo = SimulationDemo()
    demo.run()

if __name__ == '__main__':
    main()
