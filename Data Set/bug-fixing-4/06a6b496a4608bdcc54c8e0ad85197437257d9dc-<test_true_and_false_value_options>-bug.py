def test_true_and_false_value_options(self, engine, ext):
    df = pd.DataFrame([['foo', 'bar']], columns=['col1', 'col2'])
    expected = df.replace({
        'foo': True,
        'bar': False,
    })
    df.to_excel(self.path)
    read_frame = pd.read_excel(self.path, true_values=['foo'], false_values=['bar'], index_col=0)
    tm.assert_frame_equal(read_frame, expected)