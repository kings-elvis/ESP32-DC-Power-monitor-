
import streamlit as st
import pandas as pd
import json
import os

from streamlit_autorefresh import st_autorefresh

# ---------------------------------
# DASHBOARD CONFIGURATION
# ---------------------------------

st.set_page_config(
    page_title="DC Power Monitor",
    page_icon="⚡",
    layout="wide"
)

st_autorefresh(interval=2000, key="refresh")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DATA_FILE = os.path.join(BASE_DIR, "latest_data.json")
CSV_FILE = os.path.join(BASE_DIR, "measurement_history.csv")

st.title("⚡ DC Power Monitoring System")
st.caption("ESP32-C3 Based Electrical Monitoring Dashboard")

st.divider()

# ---------------------------------
# READ LATEST ESP32 MEASUREMENTS
# ---------------------------------

if not os.path.exists(DATA_FILE):
    st.error("Waiting for ESP32 measurements...")
    st.stop()

try:
    with open(DATA_FILE, "r") as file:
        data = json.load(file)

except Exception as error:
    st.error(f"Could not read ESP32 data: {error}")
    st.stop()

voltage = float(data["voltage"])
current = float(data["current"])
power = float(data["power"])
status = data["status"]

# ---------------------------------
# LIVE MEASUREMENTS
# ---------------------------------

st.subheader("Live Electrical Measurements")

col1, col2, col3 = st.columns(3)

col1.metric("Voltage", f"{voltage:.2f} V")
col2.metric("Current", f"{current:.2f} A")
col3.metric("Power", f"{power:.2f} W")

# ---------------------------------
# SYSTEM STATUS
# ---------------------------------

st.subheader("System Status")

if status == "NORMAL":
    st.success("SYSTEM NORMAL")

elif status == "BOTH FAULTS":
    st.error("OVERVOLTAGE AND OVERCURRENT")

else:
    st.error(status)

fault1, fault2 = st.columns(2)

if data["overvoltage"]:
    fault1.error("Overvoltage detected")
else:
    fault1.success("Voltage within limits")

if data["overcurrent"]:
    fault2.error("Overcurrent detected")
else:
    fault2.success("Current within limits")

st.divider()

# ---------------------------------
# HISTORICAL MEASUREMENTS
# ---------------------------------

st.subheader("Historical Measurement Analysis")

if not os.path.exists(CSV_FILE):
    st.info("No historical measurements recorded yet.")

else:
    try:
        df = pd.read_csv(CSV_FILE)

        if df.empty:
            st.info("Waiting for recorded measurements...")

        else:
            df["Timestamp"] = pd.to_datetime(df["Timestamp"])

            df = df.sort_values("Timestamp")

            st.caption(
                f"Total recorded measurements: {len(df)}"
            )

            # Voltage graph
            st.subheader("Voltage Trend")
            st.line_chart(
                df,
                x="Timestamp",
                y="Voltage (V)"
            )

            # Current graph
            st.subheader("Current Trend")
            st.line_chart(
                df,
                x="Timestamp",
                y="Current (A)"
            )

            # Power graph
            st.subheader("Power Trend")
            st.line_chart(
                df,
                x="Timestamp",
                y="Power (W)"
            )

            st.divider()

            # Measurement table
            st.subheader("Recorded Measurement History")

            st.dataframe(
                df.iloc[::-1],
                use_container_width=True,
                hide_index=True
            )

            # CSV download
            csv_data = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download Measurement History (CSV)",
                data=csv_data,
                file_name="dc_power_measurements.csv",
                mime="text/csv"
            )

    except Exception as error:
        st.error(f"Error loading measurement history: {error}")

st.divider()

st.caption(
    "ESP32-C3 | MicroPython | MQTT | Python | Streamlit"
)
