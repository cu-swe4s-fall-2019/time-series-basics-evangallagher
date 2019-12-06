# time-series-basics

## Installation

This package requires Python3 and the following python packages:

- sys
- os
- csv
- datetime
- math
- argparse
- unittest
- pycodestyle
- numpy

ssshtest is required to run functional tests `test -e ssshtest || wget -qhttps://raw.githubusercontent.com/ryanlayer/ssshtest/master/ssshtest . ssshtest`

## How to use

data_import.py is the executable function, run with data_import.sh

**For pandas:** the pandas section requires homebrew, specifically the gtime
function 

### Import Data

ImportData is the major class of data_import.py It takes a csv file that contains time and value columns.

- time: an array containing datetime objects
- value: an array containing the values
- file: filename

### Functions:

- linear_search_value: returns the values of a given datetime object. Returns -1 if no values match.

### roundTimeArray
imputs data with an object and resolution


## Outpu pandas_import.py was added. This file
Creates a csv titled base_name.csv.

## December 5th update:
Upon redoing this assignment, the file pandas_import.py was added. This file
will pull from the small data folder, and write a csv file even if it is a
pandas data frame. The file also does minor cleaning up such as getting rid of
NaN values, convert to float values, and convert to date time. The purpose of
this assignment is to benchmark the different methods and see which is quicker.

## Benchmarking results
It was found that the pandas data frames could be implemented much quicker.
Basic time series would run for a little over 5 seconds, while the pandas would
usually run for 1.5 seconds. Usually this takes a bit more memory, at just
under 100 mb for pandas.
