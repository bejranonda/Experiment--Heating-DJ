# Heating DJ - Interactive Thermal DJ System

Real-time thermal camera visualization with intelligent DJ automation that responds to temperature changes and human presence.

## Project Overview

This project combines thermal imaging with automated DJ control to create an interactive art installation or performance system. Temperature sensors detect environmental changes, human presence, and movement, triggering corresponding DJ effects, track changes, and visual feedback. The system "sees" heat and translates it into music and visuals.

## How It Works

1. **Thermal camera** (MLX90640 8x8 array) captures temperature data
2. **Real-time visualization** displays interpolated heat map
3. **Statistical analysis** detects significant temperature events
4. **DJ automation** responds with music changes and effects
5. **LED matrix** provides visual feedback of temperature readings

## Related Projects

**Integrates with**:
- **`/MixxAutoDj/`** - Uses DJ automation functions
- **`/KeyboardPress/`** - Keyboard control library for Mixxx
- **`/serial/`** - Sensor communication utilities
- **Standalone** - Can also run without DJ integration for pure visualization

## Hardware Requirements

### Essential:
- **Raspberry Pi 3/4** or Ubuntu PC
- **MLX90640 Thermal Camera** (8x8 IR array)
- **USB-Serial adapter** for sensor communication
- **LED Matrix display** (optional, for text feedback)

### Optional:
- **Arduino** for sensor preprocessing
- **Additional sensors** (electromagnetic, light, etc.)

## Software Dependencies

```bash
# Core libraries
pip install numpy matplotlib scipy
pip install pyserial
pip install pyautogui  # For DJ control
pip install scikit-image  # For interpolation

# Platform-specific
# Raspberry Pi:
pip install RPi.GPIO

# Ubuntu:
# No GPIO needed
```

## Project Structure

```
PlotTemperature/
├── README.md
├── plotCalculate.py                    # Main: Temperature + DJ automation
├── plotCalculatePlotOnly.py            # Visualization only (no DJ)
├── plotCameraText.py                   # With text display
├── plot-serial-ubuntu.py               # Basic Ubuntu version
├── plot-serial-ubuntu-interpolate.py   # With interpolation
├── plot-serial-ubuntu-interpolate2.py  # Enhanced interpolation
├── plot-interpolate2.py                # Standalone interpolation demo
└── plot-interpolate3.py                # Advanced interpolation
```

## Script Documentation

### 1. `plotCalculate.py` - Full Interactive DJ System ⭐

**Purpose**: Complete temperature-triggered DJ automation with visualization

**Features**:
- Real-time 8x8 thermal camera capture
- Cubic interpolation to 40x40 display
- Statistical event detection (9 event types)
- Automated DJ responses to temperature events
- LED matrix text feedback
- Serial communication to display

**Event Detection System**:

```python
# Event Types (loop_status values)
0  = No event
1  = Temperature minimum decreased (cooling)
2  = Temperature maximum increased (heating)
3  = Negative temperature change (rapid cool)
4  = Positive temperature change (rapid heat)
5  = Extreme cooling (> 90% threshold)
6  = Extreme heating (> 110% threshold)
7  = Extreme negative change
8  = Extreme positive change
9  = High deviation (erratic changes)
10 = Movement detected (deviation + low overall change)
```

**DJ Response Map**:
```python
if loop_status == 1:  # Cooling
    write_serial("Cool ..    ,6")
    tempo_slow()

if loop_status == 2:  # Heating
    write_serial("Hot  ..    ,5")
    tempo_fast()

if loop_status == 3:  # Rapid cool
    write_serial("Go        ,4")
    scratch(3, 2, loop_on, 1)

if loop_status == 9:  # Movement
    write_serial("Nowwww        ,p1")  # 'p' = pacman icon
    sync_tempo(3)
    auto_next()

if loop_status == 10:  # Complex movement
    write_serial("We    move    ,p1")
    sync_tempo(3)
    auto_next()
```

**Configuration Parameters**:
```python
# Event Detection Thresholds
min_threshold = 0.9               # Cool event: 90% of previous min
max_threshold = 1.2               # Heat event: 120% of previous max
negative_dif_threshold = 1.05     # Rapid cool: 5% faster
positive_dif_threshold = 1.05     # Rapid heat: 5% faster
extreme_lower_threshold = 0.9     # Extreme cool: 90% of threshold
extreme_upper_threshold = 1.1     # Extreme heat: 110% of threshold
abs_deviation_threshold = 20      # Pixel change threshold
moving_deviation_factor = 0.5     # Movement vs temperature change

# Event Loop Settings
event_loop_limit = 10             # Samples before threshold reset
play_loop_limit = 20              # Minimum loops between actions
```

**Serial Communication**:

To LED matrix display:
```python
write_serial("text,delay")        # Display text with delay
write_serial("text,p3")           # Show pacman, then text, delay 3
write_serial("25.5 c      <        <     ,3")  # Show temperature
```

**Usage**:
```bash
# Configure serial ports
# Sensor input: /dev/ttyUSB0 @ 57600
# LED output: /dev/ttyUSB1 @ 57600

python plotCalculate.py
```

**How It Works**:

```
┌─────────────────┐
│  Thermal Camera │ (8x8 pixels)
└────────┬────────┘
         │ Serial @ 57600
         ▼
┌─────────────────┐
│  Read & Parse   │ 64 temperature values
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Interpolate    │ Cubic → 40x40 pixels
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Matplotlib    │ Heat map display
│   Visualization │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Statistical   │ Compare to baseline
│    Analysis     │ Detect events
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  DJ Automation  │ Trigger effects
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  LED Display    │ Text feedback
└─────────────────┘
```

---

### 2. `plotCalculatePlotOnly.py` - Visualization Only

**Purpose**: Temperature visualization without DJ automation

**Use cases**:
- Testing thermal camera
- Pure data visualization
- Systems without Mixxx

**Differences**:
- No pyautogui import
- No DJ functions
- Lightweight for embedded systems

---

### 3. `plot-serial-ubuntu.py` - Basic Ubuntu Version

**Purpose**: Simple temperature plotting for Ubuntu

**Features**:
- Basic matplotlib plotting
- No GPIO requirements
- Good starting point

**Usage**:
```bash
python plot-serial-ubuntu.py
```

---

### 4. `plot-serial-ubuntu-interpolate.py` - Interpolated Display

**Purpose**: Enhanced Ubuntu version with smooth interpolation

**Features**:
- Scipy cubic interpolation
- 8x8 → 40x40 upscaling
- Smoother heat maps
- Better visualization of gradients

**Interpolation Method**:
```python
from scipy import interpolate

# Original 8x8 grid
xx, yy = np.linspace(0, 8, 8), np.linspace(0, 8, 8)

# Interpolate to 40x40
grid_x = np.linspace(0, 8, 40)
grid_y = np.linspace(0, 8, 40)

# Cubic interpolation
f = interpolate.interp2d(xx, yy, frame, kind='cubic')
smooth_frame = f(grid_x, grid_y)
```

---

### 5. `plot-interpolate2.py` & `plot-interpolate3.py` - Enhanced Interpolation

**Purpose**: Advanced interpolation techniques

**Additional features**:
- Alternative interpolation methods
- Performance optimizations
- Different visualization approaches

---

### 6. `plotCameraText.py` - With Text Overlay

**Purpose**: Display temperature values with text annotations

**Features**:
- Numeric overlay on heat map
- Average temperature display
- Per-pixel temperature values

---

## Temperature Data Format

**Serial Input Format**:
```
temp0,temp1,temp2,...,temp63\n
```

**Example** (8x8 = 64 values):
```
23.5,23.6,23.7,24.1,24.5,25.0,25.5,25.2,
23.4,23.8,24.2,24.8,25.5,26.0,25.8,25.0,
...
22.8,22.9,23.0,23.2,23.5,23.8,23.6,23.3
```

## Arduino Thermal Camera Code

```cpp
#include <Adafruit_MLX90640.h>

Adafruit_MLX90640 mlx;
float frame[32*24];  // MLX90640 buffer

void setup() {
  Serial.begin(57600);
  mlx.begin(MLX90640_I2CADDR_DEFAULT, &Wire);
  mlx.setMode(MLX90640_CHESS);
  mlx.setResolution(MLX90640_ADC_18BIT);
  mlx.setRefreshRate(MLX90640_2_HZ);
}

void loop() {
  if (mlx.getFrame(frame) == 0) {
    // Send 8x8 subset (or full 32x24)
    for (int i = 0; i < 64; i++) {
      Serial.print(frame[i]);
      if (i < 63) Serial.print(",");
    }
    Serial.println();
  }
  delay(500);
}
```

## Event Detection Algorithm

### Temperature Event Detection:

```python
# Track min/max over event_loop_limit samples
event_loop_max = -100
event_loop_min = 100

# For each frame:
this_loop_max = max(all_pixels)
this_loop_min = min(all_pixels)

# Compare to baseline
if this_loop_min < event_loop_min * min_threshold:
    trigger_cooling_event()
    event_loop_min = this_loop_min  # New baseline

if this_loop_max > event_loop_max * max_threshold:
    trigger_heating_event()
    event_loop_max = this_loop_max
```

### Movement Detection:

```python
# Calculate per-pixel changes
deviation = 0
abs_deviation = 0
for each pixel:
    diff = current[i] - previous[i]
    deviation += diff
    abs_deviation += abs(diff)

# High absolute but low net change = movement
if abs_deviation > threshold:
    if abs_deviation * moving_factor > abs(deviation):
        trigger_movement_event()  # Someone moved!
    else:
        trigger_temperature_event()  # Overall temp changed
```

## DJ Function Integration

Functions from `/KeyboardPress/press_mixxx2.py`:

```python
# Tempo Control
tempo_slow(deck=3, loops=4, delay=1)    # Gradual slowdown
tempo_fast(deck=3, loops=4, delay=1)    # Gradual speedup

# Effects
scratch(deck, delay, loop_on, depth=3)  # Scratch effect
sync_tempo(3)                           # Sync all decks
auto_next()                             # Load next track
auto_toggle()                           # Start AutoDJ

# Loops
loop_activate(deck, status)             # Set loop points
loop_halve(deck)                        # Halve loop length
loop_double(deck)                       # Double loop length
```

## Visualization Settings

```python
# Color map options
cmap_use = "jet"        # Rainbow colors
cmap_use = "hot"        # Fire colors
cmap_use = "coolwarm"   # Blue-white-red
cmap_use = "viridis"    # Perceptually uniform

# Temperature range
im1.set_clim(vmin=18, vmax=37)  # Human comfort range
im1.set_clim(vmin=10, vmax=25)  # Room temperature
im1.set_clim(vmin=20, vmax=30)  # Narrow range (more sensitive)

# Figure size
fig_dims = (2,2)   # Small window
fig_dims = (12,9)  # Large display
```

## Performance Optimization

### Blitting for Speed:
```python
# Save background
ax_bgnd = fig.canvas.copy_from_bbox(ax.bbox)

# In loop:
fig.canvas.restore_region(ax_bgnd)  # Restore background
im1.set_data(new_data)              # Update only image
ax.draw_artist(im1)                 # Draw only image
fig.canvas.blit(ax.bbox)            # Fast blit
fig.canvas.flush_events()
```

### Serial Buffer Management:
```python
ser.flushInput()  # Clear buffer after each read
# Prevents lag from accumulated data
```

## Troubleshooting

### No temperature data:
```bash
# Check serial devices
ls -l /dev/ttyUSB*

# Test serial connection
python -m serial.tools.miniterm /dev/ttyUSB0 57600

# Check permissions
sudo usermod -a -G dialout $USER
```

### Matplotlib not displaying:
```python
# Ensure interactive mode
plt.ion()

# Or use blocking show
plt.show(block=True)
```

### Interpolation artifacts:
```python
# Try different interpolation methods
kind='cubic'    # Smooth but can overshoot
kind='linear'   # Faster, less smooth
kind='quintic'  # Very smooth, slower
```

### Event detection too sensitive:
```python
# Increase thresholds
min_threshold = 0.85  # More tolerance
max_threshold = 1.3   # Less sensitive

# Or increase event_loop_limit
event_loop_limit = 20  # Average over more samples
```

## Use Cases

1. **Interactive Art Installation**
   - Responds to audience presence
   - Music changes based on crowd density
   - Visual feedback of thermal patterns

2. **Performance Art**
   - Dancer's movements control music
   - Body heat triggers effects
   - Proximity-based interactions

3. **Accessibility Tool**
   - Thermal data sonification
   - Non-visual environment sensing
   - Presence detection

4. **Smart DJ System**
   - Crowd energy detection
   - Auto-adjust music intensity
   - Temperature-based playlist selection

5. **Security/Monitoring**
   - Presence detection
   - Activity logging
   - Thermal anomaly detection

## Advanced Configurations

### Multiple Sensor Zones:
```python
# Divide 8x8 into quadrants
zone1 = frame[0:4, 0:4]   # Top-left
zone2 = frame[0:4, 4:8]   # Top-right
zone3 = frame[4:8, 0:4]   # Bottom-left
zone4 = frame[4:8, 4:8]   # Bottom-right

# Different responses per zone
if max(zone1) > threshold:
    trigger_effect_1()
if max(zone2) > threshold:
    trigger_effect_2()
```

### Time-Based Behavior:
```python
import datetime

hour = datetime.datetime.now().hour

if 22 <= hour or hour < 6:  # Night mode
    # Calmer responses
    sensitivity = 0.5
else:  # Day mode
    # More active
    sensitivity = 1.0
```

### Network Logging:
```python
import requests

# Send to web service
data = {
    'timestamp': time.time(),
    'temperature': avg_temp,
    'event': loop_status
}
requests.post('http://your-server/api/log', json=data)
```

## Safety Considerations

⚠️ **Important**:
- MLX90640 can get warm during operation (normal)
- Keep sensor away from direct sunlight
- Calibrate temperature ranges for your environment
- Test thresholds before live performance
- Have manual override for DJ automation

## Future Enhancements

- [ ] Machine learning for gesture recognition
- [ ] Multiple camera array for larger spaces
- [ ] 3D visualization of temperature field
- [ ] Predictive event triggering
- [ ] Cloud-based analytics
- [ ] Mobile app for remote monitoring
- [ ] Integration with lighting systems
- [ ] Recording and playback of thermal "performances"

## Credits

- MLX90640 thermal camera by Melexis
- Matplotlib for visualization
- Scipy for interpolation
- Integration with Mixxx DJ software

## License

Open source - create your own thermal interactive experiences!