@pytest.fixture
def mixed_int_frame():
    "\n    Fixture for DataFrame of different int types with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D'].\n\n                A  B    C    D\n    mUrCZ67juP  0  1    2    2\n    rw99ACYaKS  0  1    0    0\n    7QsEcpaaVU  0  1    1    1\n    xkrimI2pcE  0  1    0    0\n    dz01SuzoS8  0  1  255  255\n    ccQkqOHX75 -1  1    0    0\n    DN0iXaoDLd  0  1    0    0\n    ...        .. ..  ...  ...\n    Dfb141wAaQ  1  1  254  254\n    IPD8eQOVu5  0  1    0    0\n    CcaKulsCmv  0  1    0    0\n    rIBa8gu7E5  0  1    0    0\n    RP6peZmh5o  0  1    1    1\n    NMb9pipQWQ  0  1    0    0\n    PqgbJEzjib  0  1    3    3\n\n    [30 rows x 4 columns]\n    "
    df = DataFrame({k: v.astype(int) for (k, v) in tm.getSeriesData().items()})
    df.A = df.A.astype('int32')
    df.B = np.ones(len(df.B), dtype='uint64')
    df.C = df.C.astype('uint8')
    df.D = df.C.astype('int64')
    return df