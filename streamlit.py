import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET

st.title('Uber pickups in NYC')

DATE_COLUMN = 'date/time'
DATA_URL = ('https://s3-us-west-2.amazonaws.com/'
            'streamlit-demo-data/uber-raw-data-sep14.csv.gz')

def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows)
    lowercase = lambda x: str(x).lower()
    data.rename(lowercase, axis='columns', inplace=True)
    data[DATE_COLUMN] = pd.to_datetime(data[DATE_COLUMN])
    return data

data_load_state = st.text('Loading data...')
data = load_data(10000)
data_load_state.text("Done!")

# Retrieve the XML file from the URL
url = "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.xml?accessType=DOWNLOAD"
response = urllib.request.urlopen(url)
xml_data = response.read()

# Parse the XML data and extract the id of the pickup place
root = ET.fromstring(xml_data)
for row in root.iter("row"):
    pickup_place_id = row.find("pickup_location_id").text
    print(pickup_place_id)
col1, col2 = st.columns(2)

with col1:
            with st.form("my_form"):
                st.selectbox(
                    'Pickup location',
                    ('NYC','NYC2','NYC4','NYC5')
                )  
                st.selectbox(
                    'Dropoff location',
                    ('NYC','NYC2','NYC4','NYC5')
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
      with st.sidebar:
            st.markdown('<iframe src="https://data.cityofnewyork.us/w/d3c5-ddgc/25te-f2tw?cur=cLNQRsEjlFe&from=root" 
                        width="500" height="425" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)


