from OpenGL.GL import *      # Core OpenGL functions
from OpenGL.GLU import *     # Utility library (gluOrtho2D)
from OpenGL.GLUT import *    # GLUT functions (window creation, main loop)
import math

def Line(x1, y1, x2, y2):  #dda
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))

    
    if steps == 0:
        glBegin(GL_POINTS)
        glVertex2f(x1, y1)
        glEnd()
        return

    x_increment = dx / steps
    y_increment = dy / steps
    x = x1
    y = y1

    glBegin(GL_POINTS)
    for i in range(int(steps) + 1):
        pixel_x = round(x)
        pixel_y = round(y)
        glVertex2f(pixel_x, pixel_y)
        x += x_increment
        y += y_increment
    glEnd()



def Circle(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    draw_points(x + x0, y + y0)
    draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    draw_points(x + x0, -y + y0)
    draw_points(-x + x0, -y + y0)
    draw_points(-y + x0, -x + y0)
    draw_points(-y + x0, x + y0)
    draw_points(-x + x0, y + y0)

def HCircle_Left(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    # draw_points(x + x0, y + y0)
    # draw_points(y + x0, x + y0)
    # draw_points(y + x0, -x + y0)
    # draw_points(x + x0, -y + y0)
    draw_points(-x + x0, -y + y0)
    draw_points(-y + x0, -x + y0)
    draw_points(-y + x0, x + y0)
    draw_points(-x + x0, y + y0)

def HCircle_Right(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    draw_points(x + x0, y + y0)
    draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    draw_points(x + x0, -y + y0)
    # draw_points(-x + x0, -y + y0)
    # draw_points(-y + x0, -x + y0)
    # draw_points(-y + x0, x + y0)
    # draw_points(-x + x0, y + y0)

def HCircle_Right(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    draw_points(x + x0, y + y0)
    draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    draw_points(x + x0, -y + y0)
    # draw_points(-x + x0, -y + y0)
    # draw_points(-y + x0, -x + y0)
    # draw_points(-y + x0, x + y0)
    # draw_points(-x + x0, y + y0)

def HCircle_Top(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    draw_points(x + x0, y + y0)
    draw_points(y + x0, x + y0)
    # draw_points(y + x0, -x + y0)
    # draw_points(x + x0, -y + y0)
    # draw_points(-x + x0, -y + y0)
    # draw_points(-y + x0, -x + y0)
    draw_points(-y + x0, x + y0)
    draw_points(-x + x0, y + y0)


def HCircle_Down(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    # draw_points(x + x0, y + y0)
    # draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    draw_points(x + x0, -y + y0)
    draw_points(-x + x0, -y + y0)
    draw_points(-y + x0, -x + y0)
    # draw_points(-y + x0, x + y0)
    # draw_points(-x + x0, y + y0)
    
    
def HCircle_Down(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    # draw_points(x + x0, y + y0)
    # draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    draw_points(x + x0, -y + y0)
    draw_points(-x + x0, -y + y0)
    draw_points(-y + x0, -x + y0)
    # draw_points(-y + x0, x + y0)
    # draw_points(-x + x0, y + y0)   
    
    
def ThreeQuarterCircle(radius, x0, y0):
    x = 0
    y = radius
    d = 1 - radius  # Decision parameter

    Circlepoints(x, y, x0, y0)

    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        Circlepoints(x, y, x0, y0)

def Circlepoints(x, y, x0, y0):
    draw_points(x + x0, y + y0)
    draw_points(y + x0, x + y0)
    draw_points(y + x0, -x + y0)
    # draw_points(x + x0, -y + y0)
    # draw_points(-x + x0, -y + y0)
    draw_points(-y + x0, -x + y0)
    draw_points(-y + x0, x + y0)
    draw_points(-x + x0, y + y0)     

def draw_points(x, y):
    # glPointSize(2)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()