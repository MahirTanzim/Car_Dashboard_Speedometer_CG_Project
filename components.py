"""
components.py - Dashboard component drawing functions
Contains: Speedometer, RPM meter, Fuel meter, indicators, displays
"""

from OpenGL.GL import *
from OpenGL.GLUT import *
import math
from algorithms import midpoint_circle, dda_line, draw_filled_circle

def draw_speedometer(center_x, center_y, radius, speed):
    """Draw speedometer gauge (0-230 km/h) with warning zone"""
    # Outer circle (dark border)
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    # Background ring (creates depth)
    glColor3f(0.15, 0.15, 0.18)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    # Draw warning zone (200-230 in red)
    glColor3f(0.4, 0.0, 0.0)  # Dark red for warning zone
    for warning_speed in range(200, 240, 5):
        angle_start = 225 - (warning_speed / 230.0) * 270
        angle_end = 225 - ((warning_speed + 5) / 230.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    # Draw tick marks and numbers (0-230)
    glLineWidth(2)
    for i in range(0, 240, 10):
        angle = 225 - (i / 230.0) * 270  # 225° to -45°
        angle_rad = math.radians(angle)
        
        # Tick marks - color based on speed range
        if i % 20 == 0:
            glColor3f(1.0, 1.0, 1.0) if i < 200 else glColor3f(1.0, 0.3, 0.3)
            glLineWidth(2.5)
            x1 = center_x + (radius - 15) * math.cos(angle_rad)
            y1 = center_y + (radius - 15) * math.sin(angle_rad)
            x2 = center_x + (radius - 25) * math.cos(angle_rad)
            y2 = center_y + (radius - 25) * math.sin(angle_rad)
            dda_line(int(x1), int(y1), int(x2), int(y2))
            
            # Numbers
            if i % 40 == 0:
                glColor3f(0.9, 0.9, 0.9)
                x_text = center_x + (radius - 40) * math.cos(angle_rad)
                y_text = center_y + (radius - 40) * math.sin(angle_rad)
                draw_number(int(x_text), int(y_text), i)
    
    # Draw needle with smooth appearance
    draw_needle_smooth(center_x, center_y, radius - 30, speed, 0, 230)
    
    # Center dot with glow
    glColor3f(1.0, 0.5, 0.0)  # Orange outer
    draw_filled_circle(7, center_x, center_y)
    glColor3f(1.0, 0.0, 0.0)  # Red inner
    draw_filled_circle(4, center_x, center_y)
    
    # Label
    glColor3f(0.0, 1.0, 0.8)
    draw_text(center_x - 20, center_y - 65, "SPEED")
    glColor3f(0.9, 0.9, 0.9)
    draw_text(center_x - 10, center_y - 75, "km/h")

def draw_rpm_meter(center_x, center_y, radius, rpm):
    """Draw RPM meter (0-8 x1000 RPM) with redline zone"""
    # Outer circle (dark border)
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    # Background ring
    glColor3f(0.18, 0.15, 0.15)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    # Draw redline zone (7-8 in red)
    glColor3f(0.4, 0.0, 0.0)  # Dark red
    for rpm_val in range(7, 9):
        angle_start = 225 - (rpm_val / 8.0) * 270
        angle_end = 225 - ((rpm_val + 0.5) / 8.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    # Draw tick marks
    glLineWidth(2)
    for i in range(0, 9):
        angle = 225 - (i / 8.0) * 270
        angle_rad = math.radians(angle)
        
        # Color based on redline
        glColor3f(1.0, 1.0, 1.0) if i < 7 else glColor3f(1.0, 0.3, 0.3)
        glLineWidth(2.5)
        
        x1 = center_x + (radius - 15) * math.cos(angle_rad)
        y1 = center_y + (radius - 15) * math.sin(angle_rad)
        x2 = center_x + (radius - 25) * math.cos(angle_rad)
        y2 = center_y + (radius - 25) * math.sin(angle_rad)
        dda_line(int(x1), int(y1), int(x2), int(y2))
        
        # Numbers
        glColor3f(0.9, 0.9, 0.9)
        x_text = center_x + (radius - 40) * math.cos(angle_rad)
        y_text = center_y + (radius - 40) * math.sin(angle_rad)
        draw_number(int(x_text), int(y_text), i)
    
    # Draw needle with smooth animation
    draw_needle_smooth(center_x, center_y, radius - 30, rpm, 0, 8)
    
    # Center dot
    glColor3f(1.0, 0.5, 0.0)
    draw_filled_circle(7, center_x, center_y)
    glColor3f(1.0, 0.0, 0.0)
    draw_filled_circle(4, center_x, center_y)
    
    # Label
    glColor3f(0.0, 1.0, 0.8)
    draw_text(center_x - 25, center_y - 65, "ENGINE")
    glColor3f(0.9, 0.9, 0.9)
    draw_text(center_x - 35, center_y - 75, "RPM x1000")

def draw_fuel_meter(center_x, center_y, radius, fuel_level):
    """Draw fuel meter (0-100%) with low fuel warning zone"""
    # Outer circle (dark border)
    glColor3f(0.1, 0.1, 0.1)
    glLineWidth(3)
    midpoint_circle(radius, center_x, center_y)
    
    # Background ring
    glColor3f(0.15, 0.18, 0.15)
    for r in range(radius - 3, radius - 10, -1):
        midpoint_circle(r, center_x, center_y)
    
    # Draw low fuel warning zone (0-25% in red)
    glColor3f(0.4, 0.0, 0.0)  # Dark red
    for fuel in range(0, 30, 5):
        angle_start = 225 - (fuel / 100.0) * 270
        angle_end = 225 - ((fuel + 5) / 100.0) * 270
        draw_arc_segment(center_x, center_y, radius - 12, angle_start, angle_end)
    
    # Draw tick marks and labels
    glLineWidth(2)
    for i in range(0, 110, 25):
        angle = 225 - (i / 100.0) * 270
        angle_rad = math.radians(angle)
        
        # Color based on fuel level
        glColor3f(1.0, 0.3, 0.3) if i < 25 else glColor3f(1.0, 1.0, 1.0)
        glLineWidth(2.5)
        
        x1 = center_x + (radius - 15) * math.cos(angle_rad)
        y1 = center_y + (radius - 15) * math.sin(angle_rad)
        x2 = center_x + (radius - 25) * math.cos(angle_rad)
        y2 = center_y + (radius - 25) * math.sin(angle_rad)
        dda_line(int(x1), int(y1), int(x2), int(y2))
    
    # E and F labels
    glColor3f(1.0, 0.3, 0.3)  # Red for E (empty)
    draw_text(center_x - radius + 25, center_y - 10, "E")
    glColor3f(0.0, 1.0, 0.5)  # Green for F (full)
    draw_text(center_x + radius - 40, center_y - 10, "F")
    
    # Draw needle with smooth animation
    draw_needle_smooth(center_x, center_y, radius - 30, fuel_level, 0, 100)
    
    # Center dot
    glColor3f(1.0, 0.5, 0.0)
    draw_filled_circle(7, center_x, center_y)
    glColor3f(1.0, 0.0, 0.0)
    draw_filled_circle(4, center_x, center_y)
    
    # Label
    glColor3f(0.0, 1.0, 0.8)
    draw_text(center_x - 15, center_y - 65, "FUEL")
    glColor3f(0.9, 0.9, 0.9)
    draw_text(center_x - 10, center_y - 75, "%")

def draw_needle_smooth(cx, cy, length, value, min_val, max_val):
    """Draw gauge needle with enhanced appearance"""
    # Calculate angle based on value
    normalized = (value - min_val) / (max_val - min_val)
    normalized = max(0, min(1, normalized))  # Clamp between 0 and 1
    angle = 225 - normalized * 270  # 225° to -45°
    angle_rad = math.radians(angle)
    
    x_end = cx + length * math.cos(angle_rad)
    y_end = cy + length * math.sin(angle_rad)
    
    # Needle shadow (slightly offset, dark)
    glColor3f(0.1, 0.0, 0.0)
    glLineWidth(5)
    dda_line(int(cx + 1), int(cy - 1), int(x_end + 1), int(y_end - 1))
    
    # Main needle (orange-red)
    glColor3f(1.0, 0.2, 0.0)
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
        
        x1 = cx + radius * math.cos(angle1_rad)
        y1 = cy + radius * math.sin(angle1_rad)
        x2 = cx + radius * math.cos(angle2_rad)
        y2 = cy + radius * math.sin(angle2_rad)
        
        dda_line(int(x1), int(y1), int(x2), int(y2))

def draw_digital_display(x, y, width, height, value, label=""):
    """Draw digital display box with enhanced styling"""
    # Outer border
    glColor3f(0.0, 0.7, 0.9)
    glLineWidth(3)
    dda_line(x, y, x + width, y)
    dda_line(x + width, y, x + width, y + height)
    dda_line(x + width, y + height, x, y + height)
    dda_line(x, y + height, x, y)
    
    # Inner border for depth
    glColor3f(0.0, 0.5, 0.7)
    glLineWidth(1)
    dda_line(x + 2, y + 2, x + width - 2, y + 2)
    dda_line(x + width - 2, y + 2, x + width - 2, y + height - 2)
    dda_line(x + width - 2, y + height - 2, x + 2, y + height - 2)
    dda_line(x + 2, y + height - 2, x + 2, y + 2)
    
    # Value text (bright and large)
    glColor3f(0.0, 1.0, 1.0)  # Cyan
    text = f"{int(value)}"
    draw_text(x + 15, y + height // 2 - 8, text)
    
    # Label text (smaller)
    glColor3f(0.5, 1.0, 1.0)  # Light cyan
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
    glColor3f(0.4, 0.4, 0.4) if is_on else glColor3f(0.2, 0.2, 0.2)
    glLineWidth(2)
    midpoint_circle(radius, x, y)

def draw_turn_arrow(x, y, direction, is_on):
    """Draw turn signal arrow with enhanced styling (direction: 'left' or 'right')"""
    if is_on:
        glColor3f(1.0, 0.0, 0.0)  # Bright red
        glLineWidth(4)
    else:
        glColor3f(0.2, 0.1, 0.1)  # Very dark red
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
        glColor3f(1.0, 1.0, 0.0)  # Yellow outline
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