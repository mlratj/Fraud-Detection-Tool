import pandas as pd
import os


def main(datasource_name):
    source_path = os.path.dirname(__file__)
    data = pd.read_csv(source_path + '/datasource/' + datasource_name + '.csv')
    return None


def extension_checker(filename):
    if filename.lower().endswith('.csv'):
        return filename
    else:
        return filename + '.csv'


if __name__ == "__main__":
    file_to_check = input("Please type in a CSV file to check: ")
    main(extension_checker(file_to_check))