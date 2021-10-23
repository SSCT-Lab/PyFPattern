@pytest.fixture
def float_frame():
    "\n    Fixture for DataFrame of floats with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n    "
    return DataFrame(tm.getSeriesData())