import unittest
import os
import datetime
import data_import
from os.path import join


class TestDataImport(unittest.TestCase):

    def test_linear_search(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        d = datetime.datetime(2018, 3, 16, 12, 38)
        index = obj.linear_search_value(d)
        self.assertEqual(index, 0)

    def test_binary_search(self):
        filename = './smallData/smbg_small.csv'
        obj = data_import.ImportData(filename)
        obj.binary_sort()
        d = datetime.datetime(2018, 3, 16, 12, 38)
        index = obj.binary_search_value(d)
        self.assertEqual(index, 0)

    def test_replace_high_low(self):
        file = open('test.csv', 'w')
        file.write('time,value\n')
        file.write('4/20/20 4:20,low\n')
        file.write('4/21/20 4:20,high')
        file.close()
        instance = di.ImportData('test.csv')
        self.assertEqual(instance._value[0], 40)
        self.assertEqual(instance._value[1], 300)
        os.remove('test.csv')
        os.remove('low_high.csv')


    def test_print_array(self):
        files_lst = os.listdir('./smallData/')
        data = []
        for f in files_lst:
            data.append(data_import.ImportData(join('./smallData/', f)))
            data_5 = []
        for obj in data:
            data_5.append(data_import.roundTimeArray(obj, 5))

        r = data_import.printArray(data_5, files_lst, 'out_5','smbg_small.csv')
        self.assertTrue(os.path.exists('out_5.csv'))
        os.remove('out_5.csv')


if __name__ == '__main__':
    unittest.main()
