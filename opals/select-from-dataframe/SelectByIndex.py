from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd


# If an invalid operator or index is selected, the original dataframe will be returned unmodified.
class SelectByIndex(Algorithm):
    def __init__(self):
        super(SelectByIndex, self).__init__()
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name = 'SelectByIndex'
        self.type = 'select'
        self.description = 'Select rows or columns from a dataframe based on a vector of indices to keep or drop.'
        self.parameters_spec = [{ "indices": "Vector of integers", "Axis": "0 for row-wise; 1 for column-wise", "drop": "boolean; T= drop indices; F= keep indices"}]
        self.possible_names = []


    # Writes the resulting subset dataframe to csv
    def compute(self, inputs, indices, axis, drop=False, **kwargs):

        indata = pd.DataFrame(np.genfromtxt(inputs['matrix.csv']['rootdir'] + 'matrix.csv', delimiter=','))

        # If axis = 1, we filter column-wise
        if drop == False:
            if axis == 1:
                try:
                    outdata = indata.iloc[:,indices]

                except IndexError:
                    outdata = indata

        # Otherwise, we filter row-wise
            else:
                outdata = indata.iloc[indices, :]

        elif drop == True:
            if axis == 1:

                try:
                    outdata = indata.drop(indata.columns[indices], axis=axis, inplace=False)

                except IndexError:
                    outdata = indata

            else:
                try:
                    outdata = indata.drop(indata.index[indices], axis=axis, inplace=False)

                except IndexError:
                    outdata = indata


        # Save the results to csv
        self.results = {'matrix.csv': outdata}