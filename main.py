from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import math
import time

speed = 0          # Current speed
target_speed = 0   # Smooth animation target

def draw_text(x, y, text, scale=0.1):
    glPushMatrix()
    glTranslatef(x, y, 0)
    glScalef(scale, scale, 1)
    glColor3f(1, 1, 1)
    for c in text:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
    glPopMatrix()

def draw_semicircle():
    glColor3f(0.2, 0.2, 0.2)
    glBegin(GL_TRIANGLE_FAN)
    glVertex2f(0, 0)  # center
    for angle in range(0, 181):
        rad = math.radians(angle)
        glVertex2f(math.cos(rad), math.sin(rad))
    glEnd()

    # Outer arc border
    glLineWidth(3)
    glColor3f(1, 1, 1)
    glBegin(GL_LINE_STRIP)
    for angle in range(0, 181):
        rad = math.radians(angle)
        glVertex2f(math.cos(rad), math.sin(rad))
    glEnd()

def draw_needle():
    # Angle proportional to speed (0–180 degrees)
    angle = (speed / 180) * 180

    glPushMatrix()
    glRotatef(angle, 0, 0, 1)

    glColor3f(1, 0, 0)  # red needle
    glLineWidth(4)
    glBegin(GL_LINES)
    glVertex2f(0, 0)
    glVertex2f(0.8, 0)  # needle length
    glEnd()

    glPopMatrix()

def draw_markings():
    glColor3f(1, 1, 1)
    glLineWidth(3)
    for s in range(0, 181, 20):
        angle = math.radians(s)
        x1 = math.cos(angle)
        y1 = math.sin(angle)
        x2 = 0.9 * math.cos(angle)
        y2 = 0.9 * math.sin(angle)

        glBegin(GL_LINES)
        glVertex2f(x1, y1)
        glVertex2f(x2, y2)
        glEnd()

        # Speed numbers
        tx = 0.75 * math.cos(angle)
        ty = 0.75 * math.sin(angle)
        draw_text(tx - 0.05, ty - 0.03, str(s))

def display():
    glClear(GL_COLOR_BUFFER_BIT)
    glLoadIdentity()

    draw_semicircle()
    draw_markings()
    draw_needle()

    # Digital speed display
    draw_text(-0.15, -0.3, f"Speed: {int(speed)}", 0.15)

    glutSwapBuffers()

def update(value):
    global speed

    # Smooth movement toward target_speed
    if abs(speed - target_speed) > 0.2:
        speed += (target_speed - speed) * 0.1

    glutPostRedisplay()
    glutTimerFunc(16, update, 0)

def keyboard(key, x, y):
    global target_speed

    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()

def special_keys(key, x, y):
    global target_speed

    if key == GLUT_KEY_UP:
        target_speed += 5
        if target_speed > 180:
            target_speed = 180

    if key == GLUT_KEY_DOWN:
        target_speed -= 5
        if target_speed < 0:
            target_speed = 0

def init():
    glClearColor(0, 0, 0, 1)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1.2, 1.2, -0.5, 1.2)

if __name__ == "__main__":
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGBA)
    glutInitWindowSize(800, 600)
    glutCreateWindow("Analog Speedometer - Python OpenGL")

    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, update, 0)

    glutMainLoop()
