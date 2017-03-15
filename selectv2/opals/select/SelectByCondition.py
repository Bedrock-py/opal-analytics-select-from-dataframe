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
class SelectByCondition(Algorithm): # comment out to run unit test
#class SelectByCondition(): # uncomment to run unit test
    def __init__(self):
        super(SelectByCondition, self).__init__() # comment out to run unit test
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name ='SelectByCondition'
        self.type = 'Filter'
        self.description = 'Select rows from a dataframe based on the values of a particular column relative to a comparator.'
        self.parameters_spec = [{ "colname": "String", "Comparator": "String in {<, <=, >, >=, ==, !=}", "value": "Float"}]
        self.possible_names = [] # what goes here?
        self.comparators = ["<", "<=", ">", ">=", "==", "!="]
        self.ops = {"<": (lambda x, y: x < y),
                    "<=": (lambda x, y: x <= y),
                    ">": (lambda x, y: x > y),
                    ">=":(lambda x, y: x >= y),
                    "==": (lambda x, y: x == y),
                    "!=": (lambda x, y:	x != y)}

    # Writes the resulting subset dataframe to csv (?)
    def compute(self, inputs, colname, comparator, value, **kwargs):

        indata = pd.DataFrame(np.genfromtxt(inputs['matrix.csv']['rootdir'] + 'matrix.csv', delimiter=',')) #comment out to run unit test

        #indata = inputs #uncomment to run unit test

        # Helper func to evaluate x vs. y comparison
        def eval_expr(x, value, comparator):
            return self.ops.get(comparator)(x,value)


        # Invalid comparison
        if comparator not in self.comparators:
            outdata = indata

        else:

            # Valid comparison
            try:
                outdata = indata[indata[colname].apply(lambda x: eval_expr(x, value, comparator))]
                print outdata

            except IndexError:
                outdata = indata


        # Save the results to csv
        self.results = {'matrix.csv': outdata}
