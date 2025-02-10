import streamlit as st
import json
import os
import pandas as pd
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

st.title("Ping Pong Ball Last Location Updation App")
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

    # Table 1: Location Summary
    location_counts = df["location"].value_counts().reset_index()
    location_counts.columns = ["Location", "Times Stored"]
    
    st.write("### 📊 Location History Summary")
    st.table(location_counts)

    # Table 2: Full Data Input History
    st.write("### 📜 Data Input History")
    st.table(df)
else:
    st.write("No location history recorded yet.")
