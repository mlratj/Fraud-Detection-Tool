from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def data_load(datasource_name):
    return str(PROJECT_ROOT / 'datasource' / datasource_name)


def file_exists(file_path):
    return Path(file_path).exists()


def list_datasource_files():
    datasource_dir = PROJECT_ROOT / 'datasource'
    return sorted(f.name for f in datasource_dir.iterdir() if f.suffix.lower() == '.csv')


def extension_checker(filename):
    if filename.lower().endswith('.csv'):
        return filename
    else:
        return filename + '.csv'
