#!/usr/bin/env pyhton
'''
This file does some ETL operations on the data such as 
    1. Printing Number of Unique values in each column
    2. Removing NULL values and writting the data to a NULL-removed CSV format.
'''
def create_schema(filename):
    for line in file:
        line = line.strip().lower();
        colname = line.split()[0]
