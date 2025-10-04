# Heating DJ - Interactive Thermal DJ System

**Version 1.1**

**Heating DJ** is an interactive thermal DJ system that translates body heat into music. Using an MLX90640 8x8 IR thermal camera, it detects temperature changes, human presence, and movement—then
  automatically controls Mixxx DJ software with scratches, tempo shifts, and track changes. Like a theremin for heat, it transforms invisible thermal patterns into live audio performance.

<img width="604" height="464" alt="image" src="https://github.com/user-attachments/assets/580783a2-2b78-4942-929b-4bb12250afe0" />

*🔥 What if your body heat could DJ the party? Interactive thermal sensing system that reads temperature changes and movement—then automatically controls music, scratches, tempo. IR camera becomes
  instrument.*

## Project Overview
- Project Name: Heating DJ
- Medium: Interactive Thermal-Responsive Installation / Generative Music Performance System
- Development Period: January - February 2023
– Technologies: MLX90640 IR Thermal Camera, Raspberry Pi, Python, Mixxx DJ Software, LED Matrix DisplayFormat: Live Installation / Performance Instrument
 
## Artistic Concept
Heating DJ transforms invisible thermal energy into tangible sonic experience. The installation uses an 8x8 infrared thermal camera to "see" heat signatures—body warmth, breath, proximity, movement—and translates these invisible fluctuations into real-time DJ automation.

What emerges is a performance where the audience becomes the instrument: their collective presence, movement, and thermal footprint directly manipulate tempo, scratching, track selection, and effects.

The work questions the boundaries between performer and audience, exploring how environmental data can become a medium for generative music. Unlike traditional interactive installations that rely on buttons, screens, or cameras, Heating DJ operates through the most fundamental human presence—heat. You cannot opt out of participation; simply being present means you are performing.

## Conceptual Framework
- Invisible Made Audible: Heat is invisible to the naked eye, yet it surrounds us constantly. Heating DJ makes thermal patterns—human presence, movement, breath—perceptible through sound. The thermal camera becomes a synesthetic translator, converting infrared radiation into musical gesture.

- Body as Score: In traditional DJ performance, the DJ reads the crowd's energy and responds. Heating DJ inverts this: the crowd's thermal energy is the score. Dancers don't just inspire the DJ—they are the DJ. Movement generates heat; heat generates change; change generates music.

- Environmental Feedback Loop:The system creates a feedback loop: people move → temperature rises → music intensifies → people move more. The installation becomes a self-regulating thermal-sonic ecosystem where participants and algorithm co-perform.


<img width="287" height="297" alt="image" src="https://github.com/user-attachments/assets/330ba2e2-c0ad-4b50-ae63-0aee08989a07" />

*Interpolatiion of thermal image processed for audio control*

## Technical Artistic Decisions
- Event Detection as Composition: Ten distinct thermal events (cooling, heating, rapid changes, movement) map to specific musical gestures. This creates a thermal vocabulary—a language where temperature becomes syntax and music becomes meaning.

- Interpolation as Aesthetics: The 8x8 sensor data is interpolated to 40x40 using cubic splines, creating smooth, organic heat maps. This mirrors the artistic intent: technological precision transformed into fluid, human-scale experience.

- Real-Time Response: Zero latency between thermal event and sonic response. The work exists in the immediate present—no recording, no delay, no replay. Every performance is unrepeatable.


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

<img width="227" height="73" alt="image" src="https://github.com/user-attachments/assets/05fce5d3-4e86-44d6-876c-fde51da68ca6" />

*Secondary communication with human over LED display*


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
Heating DJ/
├── thermal_dj/                         # Main application
│   ├── event_based_dj.py              # 🎯 MAIN: Event-driven DJ automation
│   ├── main.py                        # Full DJ system with LED display
│   └── visualize_only.py              # Visualization only (no DJ)
│
├── examples/                           # Learning & testing examples
│   ├── basic_plot.py                  # Simple thermal visualization
│   ├── interpolated_plot.py           # With cubic interpolation
│   ├── advanced_interpolation.py      # Enhanced interpolation demo
│   ├── text_overlay.py                # With temperature text overlay
│   └── interpolation_demo.py          # Standalone interpolation test
│
├── KeyboardPress/                      # DJ control library
│   └── README.md                      # Keyboard automation for Mixxx
│
├── MixxAutoDj/                        # Advanced DJ automation system
│   ├── README.md                      # File-based IPC control
│   ├── djmix_test.py                  # Complex DJ routines
│   └── mixxx_controller_src/          # C++ controller sources
│
├── serial/                            # Serial communication utilities
│   ├── README.md                      # Hardware I/O layer
│   ├── read_serial.py                 # Read thermal data
│   └── write_serial.py                # Write LED feedback
│
├── README.md                          # This file
├── CREDITS.md                         # Attribution & sources
└── LICENSE                            # GPL-3.0
```

## System Architecture

The Heating DJ project is built with a modular architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                    HEATING DJ SYSTEM                         │
└─────────────────────────────────────────────────────────────┘

    ┌───────────────┐
    │ MLX90640      │  ← Thermal Camera (8x8 IR array)
    │ Thermal Camera│
    └───────┬───────┘
            │ USB Serial (57600 baud)
            ▼
    ┌───────────────┐
    │ serial/       │  ← I/O Layer: read_serial.py
    │ (Input Layer) │     Reads 64 temp values
    └───────┬───────┘
            │
            ▼
    ┌───────────────────────────────────┐
    │ thermal_dj/                       │  ← Application Layer
    │ • event_based_dj.py (PRIMARY)     │     Event detection
    │ • main.py (Full system)           │     Statistical analysis
    │ • visualize_only.py (Test)        │     Visualization
    └───────┬───────────────────────────┘
            │
            ▼
    ┌───────────────────────────────────┐
    │ KeyboardPress/ or MixxAutoDj/     │  ← Control Layer
    │ • Simple hotkeys (real-time)      │     DJ automation
    │ • Complex routines (advanced)     │     Effect control
    └───────┬───────────────────────────┘
            │
            ▼
    ┌───────────────┐
    │ Mixxx DJ      │  ← DJ Software
    │ Software      │     Music playback
    └───────────────┘

            │
            ▼
    ┌───────────────┐
    │ serial/       │  ← I/O Layer: write_serial.py
    │ (Output Layer)│     LED feedback
    └───────┬───────┘
            │
            ▼
    ┌───────────────┐
    │ LED Matrix    │  ← Visual Feedback
    │ Display       │     Temperature display
    └───────────────┘
```

<img width="528" height="452" alt="mlx90640_test_fliplr" src="https://github.com/user-attachments/assets/ff921af8-88f0-4a35-bdb6-a5afa862c200" />

*Visualization of thermal capture*


### Component Roles:

- **[serial/](serial/)** - Hardware interface layer (thermal camera input, LED display output)
- **[thermal_dj/](thermal_dj/)** - Core application (event detection, visualization, orchestration)
- **[KeyboardPress/](KeyboardPress/)** - Simple DJ control (real-time thermal responses)
- **[MixxAutoDj/](MixxAutoDj/)** - Advanced DJ control (complex routines, precise timing)
- **[examples/](examples/)** - Learning resources (visualization techniques)

Each component has its own README with detailed documentation.

## Quick Start

### Main Application (Event-Based DJ):
```bash
python thermal_dj/event_based_dj.py
```
**Best for**: Reading pre-processed event data from Arduino/sensor that includes event status in serial[64]

### Full System (with Event Detection):
```bash
python thermal_dj/main.py
```
**Best for**: Complete system with Python-based event detection, LED display, and DJ automation

### Visualization Only:
```bash
python thermal_dj/visualize_only.py
```
**Best for**: Testing thermal camera without DJ software

## Application Documentation

### 1. `thermal_dj/event_based_dj.py` - Event-Based DJ System 🎯

**Purpose**: Main production system - reads event status from sensor and triggers DJ automation

**Key Features**:
- Reads temperature + event status from serial (65 values total)
- Event status in `serial[64]` (preprocessed by Arduino/sensor)
- Lightweight - no complex event detection in Python
- Direct DJ response based on sensor events
- Real-time thermal visualization with interpolation

**Usage**:
```bash
python thermal_dj/event_based_dj.py
```

**Event Types Read from Serial[64]**:
```python
0  = No event
1-4  = Basic temperature events
5-8  = Extreme temperature events
9    = High deviation (erratic changes)
10   = Movement detected
```

---

### 2. `thermal_dj/main.py` - Full Interactive DJ System

**Purpose**: Complete temperature-triggered DJ automation with Python-based event detection

**Features**:
- Real-time 8x8 thermal camera capture
- Cubic interpolation to 40x40 display
- **Python-based statistical event detection** (10 event types)
- Automated DJ responses to temperature events
- LED matrix text feedback
- Serial communication to display

**Usage**:
```bash
python thermal_dj/main.py
```

---

### 3. `thermal_dj/visualize_only.py` - Visualization Only

**Purpose**: Temperature visualization without DJ automation

**Use cases**:
- Testing thermal camera
- Pure data visualization
- Systems without Mixxx DJ software

**Usage**:
```bash
python thermal_dj/visualize_only.py
```

---

## Example Scripts

### `examples/basic_plot.py`
Simple thermal visualization - good starting point

### `examples/interpolated_plot.py`
Enhanced with cubic interpolation for smoother visuals

### `examples/advanced_interpolation.py`
Advanced interpolation techniques demo

### `examples/text_overlay.py`
Display temperature values with text annotations

### `examples/interpolation_demo.py`
Standalone interpolation algorithm test

---

## Event Detection System

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

## Version History

### Version 1.1 (Current)
**Released: 2025-10-01**

**Major Changes:**
- 🎯 Reorganized project structure for better maintainability
- Separated main applications (`thermal_dj/`) from learning examples (`examples/`)
- Renamed files with descriptive names instead of version numbers
- Positioned `event_based_dj.py` as the primary production application
- Improved documentation and quick start guides

**File Migrations:**
- `plot-interpolate3.py` → `thermal_dj/event_based_dj.py` (PRIMARY)
- `plotCalculate.py` → `thermal_dj/main.py`
- `plotCalculatePlotOnly.py` → `thermal_dj/visualize_only.py`
- `plot-serial-ubuntu*.py` → `examples/` folder
- `plotCameraText.py` → `examples/text_overlay.py`
- `plot-interpolate2.py` → `examples/interpolation_demo.py`

### Version 1.0
**Released: 2025-10-01**

**Initial Release:**
- Thermal DJ with event detection (plotCalculate.py)
- Multiple visualization variants
- Integrated KeyboardPress, MixxAutoDj, and serial utilities
- Original flat file structure

---

## Future Enhancements

- [ ] Machine learning for gesture recognition
- [ ] Multiple camera array for larger spaces
- [ ] 3D visualization of temperature field
- [ ] Predictive event triggering
- [ ] Cloud-based analytics
- [ ] Mobile app for remote monitoring
- [ ] Integration with lighting systems
- [ ] Recording and playback of thermal "performances"

## Credits and Attribution

This project builds upon the excellent work of the open-source thermal camera community.

### Inspired By:
- **[Maker Portal's raspi-thermal-cam](https://github.com/makerportal/raspi-thermal-cam)** (GPL-3.0) - Thermal camera visualization with cubic interpolation
- **[Adafruit MLX90640 Learning Guide](https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera)** (MIT) - Sensor interfacing patterns

### Hardware & Software:
- **MLX90640 Thermal Sensor** by Melexis
- **Mixxx DJ Software** (GPL-2.0+)
- **NumPy, Matplotlib, SciPy** - Data processing and visualization
- **PyAutoGUI, PySerial** - Hardware control and communication

### Original Contributions:
The event detection system, DJ automation integration, movement detection algorithm, and temperature-to-music mapping are original work developed for this project.

For detailed attribution, see [CREDITS.md](CREDITS.md).

## License

**GPL-3.0** - This project is licensed under the GNU General Public License v3.0, ensuring it remains open source and freely available to the community.

See [LICENSE](LICENSE) for details.
