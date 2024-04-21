
# create a component using yaml definition

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
import xgboost as xgb
import pandas as pd
import numpy as np
import argparse
import os
import mlflow

# start logging

mlflow.start_run(experiment_id="diabetes_01")

mlflow.autolog()


def main(args):
    """ main function for this script """
    df = get_data(select_first_file(args.prepped_data))

    # separate features and target
    X = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    #split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state=42)

    # create Xgboost Dmatrix data format
    dtrain = xgb.DMatrix(X_train, label=y_train)
    dtest = xgb.DMatrix(X_test, label=y_test)

    # train the model with default parameters
    bst = xgb.train({}, dtrain)

    dtest = xgb.DMatrix(X_test)
    y_pred = bst.predict(dtest)

    # convert probabilities to binary predictions (0 or 1)
    y_pred_binary = np.round(y_pred)
    
    accuracy = accuracy_score(y_test, y_pred_binary)

    mlflow.log_metric("accuracy",accuracy)

    mlflow.end_run()

def select_first_file(path):
    """ select first file from path, assume only one file to be read, otherwise will have to iterate"""
    files = os.listdir(path)
    return os.path.join(path, files[0])

def get_data(filepath):
    """ function used to read blob given a uri """
    df = pd.read_csv(filepath)

    return df

def parse_args():
    """ read args passed to script"""

    parser = argparse.ArgumentParser()

    parser.add_argument("--prepped_data", type=str)

    args = parser.parse_args()

    return args

# run script

if __name__ == "__main__":

    # parse args
    args = parse_args()

    # run main function
    main(args)