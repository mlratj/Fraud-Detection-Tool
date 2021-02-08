import pandas as pd
import io
import requests
import numpy as np
from math import log, floor
from matplotlib import pyplot as plt
from extras import menu
from extras import checkers


def main(valid_file):
    print("Data loaded successfully")
    column_name = ''
    while len(column_name) < 1:
        column_name = input("Please specify a field to be checked by the tool:\n")
    try:
        df = pd.read_csv(valid_file)
        df['first_d'] = df[column_name].apply(lambda x: first_digit(x))
        first_digits = list(df['first_d'])
    except KeyError:
        print("Provided column name doesn't exists.")
        raise SystemExit
    try:
        first_digits.remove(0)
    except ValueError:
        pass
    try:
        first_digits_set = set(first_digits)
        input_occ = occurrence_count(first_digits_set, first_digits)
        input_perc_occ = percentage_of_total(input_occ)
        benford = benford_distribution()
        draw_histogram(benford, input_perc_occ)
    except:
        print("Provided data set is invalid.")
    return None


def data_source(option):
    if option == 1:
        # option 1:
        file_to_check = input("Please type in a name of CSV file to check:\n")
        valid_file = checkers.extension_checker(file_to_check)
        checkers.file_search(valid_file)
        try:
            df = checkers.data_load(valid_file)
        except FileNotFoundError:
            print("No such file.")
            raise SystemExit
    else:
        # option 2:
        url = input("Please enter an URL to the CSV file to check. \n")
        print("\n Loading...")
        s = requests.get(url).content
        s_io = io.StringIO(s.decode('utf-8'))
        df = s_io
    return df


def benford_distribution():
    """Provides a fixed list of probabilities determined by Benford's law."""
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
    perc_list = [(x / total) * 100 for x in l]
    return perc_list


def draw_histogram(benford, user_data=None):
    """Creates a data plot that allows to check if data provided by a user meets rules discovered by Frank Benford."""
    column_width = 0.4
    labels = []
    for x in range(1, 10):
        labels.append(x)
    index = np.arange(len(labels))
    plt.bar(index - column_width / 2, benford, column_width, label='Benford', color='green')
    plt.bar(index + column_width / 2, user_data, column_width, label='Data provided', color='red')
    plt.xticks(index, labels)
    plt.title("Benford distribution vs provided data")
    plt.xlabel("First digits")
    plt.ylabel("Occurrence [%]")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    load_choice = menu.print_menu()
    loaded_df = data_source(load_choice)
    main(loaded_df)
    # example parameters: 1. hydrology_areas 2.Shape__Area
