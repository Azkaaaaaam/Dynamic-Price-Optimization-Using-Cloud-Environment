import streamlit as st
import pandas as pd
import numpy as np

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

col1, col2 = st.columns(2)

with col1:

            with st.form("my_form"):
               st.write("Inside the form")
               slider_val = st.slider("Form slider")
               checkbox_val = st.checkbox("Form checkbox")
               # Some number in the range 0-23
               hour_to_filter = st.slider('hour', 0, 23, 17)
               filtered_data = data[data[DATE_COLUMN].dt.hour == hour_to_filter]
               # Every form must have a submit button.
               submitted = st.form_submit_button("Submit")
                        
                        
               pickup = st.text_input("Pickup location")
               dropoff = st.text_input("Dropoff location")
               date = st.date_input("Date of pickup")
               time = st.time_input("Time of pickup")
               if submitted:
                   st.write("slider", slider_val, "checkbox", checkbox_val)
            st.write("Outside the form")

with col2:
            st.subheader('Map of all pickups at %s:00' % hour_to_filter)
            st.map(filtered_data)
