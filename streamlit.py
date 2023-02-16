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

# Parse the XML data and extract the list of zones
root = ET.fromstring(xml_data)
zones = [elem.find("zone").text for elem in root.iter("row")]


col1, col2 = st.columns(2)

with col1:
            with st.form("my_form"):
                st.selectbox(
                    'Pickup location',
                    zones
                )  
                st.selectbox(
                    'Dropoff location',
                    zones
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


