import numpy as np
from OpenGL.GL import *

import barrier

class Wave:
    def __init__(self, position, velocity, life):
        self.position = position
        self.velocity = velocity
        self.speed = np.linalg.norm(velocity)
        self.existance_time = 0
        self.life = life
        self.makeNewWave = 0

    def propogate(self, dt, lastCollision = None):
        newPosition = self.position + self.velocity * dt
        
        collision = barrier.barrierManager.collide(self.position, newPosition, lastCollision)
        if not collision is None:
            (((x, y), normal), bar) = collision
            intersect = np.array([x, y])
            time = np.linalg.norm(self.position-intersect) / self.speed
            change = - 2 * normal * np.dot(self.velocity, normal)
            self.velocity = self.velocity + change
            self.position = intersect
            self.propogate(dt - time, lastCollision = bar)
        else:
            self.position = newPosition

        self.makeNewWave += dt
        #if self.makeNewWave > 10:
        #	makeWaveFront(self.position, self.velocity, self.life-self.existance_time)
        # 	self.makeNewWave = 0
        self.existance_time += dt

    def destroyed(self):
    	return self.existance_time > self.life

    def draw(self):
    	c = float((self.existance_time)/self.life)
    	glColor3f(c, c, c)
    	
    	glVertex2f(self.position[0], self.position[1])
    	

class WaveManager:
    def __init__(self):
        self.waves = set()
        self.newWaves = set()

    def propogate(self, dt):
        if len(self.newWaves) > 0:
            self.waves = self.waves.union(self.newWaves)
            self.newWaves = set()
        for w in self.waves:
            w.propogate(dt)

        print 'Number of Particles: ', len(self.waves)

    def draw(self):
        glBegin(GL_POINTS)
        for w in list(self.waves):
            w.draw()
            if w.destroyed():
                self.waves.remove(w)
        glEnd()

    def makeWave(self, p, v, life):
        self.newWaves.add(Wave(p, v, life))


def makeWaveFront(position, velocity, life, number = 6.0):
	number = float(number)
	speed = np.linalg.norm(velocity)
	angle = np.arctan2(velocity[1], velocity[0])
	for i in range(int(number)):
		this_angle = angle + (i-number/2.0)/number*np.pi
		waveManager.makeWave(np.array(position), 
                             np.array([speed*np.cos(this_angle),
                                       speed*np.sin(this_angle)]),
                             life)


def makeWaves(position = [0.0, 0.0], number = 120.0, speed = 100.0):
    number = float(number)
    for i in range(int(number)):
    	this_angle = i/number*2*np.pi
        waveManager.makeWave(np.array(position), 
                             np.array([speed*np.cos(this_angle),
                                       speed*np.sin(this_angle)]),
                             3.0)

waveManager = WaveManager()
        
