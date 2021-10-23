@pytest.fixture
def bool_frame_with_na():
    "\n    Fixture for DataFrame of booleans with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D']; some entries are missing\n    "
    df = (DataFrame(tm.getSeriesData()) > 0)
    df = df.astype(object)
    df.loc[5:10] = np.nan
    df.loc[15:20, (- 2):] = np.nan
    return df