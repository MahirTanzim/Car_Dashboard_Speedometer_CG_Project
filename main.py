

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
import math
import random
from components import *
from scene import *




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
target_speed = 0
target_fuel = 100
blink_counter = 0
left_blink_time = 0
right_blink_time = 0

keys_pressed = {
    'up': False,
    'down': False,
    'left': False,
    'right': False
}

camera_z = 0.0
oncoming_cars = []
trees = []
clouds = []


def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.4, 0.6, 0.9, 1.0)  
    
    
    initialize_trees()
    
    initialize_clouds()

def initialize_trees():
    
    global trees
    tree_spacing = 30
    for i in range(30):
        z = i * tree_spacing
        # Left side trees
        trees.append({
            'x': -18 - random.uniform(0, 3),
            'z': z + random.uniform(-5, 5),
            'height': 8 + random.uniform(0, 4),
            'type': random.choice(['pine'])
        })
        # Right side trees
        trees.append({
            'x': 18 + random.uniform(0, 3),
            'z': z + random.uniform(-5, 5),
            'height': 8 + random.uniform(0, 4),
            'type': random.choice(['pine'])
        })




def initialize_clouds():
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
    global rpm
    rpm = (speed / 230.0) * 7 + 0.5

def update_engine_temp():
    global engine_temp
    target_temp = 20 + (rpm * 8) + (speed * 0.2)
    if target_temp > 120:
        target_temp = 120
    
    if engine_temp < target_temp:
        engine_temp += 0.5
    elif engine_temp > target_temp:
        engine_temp -= 0.3

def consume_fuel():
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


def display():
    global blink_counter, left_turn, right_turn, left_blink_time, right_blink_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(60, WINDOW_WIDTH / WINDOW_HEIGHT, 0.1, 1000.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    gluLookAt(0, 2, camera_z, 0, 2, camera_z + 100, 0, 1, 0)
    for cloud in clouds:
        draw_cloud(cloud['x'], cloud['y'], cloud['z'], cloud['size'])

    draw_ground()
    draw_3d_road()

    for tree in trees:
        if tree['z'] > camera_z - 50 and tree['z'] < camera_z + 500:
            draw_tree(tree['x'], 0, tree['z'], tree['height'], tree['type'])

    num_houses = 10
    house_spacing = 50
    start_z = math.floor(camera_z / house_spacing) * house_spacing
    for i in range(num_houses):
        z = start_z + i * house_spacing
        draw_3d_house(25, 0, z)
        draw_3d_house(-25, 0, z)

    for car in oncoming_cars:
        draw_3d_car(car['x'], 0, car['z'], car['color'])

    # 2D Dashboard Overlay
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0, WINDOW_WIDTH, 0, WINDOW_HEIGHT, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glDisable(GL_DEPTH_TEST)
    glColor3f(0.1, 0.1, 0.1)
    glBegin(GL_QUADS)
    glVertex2f(0, 0)
    glVertex2f(WINDOW_WIDTH, 0)
    glVertex2f(WINDOW_WIDTH, 350)
    glVertex2f(0, 350)
    glEnd()

    glColor3f(0.75, 0.75, 0.78)
    draw_half_circle_frame(750, 0, 350, thickness=10)
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
    draw_speedometer(770, 210, 120, speed)
    draw_rpm_meter(560, 140, 80, rpm)
    draw_fuel_meter(980, 130, 70, fuel_level)
    draw_digital_display(695, 30, 140, 40, speed, "km/h")
    draw_digital_display(910, 200, 70, 40, engine_temp, "°C")
    draw_turn_arrow(515, 280, 'left', left_blink_show)
    draw_turn_arrow(962, 280, 'right', right_blink_show)
    draw_indicator_light(1050, 50, 10, fuel_warning, (1.0, 0.0, 0.0))
    
    # Instructions
    glColor3f(0.65, 0.66, 0.68)
    draw_text(20, 20, "UP/DOWN: Speed  |  B: Brake  |  F: Refuel  |  LEFT/RIGHT: Turn Signals  |  ESC: Exit")
    
    glEnable(GL_DEPTH_TEST)

    glutSwapBuffers()

def keyboard(key, x, y):
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
    global keys_pressed
    
    if key == GLUT_KEY_UP:
        keys_pressed['up'] = False
    elif key == GLUT_KEY_DOWN:
        keys_pressed['down'] = False

def animate(value):
    global speed, target_speed, keys_pressed, camera_z, oncoming_cars, trees, clouds
    
    dt = 0.016
    
    if keys_pressed['up']:
        if target_speed < 230:
            target_speed += 3
    
    if keys_pressed['down']:
        if target_speed > 0:
            target_speed -= 3
    
    if speed < target_speed:
        speed = min(speed + 1.6, target_speed)
    elif speed > target_speed:
        speed = max(speed - 1.6, target_speed)
    
    v_ego = speed / 3.6
    camera_z += v_ego * dt
    
    for car in oncoming_cars:
        v_onc = 60 / 3.6
        car['z'] -= v_onc * dt
    
    oncoming_cars[:] = [car for car in oncoming_cars if car['z'] > camera_z - 10]
    
    if random.random() < 0.02:
        new_z = camera_z + 300 + random.uniform(0, 100)
        new_color = (random.uniform(0.5, 1), random.uniform(0, 0.5), random.uniform(0, 0.5))
        oncoming_cars.append({'x': -3, 'z': new_z, 'color': new_color})
    
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
    
    trees[:] = [tree for tree in trees if tree['z'] > camera_z - 100]
    
    for cloud in clouds:
        cloud['x'] += cloud['speed'] * dt
        if cloud['x'] > 100:
            cloud['x'] = -100
    
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)
def initialize():
    glViewport(0, 0, WINDOW_WIDTH, WINDOW_HEIGHT)
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.4, 0.6, 0.9, 1.0)  
    
    initialize_trees()
    
    initialize_clouds()
def main():
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