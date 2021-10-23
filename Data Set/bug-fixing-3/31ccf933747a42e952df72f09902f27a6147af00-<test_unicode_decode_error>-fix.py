def test_unicode_decode_error(datapath):
    path = datapath('io', 'data', 'pickle', 'test_py27.pkl')
    df = pd.read_pickle(path)
    excols = pd.Index(['a', 'b', 'c'])
    tm.assert_index_equal(df.columns, excols)