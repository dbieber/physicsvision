from OpenGL.GL import *
import numpy as np
import scene

class Barrier:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.normal = p2 - p1
        self.normal = self.normal/np.linalg.norm(self.normal)
        self.normal = np.array([-self.normal[1], self.normal[0]])

    def draw(self):
        glColor3f(0, 0, 0)
        glBegin(GL_LINES)
        glVertex2f(self.p1[0], self.p1[1])
        glVertex2f(self.p2[0], self.p2[1])
        glEnd()

    def collide(self, p1, p2):
        intersection = lineIntersection(p1, p2, self.p1, self.p2)
        if intersection is None:
            return None
        else:
            return intersection, self.normal

class BarrierManager:
    def __init__(self):
        self.barriers = set()
        self.gridRow = 20
        self.gridCol = 20
        self.makeGrid()

    def getGridCoord(self, p):
        (x, y) = scene.convertToWindowCoords(p)
        x = int(x*self.gridCol)
        y = int(y*self.gridRow)
        return (x, y)

    def makeGrid(self):
        self.grid = []
        for i in range(self.gridRow):
            self.grid.append([])
            for j in range(self.gridCol):
                self.grid[i].append([])

        for b in self.barriers:
            print b.p1, b.p2
            (x1, y1) = self.getGridCoord(b.p1)
            (x2, y2) = self.getGridCoord(b.p2)

            minx = min(x1, x2)
            miny = min(y1, y2)
            maxx = max(x1, x2)
            maxy = max(y1, y2)

            for i in range(miny, maxy+1):
                for j in range(minx, maxx+1):
                    self.grid[i][j].append(b)

        

    def collide(self, p1, p2, ignoreBarrier = None):
        bars = set()

        (x1, y1) = self.getGridCoord(p1)
        (x2, y2) = self.getGridCoord(p2)

        minx = min(x1, x2)
        miny = min(y1, y2)
        maxx = max(x1, x2)
        maxy = max(y1, y2)

        
        for i in range(max(0, miny), min(maxy+1, len(self.grid))):
            for j in range(max(0, minx), min(maxx+1, len(self.grid[0]))):
                for b in self.grid[i][j]:
                    bars.add(b)

        for b in bars:
            if not ignoreBarrier is None:
                if b == ignoreBarrier:
                    continue
            intersection = b.collide(p1, p2)
            if not intersection is None:
                return (intersection, b)

        return None

    def draw(self):
        for b in self.barriers:
            b.draw()

    def makeBarrier(self, p1, p2):
        self.barriers.add(Barrier(p1, p2))
        self.makeGrid()

barrierManager = BarrierManager()

def lineIntersection(p1, p2, p3, p4):
    if (max(p1[0], p2[0]) < min(p3[0], p4[0]) or 
        min(p1[0], p2[0]) > max(p3[0], p4[0])):
        return None

    dx = p1[0]-p2[0]
    if (dx == 0):
        m1 = None
    else:
        m1 = (p1[1]-p2[1])/dx

    dx = p3[0]-p4[0]
    if (dx == 0):
        m2 = None
    else:
        m2 = (p3[1]-p4[1])/dx

    if m1 == m2:
        return None

    if m1 == None:
        b2 = p3[1]-m2*p3[0]
        x = p1[0]
        y = m2*p1[0]+b2
        if x > min(p3[0],p4[0]) and x < max(p3[0], p4[0]) and y > min(p1[1], p2[1]) and y < max(p1[1], p2[1]):
            return (x,y)
        else:
            return None
    elif m2 == None:
        b1 = p1[1]-m1*p1[0]
        x = p3[0]
        y = m1*p3[0]+b1
        if x > min(p1[0],p2[0]) and x < max(p1[0], p2[0]) and y > min(p3[1], p4[1]) and y < max(p3[1], p4[1]):
            return (x,y)
        else:
            return None
    else:
        b1 = p1[1]-m1*p1[0]
        b2 = p3[1]-m2*p3[0]
        x = (b2-b1)/(m1-m2)
        y = m1*x+b1

    if (x < max(min(p1[0], p2[0]), min(p3[0],p4[0]))) or (x > min(max(p1[0], p2[0]), max(p3[0], p4[0]))):
        return None
    else:
        return (x,y)
