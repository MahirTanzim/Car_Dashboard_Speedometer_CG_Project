"""
main.py - Car Dashboard Main Program
Controls the entire dashboard system
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import time
from components import *

# Global variables for dashboard state
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
# Smooth animation variables
target_speed = 0  # Smooth animation target for speed
target_fuel = 100  # Smooth animation target for fuel (for smooth refill)
blink_counter = 0  # For blinking turn signals
left_blink_time = 0  # Track when left turn was activated
right_blink_time = 0  # Track when right turn was activated

def initialize():
    """Initialize OpenGL settings"""
    glViewport(0, 0, 1000, 600)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glOrtho(0.0, 1000, 0.0, 600, 0.0, 1.0)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    glClearColor(0.0, 0.0, 0.0, 1.0)

def update_rpm():
    """Update RPM based on speed"""
    global rpm
    # RPM increases with speed (rough simulation)
    rpm = (speed / 230.0) * 7 + 0.5

def update_engine_temp():
    """Update engine temperature based on speed and RPM"""
    global engine_temp
    # Temperature increases with RPM and speed
    target_temp = 20 + (rpm * 8) + (speed * 0.2)
    if target_temp > 120:
        target_temp = 120
    
    # Gradual temperature change
    if engine_temp < target_temp:
        engine_temp += 0.5
    elif engine_temp > target_temp:
        engine_temp -= 0.3

def consume_fuel():
    """Consume fuel based on speed (not activity time)"""
    global fuel_level, fuel_consumption_counter, fuel_warning
    
    # Only consume fuel when actually moving (speed > 0)
    if speed > 0:
        fuel_consumption_counter += 1
        
        # Consume fuel every few frames based on speed
        if fuel_consumption_counter > 30:
            fuel_level -= 0.5 * (1 + speed / 100.0)  # More speed = more consumption
            fuel_consumption_counter = 0
            
            if fuel_level < 0:
                fuel_level = 0
    
    # Check fuel warning
    if fuel_level < 20:
        fuel_warning = True
    else:
        fuel_warning = False

def display():
    """Main display function"""
    global blink_counter, left_turn, right_turn, left_blink_time, right_blink_time
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glLoadIdentity()
    initialize()
    # Fill (fast)
    # glColor3f(0.10, 0.12, 0.15)
    # fill_half_circle_fast(500, 200, 350, layers=40)

    # Border
    glColor3f(0.0, 0.8, 0.9)
    draw_half_circle_frame(500, 200, 350, thickness=8)



    # Update values
    update_rpm()
    update_engine_temp()
    consume_fuel()
    blink_counter += 1
    
    # Blink effect for turn signals - blink twice (4 blinks total = 2 full cycles)
    # Each blink lasts ~250ms, total = 1 second for 2 complete on-off cycles
    current_time = time.time()
    left_blink_show = False
    right_blink_show = False
    
    if left_turn:
        time_since_left = (current_time - left_blink_time) * 1000  # Convert to ms
        # 4 states: on(0-250ms), off(250-500ms), on(500-750ms), off(750-1000ms), then auto-off
        if time_since_left < 1000:
            left_blink_show = ((int(time_since_left // 250)) % 2) == 0
        else:
            left_turn = False
    
    if right_turn:
        time_since_right = (current_time - right_blink_time) * 1000  # Convert to ms
        # 4 states: on(0-250ms), off(250-500ms), on(500-750ms), off(750-1000ms), then auto-off
        if time_since_right < 1000:
            right_blink_show = ((int(time_since_right // 250)) % 2) == 0
        else:
            right_turn = False
    
    turn_blink_left = left_blink_show
    turn_blink_right = right_blink_show
    
    # Draw dashboard title
    glColor3f(0.0, 1.0, 0.9)
    draw_text(320, 570, "=== CAR DASHBOARD SPEEDOMETER ===")
    
    # Draw main speedometer (center)
    draw_speedometer(500, 350, 120, speed)
    
    # Draw RPM meter (left)
    draw_rpm_meter(200, 350, 100, rpm)
    
    # Draw fuel meter (right)
    draw_fuel_meter(800, 350, 100, fuel_level)
    
    # Digital speed display (below speedometer)
    draw_digital_display(430, 150, 140, 40, speed, "km/h")
    
    # Engine temperature display (below RPM meter)
    draw_digital_display(130, 150, 140, 40, engine_temp, "°C")
    glColor3f(0.9, 0.9, 0.9)
    draw_text(140, 130, "Temp")
    
    # Turn signal arrows (below speedometer) - with blinking
    draw_turn_arrow(400, 100, 'left', turn_blink_left)
    draw_turn_arrow(570, 100, 'right', turn_blink_right)
    
    # Fuel warning LED (below fuel meter)
    if fuel_warning:
        draw_indicator_light(800, 150, 15, True, (1.0, 0.0, 0.0))
    else:
        draw_indicator_light(800, 150, 15, fuel_level >= 80, (0.0, 1.0, 0.0))
    
    glColor3f(0.9, 0.9, 0.9)
    draw_text(770, 130, "Fuel")
    
    # Instructions
    glColor3f(0.5, 0.8, 0.9)
    draw_text(10, 50, "UP/DOWN: Speed  |  B: Brake  |  F: Refuel  |  LEFT/RIGHT: Turn Signals  |  ESC: Exit")
    
    glutSwapBuffers()

def keyboard(key, x, y):
    """Handle keyboard input"""
    global speed, fuel_level, target_fuel, left_turn, right_turn, fuel_warning, last_activity_time
    
    last_activity_time = time.time()
    
    # Speed up
    if key == b'\x1b':  # ESC key
        glutLeaveMainLoop()
    
    # Brake
    if key == b'b' or key == b'B':
        speed = max(0, speed - 20)
    
    # Refuel - set target fuel to 100 for smooth transition
    if key == b'f' or key == b'F':
        target_fuel = 100  # Fuel will gradually increase to 100
        fuel_warning = False

def special_keys(key, x, y):
    """Handle special keys (arrow keys) with slow smooth acceleration"""
    global speed, target_speed, left_turn, right_turn, last_activity_time, left_blink_time, right_blink_time
    
    last_activity_time = time.time()
    
    if key == GLUT_KEY_UP:
        # Speed up with very smooth acceleration (slower increments)
        if target_speed < 230:
            target_speed = min(target_speed + 5, 230)  # Reduced from 10 to 5 for slower key response
    
    elif key == GLUT_KEY_DOWN:
        # Slow down (slower decrements)
        if target_speed > 0:
            target_speed = max(target_speed - 5, 0)  # Reduced from 10 to 5 for slower key response
    
    elif key == GLUT_KEY_LEFT:
        # Activate left turn signal and start blink timer
        if not left_turn:
            left_turn = True
            left_blink_time = time.time()  # Record activation time
            right_turn = False  # Turn off right turn
    
    elif key == GLUT_KEY_RIGHT:
        # Activate right turn signal and start blink timer
        if not right_turn:
            right_turn = True
            right_blink_time = time.time()  # Record activation time
            left_turn = False  # Turn off left turn
    
    glutPostRedisplay()

def animate(value):
    """Animation timer function with extra smooth speed transitions"""
    global speed, target_speed
    
    # Speed animation with faster needle movement
    # Increased increments for quicker gauge response
    if speed < target_speed:
        speed = min(speed + 1.2, target_speed)  # Increased from 0.3 for faster acceleration
    elif speed > target_speed:
        speed = max(speed - 1.5, target_speed)  # Increased from 0.5 for faster deceleration
    
    glutPostRedisplay()
    glutTimerFunc(16, animate, 0)  # ~60 FPS

def main():
    """Main function"""
    global last_activity_time
    last_activity_time = time.time()
    
    glutInit()
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(1000, 600)
    glutInitWindowPosition(100, 100)
    wind = glutCreateWindow(b"Car Dashboard Speedometer")
    
    glutDisplayFunc(display)
    glutKeyboardFunc(keyboard)
    glutSpecialFunc(special_keys)
    glutTimerFunc(0, animate, 0)
    
    glutMainLoop()

if __name__ == "__main__":
    main()
    