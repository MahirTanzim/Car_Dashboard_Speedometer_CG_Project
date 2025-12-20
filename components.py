
from OpenGL.GL import *
from OpenGL.GLUT import *
import math
from algorithms import *
def draw_half_circle_frame(cx, cy, radius, thickness=12):
    for r in range(radius, radius - thickness, -1):
        x = 0
        y = r
        d = 1 - r

        while x <= y:
            draw_point(cx + x, cy + y)
            draw_point(cx + y, cy + x)

            draw_point(cx - x, cy + y)
            draw_point(cx - y, cy + x)

            if d < 0:
                d = d + 2 * x + 3
            else:
                d = d + 2 * (x - y) + 5
                y -= 1
            x += 1
def fill_half_circle_fast(cx, cy, radius, layers=40):
    step = radius // layers
    if step < 1:
        step = 1

    for r in range(radius, 0, -step):
        x = 0
        y = r
        d = 1 - r

        while x <= y:
            draw_point(cx + x, cy + y)
            draw_point(cx + y, cy + x)

            draw_point(cx - x, cy + y)
            draw_point(cx - y, cy + x)

            if d < 0:
                d += 2 * x + 3
            else:
                d += 2 * (x - y) + 5
                y -= 1
            x += 1

    

def draw_speedometer(center_x, center_y, radius, speed):
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    glColor3f(0.22, 0.22, 0.25)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    glColor3f(0.45, 0.08, 0.08)  
    for warning_speed in range(200, 240, 5):
        angle_start = 225 - (warning_speed / 230.0) * 270
        angle_end = 225 - ((warning_speed + 5) / 230.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    glLineWidth(2)
    for i in range(0, 240, 20):
        angle = 225 - (i / 230.0) * 270  
        angle_rad = math.radians(angle)
        
        glColor3f(0.88, 0.88, 0.90) if i < 200 else glColor3f(0.75, 0.25, 0.25)
        glLineWidth(3)
        ux, uy = rotate_point(radius - 18, 0.0, angle_rad)
        x1 = center_x + ux
        y1 = center_y + uy
        ux2, uy2 = rotate_point(radius - 32, 0.0, angle_rad)
        x2 = center_x + ux2
        y2 = center_y + uy2
        dda_line(int(x1), int(y1), int(x2), int(y2))
        
        glColor3f(0.82, 0.82, 0.85)
        ux_t, uy_t = rotate_point(radius - 50, 0.0, angle_rad)
        x_text = center_x + ux_t
        y_text = center_y + uy_t
        draw_number(int(x_text), int(y_text), i)
    
    glLineWidth(1)
    for i in range(10, 240, 20):  
        angle = 225 - (i / 230.0) * 270
        angle_rad = math.radians(angle)
        
        glColor3f(0.72, 0.72, 0.75)
        ux, uy = rotate_point(radius - 20, 0.0, angle_rad)
        x1 = center_x + ux
        y1 = center_y + uy
        ux2, uy2 = rotate_point(radius - 27, 0.0, angle_rad)
        x2 = center_x + ux2
        y2 = center_y + uy2
        dda_line(int(x1), int(y1), int(x2), int(y2))
    
    draw_needle_smooth(center_x, center_y, radius - 30, speed, 0, 230)
    
    glColor3f(0.6, 0.15, 0.1)  
    draw_filled_circle(9, center_x, center_y)
    glColor3f(0.75, 0.1, 0.1)  
    draw_filled_circle(5, center_x, center_y)
    
    glColor3f(0.78, 0.78, 0.80)
    draw_text(center_x - 25, center_y - 85, "SPEED")
    glColor3f(0.82, 0.82, 0.85)
    draw_text(center_x - 15, center_y - 98, "km/h")

def draw_rpm_meter(center_x, center_y, radius, rpm):
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    glColor3f(0.22, 0.20, 0.20)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    glColor3f(0.45, 0.08, 0.08)  
    for rpm_val in range(7, 9):
        angle_start = 225 - (rpm_val / 8.0) * 270
        angle_end = 225 - ((rpm_val + 0.5) / 8.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    glLineWidth(2)
    for i in range(0, 9):
        angle = 225 - (i / 8.0) * 270
        angle_rad = math.radians(angle)
        
        glColor3f(0.88, 0.88, 0.90) if i < 7 else glColor3f(0.75, 0.25, 0.25)
        glLineWidth(2.5)
        
        ux, uy = rotate_point(radius - 15, 0.0, angle_rad)
        x1 = center_x + ux
        y1 = center_y + uy
        ux2, uy2 = rotate_point(radius - 25, 0.0, angle_rad)
        x2 = center_x + ux2
        y2 = center_y + uy2
        dda_line(int(x1), int(y1), int(x2), int(y2))
        
        glColor3f(0.82, 0.82, 0.85)
        ux_t, uy_t = rotate_point(radius - 40, 0.0, angle_rad)
        x_text = center_x + ux_t
        y_text = center_y + uy_t
        draw_number(int(x_text), int(y_text), i)
    
    draw_needle_smooth(center_x, center_y, radius - 30, rpm, 0, 8)
    
    glColor3f(0.6, 0.15, 0.1)
    draw_filled_circle(7, center_x, center_y)
    glColor3f(0.75, 0.1, 0.1)
    draw_filled_circle(4, center_x, center_y)
    
    glColor3f(0.78, 0.78, 0.80)
    glColor3f(0.82, 0.82, 0.85)
    draw_text(center_x - 35, center_y - 54, "RPM x1000")

def draw_fuel_meter(center_x, center_y, radius, fuel_level):
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    glColor3f(0.22, 0.24, 0.20)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    glColor3f(0.45, 0.08, 0.08)  
    for fuel in range(0, 30, 5):
        angle_start = 225 - (fuel / 100.0) * 270
        angle_end = 225 - ((fuel + 5) / 100.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    glLineWidth(2)
    for i in range(0, 110, 25):
        angle = 225 - (i / 100.0) * 270
        angle_rad = math.radians(angle)
        
        glColor3f(0.75, 0.25, 0.25) if i < 25 else glColor3f(0.88, 0.88, 0.90)
        glLineWidth(2.5)
        
        ux, uy = rotate_point(radius - 15, 0.0, angle_rad)
        x1 = center_x + ux
        y1 = center_y + uy
        ux2, uy2 = rotate_point(radius - 25, 0.0, angle_rad)
        x2 = center_x + ux2
        y2 = center_y + uy2
        dda_line(int(x1), int(y1), int(x2), int(y2))
    
    glColor3f(0.75, 0.25, 0.25)
    draw_text(center_x - radius + 25, center_y - 10, "E")
    glColor3f(0.15, 0.60, 0.30)  
    draw_text(center_x + radius - 40, center_y - 10, "F")
    
    draw_needle_smooth(center_x, center_y, radius - 30, fuel_level, 0, 100)
    
    glColor3f(0.6, 0.15, 0.1)
    draw_filled_circle(7, center_x, center_y)
    glColor3f(0.75, 0.1, 0.1)
    draw_filled_circle(4, center_x, center_y)
    
    glColor3f(0.78, 0.78, 0.80)
    draw_text(center_x - 20, center_y -40, "FUEL %")
    glColor3f(0.82, 0.82, 0.85)

def draw_needle_smooth(cx, cy, length, value, min_val, max_val):
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))  # Clamp between 0 and 1
    angle = 225 - normalized * 270  # 225° to -45°
    angle_rad = math.radians(angle)
    
    ux_end, uy_end = rotate_point(length, 0.0, angle_rad)
    x_end = cx + ux_end
    y_end = cy + uy_end
    
    glColor3f(0.12, 0.08, 0.08)
    glLineWidth(5)
    dda_line(int(cx + 1), int(cy - 1), int(x_end + 1), int(y_end - 1))
    
    glColor3f(0.85, 0.25, 0.0)
    glLineWidth(4)
    dda_line(int(cx), int(cy), int(x_end), int(y_end))
    
    # Needle highlight (yellow)
    glColor3f(1.0, 1.0, 0.0)
    glLineWidth(2)
    dda_line(int(cx), int(cy), int(x_end * 0.7 + cx * 0.3), int(y_end * 0.7 + cy * 0.3))

def draw_arc_segment(cx, cy, radius, angle_start, angle_end):
    """Draw an arc segment (used for warning zones)"""
    steps = 20
    for i in range(steps):
        t = i / steps
        angle1 = angle_start + (angle_end - angle_start) * t
        angle2 = angle_start + (angle_end - angle_start) * ((i + 1) / steps)
        
        angle1_rad = math.radians(angle1)
        angle2_rad = math.radians(angle2)
        
        ux1, uy1 = rotate_point(radius, 0.0, angle1_rad)
        x1 = cx + ux1
        y1 = cy + uy1
        ux2, uy2 = rotate_point(radius, 0.0, angle2_rad)
        x2 = cx + ux2
        y2 = cy + uy2
        
        dda_line(int(x1), int(y1), int(x2), int(y2))

def draw_digital_display(x, y, width, height, value, label=""):
    """Draw digital display box with enhanced styling"""
    # Outer border
    glColor3f(.42, .40, .35)
    glLineWidth(3)
    dda_line(x, y, x + width, y)
    dda_line(x + width, y, x + width, y + height)
    dda_line(x + width, y + height, x, y + height)
    dda_line(x, y + height, x, y)
    
    # Inner border for depth
    glColor3f(.25, .30, .65)
    glLineWidth(2)
    dda_line(x + 2, y + 2, x + width - 2, y + 2)
    dda_line(x + width - 2, y + 2, x + width - 2, y + height - 2)
    dda_line(x + width - 2, y + height - 2, x + 2, y + height - 2)
    dda_line(x + 2, y + height - 2, x + 2, y + 2)
    
    # Value text (bright and large)
    glColor3f(0.15, 0.30, 0.35)  # Dark blue-green
    text = f"{int(value)}"
    draw_text(x + 15, y + height // 2 - 8, text)
    
    # Label text (smaller)
    glColor3f(0.50, 0.85, 0.90)  # Light cyan metallic
    draw_text(x + width - 40, y + height // 2 - 8, label)

def draw_indicator_light(x, y, radius, is_on, color):
    """Draw indicator LED light with glow effect"""
    if is_on:
        # Glow effect (larger, dimmer circle)
        glColor3f(color[0] * 0.4, color[1] * 0.4, color[2] * 0.4)
        draw_filled_circle(radius + 3, x, y)
        
        # Main LED
        glColor3f(color[0], color[1], color[2])
        draw_filled_circle(radius, x, y)
        
        # Bright spot
        glColor3f(1.0, 1.0, 1.0)
        draw_filled_circle(radius // 3, x - 2, y + 2)
    else:
        # Off state - darker
        glColor3f(0.15, 0.15, 0.15)
        draw_filled_circle(radius, x, y)
    
    # Outline
    glColor3f(0.5, 0.5, 0.5) if is_on else glColor3f(0.18, 0.18, 0.20)
    glLineWidth(2)
    midpoint_circle(radius, x, y)

def draw_turn_arrow(x, y, direction, is_on):
    """Draw turn signal arrow with enhanced styling (direction: 'left' or 'right')"""
    if is_on:
        glColor3f(0.90, 0.15, 0.15)  # Metallic red
        glLineWidth(4)
    else:
        glColor3f(0.15, 0.08, 0.08)  # Very dark red metallic
        glLineWidth(2)
    
    if direction == 'left':
        # Left arrow (thicker lines)
        dda_line(x + 20, y, x, y + 10)
        dda_line(x, y + 10, x + 20, y + 20)
        dda_line(x, y + 10, x + 30, y + 10)
    else:
        # Right arrow (thicker lines)
        dda_line(x, y, x + 20, y + 10)
        dda_line(x + 20, y + 10, x, y + 20)
        dda_line(x + 20, y + 10, x - 10, y + 10)
    
    # Add outline for better visibility when on
    if is_on:
        glColor3f(0.70, 0.65, 0.15)  # Dark yellow metallic outline
        glLineWidth(1)
        if direction == 'left':
            dda_line(x + 22, y - 2, x - 2, y + 10)
            dda_line(x - 2, y + 10, x + 22, y + 22)
            dda_line(x - 2, y + 10, x + 32, y + 10)
        else:
            dda_line(x + 2, y - 2, x + 22, y + 10)
            dda_line(x + 22, y + 10, x + 2, y + 22)
            dda_line(x + 22, y + 10, x - 8, y + 10)

def draw_text(x, y, text):
    """Draw text at position (x, y)"""
    glRasterPos2f(x, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))

def draw_number(x, y, number):
    """Draw number at position (x, y)"""
    text = str(number)
    glRasterPos2f(x - len(text) * 3, y)
    for char in text:
        glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(char))