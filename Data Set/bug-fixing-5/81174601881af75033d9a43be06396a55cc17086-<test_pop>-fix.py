def test_pop(self, float_frame):
    float_frame.columns.name = 'baz'
    float_frame.pop('A')
    assert ('A' not in float_frame)
    float_frame['foo'] = 'bar'
    float_frame.pop('foo')
    assert ('foo' not in float_frame)
    assert (float_frame.columns.name == 'baz')
    a = DataFrame([[1, 2, 3], [4, 5, 6]], columns=['A', 'B', 'C'], index=['X', 'Y'])
    b = a.pop('B')
    b += 1
    expected = DataFrame([[1, 3], [4, 6]], columns=['A', 'C'], index=['X', 'Y'])
    tm.assert_frame_equal(a, expected)
    expected = (Series([2, 5], index=['X', 'Y'], name='B') + 1)
    tm.assert_series_equal(b, expected)