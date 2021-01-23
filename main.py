import pandas as pd
import os
import numpy as np
from math import log, floor
from matplotlib import pyplot as plt


def main(column_name):
    column_name = 'Shape__Area' # hardcoded value for test purposes
    df = data_load(file_to_check)
    df['first_d'] = df[column_name].apply(lambda x: first_digit(x))
    first_digits = list(df['first_d'])
    first_digits.remove(0)
    try:
        first_digits_set = set(first_digits)
        input_occ = occurrence_count(first_digits_set, first_digits)
        input_perc_occ = percentage_of_total(input_occ)
        benford = benford_distribution()
        draw_histogram(benford, input_perc_occ)
    except:
        print("Provided data set is invalid.")
    return None


def data_load(datasource_name):
    source_path = os.path.dirname(__file__)
    datasource_name = 'hydrology_areas'  # hardcoded value for test purposes
    data = pd.read_csv(source_path + '/datasource/' + datasource_name + '.csv')
    return data


def extension_checker(filename):
    if filename.lower().endswith('.csv'):
        return filename
    else:
        return filename + '.csv'


def benford_distribution():
    benford = []
    i = 1
    while i < 10:
        val = (log(1 + 1 / i, 10)) * 100
        benford.append(val)
        i += 1
    return benford


def first_digit(num):
    num = floor(num)
    return int(str(num)[:1])


def occurrence_count(data_set, data_list):
    data_count = []
    for i in data_set:
        count = data_list.count(i)
        data_count.append(count)
    return data_count


def percentage_of_total(l):
    total = sum(l)
    perc_list = [(x / total)*100 for x in l]
    return perc_list


def draw_histogram(benford, user_data = None):
    column_width = 0.4
    labels = []
    for x in range(1,10):
        labels.append(x)
    index = np.arange(len(labels))
    plt.bar(index - column_width/2, benford, column_width, label = 'Benford',  color = 'green')
    plt.bar(index + column_width/2, user_data, column_width, label = 'Data provided', color = 'red')
    plt.xticks(index, labels)
    plt.title("Benford distribution vs provided data")
    plt.xlabel("First digits")
    plt.ylabel("Occurrence [%]")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    file_to_check = input("Please type in a CSV file to check:\n ")
    field_to_check = input("Please specify a field to be checked by the tool:\n")
    valid_file = extension_checker(file_to_check)
    main(column_name = None)
