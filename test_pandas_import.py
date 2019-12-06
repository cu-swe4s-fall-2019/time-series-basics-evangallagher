import unittest
from os import path
import pandas_import

# Test output file creation
class TestDataImport(unittest.TestCase):

    def test_csv_presence(self):
        pandas_import.main()
        self.assertTrue(path.exists('five_min.csv'))
        self.assertTrue(path.exists('fifteen_min.csv'))

if __name__ == '__main__':
    unittest.main()
