@pytest.fixture
def mixed_int_frame():
    "\n    Fixture for DataFrame of different int types with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n    "
    df = DataFrame({k: v.astype(int) for (k, v) in tm.getSeriesData().items()})
    df.A = df.A.astype('int32')
    df.B = np.ones(len(df.B), dtype='uint64')
    df.C = df.C.astype('uint8')
    df.D = df.C.astype('int64')
    return df