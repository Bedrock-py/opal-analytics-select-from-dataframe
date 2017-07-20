from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd

# If an invalid operator or index is selected, the original dataframe will be returned unmodified.

class SelectByName(Algorithm):
    def __init__(self):
        super(SelectByName, self).__init__() # comment to run unit test
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name = 'SelectByName'
        self.type = 'select'
        self.description = 'Select columns from a dataframe based on a vector of names to keep or drop.'
        self.parameters_spec = [{ "colnames": "Vector of strings corresponding to column names", "drop": "boolean; T= drop indices; F= keep indices"}]
        self.parameters_spec = [
            {"name": "Column name" , "attrname": "colname", "value": "" , "type": "input" , "step": None , "max": None, "min": None },
            {"name": "Drop (T = drop indices; F = keep indices)", "attrname": "drop", "value": False, "type": "input", "step": None, "max": 1, "min": 0}
        ]
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

    # Writes the resulting subset dataframe to csv (?)
    def compute(self, inputs, **kwargs):
        indata = self.__build_df__(inputs)
        featuresList = self.__get_features__(inputs)
        indata.columns = featuresList

        # Since we are using names and not indices, we can only filter column-wise
        if self.drop == False:
            try:
                outdata = indata.iloc[:,self.colnames]

            except IndexError:
                outdata = indata

        elif self.drop == True:
            try:
                outdata = indata.drop(indata.columns[self.colnames], inplace=False)

            except IndexError:
                outdata = indata

        self.results = {'matrix.csv': outdata.values, 'features.txt': featuresList[0]}
