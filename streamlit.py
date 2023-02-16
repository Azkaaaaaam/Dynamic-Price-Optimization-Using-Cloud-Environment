import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt

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
                        st.selectbox(
                          'Pickup location',
                          ('NYC','NYC2','NYC4','NYC5'),
                        )  
                        st.selectbox(
                          'Dropoff location',
                          ('NYC','NYC2','NYC4','NYC5'),
                        )  
                        st.date_input(
                          'Date of pickup',
                          dt.date(2023, 25, 5)
                        )            
                        st.time_input(
                          'Label goes here',
                          dt.time(0, 0),
                          help='Help message goes here'
                        )
                        st.number_input(
                          'Number of Users',
                          1,
                          help='The number of users need to be from 1 to 5'
                        )
                             # Every form must have a submit button.
                        submitted = st.form_submit_button("Estimate my Fare")
             if submitted:
                        st.write("slider", slider_val, "checkbox", checkbox_val)

with col2:
            chart_data = pd.DataFrame(
               np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],
               columns=['lat', 'lon'])

            st.pydeck_chart(pdk.Deck(
                map_style=None,
                initial_view_state=pdk.ViewState(
                    latitude=37.76,
                    longitude=-122.4,
                    zoom=11,
                    pitch=50,
                ),
                layers=[
                    pdk.Layer(
                       'HexagonLayer',
                       data=chart_data,
                       get_position='[lon, lat]',
                       radius=200,
                       elevation_scale=4,
                       elevation_range=[0, 1000],
                       pickable=True,
                       extruded=True,
                    ),
                    pdk.Layer(
                        'ScatterplotLayer',
                        data=chart_data,
                        get_position='[lon, lat]',
                        get_color='[200, 30, 0, 160]',
                        get_radius=200,
                    ),
                ],
            ))

