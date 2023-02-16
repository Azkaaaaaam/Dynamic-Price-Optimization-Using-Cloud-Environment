import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET

st.title('Uber pickups in NYC')

# Retrieve the XML file from the URL
url = "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.xml?accessType=DOWNLOAD"
response = urllib.request.urlopen(url)
xml_data = response.read()
# Parse the XML data
root = ET.fromstring(xml_data)

# Extract the zones data
zones = []
for elem in root.iter("row"):
    zone_element = elem.find("zone")
    zone = zone_element.text if zone_element is not None else ""
    
    location_id_element = elem.find("location_id")
    location_id = location_id_element.text if location_id_element is not None else ""
    
    borough_element = elem.find("borough")
    borough = borough_element.text if borough_element is not None else ""
    
    zones.append([zone, location_id, borough])


col1, col2 = st.columns(2)

with col1:
            with st.form("my_form"):
                st.selectbox(
                    'Pickup location',
                    zone
                )  
                st.selectbox(
                    'Dropoff location',
                    zone
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


