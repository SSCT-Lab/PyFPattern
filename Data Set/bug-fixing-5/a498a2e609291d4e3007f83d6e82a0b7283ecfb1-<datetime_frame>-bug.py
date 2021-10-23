@pytest.fixture
def datetime_frame():
    "\n    Fixture for DataFrame of floats with DatetimeIndex\n\n    Columns are ['A', 'B', 'C', 'D']\n    "
    return DataFrame(tm.getTimeSeriesData())