# KeyboardPress - DJ Control Automation Library

> Part of the **[Heating DJ](../README.md)** project - An interactive thermal DJ system that translates heat into music.

Python library for automating Mixxx DJ software control through keyboard shortcuts. This is the **control layer** that enables the Heating DJ system to trigger DJ effects, tempo changes, and track transitions in response to thermal events.

## Role in Heating DJ

This library provides the bridge between temperature sensor events and DJ actions:

1. **Thermal Event** detected → 2. **KeyboardPress function** called → 3. **Mixxx responds** with music change

**Used by:**
- [`thermal_dj/main.py`](../thermal_dj/main.py) - Temperature-triggered DJ automation
- [`thermal_dj/event_based_dj.py`](../thermal_dj/event_based_dj.py) - Event-driven DJ system
- [`MixxAutoDj/`](../MixxAutoDj/) - Advanced automated DJ routines

## How It Works

When the thermal camera detects movement or temperature changes, the Heating DJ system calls these functions to control the music in real-time.

## Dependencies

```bash
pip install pyautogui    # Keyboard automation
pip install pykeyboard   # Alternative keyboard control (press_key.py only)
```

## Scripts Overview

```
KeyboardPress/
├── README.md
├── press_key.py          # Simple keyboard test
├── press_key2.py         # Alt+Tab demo
├── press_mixxx.py        # Full Mixxx control library
└── press_mixxx2.py       # Enhanced version with effects
```

## Script Documentation

### 1. `press_key.py` - Basic Key Press

**Purpose**: Simple keyboard automation test

**Usage**:
```python
from pykeyboard import PyKeyboard
k = PyKeyboard()

k.press_key(k.alt_key)
k.tap_key(k.tab_key)
k.release_key(k.alt_key)
```

**Use case**: Testing keyboard automation setup

---

### 2. `press_mixxx.py` - Core Mixxx Control Library

**Purpose**: Complete Mixxx DJ automation function library

#### Basic Controls

```python
# Track Loading
load_track(deck)           # Load selected track to deck (1, 2, or 3=both)
# Shift+Left (deck 1), Shift+Right (deck 2)

# Playback
play(deck)                 # Play/pause deck
# D (deck 1), L (deck 2)

# Tempo Control
tab_tempo(deck)            # Tap tempo
sync_tempo(deck)           # Sync to other deck
# 1 (deck 1), 6 (deck 2)
```

#### Auto DJ Controls

```python
auto_toggle()              # Toggle AutoDJ on/off
# Shift+F12

auto_next()                # Skip to next track
# Shift+F11
```

#### Loop Controls

```python
loop_activate(deck, loop_status)   # Set loop in/out points
# Q (deck 1), U (deck 2)

loop_onoff(deck, loop_status)      # Toggle loop
# 4 (deck 1), 9 (deck 2)

loop_in(deck)              # Set loop in point
# 2 (deck 1), 7 (deck 2)

loop_out(deck)             # Set loop out point
# 3 (deck 1), 8 (deck 2)

loop_halve(deck)           # Halve loop length
# W (deck 1), I (deck 2)

loop_double(deck)          # Double loop length
# E (deck 1), O (deck 2)
```

#### Utility Functions

```python
sleep_time(seconds)        # Wait with logging
sleep_after_press()        # Standard delay after key press
```

**Deck Parameter**:
- `1` = Deck 1 only
- `2` = Deck 2 only
- `3` = Both decks

---

### 3. `press_mixxx2.py` - Enhanced Library with Effects ⭐

**Purpose**: Extended version with complex effects and tempo control

**Additional Functions**:

#### Tempo Manipulation

```python
tempo_slow(deck=3, loop_n=4, delay_tempo=1)
# Gradually slow down tempo
# deck: which deck (1, 2, or 3=both)
# loop_n: number of tempo decrease steps
# delay_tempo: duration of each step

tempo_fast(deck=3, loop_n=4, delay_tempo=1)
# Gradually speed up tempo
# Same parameters as tempo_slow
```

**How it works**:
```python
# Press and hold F3/F7 for slowdown
# Or F4/F8 for speedup
# Multiple times for gradual effect
```

#### Scratch Effect

```python
scratch(deck, delay, loop_on, deep=3)
# Create scratch effect using loops
# deck: which deck
# delay: timing between loop changes
# loop_on: current loop status (bool)
# deep: complexity level (1-3)

# Returns: updated loop_on status
```

**Scratch Algorithm**:
1. Activate loop
2. Halve loop (creates stutter)
3. Optionally halve again (deep=2 or 3)
4. Quick double back to original
5. Deactivate loop

**Example**:
```python
loop_on = False
loop_on = scratch(deck=3, delay=2, loop_on=loop_on, deep=2)
# Creates 2-second scratch effect on both decks
```

---

## Usage Examples

### Example 1: Automated Loop Performance

```python
from press_mixxx2 import *

# Start playing
auto_toggle()
sleep_time(5)

while True:
    # Sync tempo
    sync_tempo(3)

    # Create scratch effect
    loop_on = scratch(3, 3, False)
    sleep_time(10)

    # Next track
    auto_next()
    sleep_time(10)
```

### Example 2: Temperature-Triggered Effects

```python
from press_mixxx2 import *

# In your main loop
if temperature > hot_threshold:
    tempo_fast(3, 4, 1)  # Speed up music

if temperature < cold_threshold:
    tempo_slow(3, 4, 1)  # Slow down music

if temperature_spike:
    scratch(3, 2, loop_on, 3)  # Create excitement
```

### Example 3: Build-up Sequence

```python
# Gradually increase energy
sync_tempo(3)

# Start with slow tempo
tempo_slow(3, 8, 0.5)

# Add loops
loop_activate(1, False)
loop_halve(1)
loop_halve(1)  # Create fast loop
sleep_time(4)

# Release and speed up
loop_onoff(1, True)
tempo_fast(3, 8, 0.5)

# Drop
auto_next()
```

### Example 4: Responsive DJ

```python
import random

while True:
    # Random effects
    effect_choice = random.randint(1, 3)

    if effect_choice == 1:
        scratch(3, random.uniform(1,3), loop_on)
    elif effect_choice == 2:
        tempo_slow(3, 4, 1)
        tempo_fast(3, 4, 1)
    else:
        loop_activate(1, False)
        sleep_time(2)
        loop_onoff(1, True)

    sleep_time(random.uniform(5, 15))
    auto_next()
```

---

## Mixxx Keyboard Shortcuts Reference

### Default Mixxx Mappings

| Action | Deck 1 | Deck 2 |
|--------|--------|--------|
| Play/Pause | D | L |
| Sync | 1 | 6 |
| Load Track | Shift+← | Shift+→ |
| Loop In | 2 | 7 |
| Loop Out | 3 | 8 |
| Loop Toggle | 4 | 9 |
| Loop Halve | W | I |
| Loop Double | E | O |
| Loop Activate | Q | U |
| Tempo Down | F3 | F7 |
| Tempo Up | F4 | F8 |
| Tap Tempo | Shift+1 | Shift+6 |

### Auto DJ

| Action | Shortcut |
|--------|----------|
| Toggle | Shift+F12 |
| Skip | Shift+F11 |
| Fade Now | Shift+F10 |

---

## Configuration

### Adjust Timing

```python
# Global delay setting (in press_mixxx2.py)
sleep_after_press_delay = 1  # seconds

# Increase for slower systems
sleep_after_press_delay = 2

# Decrease for faster response
sleep_after_press_delay = 0.5
```

### Custom Shortcuts

If your Mixxx has different key mappings:

```python
def play(deck):
    if deck == 1:
        pyautogui.press('YOUR_KEY')  # Change here
    elif deck == 2:
        pyautogui.press('YOUR_KEY')  # Change here
```

---

## Best Practices

### 1. Timing

Always wait after key presses:
```python
pyautogui.press('D')
sleep_after_press()  # Let Mixxx process
```

### 2. Loop State Tracking

Track loop status to toggle correctly:
```python
loop_on = False  # Initialize

loop_on = loop_activate(1, loop_on)  # Updates state
# Later
loop_on = loop_onoff(1, loop_on)     # Uses state
```

### 3. Error Handling

Mixxx must be focused:
```python
# Ensure Mixxx window is active
# pyautogui can fail if wrong window has focus
```

### 4. Testing

Test functions individually before combining:
```python
# Test one function
sync_tempo(1)
sleep_time(2)

# Then combine
sync_tempo(3)
scratch(3, 2, False)
```

---

## Troubleshooting

### Keys not working
- Ensure Mixxx is the active window
- Check Mixxx keyboard shortcuts in Preferences
- Increase `sleep_after_press_delay`

### Timing issues
- Adjust delays based on system performance
- Mixxx may lag under high CPU load
- Test timing with simple sequences first

### Loop functions not responding
- Verify loop shortcuts in Mixxx
- Ensure track is playing
- Check loop_status is correctly tracked

---

## Safety Features

### Focus Protection

```python
# Add at start of script
import pyautogui
pyautogui.FAILSAFE = True  # Move mouse to corner to abort
```

### Gradual Changes

Use gradual tempo changes instead of instant:
```python
# Bad: Jarring change
pyautogui.keyDown('f4')
time.sleep(5)
pyautogui.keyUp('f4')

# Good: Gradual ramp
tempo_fast(3, 10, 0.5)  # 10 steps, smooth
```

---

## Integration Patterns

### With Sensors

```python
from press_mixxx2 import *

def on_sensor_event(event_type, intensity):
    if event_type == "spike":
        scratch(3, intensity, loop_on, 3)

    if event_type == "gradual_rise":
        tempo_fast(3, int(intensity*10), 1)
```

### With Data

```python
def data_to_effect(value, min_val, max_val):
    normalized = (value - min_val) / (max_val - min_val)

    if normalized < 0.3:
        tempo_slow(3, 4, 1)
    elif normalized > 0.7:
        tempo_fast(3, 4, 1)
    else:
        scratch(3, 2, False, 2)
```

---

## Alternative Approaches

### OSC (Open Sound Control)

For more reliable control, consider OSC:
```python
from pythonosc import udp_client

client = udp_client.SimpleUDPClient("127.0.0.1", 7000)
client.send_message("/mixxx/deck1/play", 1.0)
```

### MIDI Control

Use virtual MIDI:
```python
import mido

port = mido.open_output('Mixxx')
port.send(mido.Message('note_on', note=60))
```

---

---

## Part of Heating DJ

This library is a core component of the Heating DJ project. See the [main README](../README.md) for the complete system architecture.

**Related Components:**
- [MixxAutoDj](../MixxAutoDj/) - Advanced DJ automation with file-based IPC
- [serial](../serial/) - Communication with thermal sensors
- [thermal_dj](../thermal_dj/) - Main thermal DJ applications

## Credits

- Built for [Mixxx DJ Software](https://www.mixxx.org/)
- PyAutoGUI for keyboard automation
- Part of the Heating DJ project (GPL-3.0)