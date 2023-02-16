import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET

st.title('Uber pickups in NYC')

import requests

url = "https://data.cityofnewyork.us/resource/755u-8jsi.json"
response = requests.get(url)

if response.status_code == 200:
    data = response.json()
    zones = []
    location_ids = []
    for item in data:
        zone = item.get("zone")
        if zone not in zones:
            zones.append(zone)
        location_id = item.get("location_id")
        if location_id not in location_ids:
            location_ids.append(location_id)
else:
    print(f"Error retrieving data: {response.reason}")

col1, col2 = st.columns(2)

with col1:
            with st.form("my_form"):
                st.selectbox(
                    'Pickup location',
                    zone
                )  
                st.selectbox(
                    'Dropoff location',
                    location_id
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


