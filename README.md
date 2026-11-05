# ESP32-C3 DC Power Monitoring System

An embedded systems project that simulates a DC power monitoring system using an ESP32-C3, MicroPython, MQTT, and a Python-based web dashboard.

## Project Overview

The system monitors simulated DC voltage and current, calculates power consumption, detects overvoltage and overcurrent conditions, and sends measurement data to a live dashboard.

The prototype uses potentiometers to simulate voltage and current sensor outputs in Wokwi.

## Features

- Voltage, current, and power calculation
- LCD display of measurements
- Overvoltage and overcurrent detection
- Buzzer alerts when fault conditions occur
- MQTT communication for transmitting measurements
- Python MQTT receiver for collecting data
- CSV logging of measurements
- Streamlit dashboard for live monitoring and historical analysis

## System Architecture

1. The ESP32-C3 reads the potentiometer outputs through its ADC pins.
2. MicroPython converts the readings into simulated voltage and current values.
3. The system calculates power using `P = V × I`.
4. The LCD displays measurements and the buzzer alerts when limits are exceeded.
5. Measurements are published to an MQTT broker.
6. A Python receiver collects the data and saves it to JSON and CSV files.
7. A Streamlit dashboard displays live measurements and historical trends.

## Hardware and Software

### Hardware

- ESP32-C3 DevKitM-1
- Two potentiometers (simulated sensor inputs)
- 16×2 I2C LCD
- Piezo buzzer

### Software and Technologies

- MicroPython
- Wokwi Simulator
- MQTT
- Python
- Paho MQTT
- Streamlit
- Pandas

## Pin Configuration

| Component                   | ESP32-C3 Pin |
| --------------------------- | ------------ |
| Voltage input potentiometer | GPIO 0       |
| Current input potentiometer | GPIO 1       |
| LCD SDA                     | GPIO 8       |
| LCD SCL                     | GPIO 9       |
| Buzzer                      | GPIO 7       |

## Running the Project

Install the required Python packages:

```bash
pip install -r requirements.txt
```

Run the MQTT receiver:

```bash
python mqtt_receiver.py
```

In a separate terminal, start the dashboard:

```bash
python -m streamlit run dashboard.py
```

The ESP32-C3 simulation must also be running and publishing measurements to the configured MQTT topic.

## Simulation and Limitations

This project currently uses Wokwi for simulation. The potentiometers represent sensor outputs and do not measure actual electrical voltage or current.

The system is a prototype for demonstrating embedded monitoring, fault detection, MQTT communication, and data visualisation. It is not designed to provide real-world electrical protection.

## Future Improvements

- Integrate actual voltage and current sensing circuits.
- Calibrate measurements against reference instruments.
- Test the system using a physical ESP32-C3.
- Improve data storage and remote monitoring.

## Author

Elvis King'ori K.

Microprocessor Technology and Instrumentation.  
Department of Physics.  
University of Nairobi.
