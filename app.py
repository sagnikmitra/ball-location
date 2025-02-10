import streamlit as st
import json
import os
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
from datetime import datetime

# File path for storing history
HISTORY_FILE = "location_history.json"

# Function to load location history
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    with open(HISTORY_FILE, "r") as file:
        return json.load(file)

# Function to store new location history entry
def store_history(response, location):
    history = load_history()
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history.append({"timestamp": timestamp, "response": response, "location": location})
    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

# Load location history
history = load_history()

# Get the last stored value and timestamp dynamically from history
if history:
    last_entry = history[-1]  # Get the most recent entry
    last_value = f"{last_entry['response']} - {last_entry['location']}"
    last_timestamp = last_entry["timestamp"]
else:
    last_value = "No value stored yet"
    last_timestamp = "N/A"

# 🎨 UI Enhancements
st.set_page_config(page_title="Ping Pong Ball Tracker", page_icon="🏓")
st.image('sagnik-design-logo-color.png', width=150)

# 🏓 **Title**
st.markdown("<h1 style='text-align: center; color: #FF5733;'>🏓 Ping Pong Ball Tracker 🏓</h1>", unsafe_allow_html=True)

# 📌 **Last Stored Value with Timestamp (Fetched from History)**
st.markdown(f"""
    <h3 style='text-align: center; color: #0E84FC;'>🔎 Last Stored Value: {last_value}</h3>
    <h5 style='text-align: center; color: #FF5733;'>🕒 As of {last_timestamp}</h5>
""", unsafe_allow_html=True)

st.markdown("---")

# 📍 **User Input Section**
st.markdown("### 📌 Update Ball Location")
response = st.radio("🔽 **How sure are you about the location?**", ["Surely", "Not Sure", "Probably"])

location = None
if response in ["Surely", "Probably"]:
    location = st.selectbox("📍 **Select a location:**", [
        "Under Sagnik Bed",
        "Under Arnab Bed",
        "Behind Guitar",
        "Behind Dustbin",
        "Behind Shoerack",
        "Inside Bag",
        "Under Almirah",
        "In the Bunker"
    ])

if st.button("🚀 Submit Update"):
    if response in ["Surely", "Probably"] and location:
        store_history(response, location)
        st.success("✅ Location Updated Successfully!")
        st.rerun()  # Refresh the app to update the last stored value dynamically

st.markdown("---")

# 📊 **Data Visualization**
if history:
    df = pd.DataFrame(history)
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # 📌 **Table: Location Summary**
    location_counts = df["location"].value_counts().reset_index()
    location_counts.columns = ["Location", "Times Stored"]
    
    st.markdown("### 📊 Location Summary")
    st.table(location_counts)

    # 📜 **Table: Full Data Input History**
    st.markdown("### 📜 Full Data Input History")
    st.dataframe(df, use_container_width=True)

    # 📊 **Bar Chart: Location Frequency**
    st.markdown("### 📊 Location Count Bar Chart")
    fig_bar = px.bar(location_counts, x="Location", y="Times Stored", text="Times Stored",
                     labels={"Times Stored": "Number of Times Stored"},
                     title="📌 Frequency of Locations Stored", color="Location",
                     color_discrete_sequence=px.colors.qualitative.Plotly)
    st.plotly_chart(fig_bar, use_container_width=True)

    # 📈 **Line Chart: Entries Over Time**
    df["count"] = range(1, len(df) + 1)
    st.markdown("### 📈 Data Input Over Time")
    fig_line = px.line(df, x="timestamp", y="count", markers=True,
                       title="📌 Data Input Timeline",
                       line_shape="spline", render_mode="svg")
    st.plotly_chart(fig_line, use_container_width=True)

    # 📉 **Pie Chart: Location Distribution**
    st.markdown("### 🍕 Pie Chart: Location Distribution")
    fig_pie, ax = plt.subplots()
    ax.pie(location_counts["Times Stored"], labels=location_counts["Location"],
           autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    ax.axis("equal")
    st.pyplot(fig_pie)

else:
    st.warning("⚠️ No location history recorded yet.")
