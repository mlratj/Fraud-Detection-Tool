import pandas as pd
import os
from math import log


def main(datasource_name, column_name):
    source_path = os.path.dirname(__file__)
    data = pd.read_csv(source_path + '/datasource/' + datasource_name + '.csv')
    return None


def extension_checker(filename):
    if filename.lower().endswith('.csv'):
        return filename
    else:
        return filename + '.csv'


def benford_distribution():
    benford = []
    i = 1
    while i < 10:
        val = log(1 + 1/i, 10)
        benford.append(val)
        i += 1
    return benford

if __name__ == "__main__":
    file_to_check = input("Please type in a CSV file to check:\n ")
    field_to_check = input("Please specify a field to be checked by the tool:\n")
    main(extension_checker(file_to_check), field_to_check)
