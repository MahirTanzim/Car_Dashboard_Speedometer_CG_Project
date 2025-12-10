"""
algorithms.py - Core drawing algorithms for the car dashboard
Contains: DDA Line, Midpoint Circle algorithms
"""

from OpenGL.GL import *

def draw_point(x, y, size=2):
    """Draw a single point at (x, y)"""
    glPointSize(size)
    glBegin(GL_POINTS)
    glVertex2f(x, y)
    glEnd()

def dda_line(x1, y1, x2, y2):
    """Draw a line from (x1, y1) to (x2, y2) using DDA algorithm"""
    dx = x2 - x1
    dy = y2 - y1
    steps = max(abs(dx), abs(dy))
    
    if steps == 0:
        draw_point(x1, y1)
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

def draw_circle_points(x, y, x0, y0):
    """Draw 8 symmetric points of a circle"""
    draw_point(x + x0, y + y0)
    draw_point(y + x0, x + y0)
    draw_point(y + x0, -x + y0)
    draw_point(x + x0, -y + y0)
    draw_point(-x + x0, -y + y0)
    draw_point(-y + x0, -x + y0)
    draw_point(-y + x0, x + y0)
    draw_point(-x + x0, y + y0)

def midpoint_circle(radius, x0, y0):
    """Draw a circle using Midpoint Circle algorithm"""
    x = 0
    y = radius
    d = 1 - radius
    
    draw_circle_points(x, y, x0, y0)
    
    while x < y:
        if d < 0:
            d = d + 2 * x + 3
        else:
            d = d + 2 * (x - y) + 5
            y -= 1
        x += 1
        draw_circle_points(x, y, x0, y0)

def draw_filled_circle(radius, x0, y0):
    """Draw a filled circle"""
    for r in range(radius, 0, -1):
        midpoint_circle(r, x0, y0)