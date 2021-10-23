@pytest.mark.parametrize('as_array', [True, False])
def test_setitem_sequence_mismatched_length_raises(self, data, as_array):
    ser = pd.Series(data)
    original = ser.copy()
    value = [data[0]]
    if as_array:
        value = data._from_sequence(value)
    xpr = 'cannot set using a {} indexer with a different length'
    with tm.assert_raises_regex(ValueError, xpr.format('list-like')):
        ser[[0, 1]] = value
    self.assert_series_equal(ser, original)
    with tm.assert_raises_regex(ValueError, xpr.format('slice')):
        ser[slice(3)] = value
    self.assert_series_equal(ser, original)