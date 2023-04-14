
import argparse
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import explained_variance_score, r2_score
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
import pickle

# inference functions ---------------
def model_fn(model_dir):
    with open(os.path.join(model_dir, 'model.pkl'), 'rb') as f:
        clf = pickle.load(f)
    return clf

if __name__ == '__main__':
    print('extracting arguments')
    parser = argparse.ArgumentParser()

    # hyperparameters sent by the client are passed as command-line arguments to the script.
    # to simplify the demo we don't use all sklearn RandomForest hyperparameters
    parser.add_argument('--n-estimators', type=int, default=100)
    parser.add_argument('--max_leaf_nodes', type=int, default=10)

    # Data, model, and output directories
    parser.add_argument('--model-dir', type=str, default=os.environ.get('SM_MODEL_DIR'))
    parser.add_argument('--train', type=str, default=os.environ.get('SM_CHANNEL_TRAIN'))
    parser.add_argument('--test', type=str, default=os.environ.get('SM_CHANNEL_TEST'))
    parser.add_argument('--train-file', type=str, default='surge_train.csv')
    parser.add_argument('--test-file', type=str, default='surge_test.csv')

    args, _ = parser.parse_known_args()

    print('reading data')
    train_df = pd.read_csv(os.path.join(args.train, args.train_file))
    test_df = pd.read_csv(os.path.join(args.test, args.test_file))
    #train_df = pd.read_csv('surge_train.csv')
    #test_df = pd.read_csv('surge_test.csv')
    
    print('building training and testing datasets')
   # numeric_transformer = Pipeline(steps=[('imputer', SimpleImputer(strategy='median'))])
    #preprocessor = ColumnTransformer(transformers=[('num', numeric_transformer, train_df.columns.tolist())])
    attributes = ['Day', 'Month', 'Hour', 'passenger_count', 'trip_distance', 'total_amount', 'temp', 'feelslike', 'snow', 'windspeed', 'cloudcover', 'duration']

    X_train =train_df[attributes]
    X_test = test_df[attributes]
    y_train = train_df['target']
    y_test = test_df['target']

    # train
    print('training model')
    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # persist model
    path = os.path.join(args.model_dir, "model.pkl")
    with open(path, 'wb') as f:
        pickle.dump(model, f)
    print('model persisted at ' + path)

    # print explained_variance_score
    print('validating model')
    predictions = model.predict(X_test)
    print("R2 score : %.2f" % r2_score(y_test, predictions))


