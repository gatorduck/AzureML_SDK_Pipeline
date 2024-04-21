
# component 1 - data prep

# we create this script we want to run to preprocess the data, this will become a component in our pipeline, however this will not create the component, this is the actual component itself

from sklearn.preprocessing import MinMaxScaler
import argparse
import pandas as pd
import os


def main(args):
    """ main function for this script """
    df = get_data(args.input_data)

    df_prepped = data_prep(df)

    df_prepped.to_csv(os.path.join(args.prepped_data, "prepped_data.csv"), index=False)

def get_data(filepath):
    """ function used to read blob given a uri """
    df = pd.read_csv(filepath)

    return df

def data_prep(df):
    """ scale numeric columns """
    #separate numeric columns ( excluding last column)
    numeric_columns = df.select_dtypes(include=['float64','int64']).columns[:-1]

    # initialize MinMaxScaler
    scaler = MinMaxScaler()

    # scale only the numeric columns

    df[numeric_columns] = scaler.fit_transform(df[numeric_columns])

    return df

def parse_args():
    """ read args passed to script"""
    parser = argparse.ArgumentParser()

    parser.add_argument("--input_data", type=str)
    parser.add_argument("--prepped_data",type=str)

    args = parser.parse_args()

    return args

# run script

if __name__ == "__main__":

    # parse args
    args = parse_args()

    # run main function

    main(args)
    