# Serial - Arduino/Sensor Communication Utilities

Simple Python utilities for reading and writing data over serial connections (USB/UART) with Arduino and sensor modules.

## Project Overview

These basic serial communication scripts provide the foundation for connecting Python applications to Arduino microcontrollers and sensor systems. Essential utilities used across multiple projects in this repository.

## Related Projects

**Used by**:
- **`/buzzer/`** - All buzzer scripts read sensor data via serial
- **`/PlotTemperature/`** - Thermal camera data via serial
- **Any sensor project** - Foundation for hardware communication

## Dependencies

```bash
pip install pyserial
```

## Scripts

### 1. `read_serial.py` - Basic Serial Reader

**Purpose**: Read and display serial data from Arduino/sensors

**Code**:
```python
#!/usr/bin/env python3
import serial

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.reset_input_buffer()

    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
```

**Usage**:
```bash
python read_serial.py
```

**Configuration**:
- `'/dev/ttyUSB0'` - Serial port (change for your system)
- `115200` - Baud rate (must match Arduino)
- `timeout=1` - Read timeout in seconds

---

### 2. `write_serial.py` - Basic Serial Writer

**Purpose**: Send commands to Arduino/devices

**Usage**:
```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Send command
ser.write(b'COMMAND\n')

# Send string
message = "Hello Arduino"
ser.write(message.encode())
```

---

## Finding Serial Ports

### Linux/Mac
```bash
ls /dev/tty*

# Common devices:
# /dev/ttyUSB0, /dev/ttyUSB1  - USB serial adapters
# /dev/ttyACM0, /dev/ttyACM1  - Arduino/CDC devices
# /dev/ttyS0, /dev/ttyS1      - Built-in serial ports
```

### Windows
```bash
# In Python:
import serial.tools.list_ports
ports = serial.tools.list_ports.comports()
for port in ports:
    print(port.device)

# Output: COM3, COM4, etc.
```

### Python Method
```python
import serial.tools.list_ports

def find_ports():
    ports = serial.tools.list_ports.comports()
    for port in ports:
        print(f"{port.device}: {port.description}")

find_ports()
```

---

## Common Serial Parameters

### Baud Rates
- **9600** - Standard, reliable, slower
- **57600** - Faster, good for sensors
- **115200** - High speed, common for Arduino

### Data Format
- **8 data bits** - Standard (8N1)
- **No parity** - Standard
- **1 stop bit** - Standard

### Timeout
- `timeout=None` - Block forever
- `timeout=0` - Non-blocking
- `timeout=1` - 1 second timeout

---

## Usage Examples

### Example 1: Read Temperature Sensor

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        try:
            temp = float(line)
            print(f"Temperature: {temp}°C")
        except ValueError:
            print(f"Invalid data: {line}")
```

### Example 2: CSV Data Parsing

```python
import serial

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        values = line.split(',')

        if len(values) == 3:
            sensor1 = float(values[0])
            sensor2 = float(values[1])
            sensor3 = float(values[2])
            print(f"S1:{sensor1} S2:{sensor2} S3:{sensor3}")
```

### Example 3: Command-Response Pattern

```python
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

# Send command
ser.write(b'READ_SENSOR\n')
time.sleep(0.1)  # Wait for Arduino to process

# Read response
if ser.in_waiting > 0:
    response = ser.readline().decode('utf-8').rstrip()
    print(f"Response: {response}")
```

### Example 4: Binary Data

```python
import serial
import struct

ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)

while True:
    if ser.in_waiting >= 4:  # Wait for 4 bytes
        data = ser.read(4)
        value = struct.unpack('f', data)[0]  # Float
        print(f"Value: {value}")
```

---

## Arduino Examples

### Arduino: Send Temperature

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  float temp = analogRead(A0) * 0.488;  // Example conversion
  Serial.println(temp);
  delay(1000);
}
```

### Arduino: Send CSV Data

```cpp
void setup() {
  Serial.begin(115200);
}

void loop() {
  int sensor1 = analogRead(A0);
  int sensor2 = analogRead(A1);
  int sensor3 = analogRead(A2);

  Serial.print(sensor1);
  Serial.print(",");
  Serial.print(sensor2);
  Serial.print(",");
  Serial.println(sensor3);

  delay(100);
}
```

### Arduino: Command Response

```cpp
void setup() {
  Serial.begin(9600);
}

void loop() {
  if (Serial.available() > 0) {
    String command = Serial.readStringUntil('\n');

    if (command == "READ_SENSOR") {
      int value = analogRead(A0);
      Serial.println(value);
    }
  }
}
```

---

## Error Handling

### Basic Error Handling

```python
import serial

try:
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

while True:
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
    except serial.SerialException:
        print("Lost connection!")
        break
    except UnicodeDecodeError:
        print("Received invalid data")
        ser.reset_input_buffer()
```

### Robust Reading

```python
def read_serial_safe(ser, max_retries=3):
    retries = 0
    while retries < max_retries:
        try:
            if ser.in_waiting > 0:
                line = ser.readline().decode('utf-8').rstrip()
                return line
        except:
            retries += 1
            ser.reset_input_buffer()
    return None
```

---

## Buffer Management

### Clear Old Data

```python
# Clear input buffer before starting
ser.reset_input_buffer()

# Or periodically
if ser.in_waiting > 100:  # Buffer getting full
    ser.reset_input_buffer()
```

### Flush After Write

```python
ser.write(b'COMMAND\n')
ser.flush()  # Ensure data is sent
```

---

## Troubleshooting

### Permission Denied (Linux)

```bash
# Add user to dialout group
sudo usermod -a -G dialout $USER

# Log out and back in, or:
newgrp dialout

# Or run with sudo (not recommended)
sudo python read_serial.py
```

### Device Not Found

```bash
# Check if device exists
ls -l /dev/ttyUSB*

# Check kernel messages
dmesg | grep tty

# Try different port
# Change /dev/ttyUSB0 to /dev/ttyUSB1, etc.
```

### Wrong Baud Rate

```python
# Symptoms: Garbage data
# Solution: Match Arduino baud rate exactly

# Arduino uses 9600:
Serial.begin(9600);

# Python must match:
ser = serial.Serial(..., 9600, ...)
```

### Data Corruption

```python
# Add checksums (Arduino side)
int checksum = sensor1 + sensor2 + sensor3;
Serial.print(sensor1);
Serial.print(",");
Serial.print(sensor2);
Serial.print(",");
Serial.print(sensor3);
Serial.print(",");
Serial.println(checksum);

# Verify (Python side)
values = line.split(',')
checksum = int(values[0]) + int(values[1]) + int(values[2])
if checksum == int(values[3]):
    # Data valid
```

---

## Advanced Techniques

### Non-Blocking Read

```python
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0)  # Non-blocking

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
    else:
        # Do other work
        do_something_else()
    time.sleep(0.01)
```

### Threading

```python
import serial
import threading

def read_serial():
    ser = serial.Serial('/dev/ttyUSB0', 9600)
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            process_data(line)

thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

# Main program continues
while True:
    # Other work
    pass
```

### Context Manager

```python
with serial.Serial('/dev/ttyUSB0', 9600, timeout=1) as ser:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
# Port automatically closed
```

---

## Performance Tips

1. **Match Baud Rates** - Higher = faster but less reliable
2. **Buffer Management** - Clear old data regularly
3. **Use Binary** - More efficient than text for numbers
4. **Batch Reads** - Read multiple bytes at once
5. **Minimize Writes** - Serial writes are slow

---

## Integration Patterns

### With Sensors
```python
# Used by /buzzer/ and /PlotTemperature/
ser = serial.Serial('/dev/ttyUSB0', 57600, timeout=1)

while True:
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        values = line.split(',')
        sensor_value = float(values[0])

        # Process sensor data
        trigger_action(sensor_value)
```

### With Display
```python
# Used by /PlotTemperature/
write_ser = serial.Serial('/dev/ttyUSB1', 57600, timeout=5)

def write_serial(txt):
    txt = txt + "\n"
    write_ser.write(txt.encode())

write_serial("Temperature: 25C")
```

---

## Resources

- **PySerial Documentation**: https://pyserial.readthedocs.io/
- **Arduino Serial**: https://www.arduino.cc/reference/en/language/functions/communication/serial/
- **Serial Protocol Guide**: https://learn.sparkfun.com/tutorials/serial-communication

---

## Common Use Cases

1. **Sensor Reading** - Temperature, distance, light, etc.
2. **Motor Control** - Send position commands
3. **Data Logging** - Record sensor data to file
4. **Interactive Systems** - Two-way communication
5. **Debugging** - Monitor Arduino output

---

## Credits

- **PySerial** - Chris Liechti
- Essential utility for hardware interfacing

## License

Open source - connect Python to your hardware!