
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
from components import *
from main import *
from algorithms import rotate_point
def draw_3d_road():
    """Draw the road with improved texturing"""
    near_z = camera_z
    far_z = camera_z + 500
    
    # Main road
    glColor3f(0.3, 0.3, 0.3)
    glBegin(GL_QUADS)
    glVertex3f(-10, 0, near_z)
    glVertex3f(10, 0, near_z)
    glVertex3f(10, 0, far_z)
    glVertex3f(-10, 0, far_z)
    glEnd()

    # Road edges
    glColor3f(0.8, 0.8, 0.8)
    glLineWidth(3)
    glBegin(GL_LINES)
    glVertex3f(-5, 0.01, near_z)
    glVertex3f(-5, 0.01, far_z)
    glVertex3f(5, 0.01, near_z)
    glVertex3f(5, 0.01, far_z)
    glEnd()

    # Center dashes
    dash_length = 20
    gap = 15
    pattern_length = dash_length + gap
    glColor3f(1, 0.95, 0)
    glLineWidth(3)
    current_z = near_z - ((near_z % pattern_length) - gap)
    while current_z < far_z:
        dash_start = current_z
        dash_end = min(current_z + dash_length, far_z)
        if dash_start < far_z:
            glBegin(GL_LINES)
            glVertex3f(0, 0.01, dash_start)
            glVertex3f(0, 0.01, dash_end)
            glEnd()
        current_z += pattern_length

def draw_ground():
    """Draw grass ground on sides of road"""
    near_z = camera_z
    far_z = camera_z + 500
    
    # Left grass
    glColor3f(0.2, 0.5, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-50, 0, near_z)
    glVertex3f(-10, 0, near_z)
    glVertex3f(-10, 0, far_z)
    glVertex3f(-50, 0, far_z)
    glEnd()
    
    # Right grass
    glBegin(GL_QUADS)
    glVertex3f(10, 0, near_z)
    glVertex3f(50, 0, near_z)
    glVertex3f(50, 0, far_z)
    glVertex3f(10, 0, far_z)
    glEnd()

def draw_tree(x, y, z, height, tree_type):
    """Draw a tree - either pine or round"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Trunk
    glColor3f(0.4, 0.25, 0.1)
    glBegin(GL_QUADS)
    trunk_width = 0.5
    trunk_height = height * 0.4
    # Front
    glVertex3f(-trunk_width, 0, 0)
    glVertex3f(trunk_width, 0, 0)
    glVertex3f(trunk_width, trunk_height, 0)
    glVertex3f(-trunk_width, trunk_height, 0)
    # Back
    glVertex3f(-trunk_width, 0, 0.5)
    glVertex3f(trunk_width, 0, 0.5)
    glVertex3f(trunk_width, trunk_height, 0.5)
    glVertex3f(-trunk_width, trunk_height, 0.5)
    glEnd()
    
    
        # Pine tree - triangular layers
    glColor3f(0.1, 0.4, 0.1)
    layers = 3
    for i in range(layers):
        base_y = trunk_height + i * (height * 0.15)
        base_size = 2.5 - i * 0.6
        
        glBegin(GL_TRIANGLES)
        # Front triangle
        glVertex3f(0, base_y + height * 0.2, 0.25)
        glVertex3f(-base_size, base_y, 0)
        glVertex3f(base_size, base_y, 0)
        # Back triangle
        glVertex3f(0, base_y + height * 0.2, 0.5)
        glVertex3f(-base_size, base_y, 0.5)
        glVertex3f(base_size, base_y, 0.5)
        # Side triangles
        glVertex3f(0, base_y + height * 0.2, 0.25)
        glVertex3f(-base_size, base_y, 0)
        glVertex3f(-base_size, base_y, 0.5)
        
        glVertex3f(0, base_y + height * 0.2, 0.25)
        glVertex3f(base_size, base_y, 0)
        glVertex3f(base_size, base_y, 0.5)
        glEnd()

    
    glPopMatrix()

def draw_cloud(x, y, z, size):
    """Draw a simple cloud"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor4f(1.0, 1.0, 1.0, 0.8)
    
    # Draw multiple overlapping ellipsoids for cloud effect
    positions = [
        (0, 0, 0),
        (-size*0.3, size*0.1, 0),
        (size*0.3, size*0.1, 0),
        (-size*0.15, -size*0.2, 0),
        (size*0.15, -size*0.2, 0)
    ]
    
    for px, py, pz in positions:
        glPushMatrix()
        glTranslatef(px, py, pz)
        # Draw multiple concentric, scaled fans to make the puff rounder/softer
        base_scale_x = size * 0.4
        base_scale_y = size * 0.25
        base_scale_z = size * 0.3

        # Draw 3 concentric fans with decreasing alpha and slightly larger radii
        segments = 28
        for layer in range(3, 0, -1):
            s = layer / 3.0
            alpha = 0.12 + 0.28 * s  # inner layers more opaque
            glColor4f(1.0, 1.0, 1.0, alpha)
            glPushMatrix()
            glScalef(base_scale_x * (1.0 + (3-layer) * 0.15), base_scale_y * (1.0 + (3-layer) * 0.12), base_scale_z)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0.0, 0.0, 0.0)
            for i in range(segments + 1):
                theta = 2.0 * math.pi * i / segments
                ux, uy = rotate_point(1.0, 0.0, theta)
                glVertex3f(ux, uy, 0.0)
            glEnd()
            glPopMatrix()
        glPopMatrix()
    
    glPopMatrix()

def draw_3d_house(x, y, z):
    """Draw a simplified flat house (2D billboard polygon) for performance."""
    glPushMatrix()
    # Position at world coords
    glTranslatef(x, y, z)

    # Draw the house as a single front-facing quad + triangular roof slightly offset in Z
    w = 4.0
    h = 6.0
    depth = -0.2  # slight offset so it faces the camera

    # Body
    glColor3f(0.6, 0.4, 0.2)
    glBegin(GL_QUADS)
    glVertex3f(-w, 0, depth)
    glVertex3f(w, 0, depth)
    glVertex3f(w, h, depth)
    glVertex3f(-w, h, depth)
    glEnd()

    # Roof (flat triangle)
    glColor3f(0.5, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex3f(-w - 0.5, h, depth)
    glVertex3f(w + 0.5, h, depth)
    glVertex3f(0, h + 3.0, depth)
    glEnd()

    # Windows (simple quads)
    glColor3f(0.2, 0.4, 0.6)
    glBegin(GL_QUADS)
    glVertex3f(-2.5, 3.5, depth - 0.01)
    glVertex3f(-1.2, 3.5, depth - 0.01)
    glVertex3f(-1.2, 5.0, depth - 0.01)
    glVertex3f(-2.5, 5.0, depth - 0.01)

    glVertex3f(1.2, 3.5, depth - 0.01)
    glVertex3f(2.5, 3.5, depth - 0.01)
    glVertex3f(2.5, 5.0, depth - 0.01)
    glVertex3f(1.2, 5.0, depth - 0.01)
    glEnd()

    glPopMatrix()

def draw_3d_car(x, y, z, color):
    """Draw a flat 2D car sprite (billboard) to replace heavy 3D model."""
    glPushMatrix()
    glTranslatef(x, y, z)

    w = 0.9
    h = 0.5
    depth = -0.1

    # Body (flat quad)
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex3f(-w, 0, depth)
    glVertex3f(w, 0, depth)
    glVertex3f(w, h, depth)
    glVertex3f(-w, h, depth)
    glEnd()

    # Rear window (darker quad)
    glColor3f(0.12, 0.22, 0.35)
    glBegin(GL_QUADS)
    glVertex3f(-0.35, 0.25, depth - 0.01)
    glVertex3f(0.35, 0.25, depth - 0.01)
    glVertex3f(0.42, 0.45, depth - 0.01)
    glVertex3f(-0.42, 0.45, depth - 0.01)
    glEnd()

    # Taillights (small quads)
    glColor3f(0.6, 0.15, 0.15)
    glBegin(GL_QUADS)
    glVertex3f(-w + 0.15, 0.05, depth - 0.02)
    glVertex3f(-w + 0.45, 0.05, depth - 0.02)
    glVertex3f(-w + 0.45, 0.18, depth - 0.02)
    glVertex3f(-w + 0.15, 0.18, depth - 0.02)

    glVertex3f(w - 0.45, 0.05, depth - 0.02)
    glVertex3f(w - 0.15, 0.05, depth - 0.02)
    glVertex3f(w - 0.15, 0.18, depth - 0.02)
    glVertex3f(w - 0.45, 0.18, depth - 0.02)
    glEnd()

    glPopMatrix()