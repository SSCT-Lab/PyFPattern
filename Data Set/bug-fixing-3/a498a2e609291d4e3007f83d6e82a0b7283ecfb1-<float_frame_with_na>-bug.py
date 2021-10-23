@pytest.fixture
def float_frame_with_na():
    "\n    Fixture for DataFrame of floats with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D']; some entries are missing\n    "
    df = DataFrame(tm.getSeriesData())
    df.loc[5:10] = np.nan
    df.loc[15:20, (- 2):] = np.nan
    return df