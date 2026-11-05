# ESP32-C3 DC Power Monitoring System

An embedded systems project that simulates a DC power monitoring system using an ESP32-C3, MicroPython, MQTT, and a Python-based web dashboard.

## 1. Project Overview

This project demonstrates the monitoring of DC electrical parameters, including voltage, current, and power consumption.

The system detects overvoltage and overcurrent conditions, provides local alerts through an LCD and buzzer, and transmits measurement data to a remote dashboard using MQTT.

The prototype is developed and tested using the Wokwi ESP32 simulator.

## 2. Features

- Voltage and current monitoring using ESP32-C3 ADC inputs
- Real-time power calculation using P = V × I
- LCD display of electrical measurements
- Overvoltage and overcurrent detection
- Buzzer alerts for abnormal conditions
- MQTT communication for transmitting measurements
- Python-based MQTT data receiver
- Automatic CSV measurement logging
- Streamlit dashboard for live monitoring
- Historical measurement graphs and CSV download

## 3. System Architecture

1. Two potentiometers simulate voltage and current sensor outputs.
2. The ESP32-C3 reads the analogue inputs through its ADC pins.
3. MicroPython converts the readings into voltage and current values.
4. The system calculates electrical power.
5. The LCD displays the measurements and system status.
6. A buzzer provides alerts when fault conditions are detected.
7. Measurement data is published through MQTT.
8. A Python receiver collects the data and saves it in JSON and CSV files.
9. A Streamlit dashboard displays live measurements and historical trends.

## 4. Repository Structure

```text
ESP32-DC-Power-monitor/
│
├── firmware/
│   ├── main.py
│   └── i2c_lcd.py
│
├── simulations/
│   └── diagram.json
│
├── screenshots/
│
├── dashboard.py
├── mqtt_receiver.py
├── main.py
├── requirements.txt
├── README.md
└── .gitignore
```

## 5. Hardware Configuration

| Component                   | ESP32-C3 Pin |
| --------------------------- | ------------ |
| Voltage input potentiometer | GPIO 0       |
| Current input potentiometer | GPIO 1       |
| LCD SDA                     | GPIO 8       |
| LCD SCL                     | GPIO 9       |
| Buzzer                      | GPIO 7       |

### Hardware Components

- ESP32-C3 DevKitM-1
- Two potentiometers
- 16×2 I2C LCD
- Piezo buzzer

## 6. Software and Technologies

- MicroPython
- Wokwi Simulator
- MQTT
- Python
- Paho MQTT
- Streamlit
- Pandas

## 7. Running the Project

### A. ESP32-C3 Simulation

1. Open [Wokwi](https://wokwi.com/).
2. Create or open an ESP32-C3 MicroPython project.
3. Add the components and connections represented in `simulations/diagram.json`.
4. Upload `firmware/main.py` and `firmware/i2c_lcd.py` to the Wokwi project.
5. Run the simulation.

### B. Install Python Dependencies

Clone the repository and navigate into its directory:

```bash
git clone https://github.com/kings-elvis/ESP32-DC-Power-monitor-.git
cd ESP32-DC-Power-monitor-
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### C. Start the MQTT Receiver

```bash
python mqtt_receiver.py
```

Keep this terminal running.

### D. Launch the Dashboard

Open a second terminal and run:

```bash
python -m streamlit run dashboard.py
```

The dashboard should open in your browser.

The ESP32 simulation must be running and publishing data to the configured MQTT topic.

## 8. Project Screenshots

The screenshots below demonstrate normal operation, fault detection, and historical measurement analysis.

### Dashboard Overview

![Dashboard Overview](screenshots/1.dashboard%20.png)

### Overvoltage Alert

![Overvoltage Alert](screenshots/2.over%20voltage%20alert.png)

### Overcurrent Alert

![Overcurrent Alert](screenshots/3.overcurrent%20alert.png)

### Combined Fault Alert

![Combined Fault Alert](screenshots/4.both%20fault%20alert.png)

### Voltage Graph

![Voltage Graph](screenshots/5.voltage%20graph.png)

### Current Graph

![Current Graph](screenshots/6.current%20graph.png)

### Power Graph

![Power Graph](screenshots/7.power%20graph.png)

### Measurement History

![Measurement Distribution Table](screenshots/8.distribution%20table.png)

## 9. Simulation Limitations

The current prototype uses potentiometers to simulate sensor outputs. It does not directly measure actual electrical voltage or current.

The project demonstrates embedded monitoring, fault detection, MQTT communication, data logging, and visualisation. It is not intended to provide real-world electrical protection.

The MQTT broker used is a public development broker, so the demonstration is not intended for private or safety-critical communication.

## 10. Future Improvements

- Integrate actual voltage and current sensing circuits.
- Calibrate measurements against reference instruments.
- Test the system using a physical ESP32-C3.
- Improve data storage and remote monitoring.
- Introduce secure MQTT communication.

## Author

**Elvis King'ori**

Microprocessor Technology and Instrumentation  
Department of Physics  
University of Nairobi.
