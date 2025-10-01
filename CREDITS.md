# Credits and Attribution

## Heating DJ - Interactive Thermal DJ System

This project builds upon the excellent work of the open-source thermal camera community.

## Original Inspiration

The thermal visualization code in this project was inspired by and adapted from:

### Primary Sources:

**Maker Portal - Raspberry Pi Thermal Camera**
- Repository: [makerportal/raspi-thermal-cam](https://github.com/makerportal/raspi-thermal-cam)
- Author: Maker Portal
- License: GPL-3.0
- Tutorial: [High Resolution Thermal Camera with Raspberry Pi and MLX90640](https://makersportal.com/blog/2020/6/8/high-resolution-thermal-camera-with-raspberry-pi-and-mlx90640)
- Contributions used:
  - Cubic interpolation approach using scipy.interp2d
  - MLX90640 thermal camera data visualization patterns
  - Matplotlib real-time plotting with blitting optimization

**Adafruit Industries**
- Learning Guide: [Adafruit MLX90640 IR Thermal Camera](https://learn.adafruit.com/adafruit-mlx90640-ir-thermal-camera/python-circuitpython)
- License: MIT
- Contributions used:
  - MLX90640 sensor interfacing patterns
  - CircuitPython/Python examples

### Additional References:

- Stack Overflow community discussions on thermal camera interpolation
- Various MLX90640 tutorial examples across the maker community

## Original Contributions in This Project

The following features are original work by the Heating DJ project:

- **Event Detection System**: 10-type thermal event classification algorithm
- **DJ Automation Integration**: Real-time Mixxx DJ software control based on temperature events
- **Movement Detection Algorithm**: Pixel-wise deviation analysis for human presence detection
- **Temperature-to-Music Mapping**: Intelligent mapping of thermal events to DJ effects
- **LED Matrix Feedback**: Serial communication for visual temperature feedback
- **Baseline Adaptation System**: Automatic threshold adjustment over time
- **Project Organization**: Separation of main applications from examples
- **Integration Framework**: KeyboardPress, MixxAutoDj, and serial utilities integration

## Third-Party Libraries

This project uses the following open-source libraries:

- **NumPy**: BSD License
- **Matplotlib**: PSF License
- **SciPy**: BSD License
- **PySerial**: BSD License
- **PyAutoGUI**: BSD License
- **scikit-image**: BSD License
- **Adafruit CircuitPython Libraries**: MIT License

## Hardware

- **MLX90640 Thermal Sensor** by Melexis
- **Mixxx DJ Software** - GPL-2.0+ License

## Community

Special thanks to the open-source hardware and maker communities for sharing knowledge and code that made this project possible.

---

If you've contributed to this project or notice missing attribution, please open an issue or pull request.
