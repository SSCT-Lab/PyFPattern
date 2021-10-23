@pytest.fixture
def mixed_float_frame():
    "\n    Fixture for DataFrame of different float types with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n    "
    df = DataFrame(tm.getSeriesData())
    df.A = df.A.astype('float32')
    df.B = df.B.astype('float32')
    df.C = df.C.astype('float16')
    df.D = df.D.astype('float64')
    return df