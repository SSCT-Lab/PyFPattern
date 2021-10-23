@pytest.fixture
def float_string_frame():
    "\n    Fixture for DataFrame of floats and strings with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D', 'foo'].\n    "
    df = DataFrame(tm.getSeriesData())
    df['foo'] = 'bar'
    return df