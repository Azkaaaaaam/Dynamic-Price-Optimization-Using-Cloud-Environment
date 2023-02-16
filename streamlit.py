import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET
import requests

st.title('Uber pickups in NYC')

# Set the API endpoint URL
url = "https://data.cityofnewyork.us/resource/755u-8jsi.json"

# Make a GET request to the API endpoint and store the response
response = requests.get(url)

# Check if the response was successful (status code 200)
if response.status_code == 200:
    # Convert the response to a JSON object
    data = response.json()

    # Initialize empty lists to store location_ids and zones
    location_ids = []
    zones = []

    # Loop through the data to extract the desired information
    for item in data:
        # Check if the object_id is within the desired range
        if int(item['objectid']) >= 1 and int(item['objectid']) <= 262:
            # Extract the location_id, borough, and zone from the current item
            location_id = item.get('locationid')
            borough = item.get('borough')
            zone = item.get('zone')

            # Append the extracted information to the lists
            location_ids.append(location_id)
            zones.append(zone)

            # Print the extracted information
            print(f"Location ID: {location_id}, Borough: {borough}, Zone: {zone}")
else:
    print("Error: Failed to retrieve data from the API")

# Create a dictionary to store the location_ids and zones
data_dict = {
    "Pickup location": zones,
    "Dropoff location": zones
}

# Create a pandas DataFrame from the dictionary
df = pd.DataFrame(data_dict)


col1, col2 = st.columns(2)

with col1:
            with st.form("my_form"):
                st.selectbox(
                    'Pickup location',
                    df["Pickup location"].unique()
                )  
                st.selectbox(
                    'Dropoff location',
                    df["Dropoff location"].unique()
                )  
                st.date_input(
                    'Date of pickup',
                    dt.date(2023, 5, 25)
                )            
                st.time_input(
                    'Time of pickup',
                    dt.time(0, 0),
                    help='Specify the time of pickup'
                )
                st.number_input(
                    'Number of Users',
                    value=1,
                    min_value=1,
                    max_value=5,
                    help='The number of users should be between 1 and 5'
                )

                # Every form must have a submit button.
                submitted = st.form_submit_button("Submit")
with col2:
      st.markdown('<iframe src="https://data.cityofnewyork.us/w/d3c5-ddgc/25te-f2tw?cur=cLNQRsEjlFe&from=root" width="600" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)


