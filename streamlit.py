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

    # Initialize empty lists to store location_ids, zones, and coordinates
    location_ids = []
    zones = []
    latitudes = []
    longitudes = []

    # Loop through the data to extract the desired information
    for item in data:
        # Check if the object_id is within the desired range
        if int(item['objectid']) >= 1 and int(item['objectid']) <= 262:
            # Extract the location_id, borough, and zone from the current item
            location_id = item.get('locationid')
            borough = item.get('borough')
            zone = item.get('zone')
            
            # Check if the the_geom key exists in the current item
            if 'the_geom' in item:
                # Get the coordinates from the geometry
                geometry = item['the_geom']
                if 'coordinates' in geometry:
                    coordinates = geometry['coordinates']
                    if len(coordinates) >= 2:
                        # Extract the latitude and longitude from the coordinates
                        latitude = coordinates[1]
                        longitude = coordinates[0]
                    else:
                        latitude = None
                        longitude = None
                else:
                    latitude = None
                    longitude = None
            else:
                latitude = None
                longitude = None


            # Append the extracted information to the lists
            location_ids.append(location_id)
            zones.append(zone)
            latitudes.append(latitude)
            longitudes.append(longitude)

            # Print the extracted information
            print(f"Location ID: {location_id}, Borough: {borough}, Zone: {zone}, Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Error: Failed to retrieve data from the API")

# Create a dictionary to store the location_ids, zones, latitudes, and longitudes
data_dict = {
    "Pickup location": zones,
    "Dropoff location": zones,
    "Latitude": latitudes,
    "Longitude": longitudes
}

# Create a pandas DataFrame from the dictionary
df = pd.DataFrame(data_dict)

col1, col2 = st.columns(2)

with col1:
    with st.form("my_form"):
        pickup_location = st.selectbox(
            'Pickup location',
            df["Pickup location"].unique()
        )  
        dropoff_location = st.selectbox(
            'Dropoff location',
            df["Dropoff location"].unique()
        )  
        pickup_date = st.date_input(
            'Date of pickup',
            dt.date(2023, 5, 25)
        )            
        pickup_time = st.time_input(
            'Time of pickup',
            dt.time(0, 0),
            help='Specify the time of pickup'
        )
        num_users = st.number_input(
            'Number of Users',
            value=1,
            min_value=1,
            max_value=5,
            help='The number of users should be between 1 and 5'
        )

        # Every form must have a submit button.
        submitted = st.form_submit_button("Submit")

if submitted:
    # Access the form results if the form was submitted
    pulocation = pickup_location
    dolocation = dropoff_location
    tpep_pickup_datetime = pd.to_datetime(str(pickup_date) + ' ' + str(pickup_time))
    # Do something with the form results
    st.write(f"Pickup location: {pulocation}")
    st.write(f"Dropoff location: {dolocation}")
    st.write(f"Latitude: {Latitude}")
    st.write(f"Longitude: {Longitude}")


with col2:
      st.markdown('<iframe src="https://data.cityofnewyork.us/w/d3c5-ddgc/25te-f2tw?cur=cLNQRsEjlFe&from=root" width="600" height="600" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)


