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
    df = pd.read_csv(valid_file)
    while True:
        column_name = input("Please specify a field to be checked by the tool:\n")
        if column_name in df.columns:
            break
        print(f"Column '{column_name}' not found. Available columns:")
        for col in df.columns:
            print(f"  {col}")
    if pd.to_numeric(df[column_name], errors='coerce').lt(0).any():
        print(
            f"\nColumn '{column_name}' contains negative values.\n"
            "According to Benford's Law, the analysed dataset must contain only "
            "natural numbers. Please select a different file or column."
        )
        return False
    df['first_d'] = df[column_name].apply(lambda x: first_digit(x))
    first_digits = [d for d in df['first_d'] if d != 0]
    try:
        input_occ = occurrence_count(first_digits)
        input_perc_occ = percentage_of_total(input_occ)
        benford = benford_distribution()
        draw_histogram(benford, input_perc_occ)
    except Exception:
        print("Provided data set is invalid.")
    return True


def data_source(option):
    if option == 1:
        while True:
            file_to_check = input("Please type in a name of CSV file to check:\n")
            valid_file = checkers.extension_checker(file_to_check)
            file_path = checkers.data_load(valid_file)
            if checkers.file_exists(file_path):
                return file_path
            print(f"'{valid_file}' not found. Available files in datasource:")
            for name in checkers.list_datasource_files():
                print(f"  {name}")
    else:
        url = input("Please enter an URL to the CSV file to check. \n")
        print("\n Loading...")
        s = requests.get(url).content
        return io.StringIO(s.decode('utf-8'))


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


def occurrence_count(data_list):
    return [data_list.count(d) for d in range(1, 10)]


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
    while True:
        load_choice = menu.print_menu()
        loaded_df = data_source(load_choice)
        if main(loaded_df):
            break
    # example parameters: 1. hydrology_areas 2.Shape__Area
