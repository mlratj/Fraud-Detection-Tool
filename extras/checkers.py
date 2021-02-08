import os


def data_load(datasource_name):
    source_path = (os.path.dirname(os.path.abspath(__file__)))
    source_path = source_path[:-7]
    data = (source_path + '/datasource/' + datasource_name)
    return data


def file_search(file_to_check):
    try:
        df = data_load(file_to_check)
    except FileNotFoundError:
        print("No such file.")
        raise SystemExit


def extension_checker(filename):
    if filename.lower().endswith('.csv'):
        return filename
    else:
        return filename + '.csv'