from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def data_load(datasource_name):
    return str(PROJECT_ROOT / 'datasource' / datasource_name)


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