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

               # Every form must have a submit button.
               submitted = st.form_submit_button("Submit")
               if submitted:
                   st.write("slider", slider_val, "checkbox", checkbox_val)
            st.write("Outside the form")

with col2:
            st.subheader('Map of all pickups at %s:00')
            st.map(filtered_data)
