import streamlit as st
import pandas as pd
import numpy as np
import pydeck as pdk
import datetime as dt
import urllib.request
import xml.etree.ElementTree as ET
import requests
import pydeck as pdk
from math import radians, cos, sin, asin, sqrt
import os
# from googleapiclient.discovery import build
import googleapiclient.discovery

# Setup environment credentials 
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "thesis-380313-4a81186c4101.json" # change for your GCP key
PROJECT = "thesis-380313" # change for your GCP project
REGION = "us-central1" # change for your GCP region (where your model is hosted)

st.set_page_config(layout="wide")
st.title('Yellow Taxis pickups in NYC')


url2 = "https://data.cityofnewyork.us/resource/m6nq-qud6.json?$query=SELECT%0A%20%20%60tpep_pickup_datetime%60%2C%0A%20%20%60tpep_dropoff_datetime%60%2C%0A%20%20%60passenger_count%60%2C%0A%20%20%60trip_distance%60%2C%0A%20%20%60pulocationid%60%2C%0A%20%20%60dolocationid%60%2C%0A%20%20%60total_amount%60"

response2 = requests.get(url2)
if response2.status_code == 200:
    data2 = response2.json()
    df = pd.json_normalize(data2)
    print(df.head())
else:
    print("Error: Could not retrieve data from API.")

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
    coordinates = []    

    # Loop through the data to extract the desired information
    for item in data:
        # Check if the object_id is within the desired range
        if int(item['objectid']) >= 1 and int(item['objectid']) <= 262:
            # Extract the location_id, borough, and zone from the current item
            location_id = item.get('locationid')
            borough = item.get('borough')
            zone = item.get('zone')
            # Get the coordinates from the geometry
            geometry = item.get('the_geom')
            coordinates = geometry['coordinates']
            coordinates =coordinates[0][0][0]
            latitude = coordinates[1]
            longitude = coordinates[0]
    
            # Append the extracted information to the lists
            location_ids.append(location_id)
            zones.append(zone)
            latitudes.append(latitude)
            longitudes.append(longitude)

            # Print the extracted information
            print(f"Location ID: {location_id}, Borough: {borough}, Zone: {zone}, coordinates: {coordinates}, Latitude: {latitude}, Longitude: {longitude}")
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

def haversine(lon1, lat1, lon2, lat2):
    # Convert latitude and longitude values to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Calculate the haversine distance
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of earth in kilometers
    return c * r

# Estimate the duration of a trip based on the distance and assuming that the speed average that we define later ( 60 km/h) 
def estimate_duration(distance, speed):
    # Calculate the duration in minutes
    duration = distance / speed * 60

    return duration

col1, col2, col3 = st.columns([0.25, 0.5, 0.25])

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

        # Get the latitude and longitude of the pickup and dropoff locations
        pickup_lat = df[df["Pickup location"] == pulocation]["Latitude"].iloc[0] 
        pickup_lon = df[df["Pickup location"] == pulocation]["Longitude"].iloc[0]
        dropoff_lat = df[df["Dropoff location"] == dolocation]["Latitude"].iloc[0] 
        dropoff_lon = df[df["Dropoff location"] == dolocation]["Longitude"].iloc[0]  
        # Calculate the distance between the pickup and dropoff locations
        distance =haversine(pickup_lat, pickup_lon, dropoff_lat, dropoff_lon)
        # Estimate the duration of the trip based on the distance and average speed of 50KM/H
        speed = 50  # Average speed in kilometers per hour
        duration = estimate_duration(distance, speed)

with col2:
      st.markdown('<iframe src="https://data.cityofnewyork.us/w/d3c5-ddgc/25te-f2tw?cur=cLNQRsEjlFe&from=root" width="620" height="500" frameborder="0" scrolling="no"></iframe>', unsafe_allow_html=True)
        
with col3:
    if submitted:
          st.success(f"Distance between pickup and dropoff locations: {distance:.2f} km")
          st.success(f"Trip Duration: {duration:.2f} mins")

# Do something with the form results and calculated distance
#st.write(f"Pickup location: {pulocation}")
#st.write(f"Pickup lat: {pickup_lat}")
#st.write(f"Pickup lon: {pickup_lon}")

#st.write(f"Dropoff location: {dolocation}")
#st.write(f"Dropoff lat: {dropoff_lat}")
#st.write(f"Dropoff lon: {dropoff_lon}")
#st.write(f"Distance between pickup and dropoff locations: {distance:.2f} km")
#st.write(f"Trip Duration: {duration:.2f} mins")


    # Get the user input
    pickup_datetime = pd.to_datetime(str(pickup_date) + ' ' + str(pickup_time))
    passenger_count = num_users

    # Prepare the request data
    request_data = {
        "pickup_datetime": pickup_datetime.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
        "pickup_longitude": df.loc[df["Pickup location"]==pickup_location, "Longitude"].values[0],
        "pickup_latitude": df.loc[df["Pickup location"]==pickup_location, "Latitude"].values[0],
        "dropoff_longitude": df.loc[df["Dropoff location"]==dropoff_location, "Longitude"].values[0],
        "dropoff_latitude": df.loc[df["Dropoff location"]==dropoff_location, "Latitude"].values[0],
        "passenger_count": passenger_count
    }

    # Call the prediction API
    url = f"https://{REGION}-ml.googleapis.com/v1/projects/{PROJECT}/models/taxifare:predict"
    headers = {
        "Authorization": "Bearer $(gcloud auth application-default print-access-token)",
        "Content-Type": "application/json"
    }
    response = requests.post(url, headers=headers, json={"instances": [request_data]})

    # Parse the response
    if response.status_code == 200:
        prediction = response.json()['predictions'][0]['fare_amount']
        st.success(f"The predicted fare amount is {prediction:.2f}$")
    else:
        st.error("Failed to get the prediction from the model.")
        
        import json

# Set up the required arguments
project = "thesis-380313"
region = "us-central1"
model = "surge"
version = "V2"  # or specify a version if applicable


def predict_json(project, region, model, instances, version=None):
    """Send json data to a deployed model for prediction.

    Args:
        project (str): project where the Cloud ML Engine Model is deployed.
        region (str): regional endpoint to use; set to None for ml.googleapis.com
        model (str): model name.
        instances ([Mapping[str: Any]]): Keys should be the names of Tensors
            your deployed model expects as inputs. Values should be datatypes
            convertible to Tensors, or (potentially nested) lists of datatypes
            convertible to tensors.
        version: str, version of the model to target.
    Returns:
        Mapping[str: any]: dictionary of prediction results defined by the
            model.
    """
    # Create the ML Engine service object.
    # To authenticate set the environment variable
    # GOOGLE_APPLICATION_CREDENTIALS=<path_to_service_account_file>
    prefix = "{}-ml".format(region) if region else "ml"
    api_endpoint = "https://{}.googleapis.com".format(prefix)
    client_options = ClientOptions(api_endpoint=api_endpoint)
    service = googleapiclient.discovery.build(
        'ml', 'v1', client_options=client_options)
    name = 'projects/{}/models/{}'.format(project, model)

    if version is not None:
        name += '/versions/{}'.format(version)

    response = service.projects().predict(
        name=name,
        body={'instances': instances}
    ).execute()

    if 'error' in response:
        raise RuntimeError(response['error'])

    return response['predictions']

# Create a sample input JSON request
input_data = {
    "instances": [
        [1, 1, 0, 1.495619524, 2.704968711, 15.95906133, 3.5, 0.5, 0, 25.2, 37.9, 36.94705882]
    ]
}
input_json = json.dumps(input_data)

# Call the predict_json() function
predictions = predict_json(project, region, model, input_data, version)

# Print the output
print(predictions)

