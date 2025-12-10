from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLU import *     # Utility library (gluOrtho2D)
from OpenGL.GLUT import *    # GLUT functions (window creation, main loop)
import math
from algorithm import *

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glPointSize(4.0)
    glColor3f(1.0, 0.0, 0.0)  
    
    HCircle_Right(300, 700, 600)

    glutSwapBuffers()
    
    
