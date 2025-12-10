"""
main.py - Enhanced Car Dashboard Main Program
Controls the entire dashboard system with improved 3D scene
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
from components import *


# Global variables for dashboard state

# Window size constants
WINDOW_WIDTH = 1500
WINDOW_HEIGHT = 1000
speed = 0
rpm = 0
fuel_level = 100
engine_temp = 20
left_turn = False
right_turn = False
fuel_warning = False
last_activity_time = 0
fuel_consumption_counter = 0
half_circle_drawn = False
road_offset = 0
# Smooth animation variables
target_speed = 0
target_fuel = 100
blink_counter = 0
left_blink_time = 0
right_blink_time = 0

# Key state tracking for continuous movement
keys_pressed = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

# 3D simulation variables
camera_z = 0.0
oncoming_cars = []
trees = []
clouds = []

def initialize():
    """Initialize OpenGL settings"""
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.4, 0.6, 0.9, 1.0)  # Sky blue background
    
    # Initialize trees on roadside
    initialize_trees()
    
    # Initialize clouds
    initialize_clouds()

def initialize_trees():
    """Create initial trees along the road"""
    global trees
    tree_spacing = 30
    for i in range(30):
        z = i * tree_spacing
        # Left side trees
        trees.append({
            'x': -18 - random.uniform(0, 3),
            'z': z + random.uniform(-5, 5),
            'height': 8 + random.uniform(0, 4),
            'type': random.choice(['pine', 'round'])
        })
        # Right side trees
        trees.append({
            'x': 18 + random.uniform(0, 3),
            'z': z + random.uniform(-5, 5),
            'height': 8 + random.uniform(0, 4),
            'type': random.choice(['pine', 'round'])
        })

def draw_house_2d(cx, cy, scale=1.0):
    """Simple 2D house for lightweight roadside rendering"""
    w = 40 * scale
    h = 50 * scale
    # Body
    glColor3f(0.6, 0.4, 0.2)
    glBegin(GL_QUADS)
    glVertex2f(cx - w/2, cy)
    glVertex2f(cx + w/2, cy)
    glVertex2f(cx + w/2, cy + h)
    glVertex2f(cx - w/2, cy + h)
    glEnd()
    # Roof
    glColor3f(0.35, 0.12, 0.10)
    glBegin(GL_TRIANGLES)
    glVertex2f(cx - w/2 - 4*scale, cy + h)
    glVertex2f(cx + w/2 + 4*scale, cy + h)
    glVertex2f(cx, cy + h + 18*scale)
    glEnd()

def draw_tree_2d(cx, cy, scale=1.0, tree_type='round'):
    """Simple 2D tree (pine or round crown)"""
    trunk_w = 6 * scale
    trunk_h = 14 * scale
    glColor3f(0.45, 0.28, 0.12)
    glBegin(GL_QUADS)
    glVertex2f(cx - trunk_w/2, cy)
    glVertex2f(cx + trunk_w/2, cy)
    glVertex2f(cx + trunk_w/2, cy + trunk_h)
    glVertex2f(cx - trunk_w/2, cy + trunk_h)
    glEnd()
    if tree_type == 'pine':
        glColor3f(0.08, 0.45, 0.12)
        for i in range(3):
            s = scale * (1.0 - i*0.18)
            y = cy + trunk_h + i * (12*scale)
            glBegin(GL_TRIANGLES)
            glVertex2f(cx, y + 18*s)
            glVertex2f(cx - 18*s, y)
            glVertex2f(cx + 18*s, y)
            glEnd()
    else:
        glColor3f(0.12, 0.48, 0.16)
        draw_filled_circle(int(18*scale), int(cx), int(cy + trunk_h + 8*scale))

def draw_car_2d(cx, cy, scale=1.0, color=(0.8,0.0,0.0), wheel_angle=0.0, taillight_on=False):
    """Simple 2D back-view car sprite"""
    w = 60 * scale
    h = 40 * scale
    # body
    glColor3f(*color)
    glBegin(GL_QUADS)
    glVertex2f(cx - w/2, cy)
    glVertex2f(cx + w/2, cy)
    glVertex2f(cx + w/2, cy + h)
    glVertex2f(cx - w/2, cy + h)
    glEnd()
    # rear window
    glColor3f(0.12, 0.22, 0.35)
    glBegin(GL_QUADS)
    glVertex2f(cx - w*0.22, cy + h*0.45)
    glVertex2f(cx + w*0.22, cy + h*0.45)
    glVertex2f(cx + w*0.28, cy + h*0.78)
    glVertex2f(cx - w*0.28, cy + h*0.78)
    glEnd()
    # taillights
    if taillight_on:
        glColor3f(1.0, 0.2, 0.2)
    else:
        glColor3f(0.6, 0.15, 0.15)
    glBegin(GL_QUADS)
    glVertex2f(cx - w/2 + 6*scale, cy + h*0.1)
    glVertex2f(cx - w/2 + 6*scale + 8*scale, cy + h*0.1)
    glVertex2f(cx - w/2 + 6*scale + 8*scale, cy + h*0.28)
    glVertex2f(cx - w/2 + 6*scale, cy + h*0.28)
    glVertex2f(cx + w/2 - 6*scale - 8*scale, cy + h*0.1)
    glVertex2f(cx + w/2 - 6*scale, cy + h*0.1)
    glVertex2f(cx + w/2 - 6*scale, cy + h*0.28)
    glVertex2f(cx + w/2 - 6*scale - 8*scale, cy + h*0.28)
    glEnd()

def initialize_clouds():
    """Create initial clouds in the sky"""
    global clouds
    for i in range(15):
        clouds.append({
            'x': random.uniform(-100, 100),
            'y': random.uniform(20, 40),
            'z': random.uniform(0, 500),
            'size': random.uniform(8, 15),
            'speed': random.uniform(0.1, 0.3)
        })

def update_rpm():
    """Update RPM based on speed"""
    global rpm
    rpm = (speed / 230.0) * 7 + 0.5

def update_engine_temp():
    """Update engine temperature based on speed and RPM"""
    global engine_temp
    target_temp = 20 + (rpm * 8) + (speed * 0.2)
    if target_temp > 120:
        target_temp = 120
    
    if engine_temp < target_temp:
        engine_temp += 0.5
    elif engine_temp > target_temp:
        engine_temp -= 0.3

def consume_fuel():
    """Consume fuel based on speed"""
    global fuel_level, fuel_consumption_counter, fuel_warning
    
    if speed > 0:
        fuel_consumption_counter += 1
        
        if fuel_consumption_counter > 30:
            fuel_level -= 0.5 * (1 + speed / 100.0)
            fuel_consumption_counter = 0
            
            if fuel_level < 0:
                fuel_level = 0
    
    if fuel_level < 20:
        fuel_warning = True
    else:
        fuel_warning = False

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
    
    if tree_type == 'pine':
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
    else:
        # Round tree - sphere-like crown
        glColor3f(0.15, 0.5, 0.15)
        crown_y = trunk_height + height * 0.3
        crown_size = 2.0
        
        # Rounded crown using stacked triangle fans (front + back) for smoothness
        glColor3f(0.15, 0.5, 0.15)
        segments = 20
        layers = 6
        crown_height = height * 0.4
        for li in range(layers):
            t = li / float(max(1, layers - 1))
            # vertical position for this layer (from bottom to top of crown)
            y_layer = crown_y + t * crown_height
            # radius tapers slightly towards the top
            radius = crown_size * (1.0 - 0.6 * t)

            # front face fan (z = 0)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0.0, y_layer, 0.0)
            for i in range(segments + 1):
                theta = 2.0 * 3.14159265 * i / segments
                x = radius * math.cos(theta)
                z_off = radius * math.sin(theta) * 0.25  # slight depth curve
                glVertex3f(x, y_layer, z_off)
            glEnd()

            # back face fan (z = 0.5) to give crown thickness
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(0.0, y_layer, 0.5)
            for i in range(segments + 1):
                theta = 2.0 * 3.14159265 * i / segments
                x = radius * math.cos(theta)
                z_off = 0.5 + radius * math.sin(theta) * 0.15
                glVertex3f(x, y_layer, z_off)
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
                theta = 2.0 * 3.14159265 * i / segments
                cx = math.cos(theta)
                cy = math.sin(theta)
                glVertex3f(cx, cy, 0.0)
            glEnd()
            glPopMatrix()
        glPopMatrix()
    
    glPopMatrix()

def draw_3d_house(x, y, z):
    """Draw a house on the roadside"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glColor3f(0.6, 0.4, 0.2)
    
    # Base
    glBegin(GL_QUADS)
    # Front
    glVertex3f(-4, 0, -3)
    glVertex3f(4, 0, -3)
    glVertex3f(4, 6, -3)
    glVertex3f(-4, 6, -3)
    # Back
    glVertex3f(-4, 0, 3)
    glVertex3f(4, 0, 3)
    glVertex3f(4, 6, 3)
    glVertex3f(-4, 6, 3)
    # Left
    glVertex3f(-4, 0, -3)
    glVertex3f(-4, 0, 3)
    glVertex3f(-4, 6, 3)
    glVertex3f(-4, 6, -3)
    # Right
    glVertex3f(4, 0, -3)
    glVertex3f(4, 0, 3)
    glVertex3f(4, 6, 3)
    glVertex3f(4, 6, -3)
    glEnd()
    
    # Windows
    glColor3f(0.2, 0.4, 0.6)
    glBegin(GL_QUADS)
    # Left window
    glVertex3f(-3, 3.5, -3.01)
    glVertex3f(-1.5, 3.5, -3.01)
    glVertex3f(-1.5, 5.5, -3.01)
    glVertex3f(-3, 5.5, -3.01)
    # Right window
    glVertex3f(1.5, 3.5, -3.01)
    glVertex3f(3, 3.5, -3.01)
    glVertex3f(3, 5.5, -3.01)
    glVertex3f(1.5, 5.5, -3.01)
    glEnd()
    
    # Roof
    glColor3f(0.5, 0.2, 0.1)
    glBegin(GL_TRIANGLES)
    glVertex3f(-4, 6, -3)
    glVertex3f(4, 6, -3)
    glVertex3f(0, 9, 0)
    glVertex3f(-4, 6, 3)
    glVertex3f(4, 6, 3)
    glVertex3f(0, 9, 0)
    glEnd()
    glPopMatrix()

def draw_3d_car(x, y, z, color):
    """Draw a realistic 3D car"""
    glPushMatrix()
    glTranslatef(x, y, z)
    
    # Main car body
    glColor3f(*color)
    glBegin(GL_QUADS)
    # Front
    glVertex3f(-0.7, 0, -2)
    glVertex3f(0.7, 0, -2)
    glVertex3f(0.8, 0.9, -2)
    glVertex3f(-0.8, 0.9, -2)
    # Back
    glVertex3f(-0.8, 0, 2)
    glVertex3f(0.8, 0, 2)
    glVertex3f(0.85, 0.85, 2)
    glVertex3f(-0.85, 0.85, 2)
    # Left side
    glVertex3f(-0.8, 0, -2)
    glVertex3f(-0.8, 0, 2)
    glVertex3f(-0.85, 0.85, 2)
    glVertex3f(-0.8, 0.9, -2)
    # Right side
    glVertex3f(0.8, 0, -2)
    glVertex3f(0.8, 0, 2)
    glVertex3f(0.85, 0.85, 2)
    glVertex3f(0.8, 0.9, -2)
    # Top
    glVertex3f(-0.7, 0.9, -2)
    glVertex3f(0.7, 0.9, -2)
    glVertex3f(0.75, 0.85, 2)
    glVertex3f(-0.75, 0.85, 2)
    glEnd()
    
    # Windshield
    glColor3f(0.3, 0.5, 0.8)
    glBegin(GL_QUADS)
    glVertex3f(-0.6, 0.4, -2.02)
    glVertex3f(0.6, 0.4, -2.02)
    glVertex3f(0.7, 0.85, -2.02)
    glVertex3f(-0.7, 0.85, -2.02)
    glEnd()
    
    # Headlights
    glColor3f(1.0, 1.0, 0.7)
    glBegin(GL_TRIANGLES)
    glVertex3f(-0.55, 0.15, -2.02)
    glVertex3f(-0.35, 0.15, -2.02)
    glVertex3f(-0.45, 0.35, -2.02)
    glVertex3f(0.35, 0.15, -2.02)
    glVertex3f(0.55, 0.15, -2.02)
    glVertex3f(0.45, 0.35, -2.02)
    glEnd()
    
    glPopMatrix()

def display():
    """Main display function"""
    global blink_counter, left_turn, right_turn, left_blink_time, right_blink_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()

    # 3D Scene
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 2, camera_z, 0, 2, camera_z + 100, 0, 1, 0)

    # Draw sky elements (clouds)
    for cloud in clouds:
        draw_cloud(cloud['x'], cloud['y'], cloud['z'], cloud['size'])

    draw_ground()
    draw_3d_road()

    # Draw trees
    for tree in trees:
        if tree['z'] > camera_z - 50 and tree['z'] < camera_z + 500:
            draw_tree(tree['x'], 0, tree['z'], tree['height'], tree['type'])

    # Draw houses
    num_houses = 10
    house_spacing = 50
    start_z = math.floor(camera_z / house_spacing) * house_spacing
    for i in range(num_houses):
        z = start_z + i * house_spacing
        draw_3d_house(25, 0, z)
        draw_3d_house(-25, 0, z)

    # Draw oncoming cars
    for car in oncoming_cars:
        draw_3d_car(car['x'], 0, car['z'], car['color'])

    # 2D Dashboard Overlay
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)

    # Dashboard background
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glVertex2f(WINDOW_WIDTH, 350)
    glVertex2f(0, 350)
    glEnd()

    glColor3f(0.75, 0.75, 0.78)
    draw_half_circle_frame(750, 0, 350, thickness=10)

    # Update dashboard values
    update_rpm()
    update_engine_temp()
    consume_fuel()
    blink_counter += 1
    
    # Turn signal blink logic
    current_time = time.time()
    left_blink_show = False
    right_blink_show = False
    
    if left_turn:
        time_since_left = (current_time - left_blink_time) * 1000
        if time_since_left < 1000:
            left_blink_show = ((int(time_since_left // 250)) % 2) == 0
        else:
            left_turn = False
    
    if right_turn:
        time_since_right = (current_time - right_blink_time) * 1000
        if time_since_right < 1000:
            right_blink_show = ((int(time_since_right // 250)) % 2) == 0
        else:
            right_turn = False
    
    # Draw dashboard components
    draw_speedometer(700, 200, 120, speed)
    draw_rpm_meter(340, 150, 80, rpm)
    draw_fuel_meter(980, 130, 60, fuel_level)
    draw_digital_display(610, 70, 140, 40, speed, "km/h")
    draw_digital_display(1100, 200, 140, 40, engine_temp, "°C")
    draw_turn_arrow(550, 280, 'left', left_blink_show)
    draw_turn_arrow(850, 280, 'right', right_blink_show)
    draw_indicator_light(980, 250, 10, fuel_warning, (1.0, 0.0, 0.0))
    
    # Instructions
    glColor3f(0.65, 0.66, 0.68)
    draw_text(20, 20, "UP/DOWN: Speed  |  B: Brake  |  F: Refuel  |  LEFT/RIGHT: Turn Signals  |  ESC: Exit")
    
    glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()

def keyboard(key, x, y):
    """Handle keyboard input"""
    global speed, fuel_level, target_fuel, left_turn, right_turn, fuel_warning, last_activity_time
    
    last_activity_time = time.time()
    
    if key == b'\x1b':  # ESC
        glutLeaveMainLoop()
    
    if key == b'b' or key == b'B':
        speed = max(0, speed - 20)
    
    if key == b'f' or key == b'F':
        target_fuel = 100
        fuel_warning = False

def special_keys(key, x, y):
    """Handle arrow keys"""
    global keys_pressed, left_turn, right_turn, last_activity_time, left_blink_time, right_blink_time
    
    last_activity_time = time.time()
    
    if key == GLUT_KEY_UP:
        keys_pressed['up'] = True
    elif key == GLUT_KEY_DOWN:
        keys_pressed['down'] = True
    elif key == GLUT_KEY_LEFT:
        if not left_turn:
            left_turn = True
            left_blink_time = time.time()
            right_turn = False
    elif key == GLUT_KEY_RIGHT:
        if not right_turn:
            right_turn = True
            right_blink_time = time.time()
            left_turn = False
    
    glutPostRedisplay()

def special_keys_up(key, x, y):
    """Handle key release"""
    global keys_pressed
    
    if key == GLUT_KEY_UP:
        keys_pressed['up'] = False
    elif key == GLUT_KEY_DOWN:
        keys_pressed['down'] = False

def animate(value):
    """Animation timer"""
    global speed, target_speed, keys_pressed, camera_z, oncoming_cars, trees, clouds
    
    dt = 0.016
    
    # Speed control
    if keys_pressed['up']:
        if target_speed < 230:
            target_speed += 3
    
    if keys_pressed['down']:
        if target_speed > 0:
            target_speed -= 3
    
    # Smooth speed transition
    if speed < target_speed:
        speed = min(speed + 1.6, target_speed)
    elif speed > target_speed:
        speed = max(speed - 1.6, target_speed)
    
    # Move camera
    v_ego = speed / 3.6
    camera_z += v_ego * dt
    
    # Update oncoming cars
    for car in oncoming_cars:
        v_onc = 60 / 3.6
        car['z'] -= v_onc * dt
    
    oncoming_cars[:] = [car for car in oncoming_cars if car['z'] > camera_z - 10]
    
    # Spawn new cars
    if random.random() < 0.02:
        new_z = camera_z + 300 + random.uniform(0, 100)
        new_color = (random.uniform(0.5, 1), random.uniform(0, 0.5), random.uniform(0, 0.5))
        oncoming_cars.append({'x': -3, 'z': new_z, 'color': new_color})
    
    # Update trees (add new ones as we move forward)
    if len(trees) > 0:
        max_tree_z = max(tree['z'] for tree in trees)
        if max_tree_z < camera_z + 500:
            new_z = max_tree_z + 30
            trees.append({
                'x': -18 - random.uniform(0, 3),
                'z': new_z,
                'height': 8 + random.uniform(0, 4),
                'type': random.choice(['pine', 'round'])
            })
            trees.append({
                'x': 18 + random.uniform(0, 3),
                'z': new_z,
                'height': 8 + random.uniform(0, 4),
                'type': random.choice(['pine', 'round'])
            })
    
    # Remove trees behind camera
    trees[:] = [tree for tree in trees if tree['z'] > camera_z - 100]
    
    # Update clouds (drift slowly)
    for cloud in clouds:
        cloud['x'] += cloud['speed'] * dt
        if cloud['x'] > 100:
            cloud['x'] = -100
    
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)

def main():
    """Main function"""
    global last_activity_time
    last_activity_time = time.time()
    
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_WIDTH, WINDOW_HEIGHT)
    glutInitWindowPosition(50, 50)
    wind = glutCreateWindow(b"Enhanced Car Dashboard Simulation")
    
    initialize()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutSpecialUpFunc(special_keys_up)
    glutTimerFunc(0, animate, 0)
    
    glutMainLoop()

if __name__ == "__main__":
    main()