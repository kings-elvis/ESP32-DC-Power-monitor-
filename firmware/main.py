import network
import ujson
import time
from umqtt.simple import MQTTClient
from machine import Pin, ADC, I2C, PWM
from time import sleep, ticks_ms, ticks_diff
from i2c_lcd import I2cLcd

# Wi-Fi configuration
WIFI_SSID = "Wokwi-GUEST"
WIFI_PASSWORD = ""

# MQTT configuration
MQTT_CLIENT_ID = "dc-power-monitor-73921"
MQTT_BROKER = "broker.emqx.io"
MQTT_PORT = 1883
MQTT_TOPIC = "dcpm/demo-73921"

# Connect to Wi-Fi
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

print("Connecting to Wi-Fi...")

while not wifi.isconnected():
    time.sleep(0.2)

print("Wi-Fi connected!")
print("IP address:", wifi.ifconfig()[0])

# Connect to MQTT broker
client = MQTTClient(
    MQTT_CLIENT_ID,
    MQTT_BROKER,
    port=MQTT_PORT
)

client.connect()

print("MQTT connected!")

# 1. SENSOR CONFIGURATION
voltage_sensor = ADC(Pin(0))
current_sensor = ADC(Pin(1))

voltage_sensor.atten(ADC.ATTN_11DB)
current_sensor.atten(ADC.ATTN_11DB)

# 2. LCD CONFIGURATION
i2c = I2C(0, scl=Pin(9), sda=Pin(8), freq=100000)
lcd = I2cLcd(i2c, 0x27, 2, 16)

# 3. BUZZER CONFIGURATION
buzzer = PWM(Pin(7), freq=1000, duty=0)

# 4. SYSTEM SETTINGS
MAX_VOLTAGE = 30.0
MAX_CURRENT = 2.0
ADC_MAX = 4095

VOLTAGE_LIMIT = 24.0
VOLTAGE_RESET = 23.0

CURRENT_LIMIT = 1.0
CURRENT_RESET = 0.9

# Fault states
overvoltage = False
overcurrent = False

# 5. HELPER FUNCTIONS


def pad16(text):
    text = str(text)
    return text[:16] + " " * max(0, 16 - len(text))


def read_average(sensor, samples=10):
    total = 0

    for i in range(samples):
        total += sensor.read()
        sleep(0.01)

    return total / samples


# 6. DOUBLE-BEEP ALARM
alarm_pattern = [
    (300, 512),
    (200, 0),
    (300, 512),
    (1200, 0)
]

alarm_index = 0
alarm_start = ticks_ms()
alarm_active = False


def update_alarm(fault):
    global alarm_index, alarm_start, alarm_active

    now = ticks_ms()

    if not fault:
        buzzer.duty(0)
        alarm_index = 0
        alarm_active = False
        return

    if not alarm_active:
        alarm_index = 0
        alarm_start = now
        alarm_active = True

    duration, duty = alarm_pattern[alarm_index]
    buzzer.duty(duty)

    if ticks_diff(now, alarm_start) >= duration:
        alarm_index = (alarm_index + 1) % len(alarm_pattern)
        alarm_start = now


# 7. MAIN PROGRAM
lcd.clear()

last_publish = ticks_ms()

while True:

    # Read and average sensor values
    voltage_raw = read_average(voltage_sensor)
    current_raw = read_average(current_sensor)

    # Convert ADC readings
    voltage = (voltage_raw / ADC_MAX) * MAX_VOLTAGE
    current = (current_raw / ADC_MAX) * MAX_CURRENT

    # Calculate power
    power = voltage * current

    # Voltage fault detection
    if voltage > VOLTAGE_LIMIT:
        overvoltage = True
    elif voltage < VOLTAGE_RESET:
        overvoltage = False

        # Current fault detection
        if current > CURRENT_LIMIT:
            overcurrent = True
        elif current < CURRENT_RESET:
            overcurrent = False

    # Determine system status
    if overvoltage and overcurrent:
        status = "BOTH FAULTS"
    elif overvoltage:
        status = "OVERVOLTAGE"
    elif overcurrent:
        status = "OVERCURRENT"
    else:
        status = "NORMAL"

    # Activate alarm for either fault
    any_fault = overvoltage or overcurrent
    update_alarm(any_fault)

    # LCD DISPLAY
    line1 = "V:{:.1f} I:{:.2f}".format(
        voltage, current
    )

    if overvoltage and overcurrent:
        line2 = "FAULT:BOTH"
    elif overvoltage:
        line2 = "FAULT:OVERVOLT"
    elif overcurrent:
        line2 = "FAULT:OVERCUR"
    else:
        line2 = "P:{:.1f}W NORMAL".format(power)

    lcd.move_to(0, 0)
    lcd.putstr(pad16(line1))

    lcd.move_to(0, 1)
    lcd.putstr(pad16(line2))

    # SERIAL MONITOR
    print("------------------------")
    print("Voltage: {:.2f} V".format(voltage))
    print("Current: {:.2f} A".format(current))
    print("Power: {:.2f} W".format(power))
    print("Overvoltage:", overvoltage)
    print("Overcurrent:", overcurrent)
    print("System status:", status)

    # Publish measurements every second
    if ticks_diff(ticks_ms(), last_publish) >= 1000:
        data = {
            "voltage": voltage,
            "current": current,
            "power": power,
            "overvoltage": overvoltage,
            "overcurrent": overcurrent,
            "status": status
        }
        message = ujson.dumps(data)

        client.publish(MQTT_TOPIC, message)

        print("MQTT sent:", message)

        last_publish = ticks_ms()

    sleep(0.05)
