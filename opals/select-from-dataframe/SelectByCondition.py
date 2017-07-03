from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd
import math

# If an invalid operator or index is selected, the original dataframe will be returned unmodified.

class SelectByCondition(Algorithm): # comment out to run unit test
#class SelectByCondition(): # uncomment to run unit test
    def __init__(self):
        super(SelectByCondition, self).__init__() # comment out to run unit test
        self.parameters = []
        self.inputs = ['matrix.csv']
        self.outputs = ['matrix.csv']
        self.name ='SelectByCondition'
        self.type = 'select'
        self.description = 'Select rows from a dataframe based on the values of a particular column relative to a comparator.'
        self.parameters_spec = [
            {"name": "Column name" , "attrname": "colname", "value": "" , "type": "input" , "step": None , "max": None, "min": None },
            {"name": "Comparator", "attrname": "comparator", "value": "", "type": "input", "step": None, "max": None, "min": None},
            {"name": "Value", "attrname": "value", "value": None, "type": "input", "step": 1, "max": float('inf'), "min": -float('inf')}
        ]
        #self.parameters_spec = [{ "colname": "String", "comparator": "String in {<, <=, >, >=, ==, !=}", "value": "Float"}]
        self.possible_names = []
        self.comparators = ["<", "<=", ">", ">=", "==", "!="]
        self.ops = {"<": (lambda x, y: x < y),
                    "<=": (lambda x, y: x <= y),
                    ">": (lambda x, y: x > y),
                    ">=":(lambda x, y: x >= y),
                    "==": (lambda x, y: x == y),
                    "!=": (lambda x, y:	x != y)}

    # Writes the resulting subset dataframe to csv
    def compute(self, inputs, colname, comparator, value, **kwargs):

        indata = pd.DataFrame(np.genfromtxt(inputs['matrix.csv']['rootdir'] + 'matrix.csv', delimiter=',')) #comment out to run unit test

        value = float(value)

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
