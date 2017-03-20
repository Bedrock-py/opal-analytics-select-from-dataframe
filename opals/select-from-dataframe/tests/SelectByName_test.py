import os
import unittest

import numpy as np
import pandas as pd
from opals.select.SelectByName import *


class SelByNameTest(unittest.TestCase):

    # COLUMNWISE

    # Keep the columns indicated by the array of indices passed in
    def applyColWise_DropIsFalse(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        csvPath = os.getcwd() + "/opaltest/selByname.csv"

        df.to_csv(csvPath)

        names = ['A', 'D']

        temp = SelectByName()
        temp2 = temp.compute(df, names, False)

        self.assertTrue(temp2.columns in ["A", "D"])
        self.assertTrue(temp2.shape[0] == 50) #nrows
        self.assertTrue(temp2.shape[0] == 2) #ncols
        self.assertTrue(temp2.columns not in ["B", "C"])

    # Remove the columns indicated by the array of indices passed in
    def applyColWise_DropIsTrue(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        csvPath = os.getcwd() + "/opaltest/selByname.csv"

        df.to_csv(csvPath)

        names = ['A', 'D']

        temp = SelectByName()
        temp2 = temp.compute(csvPath, names, True)

        self.assertTrue(temp2.columns in ["B", "C"])
        self.assertTrue(temp2.shape[0] == 50)  # nrows
        self.assertTrue(temp2.shape[0] == 2)  # ncols
        self.assertTrue(temp2.columns not in ["A", "D"])


    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyColWise_DropIsFalse_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        csvPath = os.getcwd() + "/opaltest/selByname.csv"

        df.to_csv(csvPath)

        names = ['A', 'E']

        temp = SelectByName()
        temp2 = temp.compute(csvPath, names, False)

        self.assertTrue(temp2 == temp)

    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyColWise_DropIsTrue_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        csvPath = os.getcwd() + "/opaltest/selByname.csv"

        df.to_csv(csvPath)

        names = ['A', 'E']

        temp = SelectByName()
        temp2 = temp.compute(csvPath, names, True)

        self.assertTrue(temp2 == temp)




if __name__ == '__main__':
    unittest.main()
