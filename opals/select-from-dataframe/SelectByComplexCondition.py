from bedrock.analytics.utils import Algorithm
from bedrock.dataloader.utils import *
import numpy as np
import pandas as pd
import math
import logging
import re

# If an invalid operator or index is selected, the original dataframe will be returned unmodified.

class SelectByComplexCondition(Algorithm): # comment out to run unit test
    def __init__(self):
        super(SelectByComplexCondition, self).__init__() # comment out to run unit test
        self.parameters = []
        self.inputs = ['matrix.csv','features.txt']
        self.outputs = ['matrix.csv','features.txt']
        self.name ='SelectByCondition'
        self.type = 'select'
        self.description = 'Select rows from a dataframe based on the values of a particular column relative to a comparator.'
        self.parameters_spec = [
            {"name": "condition" , "attrname": "condition", "value": "" , "type": "input" }
        ]
        self.possible_names = []
        self.parsed_values = ["<", "<=", ">", ">=", "==", "!=","&","|"]

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

    def __filterByCondition__(self, condition, df):
        condition = condition.replace(" ","")
        x = re.split('(\||&|!=|==|>=|>|<=|<|\(|\))',condition)
        #re.split('==|\!=|\<=|\>=|\>|\<',x)
        z = ["df[\"{}\"]".format(x) if x in df.columns else x for x in x]
        expr = "".join(z)
        return df[eval(expr)]

    # Writes the resulting subset dataframe to csv
    def compute(self, inputs, **kwargs):
        indata = self.__build_df__(inputs)
        featuresList = self.__get_features__(inputs)

        outdata = []

        try:
            outdata = self.__filterByCondition__(self.condition, indata)
        except Exception:
            logging.error("Could not eval formula")
            raise

        # Save the results to csv
        self.results = {'matrix.csv': outdata.values, 'features.txt': featuresList[0]}
