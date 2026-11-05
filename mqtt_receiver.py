
import paho.mqtt.client as mqtt
import json
import os
import csv
import time
from datetime import datetime

BROKER = "broker.emqx.io"
PORT = 1883
TOPIC = "dcpm/demo-73921"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "latest_data.json")
TEMP_FILE = os.path.join(BASE_DIR, "latest_data.tmp")
CSV_FILE = os.path.join(BASE_DIR, "measurement_history.csv")

LOG_INTERVAL = 10
last_log_time = 0


def on_connect(client, userdata, flags, reason_code, properties):
    if reason_code == 0:
        print("Connected to MQTT broker!")
        client.subscribe(TOPIC)
        print("Subscribed to:", TOPIC)
        print("CSV file:", CSV_FILE)
    else:
        print("Connection failed:", reason_code)


def on_message(client, userdata, message):
    global last_log_time

    try:
        data = json.loads(message.payload.decode())

        # Update the latest measurements for the dashboard
        with open(TEMP_FILE, "w") as file:
            json.dump(data, file)

        os.replace(TEMP_FILE, DATA_FILE)

        # Log one reading every 10 seconds
        current_time = time.monotonic()

        if current_time - last_log_time >= LOG_INTERVAL:

            file_exists = os.path.exists(CSV_FILE)

            with open(CSV_FILE, "a", newline="") as file:
                writer = csv.writer(file)

                if not file_exists:
                    writer.writerow([
                        "Timestamp",
                        "Voltage (V)",
                        "Current (A)",
                        "Power (W)",
                        "Overvoltage",
                        "Overcurrent",
                        "Status"
                    ])

                writer.writerow([
                    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    data["voltage"],
                    data["current"],
                    data["power"],
                    data["overvoltage"],
                    data["overcurrent"],
                    data["status"]
                ])

            last_log_time = current_time

            print("CSV: Measurement saved!")

        # Display incoming measurements
        print("\n------ ESP32 MEASUREMENTS ------")
        print("Voltage:", data["voltage"], "V")
        print("Current:", data["current"], "A")
        print("Power:", data["power"], "W")
        print("System status:", data["status"])
        print("--------------------------------")

    except Exception as error:
        print("Error:", error)


client = mqtt.Client(
    mqtt.CallbackAPIVersion.VERSION2,
    client_id="dcpm-python-elvis-receiver-73921"
)

client.on_connect = on_connect
client.on_message = on_message

print("Connecting to MQTT broker...")

client.connect(BROKER, PORT, 60)
client.loop_forever()
