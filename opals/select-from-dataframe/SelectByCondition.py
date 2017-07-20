from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd
import math
import logging

# If an invalid operator or index is selected, the original dataframe will be returned unmodified.

class SelectByCondition(Algorithm): # comment out to run unit test
    def __init__(self):
        super(SelectByCondition, self).__init__() # comment out to run unit test
        self.parameters = []
        self.inputs = ['matrix.csv','features.txt']
        self.outputs = ['matrix.csv','features.txt']
        self.name ='SelectByCondition'
        self.type = 'select'
        self.description = 'Select rows from a dataframe based on the values of a particular column relative to a comparator.'
        self.parameters_spec = [
            {"name": "Column name" , "attrname": "colname", "value": "" , "type": "input" , "step": None , "max": None, "min": None },
            {"name": "Comparator", "attrname": "comparator", "value": "", "type": "input", "step": None, "max": None, "min": None},
            {"name": "Value", "attrname": "value", "value": None, "type": "input", "step": 1, "max": float('inf'), "min": -float('inf')}
        ]
        self.possible_names = []
        self.valid_comparators = ["<", "<=", ">", ">=", "==", "!="]
        self.ops = {"<": (lambda x, y: x < y),
                    "<=": (lambda x, y: x <= y),
                    ">": (lambda x, y: x > y),
                    ">=":(lambda x, y: x >= y),
                    "==": (lambda x, y: x == y),
                    "!=": (lambda x, y:	x != y)}

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

        try:
            self.value = float(self.value)
        except Exception:
            logging.error("Could not convert value to float")
            raise

        # Helper func to evaluate x vs. y comparison
        def eval_expr(x, value, comparator):
            return self.ops.get(comparator)(x,value)

        outdata = []
        # Invalid comparison
        if self.comparator not in self.valid_comparators:
            logging.error("Not a valid comparison")
            raise
        else:
            # Valid comparison
            try:
                outdata = indata[indata[self.colname].apply(lambda x: eval_expr(x, self.value, self.comparator))]
                print(outdata)
            except IndexError:
                logging.error("Filtering on comparison failed")
                raise

        logging.error(featuresList[0])

        # Save the results to csv
        self.results = {'matrix.csv': outdata.values, 'features.txt': featuresList[0]}
