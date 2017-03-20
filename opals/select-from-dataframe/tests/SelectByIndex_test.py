import unittest

import numpy as np
import pandas as pd
from opals.select.SelectByIndex import *


class SelByIndexTest(unittest.TestCase):

    # COLUMNWISE

    # Keep the columns indicated by the array of indices passed in
    def applyColWise_DropIsFalse(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 3] #0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 1, False)

        self.assertTrue(temp2.columns in ["A", "D"])
        self.assertTrue(temp2.shape[0] == 50) #nrows
        self.assertTrue(temp2.shape[0] == 2) #ncols
        self.assertTrue(temp2.columns not in ["B", "C"])

    # Remove the columns indicated by the array of indices passed in
    def applyColWise_DropIsTrue(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 3]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 1, True)

        self.assertTrue(temp2.columns in ["B", "C"])
        self.assertTrue(temp2.shape[0] == 50)  # nrows
        self.assertTrue(temp2.shape[0] == 2)  # ncols
        self.assertTrue(temp2.columns not in ["A", "D"])


    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyColWise_DropIsFalse_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 5]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 1, False)

        self.assertTrue(temp2 == temp)

    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyColWise_DropIsTrue_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 5]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 1, True)

        self.assertTrue(temp2 == temp)


    #ROW-WISE  ###############################################################################

    # Keep the columns indicated by the array of indices passed in
    def applyRowWise_DropIsFalse(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 3] #0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 0, False)

        self.assertTrue(temp2.index.get_values() not in [1,2])
        self.assertTrue(temp2.shape[0] == 48) #nrows
        self.assertTrue(temp2.shape[0] == 2) #ncols
        self.assertTrue(temp2.index.get_values() in [0,3])

    # Remove the columns indicated by the array of indices passed in
    def applyRowWise_DropIsTrue(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 3]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 0, True)

        self.assertTrue(temp2.index.get_values() not in [0,3])
        self.assertTrue(temp2.shape[0] == 48)  # nrows
        self.assertTrue(temp2.shape[0] == 2)  # ncols
        self.assertTrue(temp2.index.get_values() in [1,2])


    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyRowWise_DropIsFalse_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 5]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 0, False)

        self.assertTrue(temp2 == temp)

    # Make index error and make sure the dataframe returned is the same as the input dataframe
    def applyRowWise_DropIsTrue_IndexError(self):
        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        indices = [0, 5]  # 0 = Col. A; 3 = Col. 3

        temp = SelectByIndex()
        temp2 = temp.compute(df, indices, 0, True)

        self.assertTrue(temp2 == temp)


if __name__ == '__main__':
    unittest.main()
