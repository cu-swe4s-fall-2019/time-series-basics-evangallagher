import numpy as np
import pandas as pd
import datetime as dt
from os import listdir
from os.path import isfile, join
from pathlib import Path


def main():

    """
Description: This function cleans up '_small.csv' through converting the column
'time' to datetime, converts to float64, and gets rid of NaN values. It will
take either the sum or the average of values across 5 nd 15 minute intervals.

Output: 'five.csv' or 'fifteen.csv'
    """

    folder_path = Path('smallData')
    files_list = [f for f in
                 listdir(folder_path) if isfile(join(folder_path, f))]


    data_list = []
    for files in files_list:
        data_list.append(pd.read_csv(str(
            folder_path / files), parse_dates=['time'], index_col=['time']))

    # Convert numbers to float
    for i in range(len(data_list)):
        data_list[i] = data_list[i][pd.to_numeric(
            data_list[i]['value'], errors='coerce').notnull()]
        data_list[i]['value'] = data_list[i]['value'].astype(float)
        data_list[i].rename(columns={'value': str(
            files_list[i].replace('_small.csv', ''))}, inplace=True)

    # Find parallel array location
    for i in range(len(files_list)):
        if 'cgm' in files_list[i]:
            cgmloc = i

    baseDF = data_list[cgmloc]
    framelist = data_list
    framelist.pop(cgmloc)
    baseDF = baseDF.join(framelist)


    baseDF = baseDF.fillna(0)

    # Add columns with 5 and 15
    baseDF.insert(baseDF.shape[1], 'time5', baseDF.index.round('5min'))
    baseDF.insert(baseDF.shape[1], 'time15', baseDF.index.round('15min'))


    sum_baseDF = baseDF[['activity', 'bolus', 'meal', 'time5', 'time15']]
    mean_baseDF = baseDF[['smbg', 'hr', 'basal', 'cgm', 'time5', 'time15']]

    # Mean and sum calculations
    five_mean = mean_baseDF.groupby(['time5']).mean()
    five_sum = sum_baseDF.groupby(['time5']).sum()
    fifteen_mean = mean_baseDF.groupby(['time15']).mean()
    fifteen_sum = sum_baseDF.groupby(['time15']).sum()

    five = five_mean.join(five_sum)
    fifteen = fifteen_mean.join(fifteen_sum)

    # Print csv
    five.to_csv('five.csv', index=True, header=True)
    fifteen.to_csv('fifteen.csv', index=True, header=True)

if __name__ == '__main__':
    main()
