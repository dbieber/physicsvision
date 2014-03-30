from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import random
import wave
import barrier
import numpy as np
import time



def initFun():
    glClearColor(1.0,1.0,1.0,0.0)
    glColor3f(0.0,0.0, 0.0)
    glPointSize(1.0)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-320.0,320.0,-240.0,240.0)


def displayFun():
    global global_time
    global new_wave

    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(3)

    new_time = time.time()
    dt = (new_time - global_time)
    
    global_time = new_time

    new_wave += dt
    if new_wave > .8:
        new_wave = 0
        wave.makeWaves([0.0, 0.0])
        #wave.makeWaves([-75.0, 0.0])

    wave.waveManager.propogate(dt)
    wave.waveManager.draw()

    barrier.barrierManager.draw()


    print 'fps', 1/dt
    glPointSize(1)
    glutSwapBuffers()

def keyPressedFun(*args):
    global window

    ESCAPE = '\033'
    if args[0] == ESCAPE:
        glutDestroyWindow(window)
        sys.exit()

def keyReleasedFun(*args):
    return


if __name__ == '__main__':
    global window
    global global_time
    global new_wave
    new_wave = 0

    glutInit()
    glutInitWindowSize(640,480)
    window = glutCreateWindow("Physics")
    glutInitDisplayMode(GLUT_SINGLE | GLUT_RGB)
    glutDisplayFunc(displayFun)
    glutIdleFunc(displayFun)
    glutKeyboardFunc (keyPressedFun)
    glutKeyboardUpFunc (keyReleasedFun)

    
    wave.makeWaves()
    
    #barrier.barrierManager.makeBarrier(np.array([100, -100]), np.array([100, 100]))
    barrier.barrierManager.makeBarrier(np.array([-100, -100]), np.array([100, -100]))
    barrier.barrierManager.makeBarrier(np.array([-100, 100]), np.array([-100, -100]))
    barrier.barrierManager.makeBarrier(np.array([100, 100]), np.array([-100, 100]))
    """
    barrier.barrierManager.makeBarrier(np.array([50, -50]), np.array([50, 50]))
    barrier.barrierManager.makeBarrier(np.array([-50, -50]), np.array([50, -50]))
    barrier.barrierManager.makeBarrier(np.array([-50, 50]), np.array([-50, -50]))
    barrier.barrierManager.makeBarrier(np.array([50, 50]), np.array([-50, 50]))
    """

    initFun()
    global_time = time.time()
    glutMainLoop()
