import sys
import csv
import dateutil.parser
from os import listdir
from os.path import isfile, join
import argparse
import datetime
import math
import numpy as np


class ImportData:
    def __init__(self, data_csv):
        """uses ImportData by reading csv"""

        self._time = []
        self._value = []
        self._type = 'average'

        if 'activity' in data_csv or 'bolus' in data_csv or 'meal' in data_csv:
            self._type = 'sum'

        with open(data_csv, "r") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if row['time'] == '':
                    continue
                else:
                    try:
                        hit = dateutil.parser.parse(row['time'])
                        if row['value'] == 'low':
                            print('Converting Low to 40')
                            val = 40

                        elif row['value'] == 'high':
                            print('Converting High to 300')
                            val = 300

                        else:
                            val = float(row['value'])
                        self._time.append(hit)
                        self._value.append(val)

    def linear_search_value(self, key_time):
        """linearly searches self._time based on Arguments"""

        for i in range(len(self._time)):
            curr = self._time[i]
            if key_time == curr:
                return i

        return -1

    def binary_sort(self):
        """sort lists in order to perform binary search"""

        times = self._time.copy()
        values = self._value.copy()
        zipped = zip(times, values)
        zipped_sort = sorted(zipped)

        times_tup, values_tup = zip(*zipped_sort)
        times_sorted = list(times_tup)
        values_sorted = list(values_tup)

        self._time = times_sorted
        self._value = values_sorted

        return

    def binary_search_value(self, key_time):
        """
        EC: binary search of self._time based on Arguments
        """
        # values must be sorted before this can work

        lo = -1
        hi = len(self._time)

        while (hi - lo > 1):
            mid = (hi + lo) // 2

            if key_time == self._time[mid]:
                return mid

            if key_time < self._time[mid]:
                hi = mid
            else:
                lo = mid

        return -1


def roundTimeArray(obj, res):
    """
    Grouping of times based upon a resolution

    Arguments:
    obj : ImportData object
        times taken from this object
    resolution : integer
        minute resolution of the time grouping

    Returns:
    concatinated object of the grouped times and values
    """

    time_lst = []
    vals = []
    num_times = len(obj._time)
    type = obj._duphandle
    for i in range(num_times):
        time = obj._time[i]
        bad = datetime.timedelta(minutes=time.minute % res,
                                 seconds=time.second)
        time -= bad
        if (bad >= datetime.timedelta(minutes=math.ceil(res/2))):
            time += datetime.timedelta(minutes=res)
        obj._time[i] = time

    if num_times > 0:
        time_lst.append(obj._time[0])
        sch = obj.linear_search_value(obj._time[0])  # search
        if type == 0:
            vals.append(sum(sch))  # summed
        elif type == 1:
            vals.append(sum(sch)/len(sch))  # averaged

    for i in range(1, num_times):  # check for duplicates
        if obj._time[i] == obj._time[i - 1]:
            continue
        else:
            time_lst.append(obj._time[i])
            sch = obj.linear_search_value(obj._time[i])
            if type == 0:
                vals.append(sum(sch))  # summed
            elif type == 1:
                vals.append(sum(sch)/len(sch))  # averaged

    output = zip(time_lst, vals)
    return output


def printArray(data_list, annotation_list, base_name, key_file):
    """
    write data from csvs to file, with key as the first column
    saves a new csv file to the curent working directory
    """
    data_key = []
    data_rest = []
    annotation_a = []
    annotation_b = []

    if not (key_file in annotation_list):
        print('Cannot find sort_key')
        sys.exit(1)

    else:
        for i in range(len(annotation_list)):
            if (annotation_list[i] == key_file):
                annotation_a.append(annotation_list[i])
                data_key.append(data_list[i])
            else:
                annotation_b.append(annotation_list[i])
                data_rest.append(data_list[i])

    key_times = []
    key_values = []
    for tk, vk in data_key[0]:
        key_times.append(tk)
        key_values.append(vk)

    write_array = [[] for i in range(len(key_times))]
    for i in range(len(key_times)):
        write_array[i].append(key_times[i])
        write_array[i].append(key_values[i])

    for data in data_rest:
        rest_times = []
        rest_values = []
        for tr, vr in data:
            rest_times.append(tr)
            rest_values.append(vr)
        for i in range(len(key_times)):
            if key_times[i] in rest_times:
                idx = rest_times.index(key_times[i])
                write_array[i].append(rest_values[idx])
            else:
                write_array[i].append(0)

    attributes = ['time'] + annotation_a + annotation_b

    with open(base_name + '.csv', mode='w') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerow(attributes)
        writer.writerows(write_array)

    return


if __name__ == '__main__':

    # adding arguments
    parser = argparse.ArgumentParser(description='A class to import, combine, and print data from a folder.',
                                     prog='dataImport')

    parser.add_argument('folder_name', type=str, help='Name of the folder')

    parser.add_argument('output_file', type=str, help='Name of Output file')

    parser.add_argument('sort_key', type=str, help='File to sort on')

    parser.add_argument('--number_of_files', type=int,
                        help="Number of Files", required=False)

    args = parser.parse_args()

    # pull all the folders in the file
    try:
        files_lst = listdir(args.folder_name)
    except (FileNotFoundError, NameError) as e:
        print('Folder not found', file=sys.stder)
        sys.exit(1)

    # import all the files into a list of ImportData objects (in a loop!)
    data_lst = []
    for file in files_lst:
        data_lst.append(ImportData(join(args.folder_name, file)))

    if len(data_lst) == 0:
        print('No files in folder', file=sys.stder)
        sys.exit(1)

    # create two new lists of zip objects
    # a list with time rounded to 5
    data_5 = []
    for data_obj in data_lst:
        data_5.append(roundTimeArray(data_obj, 5))

    # a list with time rounded to 15
    data_15 = []
    for data_obj in data_lst:
        data_15.append(roundTimeArray(data_obj, 15))

    # print to a csv file
    printArray(data_5, files_lst, args.output_file+'_5', args.sort_key)
    printArray(data_15, files_lst, args.output_file+'_15', args.sort_key)
