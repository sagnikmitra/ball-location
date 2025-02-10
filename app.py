import streamlit as st
import json

# Function to load last stored value
def load_last_value():
    try:
        with open("last_value.json", "r") as file:
            return json.load(file).get("last_value", "No value stored yet")
    except FileNotFoundError:
        return "No value stored yet"

# Function to store new value
def store_value(value):
    with open("last_value.json", "w") as file:
        json.dump({"last_value": value}, file)

# Load last stored value
last_value = load_last_value()

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
        st.success("Submitted successfully!")
        st.write(f"**Updated Last Stored Value:** {final_value}")
