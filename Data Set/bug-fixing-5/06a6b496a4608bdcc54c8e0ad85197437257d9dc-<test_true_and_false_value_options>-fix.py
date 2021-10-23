def test_true_and_false_value_options(self, path):
    df = pd.DataFrame([['foo', 'bar']], columns=['col1', 'col2'])
    expected = df.replace({
        'foo': True,
        'bar': False,
    })
    df.to_excel(path)
    read_frame = pd.read_excel(path, true_values=['foo'], false_values=['bar'], index_col=0)
    tm.assert_frame_equal(read_frame, expected)