# Mixxx Auto DJ - Automated DJ Control System

An automated DJ system that controls [Mixxx DJ software](https://www.mixxx.org/) through file-based IPC (Inter-Process Communication) and keyboard automation.

## Project Overview

This project creates a fully automated DJ that can load tracks, sync tempo, apply effects, control EQ, create loops, and transition between songs automatically. It's designed to work with Mixxx DJ software, using a combination of file-based communication and keyboard shortcuts to achieve hands-free DJ performances.

## How It Works

The system uses two communication methods:
1. **File-based IPC**: Custom Mixxx controller script reads commands from text files
2. **Keyboard Automation**: Direct hotkey simulation via pyautogui

This allows external Python scripts to control Mixxx as if a human DJ were operating it.

## Related Projects

This project integrates with:
- **`/KeyboardPress/`** - Provides the keyboard automation functions used here
- **`/PlotTemperature/`** - Uses this DJ automation to respond to sensor data
- **`/buzzer/`** - Can work alongside sensor-driven music systems

## Project Structure

```
MixxAutoDj/
├── README.md
├── Modify/
│   ├── djmix_test.py         # Complex automated DJ routine
│   └── mixa001_lock.py       # File-based Mixxx control demo
```

## Dependencies

```bash
pip install pyautogui  # Keyboard automation
```

### Mixxx Setup Required

1. **Install Mixxx**: https://www.mixxx.org/download/
2. **Configure Controller**: Custom Mixxx controller script needed (not included)
3. **Setup File Paths**: Configure Mixxx to read from control files

## Script Documentation

### 1. `mixa001_lock.py` - File-Based Control Demo

**Purpose**: Demonstrates file-based IPC control of Mixxx

**How it works**:
1. Writes commands to `/home/modchai/.mixxx/controlmixxx.txt`
2. Uses lock files to prevent race conditions
3. Waits for confirmation from Mixxx in `confirmixxx.txt`
4. Monitors playback position from `mixxxposition1.txt` and `mixxxposition2.txt`

**Command Format**:
```
COMMAND\nINDEX\n
```

**Example Commands**:
- `L1/path/to/track.mp3` - Load track to deck 1
- `L2/path/to/track.mp3` - Load track to deck 2
- `P10` - Play deck 1 (0=stop, 1=play)
- `P20` - Play deck 2
- `T1175` - Set deck 1 tempo to 175
- `K113` - Crossfader position (0-127)
- `Q1LC1` - EQ Low Cut deck 1, value 1
- `Q1HC1` - EQ High Cut deck 1, value 1
- `Q1LO1` - EQ Low boost deck 1, value 1
- `Q1HO1` - EQ High boost deck 1, value 1
- `FX2` - Apply effect 2

**Control Flow**:
```python
# 1. Create lock file
lockFile = os.open("controlmixxx.txt.lock", os.O_CREAT|os.O_EXCL)

# 2. Write command
controlXY.write("P10\n1\n")

# 3. Release lock
os.close(lockFile)
os.unlink("controlmixxx.txt.lock")

# 4. Wait for confirmation
while (confirmValue != expectedIndex):
    # Poll confirmation file
```

**Usage**:
```bash
python mixa001_lock.py
```

**What it does**:
1. Loads initial track to deck 1
2. Starts playback
3. Sets tempo to 175 BPM
4. Adjusts crossfader
5. Monitors playback position
6. At 58% position, loads next track to deck 2
7. Creates smooth transition with:
   - Tempo matching
   - EQ adjustments
   - Loop creation
   - Effects application
8. Continues mixing pattern

---

### 2. `djmix_test.py` - Advanced Automated DJ

**Purpose**: Full-featured automated DJ routine with complex transitions

**Features**:
- Automatic track loading based on position
- Tempo synchronization
- Complex EQ manipulation
- Loop effects
- Effect chains
- Multi-deck coordination
- Position-based triggering

**How it works**:
Monitors playback position and triggers actions at specific points:

```python
# Monitor deck 1 position
if (positionNow >= 0.5806):  # At 58% of track
    # Load next track
    # Set position
    # Match tempo
    # Apply EQ changes
    # Add effects
```

**Transition Pattern**:
Each transition includes:
1. **Pre-load** (60-80% of current track)
2. **Tempo Match** (175 BPM standard)
3. **EQ Preparation**:
   - Cut lows on incoming track
   - Cut highs on incoming track
   - Boost mids on current track
4. **Loop Creation** (for scratching/effects)
5. **Effect Application**
6. **EQ Swap**:
   - Gradually restore incoming lows/highs
   - Cut outgoing lows/highs
7. **Crossfade**

**Usage**:
```bash
python djmix_test.py
```

**Advanced Features**:

#### Position-Based Triggering
```python
# Load next track at 70% of current
if (positionNow >= 0.70982142857142858):
    write_command("L2/path/to/next/track.mp3")
```

#### EQ Manipulation
```python
# EQ Commands
Q1LC10  # Deck 1 Low Cut, value 10
Q1HC10  # Deck 1 High Cut, value 10
Q2LO1   # Deck 2 Low Boost, value 1
Q2HO1   # Deck 2 High Boost, value 1
Q2MC1   # Deck 2 Mid Cut, value 1
```

#### Loop Control
```python
Q1LC1    # Set loop in point
Q1HC1    # Set loop out point
Q1LO1    # Loop on/off
```

#### Effect Chains
```python
FX2      # Apply effect preset 2
FX3      # Apply effect preset 3
FX4      # Apply effect preset 4
```

---

## Keyboard Automation Functions

These functions from `/KeyboardPress/press_mixxx2.py` are used:

```python
# Core Functions
load_track(deck)           # Shift+Arrow to load
play(deck)                 # D/L to play/pause
sync_tempo(deck)           # 1/6 to sync
auto_toggle()              # Shift+F12 for AutoDJ
auto_next()                # Shift+F11 for next track

# Loop Functions
loop_activate(deck)        # Q/U set loop
loop_onoff(deck)          # 4/9 toggle loop
loop_halve(deck)          # W/I halve loop
loop_double(deck)         # E/O double loop

# Advanced Effects
scratch(deck, delay, loop_on)  # Complex scratch routine
tempo_slow(deck, loops, delay) # Gradual slowdown
tempo_fast(deck, loops, delay) # Gradual speedup
```

---

## Mixxx Controller Script Requirements

You need a custom Mixxx controller script that:

1. **Reads control file** (`controlmixxx.txt`)
2. **Parses commands** and executes them via Mixxx API
3. **Writes confirmations** to `confirmixxx.txt`
4. **Writes playback positions** to `mixxxposition1.txt` and `mixxxposition2.txt`
5. **Handles lock files** to prevent conflicts

### Example Controller Stub (Javascript):

```javascript
// In Mixxx controller script
var MixxControl = {
    timer: null,

    init: function() {
        // Poll control file every 10ms
        this.timer = engine.beginTimer(10, this.checkFile);
    },

    checkFile: function() {
        // Check for lock file
        if (lockExists()) return;

        // Read command file
        var cmd = readControlFile();
        if (!cmd) return;

        // Execute command
        this.executeCommand(cmd);

        // Write confirmation
        writeConfirmation(cmd.index);
    },

    executeCommand: function(cmd) {
        if (cmd.type === 'L1') {
            engine.setValue('[Channel1]', 'LoadSelectedTrack', 1);
        }
        // ... more commands
    }
};
```

---

## File Paths Configuration

Default paths (Ubuntu):
```python
CONTROL_FILE = "/home/modchai/.mixxx/controlmixxx.txt"
CONFIRM_FILE = "/home/modchai/.mixxx/confirmixxx.txt"
LOCK_FILE = "/home/modchai/.mixxx/controlmixxx.txt.lock"
POSITION1_FILE = "/home/modchai/.mixxx/mixxxposition1.txt"
POSITION2_FILE = "/home/modchai/.mixxx/mixxxposition2.txt"
```

Adjust for your system:
```python
# Windows
CONTROL_FILE = "C:/Users/YourName/AppData/Local/Mixxx/controlmixxx.txt"

# macOS
CONTROL_FILE = "/Users/YourName/Library/Application Support/Mixxx/controlmixxx.txt"
```

---

## Integration Examples

### With Temperature Sensors (`/PlotTemperature/`)

```python
from press_mixxx2 import *

# In temperature monitoring loop
if temperature_spike:
    scratch(3, 2, loop_on)    # Create excitement
    auto_next()               # Change track

if temperature_drop:
    tempo_slow(3, 4, 1)       # Cool down music
```

### With Sensor Data (`/buzzer/`)

```python
# Map sensor to DJ actions
sensor_value = read_sensor()

if sensor_value > threshold:
    sync_tempo(3)
    auto_next()
```

---

## Advanced Techniques

### Creating Custom Transitions

```python
def smooth_transition(from_deck, to_deck):
    # 1. Match tempo
    sync_tempo(3)

    # 2. Set up EQ
    # Cut lows on incoming
    # Cut highs on incoming

    # 3. Create loop for drama
    loop_on = scratch(to_deck, 2, False)

    # 4. Gradual EQ swap
    sleep_time(2)

    # 5. Auto advance
    auto_next()
```

### BPM-Synced Effects

```python
def apply_beat_effects(bpm):
    loop_length = 60.0 / bpm  # One beat duration

    # Create quarter-note loop
    loop_activate(1)
    sleep_time(loop_length * 4)

    # Halve twice for 1/16 notes
    loop_halve(1)
    loop_halve(1)

    # Release
    sleep_time(loop_length * 2)
    loop_onoff(1)
```

---

## Performance Tips

1. **File I/O Optimization**:
   - Use small polling intervals (0.004s)
   - Always use lock files
   - Handle file not found gracefully

2. **Timing**:
   - Account for Mixxx processing delay (~50ms)
   - Add buffer time before transitions
   - Test timing with specific tracks

3. **Error Handling**:
   ```python
   try:
       position = float(readFile())
   except:
       time.sleep(0.004)
       continue
   ```

---

## Troubleshooting

### Commands not executing
- Check file permissions
- Verify Mixxx controller script is loaded
- Test with manual file writes

### Timing issues
- Adjust `sleep_after_press_delay`
- Increase polling frequency
- Check system load

### Lock file conflicts
- Ensure proper cleanup
- Add timeout to lock acquisition
- Check for orphaned locks

---

## Future Enhancements

- [ ] OSC (Open Sound Control) integration
- [ ] Network control (WebSocket/HTTP API)
- [ ] Machine learning for transition point detection
- [ ] Beat-matched effect timing
- [ ] Auto BPM detection
- [ ] Spotify/streaming integration
- [ ] Visual waveform analysis
- [ ] Crowd response feedback (mic input)

---

## Safety Notes

⚠️ **Important**:
- Always test with backed-up music library
- Start with `sleep_after_press_delay = 2` and decrease gradually
- Monitor CPU usage during automated performances
- Have manual override ready (mouse/keyboard)

---

## Use Cases

1. **Sensor-Driven DJ Sets**: React to environmental data
2. **Art Installations**: Autonomous music systems
3. **Radio Automation**: Unattended broadcasting
4. **Fitness Classes**: Pre-programmed music routines
5. **Testing**: Automated DJ software testing

---

## Credits

- Built for [Mixxx DJ Software](https://www.mixxx.org/)
- Keyboard automation via PyAutoGUI
- Inspired by autonomous DJ systems

## License

Open source - adapt for your automated DJ needs!