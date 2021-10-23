def test_unicode_decode_error():
    path = os.path.join(os.path.dirname(__file__), 'data', 'pickle', 'test_py27.pkl')
    df = pd.read_pickle(path)
    excols = pd.Index(['a', 'b', 'c'])
    tm.assert_index_equal(df.columns, excols)