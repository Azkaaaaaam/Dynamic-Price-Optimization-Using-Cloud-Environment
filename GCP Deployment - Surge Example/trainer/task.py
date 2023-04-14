import logging
import subprocess
import os, logging , argparse
#from joblib import dump
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split, cross_val_score , StratifiedShuffleSplit
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.datasets import make_regression
import pickle

# # 1- Loading Dataset

from google.cloud import storage
import io

# Set logging to see the Docker container logs
logging.basicConfig(level=logging.INFO)

# Load dataset from Google Cloud Storage
from google.cloud import storage
client = storage.Client()
bucket_name = "datasets_thesis"
blob_name = "preprocessed_surge.csv"
bucket = client.bucket(bucket_name)
blob = bucket.blob(blob_name)
data = blob.download_as_string().decode("utf-8")
merged_df = pd.read_csv(io.StringIO(data))

# Filter the merged_df DataFrame to keep only the desired clusters
merged = merged_df

# Reset the index of the merged DataFrame
merged.reset_index(drop=True, inplace=True)

# In[30]:


X = merged.drop(["surge_multiplier"], axis=1)
y = merged["surge_multiplier"]

X_train, X_test, y_train, y_test = train_test_split(merged.drop("surge_multiplier", axis=1), merged["surge_multiplier"], test_size=0.2)

model = RandomForestRegressor(n_estimators=100, random_state=42).fit(X_train, y_train)

with open('model.pkl', 'wb') as f:
        pickle.dump(model, f)
# ### 4.3 Model Prediction

def prediction(X_test, model):
  
    # Predicton on test with giniIndex
    y_pred = model.predict(X_test)
    print("Predicted values:")
    print(y_pred)
    return y_pred

# # 5. Main Dataset: Running & Evaluating the Models

# #### Random Forest

y_pred_forest= prediction(X_test, model)
print(y_pred_forest)

artifact_filename = 'model.pkl'
local_path = artifact_filename
model_directory = os.environ.get('AIP_MODEL_DIR', '.')
storage_path = f'gs://boxwood-bliss-382412-bucket/{model_directory}/{artifact_filename}'
blob = storage.blob.Blob.from_string(storage_path, client=storage.Client())
blob.upload_from_filename(local_path)
logging.info("Model exported to: {}".format(storage_path))

