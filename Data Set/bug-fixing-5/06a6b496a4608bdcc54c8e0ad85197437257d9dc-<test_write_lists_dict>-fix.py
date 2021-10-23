def test_write_lists_dict(self, path):
    df = DataFrame({
        'mixed': ['a', ['b', 'c'], {
            'd': 'e',
            'f': 2,
        }],
        'numeric': [1, 2, 3.0],
        'str': ['apple', 'banana', 'cherry'],
    })
    df.to_excel(path, 'Sheet1')
    read = pd.read_excel(path, 'Sheet1', header=0, index_col=0)
    expected = df.copy()
    expected.mixed = expected.mixed.apply(str)
    expected.numeric = expected.numeric.astype('int64')
    tm.assert_frame_equal(read, expected)