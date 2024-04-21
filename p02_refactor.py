
# refactor

# we will be creating a two component pipeline with this example, including a data prep component + training component
# illustrating the changes by combining both components into one script, however I will have to separate scripts

from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
import numpy as np
import pandas as pd
import argparse


def main(args):

    #component 1 for data prep
    df = get_data(args.training_data)

    df_prepped = data_prep(df)

    # component 2 for training
    diabetes_model = train(df_prepped)

    return diabetes_model

def get_data():

    df = pd.read_csv(filepath)

    return df

def parse_args():

    parser = argparse.ArgumentParser()

    parser.add_argument("--training_data", type=str)

    args = parser.parse_args()

    return args

def data_prep(df):

    #separate numeric columns ( excluding last column)
    numeric_columns = df.select_dtypes(include=['float64','int64']).columns[:-1]

    # initialize MinMaxScaler
    scaler = MinMaxScaler()

    # scale only the numeric columns

    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df

def train(df):

    # separate features (x) and target (y)
    x = df.drop(columns=["Outcome"])
    y = df["Outcome"]

    # split the data into training and test sets 
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.20, random_state=42)

    # create xgboost dmatrix
    dtrain = xgb.DMatrix(x_train, label=y_train)
    dtest = xgb.DMatrix(x_test, label=y_test)

    # train with the default parameters

    bst = xgb.train({}, dtrain)

    dtest = xgb.DMatrix(x_test)
    y_pred = bst.predict(dtest)

    # convert probabilities to binary predictions (0 or 1)

    y_pred_binary = np.round(y_pred)

    print(classification_report(y_test, y_pred_binary))

    return bst


if __name__ == "__main__":

    #parse args
    args = parse_args()

    # run main function
    main(args)