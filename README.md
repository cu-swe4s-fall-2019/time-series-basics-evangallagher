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

### Import Data

ImportData is the major class of data_import.py It takes a csv file that contains time and value columns.

- time: an array containing datetime objects
- value: an array containing the values
- file: filename

### Functions:

- linear_search_value: returns the values of a given datetime object. Returns -1 if no values match.

### roundTimeArray
imputs data with an object and resolution


## Output

Creates a csv titled base_name.csv.

## December 5th update:
