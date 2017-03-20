import unittest

import numpy as np
import pandas as pd
from opals.select.SelectByCondition import *

class SelByConditionTest(unittest.TestCase):

    def testAllOps(self):

        temp = SelectByCondition()

        ops = temp.ops

        def eval_expr(x, ops, value, comparator):
            return ops.get(comparator)(x, value)

        df = pd.DataFrame(np.random.randn(50, 4), columns=list('ABCD'))

        for o in temp.comparators:

            print temp
            print o
            temp2 = temp.compute(df, 'A', o, 0)
            print temp2


            if temp2 is not None:

                for i in range(0, len(temp2)):
                    self.assertTrue(eval_expr(ops, temp2.loc[i, 'A'], 0, o))


if __name__ == '__main__':
    unittest.main()

