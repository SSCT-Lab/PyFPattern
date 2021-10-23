@pytest.fixture
def csv1(csv_dir_path):
    '\n    The path to the data file "test1.csv" needed for parser tests.\n    '
    return os.path.join(csv_dir_path, 'test1.csv')