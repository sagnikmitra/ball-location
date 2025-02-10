import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# File paths
LAST_VALUE_FILE = "last_value.json"
HISTORY_FILE = "location_history.json"

# Function to load last stored value
def load_last_value():
    try:
        with open(LAST_VALUE_FILE, "r") as file:
            return json.load(file).get("last_value", "No value stored yet")
    except FileNotFoundError:
        return "No value stored yet"

# Function to store new value
def store_value(value):
    with open(LAST_VALUE_FILE, "w") as file:
        json.dump({"last_value": value}, file)

# Function to load location history
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)

# Function to store location history with timestamp
def store_history(response, location):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({"timestamp": timestamp, "response": response, "location": location})
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Load last stored value
last_value = load_last_value()
st.logo('sagnik-design-logo-color.png', size="large")

st.title("🏓 Ping Pong Ball Last Location Tracker")
st.write(f"**Last Stored Value:** {last_value}")

# User selection for surety
response = st.radio("Select an option:", ["Surely", "Not Sure", "Probably"])

location = None
if response in ["Surely", "Probably"]:
    location = st.radio("Select a location:", [
        "Under Sagnik Bed",
        "Under Arnab Bed",
        "Behind Guitar",
        "Behind Dustbin",
        "Behind Shoerack",
        "Inside Bag",
        "Under Almirah",
        "In the Bunker"
    ])

if st.button("Submit"):
    if response in ["Surely", "Probably"] and location:
        final_value = f"{response} - {location}"
        store_value(final_value)
        store_history(response, location)  # Store in history
        st.success("Submitted successfully!")
        st.write(f"**Updated Last Stored Value:** {final_value}")

history = load_history()

if history:
    df = pd.DataFrame(history)

    # Convert timestamp column to datetime for better processing
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Table 1: Location Summary
    location_counts = df["location"].value_counts().reset_index()
    location_counts.columns = ["Location", "Times Stored"]
    
    st.write("### 📊 Location History Summary")
    st.table(location_counts)

    # Table 2: Full Data Input History
    st.write("### 📜 Data Input History")
    st.table(df)

    # 📊 **Bar Chart: Location Frequency**
    st.write("### 📊 Location Count Bar Chart")
    fig_bar = px.bar(location_counts, x="Location", y="Times Stored", text="Times Stored",
                        labels={"Times Stored": "Number of Times Stored"},
                        title="📌 Frequency of Locations Stored",
                        color="Location")
    st.plotly_chart(fig_bar)

    # 📈 **Line Chart: Entries Over Time**
    df["count"] = range(1, len(df) + 1)  # Assign incremental count for tracking
    st.write("### 📈 Data Input Over Time")
    fig_line = px.line(df, x="timestamp", y="count", markers=True, title="📌 Data Input Timeline")
    st.plotly_chart(fig_line)

    # 📉 **Matplotlib Pie Chart**
    st.write("### 🍕 Pie Chart: Location Distribution")
    fig_pie, ax = plt.subplots()
    ax.pie(location_counts["Times Stored"], labels=location_counts["Location"], autopct='%1.1f%%', startangle=90)
    ax.axis("equal")
    st.pyplot(fig_pie)

else:
    st.write("No location history recorded yet.")
