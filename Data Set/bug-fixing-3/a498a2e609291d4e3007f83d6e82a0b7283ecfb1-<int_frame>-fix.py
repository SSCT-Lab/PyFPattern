@pytest.fixture
def int_frame():
    "\n    Fixture for DataFrame of ints with index of unique strings\n\n    Columns are ['A', 'B', 'C', 'D']\n\n                A  B  C  D\n    vpBeWjM651  1  0  1  0\n    5JyxmrP1En -1  0  0  0\n    qEDaoD49U2 -1  1  0  0\n    m66TkTfsFe  0  0  0  0\n    EHPaNzEUFm -1  0 -1  0\n    fpRJCevQhi  2  0  0  0\n    OlQvnmfi3Q  0  0 -2  0\n    ...        .. .. .. ..\n    uB1FPlz4uP  0  0  0  1\n    EcSe6yNzCU  0  0 -1  0\n    L50VudaiI8 -1  1 -2  0\n    y3bpw4nwIp  0 -1  0  0\n    H0RdLLwrCT  1  1  0  0\n    rY82K0vMwm  0  0  0  0\n    1OPIUjnkjk  2  0  0  0\n\n    [30 rows x 4 columns]\n    "
    df = DataFrame({k: v.astype(int) for (k, v) in tm.getSeriesData().items()})
    return DataFrame({c: s for (c, s) in df.items()}, dtype=np.int64)