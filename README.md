# Car Dashboard Speedometer - Python OpenGL Project

A computer graphics project showcasing an interactive car dashboard built with Python and OpenGL. Features a realistic speedometer, RPM meter, fuel gauge, and engine temperature display.

## Features

### 🚗 Dashboard Gauges
- **Speedometer** (0-230 km/h): Main gauge with warning zone (200-230 in red)
- **RPM Meter** (0-8 x1000): Engine RPM with redline warning zone (7-8 in red)
- **Fuel Meter** (0-100%): Fuel level with low fuel warning zone (0-25% in red)

### 📊 Digital Displays
- **Speed Display**: Real-time speed in km/h
- **Engine Temperature Display**: Temperature in °C with smooth transitions
- **Warning Indicators**: LED lights for fuel status (red when low, green when normal)

### 🎮 Interactive Controls
- **Arrow Up**: Accelerate (smooth acceleration)
- **Arrow Down**: Decelerate (smooth braking)
- **Left Arrow**: Toggle left turn signal (blinking red)
- **Right Arrow**: Toggle right turn signal (blinking red)
- **B / b**: Emergency brake (instant speed reduction)
- **F / f**: Refuel (restores fuel to 100%)
- **ESC**: Exit application

### ✨ Visual Enhancements
- **Smooth Needle Animation**: Needles smoothly transition to new values
- **Blinking Turn Signals**: Turn arrows blink when activated
- **Warning Zones**: Visual danger zones (red) on gauges
- **Glow Effects**: LED indicators have glow effects
- **Color-Coded Gauges**: Different colors for safe vs. warning ranges
- **Digital-Style Displays**: Cyan-colored digital readouts

### 🔧 System Features
- **Fuel Consumption**: Fuel decreases based on speed and driving duration
- **Engine Temperature**: Temperature increases with RPM, cools when idle
- **Smooth Transitions**: All values animate smoothly for realistic feel
- **60 FPS Rendering**: Smooth 60 frames-per-second animation

## Installation

### Prerequisites
- Python 3.6 or higher
- OpenGL support

### Setup Instructions

1. **Clone or download the project**
   ```powershell
   cd Car_Dashboard_Speedometer_CG_Project
   ```

2. **Create and activate virtual environment** (Windows PowerShell)
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install PyOpenGL PyOpenGL_accelerate
   ```

4. **Windows GLUT Setup** (if needed)
   - Download freeglut from: http://freeglut.sourceforge.net/
   - Extract and find `freeglut.dll`
   - Place `freeglut.dll` in your system PATH or project root directory

## Running the Application

```powershell
# Ensure virtual environment is activated
python main.py
```

The dashboard window will open at 1000x600 pixels. Use the controls listed above to interact with the dashboard.

## Project Structure

```
Car_Dashboard_Speedometer_CG_Project/
├── main.py              # Main application (initialization, event handling, display loop)
├── components.py        # Dashboard drawing functions (gauges, displays, indicators)
├── algorithms.py        # Core graphics algorithms (DDA line, Midpoint circle)
├── display.py          # (Optional) Display utilities
├── README.md           # This file
└── .gitignore          # Git ignore file
```

## Code Overview

### main.py
- Initializes OpenGL window
- Manages global state (speed, RPM, fuel, temperature)
- Handles keyboard input
- Updates gauge values based on simulation
- Calls display functions from components

### components.py
- `draw_speedometer()`: Main speed gauge
- `draw_rpm_meter()`: Engine RPM gauge
- `draw_fuel_meter()`: Fuel level gauge
- `draw_digital_display()`: Digital value displays
- `draw_needle_smooth()`: Animated gauge needles
- `draw_turn_arrow()`: Turn signal indicators
- `draw_indicator_light()`: LED-style warning lights

### algorithms.py
- `dda_line()`: Digital Differential Analyzer for line drawing
- `midpoint_circle()`: Midpoint circle algorithm for circle drawing
- `draw_filled_circle()`: Filled circle rendering

## Technical Details

### Graphics Algorithms Used
- **DDA (Digital Differential Analyzer)**: Efficient line rasterization
- **Midpoint Circle Algorithm**: Accurate circle rendering using integer arithmetic
- **2D Orthographic Projection**: Flat dashboard view

### Key Implementation Concepts
- **OpenGL State Machine**: Managing colors, line widths, transformations
- **Animation Loop**: Timer-based updates for smooth motion
- **Global State Management**: Tracking dashboard values and user inputs
- **Blinking Effect**: Counter-based visual feedback for turn signals

## Customization Ideas

### Easy Enhancements
1. Change gauge ranges (max speed, max RPM)
2. Adjust fuel consumption rate
3. Modify colors in `draw_*` functions
4. Add more warning zones to gauges
5. Increase window size in `glutInitWindowSize()`

### Advanced Features
1. Add sound effects for turn signals
2. Implement multiple gauge themes
3. Add data logging to CSV file
4. Create multi-screen dashboard views
5. Add warning messages for overheating

## Learning Outcomes

This project demonstrates:
- **Computer Graphics Fundamentals**: Line and circle algorithms, transformations
- **OpenGL/GLUT Programming**: Window management, rendering pipeline
- **Real-time Animation**: Timer-based updates, smooth transitions
- **User Interaction**: Keyboard input handling
- **State Management**: Tracking and updating multiple values
- **Software Architecture**: Modular design with separate concerns (graphics, logic, display)

## Troubleshooting

### "ModuleNotFoundError: No module named 'OpenGL'"
```powershell
pip install PyOpenGL
```

### "GLUT Error: ... freeglut.dll not found"
- Download freeglut.dll
- Place in system PATH (e.g., C:\Windows\System32) or project root
- Restart the application

### "Window doesn't appear"
- Ensure you have a compatible graphics card
- Try running from command line to see error messages
- Check if OpenGL is installed: `python -m OpenGL.tests`

### Poor performance / Low FPS
- Reduce window size in main.py
- Disable PyOpenGL error checking: `os.environ['PYOPENGL_PLATFORM'] = 'osmesa'`

## Author
Created as a Computer Graphics course project

## License
Open source - feel free to modify and distribute

---

**Happy Coding! 🚗💨**
