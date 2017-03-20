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
        self.possible_names = []

    # Writes the resulting subset dataframe to csv (?)
    def compute(self, inputs, colnames, drop=False, **kwargs):

        indata = pd.DataFrame(np.genfromtxt(inputs['matrix.csv']['rootdir'] + 'matrix.csv', delimiter=','))

        # Since we are using names and not indices, we can only filter column-wise
        if drop == False:
            try:
                outdata = indata.iloc[:,colnames]

            except IndexError:
                outdata = indata

        elif drop == True:
            try:
                outdata = indata.drop(indata.columns[colnames], inplace=False)

            except IndexError:
                outdata = indata

        self.results = {'matrix.csv': outdata}