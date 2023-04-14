
# Dynamic Price Optimization Using Cloud Environment: A New Approach for NYC Taxi Fare Pricing

This  study aims to estimate the cost of taxi rides in New York City using machine learning techniques. The methodology entails data gathering, preprocessing, and modeling with the surge multiplier effect and weather conditions taken into account in the regression. A new static price dataset was constructed by combining two existing datasets. By estimating the number of trips per hour for each day and adding surge multipliers based on quartiles of the demand for taxis, the surge multiplier impact was captured. The data was then preprocessed using feature engineering, data cleansing, and data transformation. The results showed that the random forest model performed better than the other models (Decision Trees, Monte Carlo, LSTM) across all evaluation metrics when four machine learning models were applied. 
The models were deployed in both Google Cloud Platform and Amazon Web Services, and a real-time simulation application was developed to showcase the successful implementation of the models.




# Related Links

Here are some important links related  to the projects

[Streamlit Application - Real Time Simulation](https://azkaaaaaam-thesis-streamlit-1r5biv.streamlit.app/)

[Step by Step - How to Deploy a Model in Cloud - GCP ](https://github.com/Azkaaaaaam/Thesis/blob/ec3176c7e9929c882250a893e08b3fffdba05e9c/GCP%20Deployment%20-%20Surge%20Example/Step%20by%20Step%20-%20How%20to%20Deploy%20a%20Model%20in%20Cloud.pdf)

correct this link !
[Report Explaining the detailed work ](https://github.com/Azkaaaaaam/Thesis/blob/ec3176c7e9929c882250a893e08b3fffdba05e9c/GCP%20Deployment%20-%20Surge%20Example/Step%20by%20Step%20-%20How%20to%20Deploy%20a%20Model%20in%20Cloud.pdf)

# Repository Tour 


## Data Collection
Two datasets were collected: one containing information about taxi rides and the other about weather conditions in the city. These datasets were merged to create a new static price dataset. The surge multiplier effect was captured by calculating the number of trips per hour for each day and adding surge multipliers based on quartiles of the demand for taxis.

## Data Modeling
The data was preprocessed through data cleaning, transformation, and feature engineering. Four machine learning models were used to estimate surge and price: decision tree, random forest, LSTM (only for pricing modeling), and Monte Carlo simulation. The random forest model outperformed the other models in terms of all evaluation metrics.
## AWS Deployment - Surge Example
This repository contains the code and data files used for deploying a machine learning model to estimate surge pricing for taxi rides in New York City using Amazon Web Services (AWS).

## GCP Deployment
The same machine learning models were deployed in Google Cloud Platform (GCP) and a comparison was made between AWS and GCP in terms of machine learning services, pricing, and control levels.

## Real-time Simulation Application
A real-time simulation application was developed using the library "streamlit" to showcase how the machine learning models have been successfully implemented. The application collects various inputs such as trip distance, trip duration, departure location ID, date, time of pickup, number of passengers, and weather information to estimate the dynamic surge price of the trip using two pre-trained models.

#### Files
- Weather2021_2022.csv: weather data file
- model.pkl: pre-trained surge model file
- modelprice.pkl: pre-trained price model file
- rows.rdf: dataset file
- streamlit.py: code for the real-time simulation application
- taxi_zones.csv: taxi zone lookup file
- requirements.txt: list of required Python packages

### NB:
Note that the endpoint for invoking the pre-trained models in the front-end application is not activated due to billing options not being activated. Instead, the pre-trained models can be uploaded to the repository and called from there.

## 🚀 Context
This work is done by me - Azza Kamoun - as part of my research thesis for my 2nd year of masters, with the supervision of my profesor Madan Radhakrishnan. The project had some important learning points mainly the cloud deployment with both AWS & GCP.
