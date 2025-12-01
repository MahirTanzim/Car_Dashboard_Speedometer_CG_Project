from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLU import *     # Utility library (gluOrtho2D)
from OpenGL.GLUT import *    # GLUT functions (window creation, main loop)
import math
from algorithms import dda
from algorithms import draw_circle
from algorithms import midpoint

# Window size constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 800

# Line endpoints for demonstration
X0, Y0 = 100, 80
X1, Y1 = 200, 520



def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()
    points = dda(X0, Y0, X1, Y1)
    glPointSize(5)
    glBegin(GL_POINTS)
    for point in points:
        glVertex2i(point[0], point[1])
    glEnd()
    
    glutSwapBuffers()
    

def reshape(width, height):
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(0, width, 0, height)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def init_glut_window():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(400, 100)
    glutCreateWindow(b"DDA Line Drawing Algorithm - PyOpenGL + GLUT")
    glutDisplayFunc(display)
    glutReshapeFunc(reshape)
    glClearColor(0.0, 0.0, 0.0, 0.0)  # Black background

def main():
    init_glut_window()
    glutMainLoop()

if __name__ == "__main__":
    main()
