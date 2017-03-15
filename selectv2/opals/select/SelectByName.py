#****************************************************************
# Copyright (c) 2015, Georgia Tech Research Institute
# All rights reserved.
#
# This unpublished material is the property of the Georgia Tech
# Research Institute and is protected under copyright law.
# The methods and techniques described herein are considered
# trade secrets and/or confidential. Reproduction or distribution,
# in whole or in part, is forbidden except by the express written
# permission of the Georgia Tech Research Institute.
#****************************************************************/

from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd

# REFERENCE SYNTAX:  # data.iloc[[0, 4, 7, 25], [0, 5, 6]]  # 1st, 4th, 7th, 25th row + 1st 6th 7th columns.
class SelectByName(Algorithm):
#class SelectByName(): # uncomment to run unit test
    def __init__(self):
        super(SelectByName, self).__init__() # comment to run unit test
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name = 'SelectByName'
        self.type = 'Filter'
        self.description = 'Select columns from a dataframe based on a vector of names to keep or drop.'
        self.parameters_spec = [{ "colnames": "Vector of strings corresponding to column names", "drop": "boolean; T= drop indices; F= keep indices"}]
        self.possible_names = [] # what goes here?

    # Writes the resulting subset dataframe to csv (?)
    def compute(self, inputs, colnames, drop, **kwargs):

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