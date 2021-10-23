@pytest.fixture
def int_frame():
    "\n    Fixture for DataFrame of ints with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D']\n    "
    df = DataFrame({k: v.astype(int) for (k, v) in tm.getSeriesData().items()})
    return DataFrame({c: s for (c, s) in df.items()}, dtype=np.int64)