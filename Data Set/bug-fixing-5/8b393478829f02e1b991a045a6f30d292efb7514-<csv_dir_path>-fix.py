@pytest.fixture
def csv_dir_path(datapath):
    '\n    The directory path to the data files needed for parser tests.\n    '
    return datapath('io', 'parser', 'data')