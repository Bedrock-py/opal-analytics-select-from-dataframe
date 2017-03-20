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
#class SelectByIndex(Filter):
class SelectByIndex(Algorithm):
    def __init__(self):
        super(SelectByIndex, self).__init__()
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name = 'SelectByIndex'
        self.type = 'Filter' # what goes here?
        self.description = 'Select rows or columns from a dataframe based on a vector of indices to keep or drop.'
        self.parameters_spec = [{ "indices": "Vector of integers", "Axis": "0 for row-wise; 1 for column-wise", "drop": "boolean; T= drop indices; F= keep indices"}]
        self.possible_names = [] # what goes here?


    # Writes the resulting subset dataframe to csv (?)
    def compute(self, inputs, indices, axis, drop, **kwargs):

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