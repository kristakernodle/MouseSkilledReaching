import unittest
from Mouse import Mouse


class MouseTestCase(unittest.TestCase):
    def test_declareAttributes(self):
        mouse1 = Mouse('1', 'WT', ['SR', 'PH'])
        self.assertEqual([mouse1.etNum, mouse1.genotype, mouse1.experiments], ['1', 'WT', ['SR', 'PH']])


if __name__ == '__main__':
    unittest.main()
