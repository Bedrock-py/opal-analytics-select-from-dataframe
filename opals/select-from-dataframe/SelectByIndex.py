from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd
import logging


# If an invalid operator or index is selected, the original dataframe will be returned unmodified.
class SelectByIndex(Algorithm):
    def __init__(self):
        super(SelectByIndex, self).__init__()
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name = 'SelectByIndex'
        self.type = 'select'
        self.description = 'Select rows or columns from a dataframe based on a vector of indices to keep or drop.'
        self.parameters_spec = [
            {"name": "Indices (a vector of integers)" , "attrname": "indices", "value": "" , "type": "input" , "step": None , "max": None, "min": None },
            {"name": "Axis (0 for row-wise; 1 for column-wise)", "attrname": "axis", "value": 0, "type": "input", "step": 1, "max": 1, "min": 0},
            {"name": "Drop (T = drop indices; F = keep indices)", "attrname": "drop", "value": True, "type": "input", "step": None, "max": 1, "min": 0}
        ]
        #self.parameters_spec = [{ "indices": "Vector of integers", "Axis": "0 for row-wise; 1 for column-wise", "drop": "boolean; T= drop indices; F= keep indices"}]
        self.possible_names = []

    def __build_df__(self, filepath):
        featuresPath = filepath['features.txt']['rootdir'] + 'features.txt'
        matrixPath = filepath['matrix.csv']['rootdir'] + 'matrix.csv'
        df = pd.read_csv(matrixPath, header=-1)
        featuresList = pd.read_csv(featuresPath, header=-1)

        df.columns = featuresList.T.values[0]

        return df

    def __get_features__(self,filepath):
        featuresPath = filepath['features.txt']['rootdir'] + 'features.txt'
        featuresList = pd.read_csv(featuresPath, header=-1)

        return featuresList.T.values

    # Writes the resulting subset dataframe to csv
    def compute(self, inputs, **kwargs):
        indata = self.__build_df__(inputs)
        featuresList = self.__get_features__(inputs)
        indata.columns = featuresList

        # If axis = 1, we filter column-wise
        if self.drop == False:
            if self.axis == 1:
                try:
                    outdata = indata.iloc[:,self.indices]

                except IndexError:
                    raise

        # Otherwise, we filter row-wise
            else:
                outdata = indata.iloc[self.indices, :]

        elif self.drop == True:
            if axis == 1:

                try:
                    outdata = indata.drop(indata.columns[self.indices], axis=axis, inplace=False)

                except IndexError:
                    raise

            else:
                try:
                    outdata = indata.drop(indata.index[self.indices], axis=axis, inplace=False)

                except IndexError:
                    raise


        # Save the results to csv
        self.results = {'matrix.csv': outdata.values, 'features.txt': featuresList[0]}
