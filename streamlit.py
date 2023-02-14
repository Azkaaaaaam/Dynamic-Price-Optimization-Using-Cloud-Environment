!pip install joblib

import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the machine learning model and preprocessing objects
model = joblib.load('model.pkl')
scaler = joblib.load('scaler.pkl')
onehot = joblib.load('onehot.pkl')

# Define the Streamlit app
def app():
    # Define the app title
    st.title('NYC Taxi Fare Prediction App')
    
    # Define the input fields
    pickup_datetime = st.date_input("Pickup Date")
    pickup_time = st.time_input("Pickup Time")
    pickup_longitude = st.number_input("Pickup Longitude")
    pickup_latitude = st.number_input("Pickup Latitude")
    dropoff_longitude = st.number_input("Dropoff Longitude")
    dropoff_latitude = st.number_input("Dropoff Latitude")
    passenger_count = st.number_input("Passenger Count", min_value=1, max_value=6, value=1)
    
    # Prepare the input data
    input_data = pd.DataFrame({
        'pickup_datetime': [pd.to_datetime(str(pickup_datetime) + ' ' + str(pickup_time))],
        'pickup_longitude': [pickup_longitude],
        'pickup_latitude': [pickup_latitude],
        'dropoff_longitude': [dropoff_longitude],
        'dropoff_latitude': [dropoff_latitude],
        'passenger_count': [passenger_count]
    })
    
    # Preprocess the input data
    input_data['hour'] = input_data['pickup_datetime'].dt.hour
    input_data['weekday'] = input_data['pickup_datetime'].dt.weekday
    input_data = scaler.transform(input_data)
    input_data = onehot.transform(input_data)
    
    # Make the prediction
    prediction = model.predict(input_data)
    
    # Display the prediction
    st.header("Estimated Taxi Fare:")
    st.write("$" + str(round(prediction[0], 2)))
